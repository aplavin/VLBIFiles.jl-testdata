#!/bin/sh
# MAKE.sh — regenerate every excerpt in this repository from its ORIGINAL source.
#
# Nothing here is required to *use* the repository; it exists so that any excerpt can be
# reproduced bit for bit from the published bytes it was cut from, and so that the exact
# row/group selection is documented as code rather than prose.
#
# Every excerpt is a byte-verbatim copy of its source except that the visibility container
# holds only the selected records and the single row-count card (FITS-IDI `NAXIS2`,
# UVFITS `GCOUNT`) is rewritten.  `verify_excerpt.py FULL EXCERPT` re-proves that property.
#
#   requirements: python3.11, astropy >= 6, numpy >= 1.24, curl
#   usage:        SRC=/some/scratch/dir sh MAKE.sh          (needs ~17 GB of scratch)
#
# The excerpts committed here were built with python 3.11.11, astropy 8.0.1 and numpy 2.2.5.
# Three of the calls below rank source-blocks by amplitude (--blocks > 0) and probe them with
# rows drawn from numpy's default_rng, so which rows they keep depends on the seed; `--seed 0`
# is written out there rather than left to trim_idifits.py's default, which is the same 0.
# Checked 2026-08-19: bd152ie rebuilt with the explicit flag is byte-identical to the excerpt
# committed here.
#
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
SRC=${SRC:-$ROOT/_sources}
PY=${PY:-python3.11}
mkdir -p "$SRC"

TRIM_IDI="$PY $HERE/trim_idifits.py"
TRIM_UVF="$PY $HERE/trim_uvfits_groups.py"
VERIFY="$PY $HERE/verify_excerpt.py"

get() {  # get URL LOCALNAME
    [ -f "$SRC/$2" ] || curl -L -C - -o "$SRC/$2" "$1"
}

# =====================================================================================
# astrogeo/ — everything below is a plain, listable, no-login Apache tree (Leonid Petrov)
# =====================================================================================

# --- 2012_04_17_raes03v_C_01 : DiFX-ra (RadioAstron branch), LSB + PHASE-CAL, 115.7 MB ---
# Keep every record of the three GROUND-GROUND baselines (EF-MC, EF-YS, MC-YS; antenna 3 is
# the RadioAstron spacecraft, whose >500 ns delays are not usable for the sideband test),
# plus every 10th autocorrelation record of all four antennas.  PHASE-CAL(371) untouched.
get http://astrogeo.org/s0/radik_fits/raes03v/2012_04_17_raes03v_C_01.fits \
    2012_04_17_raes03v_C_01.fits
$TRIM_IDI "$SRC/2012_04_17_raes03v_C_01.fits" \
    "$ROOT/astrogeo/2012_04_17_raes03v_C_01.excerpt.fits" \
    --keep EF-MC --keep EF-YS --keep MC-YS --keep 'AUTO%10' --blocks 0 --no-sparse
$VERIFY "$SRC/2012_04_17_raes03v_C_01.fits" \
    "$ROOT/astrogeo/2012_04_17_raes03v_C_01.excerpt.fits"

# --- 2011_06_28_rdv87_alt_01 : RDV87, DIFX-2.0.1, 8xLSB (X band) + PHASE-CAL(12494), 9.69 GB ---
# Keep the 83 records of the FD-PT scan on source 34 that the VIS test in
# astrogeo_geo/README.md uses (2011-06-29 04:37:43 .. 04:43:11), the FD and PT
# autocorrelations of the same scan, and a 1-in-2111 sparse sample of everything else so that
# every antenna, baseline and source still appears.  UV rows are 32 880 B here, so ~390 rows
# is the whole 40 MB budget once the 27.1 MB of auxiliary tables are kept whole.
get http://astrogeo.org/s0/vlba_fits/rdv87/2011_06_28_rdv87_alt_01.fits \
    2011_06_28_rdv87_alt_01.fits
$TRIM_IDI "$SRC/2011_06_28_rdv87_alt_01.fits" \
    "$ROOT/astrogeo/2011_06_28_rdv87_alt_01.excerpt.fits" \
    --keep 'FD-PT@2011-06-29T04:37:40/2011-06-29T04:43:15' \
    --keep 'FD-FD@2011-06-29T04:37:40/2011-06-29T04:43:15' \
    --keep 'PT-PT@2011-06-29T04:37:40/2011-06-29T04:43:15' \
    --blocks 0 --target-mb 39.9
$VERIFY "$SRC/2011_06_28_rdv87_alt_01.fits" \
    "$ROOT/astrogeo/2011_06_28_rdv87_alt_01.excerpt.fits"

# --- VLBA_BD152IE_gatedie : DIFX-2.1, 5 merged jobs -> ANTENNA has 50 rows, GATEMODL, 353 MB ---
# Structural fixture only (all-USB); the UV subset just has to load.  Two strong scans in full
# plus a 1-in-26 sparse sample.
get http://astrogeo.org/s0/vlba_fits/bd152ie/VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.idifits \
    VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.idifits
$TRIM_IDI "$SRC/VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.idifits" \
    "$ROOT/astrogeo/VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.excerpt.idifits" \
    --target-mb 18 --blocks 2 --nbl 2 --nauto 2 --seed 0
$VERIFY "$SRC/VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.idifits" \
    "$ROOT/astrogeo/VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.excerpt.idifits"

# astrogeo/ files copied whole (no transformation, no command needed):
#   leotest+1.5us.fits           http://astrogeo.org/s0/corr_fits/r1482/leotest+1.5us.fits
#   2013_08_27_rk01ak_L_01.fits  http://astrogeo.org/s0/radik_fits/2013_08_27_rk01ak_L_01.fits
#   2008_05_04_bw089_03.fits     http://astrogeo.org/s0/vlba_fits/bw089/2008_05_04_bw089_03.fits
#   2008_05_04_bw089_04.fits     http://astrogeo.org/s0/vlba_fits/bw089/2008_05_04_bw089_04.fits

# =====================================================================================
# vlba-difx/ — NRAO archive.  These two are NOT plain URLs: they come from an anonymous
# staging request at https://data.nrao.edu/portal/ (see MANIFEST.md for the product
# locators).  Point $SRC at the downloaded .idifits and the commands below reproduce the
# published excerpts bit for bit (SHA1s in MANIFEST.md).
# The --anchor windows are exactly the scans the gated VLBIFiles.jl testitems name.
# =====================================================================================
AC="$SRC/VLBA_BL178AC_bl178ac_BIN0_SRC0_0_111228T171125.idifits"
AL="$SRC/VLBA_BL178AL_bl178al_BIN0_SRC0_0_120712T141309.idifits"
if [ -f "$AC" ]; then
    $TRIM_IDI "$AC" \
        "$ROOT/vlba-difx/VLBA_BL178AC_bl178ac_BIN0_SRC0_0_111228T171125.excerpt.idifits" \
        --target-mb 60 --anchor 'KP-LA@2011-12-12T02:09:30/2011-12-12T02:12:44' --seed 0
    $VERIFY "$AC" \
        "$ROOT/vlba-difx/VLBA_BL178AC_bl178ac_BIN0_SRC0_0_111228T171125.excerpt.idifits"
else
    echo "skip BL178AC: $AC not present (NRAO staging request required)"
fi
if [ -f "$AL" ]; then
    $TRIM_IDI "$AL" \
        "$ROOT/vlba-difx/VLBA_BL178AL_bl178al_BIN0_SRC0_0_120712T141309.excerpt.idifits" \
        --target-mb 50 --anchor 'FD-LA@2012-06-25T23:30:44/2012-06-25T23:36:30' --seed 0
    $VERIFY "$AL" \
        "$ROOT/vlba-difx/VLBA_BL178AL_bl178al_BIN0_SRC0_0_120712T141309.excerpt.idifits"
else
    echo "skip BL178AL: $AL not present (NRAO staging request required)"
fi

# =====================================================================================
# misc/ — UVFITS random-groups files.  trim_idifits.py does NOT apply to these: the
# visibilities are random groups in the primary HDU, not a UV_DATA binary table, and the
# AIPS AN/FQ/SU tables FOLLOW the data instead of preceding it.
# =====================================================================================

# --- GMRT GVFITS pair, 2004 Venus campaign, 532 MB each (Zenodo 4529203, CC-BY) ---
# The FQ-sign witness pair: LTA has CH WIDTH = -125000 with SIDEBAND = +1 (the AIPS
# encoding of a descending axis), LTB is its +125000 twin.  The excerpts keep the first
# 19112 of 339300 groups; the AIPS FQ table is byte-identical, which is the whole point.
get 'https://zenodo.org/records/4529203/files/05BBA01_VENUS22.LTA_LL.1FITS.fits?download=1' \
    05BBA01_VENUS22.LTA_LL.1FITS.fits
get 'https://zenodo.org/records/4529203/files/05BBA01_VENUS22.LTB_LL.1FITS.fits?download=1' \
    05BBA01_VENUS22.LTB_LL.1FITS.fits
for T in LTA LTB; do
    $TRIM_UVF "$SRC/05BBA01_VENUS22.${T}_LL.1FITS.fits" \
        "$ROOT/misc/05BBA01_VENUS22.${T}_LL.1FITS.excerpt.fits" --target-mb 30
    $VERIFY "$SRC/05BBA01_VENUS22.${T}_LL.1FITS.fits" \
        "$ROOT/misc/05BBA01_VENUS22.${T}_LL.1FITS.excerpt.fits"
done

# --- CARMA via casacore, 16 IFs, CH WIDTH < 0 AND SIDEBAND = -1, 135 MB ---
get https://open-bitbucket.nrao.edu/projects/CASA/repos/casatestdata/raw/uvfits/mirsplit.UVFITS \
    mirsplit.UVFITS
$TRIM_UVF "$SRC/mirsplit.UVFITS" "$ROOT/misc/mirsplit.excerpt.UVFITS" --target-mb 30
$VERIFY "$SRC/mirsplit.UVFITS" "$ROOT/misc/mirsplit.excerpt.UVFITS"

# --- SMA SWARM, 16384 channels, negative TOTAL BANDWIDTH, 263 MB ---
get https://dataverse.harvard.edu/api/access/datafile/3175052 \
    SVS13C.sub.SWARM.lsb.s3.170127.uvfits
$TRIM_UVF "$SRC/SVS13C.sub.SWARM.lsb.s3.170127.uvfits" \
    "$ROOT/misc/sma_masses/SVS13C.sub.SWARM.lsb.s3.170127.excerpt.uvfits" --target-mb 30
$VERIFY "$SRC/SVS13C.sub.SWARM.lsb.s3.170127.uvfits" \
    "$ROOT/misc/sma_masses/SVS13C.sub.SWARM.lsb.s3.170127.excerpt.uvfits"

# --- K08161.0.FITS : one member of the MPIfR DiFX 1.5.0 test-data tarball, 1 370 554 B ---
# The one file here whose published bytes are not a download but a tarball member, so
# extracting it is the whole procedure — no trimming, no rewriting.  The member is 216 000 B
# and comes out byte for byte as committed, which the SHA1SUMS line below is the proof of.
get https://ftp.mpifr-bonn.mpg.de/vlbiarchive/DiFX_testdata/k08161/k08161.difx-1.5.0.outputfiles.tar.gz \
    k08161.difx-1.5.0.outputfiles.tar.gz
tar -xzOf "$SRC/k08161.difx-1.5.0.outputfiles.tar.gz" K08161.0.FITS > "$ROOT/misc/K08161.0.FITS"
(cd "$ROOT" && grep ' misc/K08161\.0\.FITS$' SHA1SUMS | sha1sum -c -)

# Files copied whole (no transformation, no command needed) — see README.md for every URL:
#   misc/emerlin_multiuv.IDI1,
#   misc/sma_masses/Per35.SWARM.1.3mm.s1.{lsb,usb}.1.151006.uvfits,
#   vsop/v050c.fits.1-8, jive/n09q2_1_1-shortened.IDI1, jive/ep075f_WSRT.IDI1

echo
echo "all excerpts regenerated; compare against SHA1SUMS with:  sha1sum -c ../SHA1SUMS"
