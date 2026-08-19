#!/usr/bin/env python3.11
"""
trim_uvfits_groups.py — shorten a large UVFITS random-groups file by keeping only a
SUBSET OF GROUPS (visibility records).  The sibling of `trim_idifits.py`, which does the
same job for FITS-IDI (where the visibilities live in a `UV_DATA` binary table instead).

Purpose
    Turn a several-hundred-MB published UVFITS file into a repository-sized excerpt
    without changing a single value in it.

Verbatim-subset guarantee
    The output is a byte-exact copy of the input except that
      * the random-groups data segment of the primary HDU contains only the first N
        groups, each copied verbatim (all PCOUNT parameter words -- UU, VV, WW, BASELINE,
        DATE1, DATE2, INTTIM, SOURCE, FREQSEL ... -- followed by the full
        NAXIS2 x ... x NAXISn data array of that group), in the original order;
      * the single card `GCOUNT` in the primary header is rewritten to the new group count
        (same 80-byte card slot, so the header block count is unchanged).
    No value is recomputed, rescaled, averaged or synthesised, and no keyword other than
    GCOUNT is touched -- in particular `BSCALE`/`BZERO`, the `CTYPEn/CRVALn/CDELTn/CRPIXn`
    frequency axis and every `PTYPEn/PSCALn/PZEROn` stay exactly as written.
    **Every table extension is preserved byte for byte.**  In a UVFITS file the `AIPS AN`,
    `AIPS FQ`, `AIPS SU`, `AIPS NX`, ... tables FOLLOW the groups data, so shrinking the
    data segment moves them to a lower file offset; their bytes are unchanged, only their
    position is.  (That is the one structural difference from `trim_idifits.py`, where the
    trimmed HDU is the last big thing in the file.)  `verify_excerpt.py FULL EXCERPT`
    re-proves the whole property, table by table.

    Group layout (FITS standard, "random groups" convention):
      NAXIS1 == 0, GROUPS == T, GCOUNT == number of groups, PCOUNT == parameters per group
      group size = (PCOUNT + NAXIS2*NAXIS3*...*NAXISn) * |BITPIX|/8
      data segment size = GCOUNT * group size, zero-padded to a multiple of 2880

Usage
    trim_uvfits_groups.py IN.uvfits OUT.uvfits (--target-mb MB | --ngroups N)

    --target-mb   choose N so that the whole output file is at most this many MB
    --ngroups N   keep exactly the first N groups
    Either way the kept groups are the *first* N, i.e. a contiguous time range from the
    start of the observation.  See MAKE.sh for the command behind every excerpt here.
"""
import argparse
import math
import os
import sys

import numpy as np
from astropy.io import fits

BLOCK = 2880


def groups_layout(path):
    """Locate the random-groups primary HDU of `path` and describe its byte layout."""
    with fits.open(path, memmap=True, lazy_load_hdus=True) as hdul:
        ph = hdul[0]
        h = ph.header
        if not h.get("GROUPS", False) or h.get("NAXIS1", None) != 0:
            raise SystemExit(f"{path}: primary HDU is not a random-groups HDU "
                             f"(GROUPS={h.get('GROUPS')}, NAXIS1={h.get('NAXIS1')}) -- "
                             f"if this is FITS-IDI use trim_idifits.py instead")
        fi = ph.fileinfo()
        naxis = h["NAXIS"]
        dims = [h[f"NAXIS{k}"] for k in range(2, naxis + 1)]
        nelem = 1
        for d in dims:
            nelem *= d
        gsize = (h["PCOUNT"] + nelem) * abs(h["BITPIX"]) // 8
        lay = dict(hdrLoc=fi["hdrLoc"], datLoc=fi["datLoc"], datSpan=fi["datSpan"],
                   datEnd=fi["datLoc"] + fi["datSpan"],
                   gcount=h["GCOUNT"], pcount=h["PCOUNT"], gsize=gsize, dims=dims,
                   bitpix=h["BITPIX"], header=h.copy())
        if lay["gcount"] * gsize > lay["datSpan"] or \
                lay["datSpan"] - lay["gcount"] * gsize >= BLOCK:
            raise SystemExit(f"{path}: GCOUNT*groupsize = {lay['gcount']*gsize} does not "
                             f"match the data span {lay['datSpan']}")
        lay["tables"] = [(x.name, x.fileinfo()["hdrLoc"],
                          x.fileinfo()["datLoc"] + x.fileinfo()["datSpan"]) for x in hdul[1:]]
    return lay


def patch_gcount(hdr_bytes, n):
    """Rewrite the GCOUNT card in a raw header block, leaving every other byte alone."""
    out = bytearray(hdr_bytes)
    for i in range(0, len(out), 80):
        if out[i:i + 8] == b"GCOUNT  ":
            rest = bytes(out[i:i + 80])
            j = rest.find(b"/")
            comment = rest[j:].rstrip() if j > 30 else b""
            new = f"GCOUNT  = {n:20d}".encode("ascii")
            new = (new + (b" " + comment if comment else b""))[:80].ljust(80)
            out[i:i + 80] = new
            return bytes(out)
    raise SystemExit("GCOUNT card not found in the primary header")


def write_trimmed(src, dst, lay, n, chunk=4096):
    """Copy `src` to `dst` byte for byte, except that the groups data segment holds only
    the first `n` groups (and the GCOUNT card is rewritten)."""
    gs = lay["gsize"]
    with open(src, "rb") as fi, open(dst, "wb") as fo:
        # ---- primary header, one card changed
        fi.seek(lay["hdrLoc"])
        fo.write(patch_gcount(fi.read(lay["datLoc"] - lay["hdrLoc"]), n))
        # ---- groups, verbatim
        m = np.memmap(src, dtype=np.uint8, mode="r", offset=lay["datLoc"],
                      shape=(lay["gcount"], gs))
        for i in range(0, n, chunk):
            fo.write(m[i:min(i + chunk, n)].tobytes())
        del m
        pad = (-(n * gs)) % BLOCK
        if pad:
            fo.write(b"\0" * pad)
        # ---- every table extension, verbatim (they simply move up in the file)
        fi.seek(lay["datEnd"])
        total = os.path.getsize(src) - lay["datEnd"]
        while total:
            b = fi.read(min(1 << 24, total))
            if not b:
                break
            fo.write(b)
            total -= len(b)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("infile")
    ap.add_argument("outfile")
    ap.add_argument("--ngroups", type=int, default=None)
    ap.add_argument("--target-mb", type=float, default=None)
    args = ap.parse_args()

    lay = groups_layout(args.infile)
    total = os.path.getsize(args.infile)
    other = total - lay["datSpan"]
    print(f"IN  {args.infile}")
    print(f"    total {total/1e6:.1f} MB, groups data {lay['datSpan']/1e6:.1f} MB "
          f"({100*lay['datSpan']/total:.2f} %), everything else {other/1e6:.3f} MB")
    print(f"    GCOUNT={lay['gcount']} PCOUNT={lay['pcount']} BITPIX={lay['bitpix']} "
          f"dims(NAXIS2..n)={lay['dims']} -> {lay['gsize']} B/group")
    print(f"    tables: {[t[0] for t in lay['tables']]}")

    if args.ngroups is None:
        if args.target_mb is None:
            raise SystemExit("give --ngroups or --target-mb")
        n = int((args.target_mb * 1e6 - other) // lay["gsize"])
        if n < 1:
            raise SystemExit(f"target {args.target_mb} MB is below the {other/1e6:.3f} MB "
                             f"floor set by the headers and tables")
    else:
        n = args.ngroups
    n = min(n, lay["gcount"])
    est = other + math.ceil(n * lay["gsize"] / BLOCK) * BLOCK
    print(f"SELECTION: the first {n} of {lay['gcount']} groups, "
          f"estimated output {est/1e6:.1f} MB")
    write_trimmed(args.infile, args.outfile, lay, n)
    print(f"OUT {args.outfile}: {n} groups, {os.path.getsize(args.outfile)/1e6:.1f} MB")

    # ---- verification -----------------------------------------------------
    got = os.path.getsize(args.outfile)
    if got != est:
        sys.exit(f"VERIFICATION FAILED: output is {got} B, expected exactly {est} B")
    lay2 = groups_layout(args.outfile)
    assert lay2["gcount"] == n and lay2["gsize"] == lay["gsize"]
    with fits.open(args.outfile, memmap=False) as hdul:      # full read, not lazy
        hdul.verify("exception")
        names = [x.name for x in hdul]
        _ = hdul[0].data                                      # forces the group parser
    m1 = np.memmap(args.infile, dtype=np.uint8, mode="r", offset=lay["datLoc"],
                   shape=(lay["gcount"], lay["gsize"]))
    m2 = np.memmap(args.outfile, dtype=np.uint8, mode="r", offset=lay2["datLoc"],
                   shape=(n, lay["gsize"]))
    step = max(1, n // 2000)
    ok = np.array_equal(m1[:n][::step], m2[::step])
    del m1, m2
    # tables byte-identical, one by one
    tabs = []
    with open(args.infile, "rb") as f1, open(args.outfile, "rb") as f2:
        for (nm, h0, d1), (nm2, h02, d12) in zip(lay["tables"], lay2["tables"]):
            f1.seek(h0); f2.seek(h02)
            tabs.append((nm, nm == nm2 and (d1 - h0) == (d12 - h02)
                         and f1.read(d1 - h0) == f2.read(d12 - h02)))
    print(f"  verify: HDUs {names}")
    print(f"  verify: astropy full read + verify OK; group bytes identical on a "
          f"{len(range(0, n, step))}-group sample: {ok}")
    print(f"  verify: table HDUs byte-identical: "
          f"{', '.join(f'{nm}={v}' for nm, v in tabs)}")
    if not ok or not all(v for _, v in tabs):
        sys.exit("VERIFICATION FAILED")


if __name__ == "__main__":
    main()
