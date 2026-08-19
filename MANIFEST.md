# MANIFEST — VLBIFiles.jl test data

Every file here is either **a byte-identical copy of a published file**, or **a verbatim subset
of one**: a copy in which only the visibility container was shortened (a subset of records, each
copied byte for byte, in the original order) and exactly one header card — FITS-IDI `NAXIS2` or
UVFITS `GCOUNT` — was rewritten to the new record count. No value is ever recomputed, rescaled,
averaged, reordered or synthesised, and no other HDU is altered in any way. The files in
`pkg-data/` are byte-identical copies too, but of the fixtures that lived in
`VLBIFiles.jl/test/data/` rather than of an archive URL — see that section for what is and is
not known about where each came from.

The two cutting tools and the checker live in `scripts/`:

| script | what it does |
|---|---|
| `trim_idifits.py` | FITS-IDI: keeps a subset of `UV_DATA` rows, rewrites `NAXIS2`, copies every other HDU as raw bytes |
| `trim_uvfits_groups.py` | UVFITS random groups: keeps a subset of groups, rewrites `GCOUNT`, copies every table extension as raw bytes (they move up in the file because the tables *follow* the data) |
| `verify_excerpt.py` | re-proves the guarantee: hashes everything outside the trimmed segment of the full file and of the excerpt and diffs the trimmed HDU's header card by card |
| `MAKE.sh` | regenerates every excerpt from its source URL, then runs `verify_excerpt.py` on it |

`verify_excerpt.py` was run on all nine excerpts below; all nine report
**`VERDICT: verbatim subset`** with exactly one differing card.

`README.md` is the front page: it lists every file with its source URL, original size and
SHA1, staged SHA1 and the testitem that uses it, plus the provenance and acknowledgments.
This manifest carries the detail underneath that table — what each file's header actually
contains, and which reader behaviour it pins down.

---

## `astrogeo/` — astrogeo.org, Leonid Petrov's open Apache tree (plain HTTP, no login)

| file | bytes | staged SHA1 | transformation |
|---|---|---|---|
| `leotest+1.5us.fits` | 1 126 080 | `9fb19c15c6f503ab7b57b865e54dbe0a73cd9877` | none |
| `2013_08_27_rk01ak_L_01.fits` | 3 804 480 | `8687018ba3c4f5affd8de13b57f3e68a584c8bd1` | none |
| `2008_05_04_bw089_03.fits` | 5 529 600 | `fc462650536002b22c5d5d71376ac86efce2807a` | none |
| `2008_05_04_bw089_04.fits` | 5 673 600 | `cd3b71ac93a0e0d8a9a3cb716ea077c9b8c67514` | none |
| `VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.excerpt.idifits` | 18 270 720 | `e26b6a0b74df1b2e9accbae0336f346824f5590f` | verbatim subset of `UV_DATA` rows, 7 896 of 173 484; all other HDUs byte-identical; one card (`NAXIS2`) rewritten |
| `2012_04_17_raes03v_C_01.excerpt.fits` | 39 487 680 | `1b72988fd03740c21958128ef126a619839a6966` | verbatim subset of `UV_DATA` rows, 9 354 of 27 599; all other HDUs byte-identical; one card (`NAXIS2`) rewritten |
| `2011_06_28_rdv87_alt_01.excerpt.fits` | 39 916 800 | `5c6ab9cca75c811187ba6320bb4743ebf121a76d` | verbatim subset of `UV_DATA` rows, 389 of 293 750; all other HDUs byte-identical; one card (`NAXIS2`) rewritten |

### Sources and what each file is for

**`leotest+1.5us.fits`** — <http://astrogeo.org/s0/corr_fits/r1482/leotest+1.5us.fits>,
original SHA1 `9fb19c15c6f503ab7b57b865e54dbe0a73cd9877` (1 126 080 B, unchanged).
DiFX-trunk 2011, 16 bands, LSB on bands 2 and 10, `NO_STKD = 1`, no PHASE-CAL.
*Serves:* the cleanest LSB **visibility** witness on the open web — the 14 USB bands read
−1425…−1502 ns and the two LSB bands read **+1504.8 / +1508.2** raw, **−1504.8 / −1508.2**
conjugated. Also the single-polarization reader path (`interferometer_model`, `model_comps`,
`system_temperature` all name `_2` columns that do not exist when `NO_POL = 1`).

**`2013_08_27_rk01ak_L_01.fits`** —
<http://astrogeo.org/s0/radik_fits/2013_08_27_rk01ak_L_01.fits>, original SHA1
`8687018ba3c4f5affd8de13b57f3e68a584c8bd1` (3 804 480 B, unchanged).
`CORRVERS = DiFX-ra` (RadioAstron branch), `SIDEBAND = [-1, 1]`, `BANDFREQ = [0, 0]`,
`CRPIX3 = 0.75`, extra `SPACECRAFT_ORBIT`, `SYSTEM_TEMPERATURE` with **0 rows**.
*Serves:* small DiFX-ra structural fixture and an LSB visibility witness
(raw −49.93 / +56.27 ns → conjugation makes them agree). It is **not** a pcal-convention
witness (2 antennas, 10 MHz tone spacing → the tone-pair delay wraps).

**`2008_05_04_bw089_0{3,4}.fits`** —
<http://astrogeo.org/s0/vlba_fits/bw089/2008_05_04_bw089_03.fits> and `…_04.fits`,
original SHA1s `fc462650536002b22c5d5d71376ac86efce2807a` / `cd3b71ac93a0e0d8a9a3cb716ea077c9b8c67514`
(5 529 600 / 5 673 600 B, unchanged).
VLBA **hardware** correlator (`FXCORVER = 4.22`, no `CORRELAT`/`CORRVERS`),
`SIDEBAND = [-1,1,-1,1]`, `CRPIX3 = 0.5625`, UVW columns named `UU-L/VV-L/WW-L`, and the full
aux-table set (`FLAG`, `SYSTEM_TEMPERATURE`, `PHASE-CAL`, `WEATHER`, `GAIN_CURVE`,
`TAPE_STATISTICS`, 0-row `SPACECRAFT_ORBIT`) placed **before** `UV_DATA`.
*Serves:* the only known public hardware-correlator files with `SIDEBAND = -1` **and** nonzero
LSB visibilities **and** a PHASE-CAL table — raw +30.51 / −30.75 ns → conjugated consistent, so
the DiFX visibility convention is confirmed for a non-DiFX writer. Also the `NO_TONES = 1`
PHASE-CAL case in which no tone ordering exists and the version gate must refuse.

**`VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.excerpt.idifits`** —
<http://astrogeo.org/s0/vlba_fits/bd152ie/VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.idifits>,
original 370 641 600 B, original SHA1 `15c7fa2bc3c5be91a4f36e137ce4c2f30bb8a369`
(server `Last-Modified: Sun, 22 Feb 2026 01:00:53 GMT`).
`CORRELAT = DIFX`, **`CORRVERS = DIFX-2.1`**, 5 merged `DIFXJOB`s, VLBA pulsar-gating experiment.
*Serves:* the **duplicated-ANTENNA** claim — `ANTENNA` has **50 rows = 10 antennas × 5 jobs**,
`ANTENNA_NO` cycling 1…10 five times — plus the `GATEMODL` extension and a genuine DIFX-2.1-era
header. All-USB (`SIDEBAND = [1,1,1,1]`), so it carries no sideband information; the UV subset
only has to load. PHASE-CAL(599) is present and untouched.
*Excerpt:* the two strongest source-blocks in full (baselines 3-9/3-4 and 2-5/1-4 with their
autocorrelations) plus a 1-in-26 sparse sample of everything else → 55 baselines, 1 824
autocorrelations.

**`2012_04_17_raes03v_C_01.excerpt.fits`** —
<http://astrogeo.org/s0/radik_fits/raes03v/2012_04_17_raes03v_C_01.fits>,
original 115 678 080 B, original SHA1 `fa4c172f1b01ac925d990dc604e1f850692b562c`.
(The local working copy was named `raes03v_C_01.fits`; the staged name is the original one.)
`CORRVERS = DiFX-ra`, FITS written 2012-12-10, C band, antennas EF/MC/**RA**/YS,
`SIDEBAND = [-1, 1]`, `PHASE-CAL` 371 rows × 2 pol, `NO_TONES = 2`, ascending `PC_FREQ` in
every row of both bands.
*Serves:* **the file that pins the DiFX-ra PHASE-CAL convention to `op = :values`** (conjugate
the tone values and reverse the tone axis, leave `PC_FREQ` alone — the DiFX ≤ 2.0.1 class), and
a high-SNR LSB visibility witness.
*Excerpt:* every record of the three **ground–ground** baselines EF-MC, EF-YS, MC-YS (RA is the
RadioAstron spacecraft, whose |τ| > 500 ns space baselines are not usable for the sideband test)
plus every 10th autocorrelation record of all four antennas — 9 354 of 27 599 rows.
`PHASE-CAL`, `SPACECRAFT_ORBIT`, `SYSTEM_TEMPERATURE`(0 rows), `INTERFEROMETER_MODEL`, `CALC`,
`MODEL_COMPS` are all byte-identical to the full file.

**`2011_06_28_rdv87_alt_01.excerpt.fits`** —
<http://astrogeo.org/s0/vlba_fits/rdv87/2011_06_28_rdv87_alt_01.fits>,
original 9 685 624 320 B, original SHA1 `0f20f46859f7ed133e3025f5ac8b7f9f80f576a3`
(server `Last-Modified: Thu, 09 Feb 2012 15:42:03 GMT`).
RDV87 geodetic S/X, `CORRVERS = DIFX-2.0.1`, 8 antennas, `NO_BAND = 16` alternating S(USB) and
X(LSB), `NO_CHAN = 256`, `NO_STKD = 1`, `PHASE-CAL` **12 494 rows**, `NO_POL = 1`.
*Serves:* the **plain-HTTP claim-(B) witness** — a second, independent DIFX-2.0.1 file that
confirms the baseband LSB visibility convention and the conjugation half of the DiFX ≤ 2.0.1
PHASE-CAL bug. (It cannot resolve the tone-*order* half: the X-band tone pair is 22 MHz apart
and the statistic wraps.) Also a `NO_POL = 1` PHASE-CAL table, which the current `phase_cal`
reader cannot read.
*Excerpt:* the 83 records of the **FD–PT** scan on source 34 (2011-06-29 04:37:43…04:43:11) that
the VIS test in `astrogeo_geo/README.md` uses, the FD and PT autocorrelations of the same scan,
and a 1-in-2111 sparse sample of everything else — 389 of 293 750 rows, covering 32 baselines
and 76 sources. UV rows are 32 880 B here and the auxiliary tables alone are 27.1 MB, so ~390
rows is the whole 40 MB budget. `PHASE-CAL`(12 494), `FLAG`(3 864), `SYSTEM_TEMPERATURE`(6 340),
`WEATHER`(1 304), `GAIN_CURVE`(8), `INTERFEROMETER_MODEL`(6 968), `MODEL_COMPS`(6 968) and
`CALC`(5) are all byte-identical to the full file.

---

## `vlba-difx/` — NRAO archive (anonymous staging request, not a plain URL)

| file | bytes | staged SHA1 | transformation |
|---|---|---|---|
| `VLBA_BL178AL_bl178al_BIN0_SRC0_0_120712T141309.excerpt.idifits` | 50 005 440 | `e51d5eb5c767a7788f4489a509cf8124acd4dfd2` | verbatim subset of `UV_DATA` rows, 3 801 of 1 162 555; all other HDUs byte-identical; one card (`NAXIS2`) rewritten |
| `VLBA_BL178AC_bl178ac_BIN0_SRC0_0_111228T171125.excerpt.idifits` | 60 004 800 | `490eac599ad4f7b527a0f77f398a0f5c778dc109` | verbatim subset of `UV_DATA` rows, 5 797 of 1 385 432; all other HDUs byte-identical; one card (`NAXIS2`) rewritten |

**`…BL178AC…excerpt.idifits`** — source
`VLBA_BL178AC_bl178ac_BIN0_SRC0_0_111228T171125.idifits`, 5 953 806 720 B, SHA1
`5d6515577b94107445719c3a0619830953292ef9` (matches the archive-provided `SHA1SUMS`).
Obtained through <https://data.nrao.edu/portal/> with product locator
`uid://vlba/correlation/fd2b205c-0f70-40a6-847e-1198becf2bf0`; there is no direct URL.
MOJAVE 15 GHz, `CORRVERS = DIFX-2.0.1`, `SIDEBAND = [-1,1,-1,1,-1,1,-1,1]`,
`PHASE-CAL` with `NO_TONES = 2`, `NO_BAND = 8`.
*Serves:* **the** claim-(B) reference — LSB visibilities baseband, and LSB PHASE-CAL tone values
conjugated *and* tone-reversed (band-centre tone-phase correlation −0.99 as stored). The
excerpt's `--anchor` keeps in full the 3C84 scan (KP–LA, 2011-12-12 02:09:30…02:12:44) that the
gated VLBIFiles.jl testitem addresses by name.

**`…BL178AL…excerpt.idifits`** — source
`VLBA_BL178AL_bl178al_BIN0_SRC0_0_120712T141309.idifits`, 5 000 201 280 B, SHA1
`cdc2f0270fbf576380dac033c8aabb398018e3df` (verified against the request's `SHA1SUMS`),
request 152951576, download URL
`https://dl-dsoc.nrao.edu/anonymous/152951576/667047394073cca89fb17619ed0153ad/BL178/BL178AL/VLBA_BL178AL_bl178al_BIN0_SRC0_0_120712T141309.idifits`
(request-scoped, expires).
Same MOJAVE 8×LSB/USB setup, `CORRVERS = DIFX-2.1`.
*Serves:* **the** claim-(C) reference — LSB visibilities still baseband, but LSB PHASE-CAL now
**clean** (cross-sideband tone-phase correlation **+0.99 with no transform**, the exact mirror of
BL178AC's −0.99), i.e. the DiFX-2.1 fix. The `--anchor` keeps in full the 0923+392 scan
(FD–LA, 2012-06-25 23:30:44…23:36:30, 111 records) that the gated testitem names.

> **Size note.** The BL178AC excerpt is 60.0 MB, above GitHub's 50 MB *warning* threshold
> (well below the 100 MB hard block). A proven 38.0 MB alternative exists with the same anchor
> scan (`--target-mb 38 --blocks 2 --nbl 2 --nauto 2`, SHA1
> `2d650302cb1e88cd4c5fc5f9337e3b2a3cefe934`) if the warning is unwanted; a 25 MB variant is
> only reachable by dropping `INTERFEROMETER_MODEL` and `MODEL_COMPS` entirely, because those
> two tables plus PHASE-CAL set a 35.2 MB floor.

---

## `misc/` — UVFITS random-groups files and two small FITS-IDI files

| file | bytes | staged SHA1 | transformation |
|---|---|---|---|
| `K08161.0.FITS` | 216 000 | `8628431e8fd0a94e006818bee3d29b294957ff15` | none |
| `emerlin_multiuv.IDI1` | 2 128 320 | `811e6008d39087a58f9b238b3072b54fcc57b7bd` | none |
| `05BBA01_VENUS22.LTA_LL.1FITS.excerpt.fits` | 30 000 960 | `cbba34afa74bd8d8318a0252f720fe7f7d5509ea` | verbatim subset of random groups, 19 112 of 339 300; all table HDUs byte-identical; one card (`GCOUNT`) rewritten |
| `05BBA01_VENUS22.LTB_LL.1FITS.excerpt.fits` | 30 000 960 | `c2299f8eaa4b4674b7cb5925ab4428fa1ee80ede` | verbatim subset of random groups, 19 112 of 339 300; all table HDUs byte-identical; one card (`GCOUNT`) rewritten |
| `mirsplit.excerpt.UVFITS` | 30 000 960 | `11d538fa7f66d588d83cf75c13c96860906508bf` | verbatim subset of random groups, 3 983 of 18 000; all table HDUs byte-identical; one card (`GCOUNT`) rewritten |

**`emerlin_multiuv.IDI1`** —
<https://open-bitbucket.nrao.edu/projects/CASA/repos/casatestdata/raw/fits/emerlin_multiuv.IDI1>,
original SHA1 `811e6008d39087a58f9b238b3072b54fcc57b7bd` (2 128 320 B, unchanged).
`CORRELAT = 'e-MERLIN'`, `SIDEBAND = [1,1,1,1]`, no PHASE-CAL, `MAXIS1 = 2` with
`CRVAL1 = 1.0` (1-based COMPLEX axis, no weight plane), and — the point of the file — **two
`UV_DATA` HDUs of 63 rows each**.
*Serves:* the duplicated-EXTNAME case. `fits[extname]` answers with the first HDU of that name
and says nothing about the others, so half the visibilities would go missing silently; the
reader must refuse the file instead. The only real file found with a repeated table name.

**`K08161.0.FITS`** — member `K08161.0.FITS` of
<https://ftp.mpifr-bonn.mpg.de/vlbiarchive/DiFX_testdata/k08161/k08161.difx-1.5.0.outputfiles.tar.gz>
(tarball 1 370 554 B); extracted file 216 000 B, SHA1
`8628431e8fd0a94e006818bee3d29b294957ff15` (unchanged).
`CORRELAT = DIFX` with **no `CORRVERS` card**, LSB on bands 2 and 10, `CRPIX3 = 0.5625`,
single polarization, no PHASE-CAL.
*Serves:* the "DiFX file that does not identify its version" branch of the correlator-version
logic, and the `NO_POL = 1` reader paths. Its 60 UV rows are too few for a delay statistic —
that is a property of the published file, not of anything done here.

**`05BBA01_VENUS22.LTA_LL.1FITS.excerpt.fits`** —
<https://zenodo.org/records/4529203/files/05BBA01_VENUS22.LTA_LL.1FITS.fits?download=1>
(Zenodo record 4529203, DOI 10.5281/zenodo.4529203, CC-BY), original 532 054 080 B, original
SHA1 `4f147ad15b3ed917a56a430748c371258eeb546b`.
GMRT GVFITS, 2004 Venus campaign, 244 MHz, 128 channels, 30 antennas.
`CDELT4 = -125000`; AIPS FQ: `IF FREQ = 0`, **`CH WIDTH = -125000`**, `TOTAL BANDWIDTH = +1.6e7`,
**`SIDEBAND = +1`** — the AIPS-style encoding in which the descending axis is carried by the
sign of `CH WIDTH` while `SIDEBAND` stays `+1`.
*Serves:* the first half of the `UVFITS FQ sign conventions (real files)` testitem: the OR-rule
`sideband = -1 iff (CH WIDTH < 0 or SIDEBAND < 0)`, `nchan == 128`, `width == 1.6e7 Hz`,
`frequencies[1] == 243 937 500 Hz`, `frequencies[end] == 228 062 500 Hz`, descending.

**`05BBA01_VENUS22.LTB_LL.1FITS.excerpt.fits`** —
<https://zenodo.org/records/4529203/files/05BBA01_VENUS22.LTB_LL.1FITS.fits?download=1>,
original 532 054 080 B, original SHA1 `96b4e1f0ce90708df66e18b12e9534bb14e2a627`.
The ascending twin of the same observation: `CH WIDTH = +125000`, everything else identical.
*Serves:* the control half of the same testitem (`sideband == +1`, `frequencies[1] ==
244 062 500 Hz`, `frequencies[end] == 259 937 500 Hz`, ascending) — the sign rule must not
disturb it.

**`mirsplit.excerpt.UVFITS`** —
<https://open-bitbucket.nrao.edu/projects/CASA/repos/casatestdata/raw/uvfits/mirsplit.UVFITS>,
original 135 463 680 B, original SHA1 `49e03a8fc019d4a659fadd65d737fca8e148e3c2`.
CARMA, written by casacore (CASA `exportuvfits`), 16 IFs, every one with
`CH WIDTH = -12 500 000` **and** `SIDEBAND = -1` **and** `TOTAL BANDWIDTH = +487 500 000`.
*Serves:* the third case of the same testitem — both indicators negative at once, so the rule
must be OR and not XOR: 16 windows, all `sideband == -1`, all `nchan == 39`, all descending.
Copied whole would be 135 MB, above GitHub's 100 MB hard block, hence the excerpt.

### `misc/sma_masses/` — SMA, Harvard Dataverse (MASSES survey, Ian Stephens)

All fetched as `https://dataverse.harvard.edu/api/access/datafile/<id>`; both datasets are
CC0 1.0. The three files kept are the ones the FQ-sign testitem needs — the negative-
`TOTAL BANDWIDTH` trigger with its upper-sideband control, and the 16 384-channel excerpt.
(The MASSES release also holds ~17 small `*.sub.cont*` MIRIAD-converted continuum files of the
same targets; they are not kept here, because the sign information is lost in that conversion,
so they exercise nothing the two SWARM files do not.)

| file | bytes | staged SHA1 | datafile id | dataset DOI | transformation |
|---|---|---|---|---|---|
| `Per35.SWARM.1.3mm.s1.lsb.1.151006.uvfits` | 36 253 440 | `872c7202fb5bc85c92198848696f790bab223375` | 3616840 | 10.7910/DVN/NGA7DX | none |
| `Per35.SWARM.1.3mm.s1.usb.1.151006.uvfits` | 36 253 440 | `5eed0adc47d3d5e29d45b8d6d452d9b2d655a740` | 3616842 | 10.7910/DVN/NGA7DX | none |
| `SVS13C.sub.SWARM.lsb.s3.170127.excerpt.uvfits` | 29 923 200 | `a1fc17cfc91a0b075b54f09174088a4a24c9a684` | 3175052 | 10.7910/DVN/GQTCQR | verbatim subset of random groups, 152 of 1 340; all table HDUs byte-identical; one card (`GCOUNT`) rewritten |

**`Per35.SWARM.1.3mm.s1.lsb.1.151006.uvfits`** (36 MB, copied whole) — SMA SWARM lower sideband
written by MIR (IDL). `CH WIDTH = -1 625 000`, **`TOTAL BANDWIDTH = -1 664 000 000` (negative)**,
`SIDEBAND = -1`.
*Serves:* the fourth case of the FQ-sign testitem — the negative `TOTAL BANDWIDTH` that used to
produce a negative `nchan` and throw from `frequencies`. Assertions: `sideband == -1`,
`nchan == 1024`, `width == 1.664e9 Hz`, descending, `frq[1] - frq[end] ≈ width·(nchan-1)/nchan`.
Its `…usb…` twin is the all-positive control.

**`SVS13C.sub.SWARM.lsb.s3.170127.excerpt.uvfits`** — original 263 531 520 B, original SHA1
`abdc3e5b75b21a5979e486deb79fc1f56a02ca6e`. `CH WIDTH = -139 648.4375`,
`TOTAL BANDWIDTH = -2 288 000 000`, `SIDEBAND = -1`, **16 384 channels**, `BITPIX = 32`.
*Serves:* the fifth case of the same testitem (`sideband == -1`, `nchan == 16384`, descending)
and the very-wide-spectrum path. Copied whole it would be 263 MB, above the 100 MB hard block.

---

## `jive/` — EVN, correlated at JIVE

| file | bytes | staged SHA1 | transformation |
|---|---|---|---|
| `n09q2_1_1-shortened.IDI1` | 1 725 120 | `5af29bac3f7bf102fe4f0144bddb56faa13f1365` | none |
| `ep075f_WSRT.IDI1` | 77 771 520 | `8792ddd266d2bc25b94f9a49ee4cf71220a01d8a` | none |

**`n09q2_1_1-shortened.IDI1`** —
<https://open-bitbucket.nrao.edu/projects/CASA/repos/casatestdata/raw/fits/n09q2_1_1-shortened.IDI1>
(the shortened copy NRAO distributes; EVN experiment N09Q2, SFXC). 43 GHz, 8 bands × 16
channels, `LL` only, `SIDEBAND` all `+1`.
*Serves:* the plain reading half of the zero-based-`COMPLEX`-axis testitem — `CTYPE1='COMPLEX'`
with `MAXIS1 = 3, CRVAL1 = 0, CDELT1 = 1, CRPIX1 = 1`, i.e. axis values 0,1,2 where VLBA/DiFX
writes 1,2,3. The components must be identified by position, not by coordinate value.

**`ep075f_WSRT.IDI1`** — <https://archive.jive.nl/exp/EP075F_130526/fits/ep075f_WSRT.IDI1>.
`CORRELAT = 'DZB'` (WSRT), 4.9 GHz, 8 bands × 64 channels, 4 Stokes; `SIDEBAND = +1` on every
band with **`CH_WIDTH` alternating ±312 500 Hz**, and the two bands of each pair sharing their
`BANDFREQ`.
*Serves:* the same zero-based axis, plus the end-to-end proof of the `read_freqs` OR-rule on a
correlator that carries the sideband only in the sign of `CH_WIDTH`: the per-band delay of each
`CH_WIDTH < 0` band agrees in sign with its USB partner's only after the conjugation VLBIFiles
applies (93 % of 251 well-determined baseline/band pairs; 0.63 ns median difference).

---

## `vsop/` — VSOP/HALCA, VLBA hardware correlator, DARTS (ISAS/JAXA)

| file | bytes | staged SHA1 | transformation |
|---|---|---|---|
| `v050c.fits.1-8` | 1 699 200 | `d4ddb1a4277efb859a4ba5c56e9902e044969159` | none |

<https://data.darts.isas.jaxa.jp/pub/halca/VSOP_CorrelatedData/v050c/event/v050c.fits.1-8>,
original SHA1 `d4ddb1a4277efb859a4ba5c56e9902e044969159` (1 699 200 B, unchanged).
`ORIGIN = 'VLBA Correlator'`, `FXCORVER = 4.20`, `DATE-OBS = 1999-04-01`, 2 bands (both USB),
`LL` only, with the full instrumental table set — `PHASE-CAL` (`NO_TONES = 3`, `NO_POL = 1`,
tone frequencies **not monotonic**: band 1 = [4801, 4813, 4802] MHz), `SYSTEM_TEMPERATURE`,
`GAIN_CURVE`, `FLAG`, `WEATHER`, `SPACECRAFT_ORBIT`.
*Serves:* the instrumental half of the single-polarization aux-table testitem — `PHASE-CAL`,
`SYSTEM_TEMPERATURE` and `GAIN_CURVE` written with `_1` columns only. Both bands being upper
sideband, no band is classified or transformed, so the non-monotonic tone order is harmless
here — and it is the counterexample to any "descending `PC_FREQ` means LSB" heuristic.

---

## `pkg-data/` — the fixtures VLBIFiles.jl used to carry in `test/data/`

Copied **byte for byte** out of the package repository when the package stopped carrying data
of its own; nothing here was cut, rewritten or regenerated. Unlike the rest of this repository
they are not all raw correlator output — three are images, three are difmap model files and one
is a fourfit `alist` summary — and only six have an exact recorded source URL, namely the six
the test suite used to fetch on demand (the URL is the one in the code that fetched them). The
others are stated as *legacy VLBIFiles test fixture, original source not re-verified*: the
header identification below is read out of the file itself and is fact; the download it came
from is not recorded anywhere and is not guessed at here.

| file | bytes | staged SHA1 | transformation |
|---|---|---|---|
| `0332-391.uvfits` | 14 670 720 | `7e4e2a73864816ee1a21adfa0ba850e04df49da0` | none |
| `BL146_1.fits` | 2 448 000 | `f4ab6eea1ece41483b3dc5ec247d69c342be633c` | none |
| `DDTSUVDATA.fits` | 596 160 | `12e46c6deefa634b96065ed461e93d9d4eb1392c` | none |
| `J1256-0547_X_2020_10_18_pet_vis.fits` | 236 160 | `daa9bd688580ab5016caa2708ae57d24b8ca9fed` | none |
| `SR1_3C279_2017_101_hi_hops_netcal_StokesI.uvfits` | 1 238 400 | `98c4fdcab7243b66ca02b8165ceebb0f6f8dd5d5` | none |
| `alist_v6.fsumm` | 127 814 | `77226072ae5dba628e2e855f68c130f2356c69f8` | none |
| `datafile_01-01_230GHz.uvfits` | 178 560 | `c1ae1e63c2c297a9442a9eb57d28fee0c8e9694c` | none |
| `difmap_model.mod` | 532 | `7520d0c60635a889c766ba7b8e1cd4427c70715d` | none |
| `difmap_model_clean.mod` | 24 964 | `80163e3eea24b0dc4489465bf81178d0b64566e4` | none |
| `difmap_model_empty.mod` | 60 | `463d1702e22794fc0b1b68b86a6dd8e3cd6b5218` | none |
| `hops_3600_OJ287_LO+HI.medcal_dcal_full.uvfits` | 794 880 | `02bb180639a3dad2233be7d867a44ed9f2d4f57c` | none |
| `map.fits` | 1 071 360 | `9cba0872d2d8ea73bcc56dfdc84dbbfef7c5ad87` | none |
| `map_stacked.fits` | 2 234 880 | `132092bcf885761e3e88388ef1cb437407850e4b` | none |
| `mwa_1061316296.uvfits` | 1 529 280 | `947eb742ae446f7414e43b9bc30d9365965639aa` | none |
| `paper_zen.uvfits` | 66 240 | `136e6beaf0c02e11b7bf3b4ad4a8eb4770e70158` | none |
| `sampling_mean.fits` | 529 920 | `2689580af4d20ca33b98ac40afb2616423c6e920` | none |
| `vis.fits` | 2 131 200 | `9869f076976bdc1881f3b7174311b0994d2d2b19` | none |
| `vis_multichan.vis` | 826 560 | `70c38e69b4ff67f098aeffdf4cc0c26922097c21` | none |

### Sources and what each file is for

**`vis.fits`** — legacy VLBIFiles test fixture, original source not re-verified.
UVFITS random groups written by AIPS (`ORIGIN = 'AIPSphys43 … 31DEC11'`), `TELESCOP = VLBA`,
`OBSERVER = BL149CZ`, `DATE-OBS = 2010-12-24`, J1033+6051 at 15.33 GHz, `NAXIS = 7` with
8 IFs × 1 channel × 4 Stokes, 5 082 groups, `AIPS NX/FQ/AN` present, all-zero `POLAA/POLAB`.
*Serves:* the package's default UVFITS path end to end — `uvf simple` (uvtable values, baseline
and frequency bookkeeping), `uvf antenna polarization`, `closures calculations`, `sources`,
`uvtable_wide`, `coherencymatrices`, `lazycolumntable groupdata labeling`, `prefetch!`, and the
three `grouphdu …` items, which copy it to a temporary file and delete `BSCALE`/`PSCAL4`/`PZERO6`
from the copy to check the FITS defaults (the fixture itself is never modified).

**`vis_multichan.vis`** — legacy VLBIFiles test fixture, original source not re-verified.
AIPS UVFITS, `OBSERVER = BH019`, `DATE-OBS = 1996-06-05`, J0414+053A at 4.60 GHz, 8 IFs ×
16 channels, 515 groups.
*Serves:* the multi-channel window arithmetic (`uvf multichannel`, `frequency correctness
CRPIX=1 multichan`) and the `.vis` extension branch of `guess_type`.

**`BL146_1.fits`** — <https://fits.gsfc.nasa.gov/registry/fitsidi/BL146_1.fits>, the FITS-IDI
registry sample of the NASA GSFC FITS Support Office (2 448 000 B, unchanged).
VLBA hardware correlator, `ORIGIN = 'VLBA Correlator'`, `FXCORVER = 4.22`,
`DATE-OBS = 2007-08-23`, 4 bands × 8 channels × 4 Stokes, 1 000 `UV_DATA` rows, and the full
auxiliary set: `INTERFEROMETER_MODEL` (640), `MODEL_COMPS` (1 060), `PHASE-CAL` (241),
`SYSTEM_TEMPERATURE` (398), `FLAG` (1 058), `WEATHER` (70), `GAIN_CURVE` (10),
`TAPE_STATISTICS` (1 000), 0-row `SPACECRAFT_ORBIT`.
*Serves:* the FITS-IDI reader wherever a two-polarization file is needed — `FITS IDI small`,
`uvtable fitsidi`, `mmap column read`, `UV_DATA axis order`, `FITS-IDI auxiliary tables`,
`RDATE fallback to ARRAY_GEOMETRY`, the `NO_POL = 2` control of the single-polarization item,
the per-band `FLAG` widening path, and the one-HDU-per-name control of the e-MERLIN item.

**`DDTSUVDATA.fits`** — <https://fits.gsfc.nasa.gov/samples/DDTSUVDATA.fits> (596 160 B,
unchanged). VLA, 3C161, `DATE-OBS = 29/01/84`, written by AIPS in 1995
(`ORIGIN = 'AIPSRhesus NRAO/CV 580 15JUL95'`), 1.420 GHz, 28 antennas, 7 956 groups.
`NAXIS = 6`: the axis set is COMPLEX/STOKES/FREQ/RA/DEC with **no IF axis at all**.
*Serves:* `uvf NAXIS=6 no IF axis (DDTSUVDATA)` — the reader must synthesise the single
frequency window instead of indexing a missing axis. Also the oldest date any fixture carries,
which pins the two-digit-year `DD/MM/YY` date parsing.

**`0332-391.uvfits`** —
<https://github.com/astro-informatics/purify/raw/development/data/atca/0332-391.uvfits>
(14 670 720 B, unchanged). ATCA, `DATE-OBS = 2001-05-20`, written by Miriad `atlod`/`fits`,
1.432 GHz, 13 channels, Stokes I/Q/U/V, 6 antennas, 22 675 groups, **`CDELT4 < 0` with no
`AIPS FQ` table**.
*Serves:* `uvf NAXIS=6 no IF axis (ATCA)` — the sideband has to come from `sign(CDELT4)` when
there is no FQ table, and UVFITS values stay verbatim (no conjugation) even so, unlike the
FITS-IDI meaning of `sideband == -1`.

**`mwa_1061316296.uvfits`** — <https://github.com/RadioAstronomySoftwareGroup/rasg-datasets>
`v0.0.4/visibility_data/MWA/1061316296.uvfits`, renamed (1 529 280 B, unchanged).
MWA, `DATE-OBS = 2013-08-23`, written by pyuvdata 2.1.3, 167.075 MHz, linear feeds
(`XX/YY/XY/YX`), 16 256 groups, **every weight ≤ 0**.
*Serves:* `uvf linear polarization (MWA)` — linear-feed Stokes labelling, and the
all-flagged case in which `uvtable` legitimately comes out empty while `uvtable_wide` does not.

**`paper_zen.uvfits`** — same repository,
`v0.0.4/visibility_data/PAPER/zen.2456865.60537.xy.uvcRREAAM.uvfits`, renamed (66 240 B,
unchanged). PAPER, `DATE-OBS = 2014-07-27`, Miriad, 100 MHz, 11 channels, `NAXIS = 6`,
a single `XY` product, 285 groups.
*Serves:* `uvf NAXIS=6 linear pol (PAPER)`, and `faithful warnings` — the file that makes the
reader warn exactly once about what it cannot represent faithfully.

**`J1256-0547_X_2020_10_18_pet_vis.fits`** —
<https://astrogeo.org/images/J1256-0547/J1256-0547_X_2020_10_18_pet_vis.fits> (236 160 B,
unchanged). VLBA X-band, `DATE-OBS = 2020-10-18`, experiment `uh007b`, merged by
`UVA_MERGE v 2.1`: **three `AIPS AN` tables** (subarrays 1, 2, 3) with 8, 9 and 10 antennas,
1 132 groups.
*Serves:* `uvf multi-array baselines` — the baseline number carries the subarray in its
fractional part, so antenna lookup must pick the right array's table.

**`SR1_3C279_2017_101_hi_hops_netcal_StokesI.uvfits`** — legacy VLBIFiles test fixture from an
EHT 2017 April public data release, original download not re-verified.
`OBSERVER = EHT`, `DATE-OBS = 2017-04-11`, 3C279 at 229.07 GHz, HOPS → `netcal`, Stokes I only,
14 455 groups, `AIPS AN` with 9 stations.
*Serves:* `uvf EHT 2`, and the real-ECEF cross-check of `antenna catalog` (the SMT/`AZ` station
position, geodetic → ECEF within 100 m).

**`hops_3600_OJ287_LO+HI.medcal_dcal_full.uvfits`** — legacy VLBIFiles test fixture, EHT 2017
April HOPS product, original download not re-verified. `DATE-OBS = 2017-04-09`, OJ 287 at
227.07 GHz, the LO and HI bands as 2 IFs, 6 220 groups.
*Serves:* `uvf EHT 1` — two-band EHT UVFITS, source coordinates from the header.

**`datafile_01-01_230GHz.uvfits`** — legacy VLBIFiles test fixture, EHT 2013 campaign product,
original download not re-verified. `DATE-OBS = 2013-01-01`, M87 at 230 GHz, 1 772 groups,
`AIPS NX` present.
*Serves:* `uvf EHT 3`.

**`alist_v6.fsumm`** — legacy VLBIFiles test fixture, original source not re-verified.
HOPS `alist` **version 6** fringe summary, header line `* This file processed by alist, Tue Jul
26 09:28:16 2016`, 318 fringe records at ~228 GHz.
*Serves:* the entire `Alist` reader — `alist` (column parsing, SNR/phase/delay fields, times)
and the `.fsumm` branch of `guess_type`. The only alist fixture there is.

**`map.fits`** — legacy VLBIFiles test fixture, original source not re-verified.
512² CLEAN image of J0000+0248, `OBSERVER = bp192d3`, `DATE-OBS = 2016-01-03`, written by
`PIMA v 2.26`, `BUNIT = JY/BEAM`, 0.2 mas pixels, with an `AIPS CC` table of **361** components.
*Serves:* the image reader end to end — `img don't read data` (header-only load, beam),
`img read data`, `img read clean` (CC table → `MultiComponentModel`),
`img clean/residual/combined` (lazy vs materialised images), and the model round-trip in
`difmap model`.

**`map_stacked.fits`** — legacy VLBIFiles test fixture, original source not re-verified.
512² stacked CLEAN image of J0738+17, `OBSERVER = BR034`, `DATE-OBS = 1996-01-19`, difmap →
AIPS (`HISTORY DIFMAP Saved clean-map to fits file`), circular restoring beam and **no CC
table** at all.
*Serves:* `img stacked` — a stacked map has no component list, so the `MultiComponentModel`
load must fail (the item's `@test_broken`), while the image itself reads.

**`sampling_mean.fits`** — legacy VLBIFiles test fixture, original source not re-verified.
256² map, `TELESCOP = 'VLBI'`, `OBJECT = 'Unknown'`, `BUNIT = 'JY/PIXEL'`, no `BMAJ`/`BMIN`
cards, 0.003125° pixels — a mean uv-sampling map rather than a sky image.
*Serves:* `img nonstandard header names` — axes and units must still read, and `beam` must
report the missing `BMAJ` key rather than inventing one.

**`difmap_model.mod`, `difmap_model_clean.mod`, `difmap_model_empty.mod`** — legacy VLBIFiles
test fixtures, original source not re-verified. difmap model files: 4 components with
`v`-marked free parameters and a `SpecIndex` column; 631 delta components; and a file with a
phase-centre comment and nothing else.
*Serves:* `difmap model` — reading all three, the concrete `Point` element type of the clean
one, the empty case, and save/load round-trips through `tempname()`.

---

## Totals

| directory | files | bytes |
|---|---|---|
| `astrogeo/` | 7 | 113 808 960 |
| `vlba-difx/` | 2 | 110 010 240 |
| `jive/` | 2 | 79 496 640 |
| `vsop/` | 1 | 1 699 200 |
| `misc/` | 8 | 194 777 280 |
| `pkg-data/` | 18 | 28 705 690 |
| `scripts/` | 4 | 42 189 |
| **total (data + scripts)** | **38 + 4** | **528 540 199 B ≈ 528.5 MB** |

Largest single file: `vlba-difx/VLBA_BL178AC_…excerpt.idifits`, 60.0 MB (see the size note
above). Every other file is ≤ 78 MB; nothing is anywhere near GitHub's 100 MB hard limit.
