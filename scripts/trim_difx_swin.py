#!/usr/bin/env python3.11
"""
trim_difx_swin.py — cut the leading integrations of a DiFX SWIN visibility file.

Purpose
    A DiFX SWIN file (`<job>.difx/DIFX_<mjd>_<sec>.s<nnnn>.b<nnnn>`, written by mpifxcorr
    `Visibility::writedifx`) has no file header: it is a plain sequence of records, each a
    74-byte binary header followed by its complex float32 samples.  An excerpt is therefore a
    byte PREFIX of the original, cut at a record boundary: nothing is rewritten at all.

What it does
    Walks every record of FULL, reading only the headers (checking the sync word 0xFF00FF00
    and header version 1 of each, little-endian, and that the freq index is one of the FREQ
    TABLE), with the record lengths taken from the FREQ TABLE of the job's `.input`
    (`NUM CHANNELS i` / `CHANS TO AVG i` samples of 8 bytes each), and checks that the records
    tile the file exactly.  It then keeps the records before the first record of the
    (N+1)-th distinct integration time (MJD, seconds) in file order, after checking that no
    later record has one of the first N times — so the prefix holds every record of the first
    N integrations and nothing else.

Header layout (mpifxcorr `Visibility::writeDiFXHeader`, DiFX 2.6 and 2.7)
    uint32 sync, int32 version, int32 baseline, int32 mjd, float64 seconds, int32 config,
    int32 source, int32 freq index, char[2] polarization pair, int32 pulsar bin,
    float64 weight, float64[3] u, v, w — packed, 74 bytes.

Usage
    trim_difx_swin.py FULL INPUT EXCERPT --integrations N
    Prints the record and byte counts.  `head -c <bytes> FULL | cmp - EXCERPT` re-proves that
    the excerpt is a prefix of FULL.
"""
import argparse
import os
import re
import struct

HEADER = struct.Struct('<Iiiidiii2sid3d')
assert HEADER.size == 74


def samples_per_record(input_path):
    text = open(input_path, encoding='ascii').read()
    nchan = {int(m[1]): int(m[2]) for m in re.finditer(r'^NUM CHANNELS (\d+):\s*(\d+)$', text, re.M)}
    avg = {int(m[1]): int(m[2]) for m in re.finditer(r'^CHANS TO AVG (\d+):\s*(\d+)$', text, re.M)}
    assert nchan and nchan.keys() == avg.keys() == set(range(len(nchan))), 'FREQ TABLE not understood'
    return [nchan[i] // avg[i] for i in range(len(nchan))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('full')
    ap.add_argument('input')
    ap.add_argument('excerpt')
    ap.add_argument('--integrations', type=int, required=True)
    a = ap.parse_args()

    nsamp = samples_per_record(a.input)
    size = os.path.getsize(a.full)
    pos, records = 0, []  # (byte offset, (mjd, seconds))
    with open(a.full, 'rb') as f:
        while pos < size:
            f.seek(pos)
            header = f.read(HEADER.size)
            assert len(header) == HEADER.size, f'{a.full} ends inside the record header at byte {pos}'
            sync, version, _bl, mjd, sec, _cfg, _src, freq = HEADER.unpack(header)[:8]
            assert sync == 0xFF00FF00 and version == 1, f'bad record header at byte {pos}'
            assert 0 <= freq < len(nsamp), f'freq index {freq} outside the FREQ TABLE at byte {pos}'
            records.append((pos, (mjd, sec)))
            pos += HEADER.size + 8 * nsamp[freq]
    assert pos == size, f'records do not tile {a.full}: last one ends at {pos}'

    times = list(dict.fromkeys(t for _, t in records))
    assert len(times) > a.integrations, 'the file has no more integrations than requested'
    kept = set(times[:a.integrations])
    cut = next(i for i, (_, t) in enumerate(records) if t not in kept)
    assert all(t not in kept for _, t in records[cut:]), 'records of a kept integration follow the cut'
    nbytes = records[cut][0]

    with open(a.full, 'rb') as src, open(a.excerpt, 'wb') as dst:
        left = nbytes
        while left:
            chunk = src.read(min(left, 1 << 20))
            assert chunk, f'{a.full} shrank while being read'
            dst.write(chunk)
            left -= len(chunk)
    print(f'{a.excerpt}: {cut} of {len(records)} records, {nbytes} of {size} bytes, '
          f'integrations {times[:a.integrations]}')


if __name__ == '__main__':
    main()
