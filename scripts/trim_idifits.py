#!/usr/bin/env python3.11
"""
trim_idifits.py — shorten a large FITS-IDI file by keeping only a SUBSET OF UV_DATA ROWS.

Purpose
    Turn a multi-GB published FITS-IDI file into a repository-sized excerpt without
    changing a single value in it.

Verbatim-subset guarantee
    The output is a byte-exact copy of the input except that
      * the UV_DATA data segment contains only the selected rows, each copied verbatim
        (the whole row: UU/VV/WW, DATE, TIME, BASELINE, FILTER, SOURCE, FREQID, INTTIM,
        WEIGHT, FLUX), in the original chronological order;
      * the single card `NAXIS2` in the UV_DATA header is rewritten to the new row count
        (same 80-byte card slot, so the header block count is unchanged).
    Nothing is recomputed, rescaled, averaged, reordered or synthesised, and every other
    HDU (PRIMARY, ARRAY_GEOMETRY, SOURCE, ANTENNA — including difx2fits' one-block-per-job
    duplicates —, FREQUENCY, INTERFEROMETER_MODEL, CALC, MODEL_COMPS, GATEMODL, FLAG,
    SYSTEM_TEMPERATURE, PHASE-CAL, WEATHER, GAIN_CURVE, ...) is transferred as raw bytes,
    so duplicate EXTNAMEs, zero-width columns, non-standard keywords and the primary
    HISTORY block all survive untouched.  `verify_excerpt.py FULL EXCERPT` re-proves it.

Row selection (every category is a union of verbatim rows)
    anchor  rows of one baseline in one UTC window, kept in full — used to pin the exact
            scans that the VLBIFiles.jl testitems reference by name.
    keep    rows matching an explicit selector, `SEL[@ISO/ISO][%STRIDE]` with SEL one of
            'A1-A2', 'AUTO', 'CROSS', '*'.  Declarative: it never looks at the visibility
            values, so the selection is reproducible without reading FLUX.
    strong  inside the N strongest source-blocks (a source-block = a contiguous run of
            equal SOURCE with no time gap > --gap s), all records of the K strongest cross
            baselines and all autocorrelations of A antennas.
    sparse  every Nth row of everything else, stride chosen to fill the size budget, so
            that every baseline, source, scan and antenna still appears somewhere.

Usage
    trim_idifits.py IN.idifits OUT.idifits [--target-mb 50]
        [--anchor KP-LA@2011-12-12T02:09:30/2011-12-12T02:12:44]
        [--keep 'EF-MC' --keep 'AUTO%10'] [--blocks 6] [--nbl 3] [--nauto 2]
        [--gap 60] [--no-sparse]

    `--target-mb` is only an upper target for the sparse filler: the non-UV_DATA tables are
    always kept whole and set a hard size floor (27.1 MB for rdv87, 35.2 MB for BL178AC).
    See MAKE.sh for the exact command behind every excerpt in this repository.
"""
import argparse
import math
import os

import numpy as np
from astropy.io import fits

BLOCK = 2880


# ---------------------------------------------------------------- file layout
def uv_layout(path):
    """Locate the UV_DATA HDU inside `path` and describe its byte layout."""
    with fits.open(path, memmap=True, lazy_load_hdus=True) as hdul:
        idx = [i for i, h in enumerate(hdul) if h.name == "UV_DATA"]
        if len(idx) != 1:
            raise SystemExit(f"expected exactly one UV_DATA HDU, found {len(idx)}")
        uv = hdul[idx[0]]
        fi = uv.fileinfo()
        h = uv.header
        cols = [(c.name, c.format) for c in uv.columns]
        lay = dict(
            hdrLoc=fi["hdrLoc"], datLoc=fi["datLoc"],
            nrow=h["NAXIS2"], rowlen=h["NAXIS1"],
            datEnd=fi["datLoc"] + math.ceil(h["NAXIS1"] * h["NAXIS2"] / BLOCK) * BLOCK,
            cols=cols, header=h.copy(),
            nband=h["NO_BAND"], nchan=h["NO_CHAN"],
            nstk=h.get("NO_STKD", h["MAXIS2"]), ncx=h["MAXIS1"],
        )
        ag = hdul["ARRAY_GEOMETRY"].data
        lay["ants"] = {str(r["ANNAME"]).strip().upper(): int(r["NOSTA"]) for r in ag}
    return lay


def col_offsets(cols, rowlen):
    sz = {"E": 4, "D": 8, "J": 4, "I": 2, "A": 1, "B": 1, "L": 1, "C": 8, "M": 16}
    off, out = 0, {}
    for name, fmt in cols:
        rep = int("".join(ch for ch in fmt if ch.isdigit()) or 1)
        out[name] = (off, rep, fmt[-1])
        off += rep * sz[fmt[-1]]
    if off != rowlen:
        raise SystemExit(f"column offsets {off} != NAXIS1 {rowlen}")
    return out


def read_meta(path, lay):
    """Read the small per-row columns of UV_DATA with a strided memmap (no FLUX)."""
    offs = col_offsets(lay["cols"], lay["rowlen"])
    want = {"DATE": ">f8", "TIME": ">f8", "BASELINE": ">i4", "SOURCE": ">i4"}
    dt = np.dtype({"names": list(want), "formats": list(want.values()),
                   "offsets": [offs[k][0] for k in want], "itemsize": lay["rowlen"]})
    m = np.memmap(path, dtype=dt, mode="r", offset=lay["datLoc"], shape=(lay["nrow"],))
    meta = {k: np.asarray(m[k]) for k in want}
    meta["JD"] = meta["DATE"] + meta["TIME"]
    return meta, offs


def flux_memmap(path, lay, offs):
    n = offs["FLUX"][1]
    dt = np.dtype({"names": ["FLUX"], "formats": [(">f4", (n,))],
                   "offsets": [offs["FLUX"][0]], "itemsize": lay["rowlen"]})
    return np.memmap(path, dtype=dt, mode="r", offset=lay["datLoc"], shape=(lay["nrow"],))


def med_amp(fm, lay, rows):
    """Median |V| of pol 0 over the given rows, read verbatim from the file."""
    rows = np.sort(np.asarray(rows))
    f = np.asarray(fm["FLUX"][rows]).reshape(len(rows), lay["nband"], lay["nchan"],
                                             lay["nstk"], lay["ncx"])
    a = np.hypot(f[..., 0, 0], f[..., 0, 1])
    return float(np.nanmedian(a))


# ---------------------------------------------------------------- selection
def source_blocks(meta, gap):
    jd, src = meta["JD"], meta["SOURCE"]
    brk = np.where((np.diff(jd) * 86400.0 > gap) | (np.diff(src) != 0))[0]
    starts = np.r_[0, brk + 1]
    ends = np.r_[brk, len(jd) - 1]
    return list(zip(starts.tolist(), ends.tolist()))


def parse_anchor(spec, ants):
    """'KP-LA@2011-12-12T02:09:30/2011-12-12T02:12:44' -> (baseline, jd0, jd1)"""
    from astropy.time import Time
    blpart, _, tpart = spec.partition("@")
    a, b = blpart.upper().split("-")
    n1, n2 = ants[a], ants[b]
    bl = min(n1, n2) * 256 + max(n1, n2)
    t0, t1 = tpart.split("/")
    return bl, Time(t0, scale="utc").jd, Time(t1, scale="utc").jd


def keep_mask(spec, lay, meta):
    """Explicit, fully deterministic row selector.

    SPEC := SEL [ '@' ISO '/' ISO ] [ '%' STRIDE ]
    SEL  := 'A1-A2' (one baseline, autocorrelations allowed as 'A1-A1')
          | 'AUTO'  (every autocorrelation)
          | 'CROSS' (every cross-correlation)
          | '*'     (everything)
    The optional @-window restricts to a UTC interval, the optional %STRIDE keeps
    every STRIDEth of the matching rows (in file order).  Selected rows are copied
    verbatim; this option only decides *which* rows, never their content.
    """
    from astropy.time import Time
    bl, jd = meta["BASELINE"], meta["JD"]
    a1, a2 = bl // 256, bl % 256
    body, _, strpart = spec.partition("%")
    selpart, _, tpart = body.partition("@")
    s = selpart.strip().upper()
    if s in ("*", "ALL"):
        m = np.ones(len(bl), bool)
    elif s == "AUTO":
        m = a1 == a2
    elif s == "CROSS":
        m = a1 != a2
    else:
        p, q = s.split("-")
        n1, n2 = lay["ants"][p], lay["ants"][q]
        m = bl == (min(n1, n2) * 256 + max(n1, n2))
    if tpart:
        t0, t1 = tpart.split("/")
        m &= (jd >= Time(t0, scale="utc").jd - 1e-9) & (jd <= Time(t1, scale="utc").jd + 1e-9)
    stride = int(strpart) if strpart else 1
    if stride > 1:
        idx = np.where(m)[0]
        m = np.zeros(len(bl), bool)
        m[idx[::stride]] = True
    return m


def select(path, lay, meta, offs, args, log=print):
    nrow = lay["nrow"]
    bl, jd, src = meta["BASELINE"], meta["JD"], meta["SOURCE"]
    a1, a2 = bl // 256, bl % 256
    auto = a1 == a2
    keep = np.zeros(nrow, bool)
    tag = {}

    # --- anchors -----------------------------------------------------------
    for spec in args.anchor:
        b, j0, j1 = parse_anchor(spec, lay["ants"])
        m = (bl == b) & (jd >= j0 - 1e-9) & (jd <= j1 + 1e-9)
        log(f"  anchor {spec}: baseline {b//256}-{b%256}, {m.sum()} rows")
        keep |= m
    tag["anchor"] = int(keep.sum())

    # --- explicit --keep selectors ----------------------------------------
    for spec in args.keep:
        m = keep_mask(spec, lay, meta)
        log(f"  keep {spec}: {int(m.sum())} rows")
        keep |= m
    tag["keep"] = int(keep.sum()) - tag["anchor"]

    # --- strong source-blocks ---------------------------------------------
    if args.blocks <= 0:
        tag["strong"] = 0
        if args.target_mb is not None and not args.no_sparse:
            _sparse(meta, args, lay, keep, log)
        tag["sparse"] = int(keep.sum()) - tag["anchor"] - tag["keep"] - tag["strong"]
        return keep, tag
    fm = flux_memmap(path, lay, offs)
    blocks = source_blocks(meta, args.gap)
    rng = np.random.default_rng(args.seed)
    strengths = []
    for (s, e) in blocks:
        idx = np.arange(s, e + 1)
        cidx = idx[~auto[idx]]
        if len(cidx) < 50:
            strengths.append(-1.0)
            continue
        smp = np.sort(rng.choice(cidx, size=min(args.probe, len(cidx)), replace=False))
        strengths.append(med_amp(fm, lay, smp))
    strengths = np.array(strengths)
    order = np.argsort(-strengths)
    # take the strongest blocks but spread them over the session: walk the ranked
    # list and skip a block that is within `spread` of an already chosen one
    chosen = []
    span = jd[-1] - jd[0]
    for k in order:
        if strengths[k] <= 0:
            continue
        s, e = blocks[k]
        if all(abs(jd[s] - jd[blocks[c][0]]) > args.spread * span for c in chosen):
            chosen.append(k)
        if len(chosen) >= args.blocks:
            break
    chosen.sort()
    for k in chosen:
        s, e = blocks[k]
        idx = np.arange(s, e + 1)
        # strongest cross baselines inside this block
        cand = np.unique(bl[idx][~auto[idx]])
        amps = []
        for b in cand:
            r = idx[bl[idx] == b]
            if len(r) < 10:
                continue
            smp = np.sort(rng.choice(r, size=min(args.probe, len(r)), replace=False))
            amps.append((med_amp(fm, lay, smp), int(b)))
        amps.sort(reverse=True)
        bsel = [b for _, b in amps[:args.nbl]]
        m = np.isin(bl, bsel) & (np.arange(nrow) >= s) & (np.arange(nrow) <= e)
        # autocorrelations of the antennas of the strongest baseline (+ any extra)
        aants = []
        for _, b in amps[:args.nbl]:
            for x in (b // 256, b % 256):
                if x not in aants:
                    aants.append(x)
        aants = aants[:args.nauto]
        ma = auto & np.isin(a1, aants) & (np.arange(nrow) >= s) & (np.arange(nrow) <= e)
        log(f"  block rows {s}-{e} src={src[s]} amp={strengths[k]:.4f}: "
            f"baselines {[f'{b//256}-{b%256}' for b in bsel]} ({m.sum()} rows) + "
            f"autos {aants} ({ma.sum()} rows)")
        keep |= m | ma
    tag["strong"] = int(keep.sum()) - tag["anchor"] - tag["keep"]

    # --- sparse background -------------------------------------------------
    if args.target_mb is not None and not args.no_sparse:
        _sparse(meta, args, lay, keep, log)
    tag["sparse"] = int(keep.sum()) - tag["anchor"] - tag["keep"] - tag["strong"]
    return keep, tag


def _sparse(meta, args, lay, keep, log):
    """Fill the remaining size budget with every Nth of the not-yet-kept rows."""
    budget = int(args.target_mb * 1e6 - (args.other_bytes)) // lay["rowlen"]
    room = budget - int(keep.sum())
    rest = np.where(~keep)[0]
    if room > 0 and len(rest):
        stride = max(1, len(rest) // room)
        sel = rest[::stride]
        keep[sel] = True
        log(f"  sparse: every {stride}th of the remaining {len(rest)} rows "
            f"-> {len(sel)} rows")
    else:
        log(f"  sparse: no room left (budget {budget}, already {keep.sum()})")


# ---------------------------------------------------------------- writing
def patch_naxis2(hdr_bytes, nrow):
    """Rewrite the NAXIS2 card in a raw header block, leaving every other byte alone."""
    out = bytearray(hdr_bytes)
    for i in range(0, len(out), 80):
        if out[i:i + 8] == b"NAXIS2  ":
            card = f"NAXIS2  = {nrow:20d}".encode("ascii")
            rest = bytes(out[i:i + 80])
            # keep any trailing comment
            j = rest.find(b"/")
            comment = rest[j:].rstrip() if j > 30 else b""
            new = card + (b" " + comment if comment else b"")
            new = new[:80].ljust(80)
            out[i:i + 80] = new
            return bytes(out)
    raise SystemExit("NAXIS2 card not found in UV_DATA header")


def hdu_segments(path):
    """[(name, hdrLoc, hdrEnd, datEnd)] for every HDU, in file order.

    The spans come from astropy's own `fileinfo()['datSpan']` (already block-padded), and
    the result is asserted to tile the file exactly: segment k+1 starts where segment k
    ends and the last one ends at EOF.  That assertion is what makes `write_trimmed`'s
    "copy each segment verbatim" honest -- a hand-rolled size formula that is off by one
    block on some HDU would otherwise silently duplicate or drop a 2880-byte block.
    (It did: `max(NAXISk, 1)` turned the legal `NAXIS=1 / NAXIS1=0` empty primary array of
    astrogeo-style FITS-IDI into a 1-byte one.)
    """
    out = []
    with fits.open(path, memmap=True, lazy_load_hdus=True) as hdul:
        for h in hdul:
            fi = h.fileinfo()
            out.append((h.name, fi["hdrLoc"], fi["datLoc"], fi["datLoc"] + fi["datSpan"]))
    pos = 0
    for name, h0, d0, d1 in out:
        if h0 != pos:
            raise SystemExit(f"HDU {name}: segment starts at {h0}, previous ended at {pos}")
        pos = d1
    if pos != os.path.getsize(path):
        raise SystemExit(f"segments end at {pos}, file is {os.path.getsize(path)} bytes")
    return out


def write_trimmed(src, dst, lay, keep, chunk=4096):
    """Copy `src` to `dst` byte for byte, except that UV_DATA keeps only `keep` rows
    (and its NAXIS2 card is rewritten)."""
    rows = np.where(keep)[0]
    n = len(rows)
    rowlen = lay["rowlen"]
    with open(src, "rb") as fi, open(dst, "wb") as fo:
        for name, h0, d0, d1 in hdu_segments(src):
            if name == "UV_DATA":
                fi.seek(h0)
                fo.write(patch_naxis2(fi.read(d0 - h0), n))     # header, one card changed
                m = np.memmap(src, dtype=np.uint8, mode="r", offset=d0,
                              shape=(lay["nrow"], rowlen))
                for i in range(0, n, chunk):                     # rows, verbatim
                    fo.write(m[rows[i:i + chunk]].tobytes())
                del m
                pad = (-(n * rowlen)) % BLOCK
                if pad:
                    fo.write(b"\0" * pad)
            else:
                fi.seek(h0)
                remaining = d1 - h0
                while remaining:
                    b = fi.read(min(1 << 24, remaining))
                    if not b:
                        break
                    fo.write(b)
                    remaining -= len(b)
    return n


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("infile")
    ap.add_argument("outfile")
    ap.add_argument("--target-mb", type=float, default=None,
                    help="approximate total output size; the sparse sample fills up to it")
    ap.add_argument("--anchor", action="append", default=[],
                    metavar="A1-A2@ISO/ISO", help="keep every row of this baseline in this "
                    "UTC window (repeatable)")
    ap.add_argument("--keep", action="append", default=[],
                    metavar="SEL[@ISO/ISO][%STRIDE]",
                    help="explicit deterministic row selector, repeatable.  SEL is 'A1-A2', "
                         "'AUTO', 'CROSS' or '*'; see keep_mask().  Unlike --blocks this does "
                         "not look at the data at all.")
    ap.add_argument("--blocks", type=int, default=6, help="number of strong source-blocks "
                    "(0 disables the amplitude-ranked selection entirely)")
    ap.add_argument("--nbl", type=int, default=3, help="strongest cross baselines per block")
    ap.add_argument("--nauto", type=int, default=2, help="antennas whose autos are kept in full")
    ap.add_argument("--gap", type=float, default=60.0, help="source-block splitting gap [s]")
    ap.add_argument("--spread", type=float, default=0.08,
                    help="minimum separation of chosen blocks, as a fraction of the session")
    ap.add_argument("--probe", type=int, default=24, help="rows sampled to rank amplitudes")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-sparse", action="store_true")
    args = ap.parse_args()

    lay = uv_layout(args.infile)
    total = os.path.getsize(args.infile)
    uv_bytes = lay["datEnd"] - lay["datLoc"]
    args.other_bytes = total - uv_bytes
    print(f"IN  {args.infile}")
    print(f"    total {total/1e6:.1f} MB, UV_DATA {uv_bytes/1e6:.1f} MB "
          f"({100*uv_bytes/total:.2f} %), everything else {args.other_bytes/1e6:.1f} MB")
    print(f"    UV_DATA: {lay['nrow']} rows x {lay['rowlen']} B, "
          f"NO_BAND={lay['nband']} NO_CHAN={lay['nchan']} NO_STKD={lay['nstk']}")
    if args.target_mb is not None and args.target_mb * 1e6 < args.other_bytes:
        print(f"    NOTE: target {args.target_mb} MB is below the {args.other_bytes/1e6:.1f} MB "
              f"floor set by the other tables; output will be larger.")

    meta, offs = read_meta(args.infile, lay)
    print("SELECTION")
    keep, tag = select(args.infile, lay, meta, offs, args)
    n = int(keep.sum())
    est = args.other_bytes + math.ceil(n * lay["rowlen"] / BLOCK) * BLOCK
    print(f"  kept {n} of {lay['nrow']} rows ({100*n/lay['nrow']:.3f} %) "
          f"[anchor {tag['anchor']}, keep {tag['keep']}, strong {tag['strong']}, "
          f"sparse {tag['sparse']}]")
    bl = meta["BASELINE"][keep]
    print(f"  -> {len(np.unique(bl))} baselines, {len(np.unique(meta['SOURCE'][keep]))} sources, "
          f"{int(((bl//256)==(bl%256)).sum())} autocorrelations")
    print(f"  estimated output size {est/1e6:.1f} MB")
    written = write_trimmed(args.infile, args.outfile, lay, keep)
    print(f"OUT {args.outfile}: {written} rows, {os.path.getsize(args.outfile)/1e6:.1f} MB")

    # verification: structure valid, and the kept rows are byte-identical
    with fits.open(args.outfile, memmap=True) as hdul:
        hdul.verify("exception")
        names = [h.name for h in hdul]
        assert hdul["UV_DATA"].header["NAXIS2"] == written
    rows = np.where(keep)[0]
    lay2 = uv_layout(args.outfile)
    m1 = np.memmap(args.infile, dtype=np.uint8, mode="r", offset=lay["datLoc"],
                   shape=(lay["nrow"], lay["rowlen"]))
    m2 = np.memmap(args.outfile, dtype=np.uint8, mode="r", offset=lay2["datLoc"],
                   shape=(written, lay2["rowlen"]))
    step = max(1, written // 2000)
    ok = np.array_equal(m1[rows[::step]], m2[::step][:len(rows[::step])])
    del m1, m2
    print(f"  verify: HDUs {names}")
    print(f"  verify: astropy verify OK, row bytes identical on a {len(rows[::step])}-row "
          f"sample: {ok}")


if __name__ == "__main__":
    main()
