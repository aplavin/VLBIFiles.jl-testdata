#!/usr/bin/env python3.11
"""
verify_excerpt.py — prove that an excerpt really is a verbatim subset of its source.

Purpose
    Re-establish, from the two files alone and without trusting the tool that made them,
    the guarantee that `trim_idifits.py` / `trim_uvfits_groups.py` claim: everything
    outside the trimmed visibility container is byte-identical, and the trimmed HDU's
    header differs in exactly one card, the record count.

What it compares
    FITS-IDI excerpt (made with `trim_idifits.py`):
      * every byte before the UV_DATA header, hashed;
      * every byte after the UV_DATA data segment, hashed;
      * the UV_DATA header block, card by card -- expected: the single card `NAXIS2`.
    UVFITS random-groups excerpt (made with `trim_uvfits_groups.py`):
      * the primary header block, card by card -- expected: the single card `GCOUNT`;
      * every table extension, byte for byte (they move up in the file but do not change).

Usage
    verify_excerpt.py FULL.fits EXCERPT.fits
    Prints a per-item report ending in `VERDICT: verbatim subset`, and exits 0, iff the
    only difference is that one record-count card plus the omitted rows/groups themselves.
"""
import hashlib
import os
import sys

from astropy.io import fits


def sha1_range(path, a, b):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        f.seek(a)
        rem = b - a
        while rem > 0:
            x = f.read(min(1 << 24, rem))
            if not x:
                break
            h.update(x)
            rem -= len(x)
    return h.hexdigest()


def read_range(path, a, b):
    with open(path, "rb") as f:
        f.seek(a)
        return f.read(b - a)


def card_diff(ha, hb):
    return [(ha[i:i + 80].decode("ascii", "replace").rstrip(),
             hb[i:i + 80].decode("ascii", "replace").rstrip())
            for i in range(0, min(len(ha), len(hb)), 80) if ha[i:i + 80] != hb[i:i + 80]]


def locate(path):
    """(kind, hdrLoc, datLoc, datEnd, nrec, tables) of the trimmed HDU."""
    with fits.open(path, memmap=True, lazy_load_hdus=True) as hdul:
        # FITS-IDI first: some FITS-IDI writers (difx2fits, astrogeo .fits) leave GROUPS = T
        # in an otherwise empty primary header, so the primary alone does not discriminate.
        idx = [i for i, h in enumerate(hdul) if h.name == "UV_DATA"]
        if len(idx) == 1:
            uv = hdul[idx[0]]
            fi = uv.fileinfo()
            return ("uvdata", fi["hdrLoc"], fi["datLoc"], fi["datLoc"] + fi["datSpan"],
                    uv.header["NAXIS2"], None)
        ph = hdul[0]
        if ph.header.get("GROUPS", False) and ph.header.get("NAXIS1", None) == 0 \
                and ph.header.get("GCOUNT", 0) > 0:
            fi = ph.fileinfo()
            tabs = [(x.name, x.fileinfo()["hdrLoc"],
                     x.fileinfo()["datLoc"] + x.fileinfo()["datSpan"]) for x in hdul[1:]]
            return ("groups", fi["hdrLoc"], fi["datLoc"], fi["datLoc"] + fi["datSpan"],
                    ph.header["GCOUNT"], tabs)
        raise SystemExit(f"{path}: neither one UV_DATA HDU nor a random-groups primary")


def main():
    A, B = sys.argv[1], sys.argv[2]
    ka, h0a, d0a, d1a, na, tabsa = locate(A)
    kb, h0b, d0b, d1b, nb, tabsb = locate(B)
    if ka != kb:
        sys.exit(f"different kinds of file: {ka} vs {kb}")
    ok = True
    print(f"{A}\n{B}\n  kind: {ka}   records {na} -> {nb}")

    diffs = card_diff(read_range(A, h0a, d0a), read_range(B, h0b, d0b))
    want = "NAXIS2" if ka == "uvdata" else "GCOUNT"
    print(f"  trimmed-HDU header: {len(diffs)} differing card(s)")
    for x, y in diffs:
        print(f"    - {x}\n    + {y}")
    if len(diffs) != 1 or not diffs[0][0].startswith(want):
        ok = False
        print(f"  !! expected exactly one differing card ({want})")

    if ka == "uvdata":
        pre = (sha1_range(A, 0, h0a), sha1_range(B, 0, h0b))
        post = (sha1_range(A, d1a, os.path.getsize(A)), sha1_range(B, d1b, os.path.getsize(B)))
        print(f"  bytes before UV_DATA: {h0a} / {h0b}  identical={pre[0] == pre[1]}")
        print(f"  bytes after  UV_DATA: {os.path.getsize(A)-d1a} / {os.path.getsize(B)-d1b}"
              f"  identical={post[0] == post[1]}")
        ok = ok and pre[0] == pre[1] and post[0] == post[1]
    else:
        if len(tabsa) != len(tabsb):
            ok = False
            print(f"  !! {len(tabsa)} table extension(s) in the full file, {len(tabsb)} in the "
                  f"excerpt — the data segment does not end where GCOUNT says it does")
        for (nm, s0, s1), (nm2, t0, t1) in zip(tabsa, tabsb):
            same = nm == nm2 and (s1 - s0) == (t1 - t0) and \
                read_range(A, s0, s1) == read_range(B, t0, t1)
            print(f"  table {nm:12s} {s1-s0:8d} B at {s0} -> {t0}  identical={same}")
            ok = ok and same

    print("VERDICT:", "verbatim subset" if ok else "NOT a verbatim subset")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
