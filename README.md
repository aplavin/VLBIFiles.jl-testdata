# VLBIFiles.jl test data

Real VLBI data files for the test suite of [VLBIFiles.jl](https://github.com/JuliaAPlavin/VLBIFiles.jl).

Every file here is a **real observation** — or, for the correlator products, real correlator
output of a real observation. **Nothing in this repository is synthetic**: no file was
generated, simulated, hand-edited or "constructed to trigger" anything. They are published
files from public archives, downloaded and (where too large) shortened by the
strictly-verbatim procedure described below. The repository exists for one reason: so that
VLBIFiles.jl can test its readers against the real formats real correlators write —
lower-sideband conventions, single-polarization auxiliary tables, duplicated table names,
zero-based axes, negative bandwidths — instead of against fixtures written by the same
assumptions the reader is being tested for.

`pkg-data/` is the one directory with a different history: it holds the fixtures that lived in
`VLBIFiles.jl/test/data/` since the package began, moved here so that the package repository
carries no data at all. They are real files too — real visibilities, and real *products* of
real data (CLEAN images, difmap models, a fourfit alist summary, a mean uv-sampling map), which
raw correlator output is not. Seven of them have an exact source URL, recorded below; the rest
are long-standing fixtures whose original download was never recorded, and they are marked as
such rather than given a plausible-looking provenance.

The files are too large, and too numerous, to live inside the package repository, so the test
suite of VLBIFiles.jl clones this repository into `VLBIFiles.jl/test/VLBIFiles.jl-testdata/`
the first time a testitem needs a file, and uses an existing directory there as it is — no
fetch, no update, no network access. A checkout moves forward only when you `git pull` in it.
Testitems whose files are absent (no checkout and no network) skip themselves with a message.

## The verbatim-subset excerpt

Nine files were too large to publish whole (up to 9.7 GB), so this repository carries an
**excerpt**: a copy of the published file in which the visibility container holds only a
subset of the records — each record copied **byte for byte**, in the original order — and in
which exactly **one header card** was rewritten, the record count of that container
(FITS-IDI `NAXIS2`, UVFITS `GCOUNT`). Nothing else changes: every other HDU (`FREQUENCY`,
`ANTENNA` with its correlator-job duplicates, `PHASE-CAL`, `FLAG`, `SYSTEM_TEMPERATURE`,
`INTERFEROMETER_MODEL`, `AIPS AN/FQ/SU`, …) is transferred as raw bytes and is identical to
the published file, and no value is ever recomputed, rescaled, averaged, reordered or
synthesised. `scripts/` holds the two cutting tools, the checker that re-proves the property
from the two files alone (`verify_excerpt.py FULL EXCERPT` → `VERDICT: verbatim subset`), and
`MAKE.sh`, which regenerates every excerpt in this repository from its original source URL
bit for bit.

## Files

Sizes are bytes. "orig SHA1" is the SHA1 of the published file the copy was made from;
"staged SHA1" is the SHA1 of the file in this repository (identical to it when the file was
copied whole). All staged SHA1s are also in `SHA1SUMS`, which covers every data file and
every script in the repository — `sha1sum -c SHA1SUMS` checks the lot.

### `astrogeo/` — [astrogeo.org](http://astrogeo.org/), L. Petrov's open archive of raw correlator output

| file | source URL | orig size / SHA1 | done | staged size / SHA1 | used by |
|---|---|---|---|---|---|
| `leotest+1.5us.fits` | [`corr_fits/r1482/leotest+1.5us.fits`](http://astrogeo.org/s0/corr_fits/r1482/leotest+1.5us.fits) | 1 126 080 / `9fb19c15c6f503ab7b57b865e54dbe0a73cd9877` | none | 1 126 080 / `9fb19c15c6f503ab7b57b865e54dbe0a73cd9877` | `FITS-IDI single-polarization aux tables (NO_POL=1)` |
| `2013_08_27_rk01ak_L_01.fits` | [`radik_fits/2013_08_27_rk01ak_L_01.fits`](http://astrogeo.org/s0/radik_fits/2013_08_27_rk01ak_L_01.fits) | 3 804 480 / `8687018ba3c4f5affd8de13b57f3e68a584c8bd1` | none | 3 804 480 / `8687018ba3c4f5affd8de13b57f3e68a584c8bd1` | small `CORRVERS = DiFX-ra` structural fixture: `SIDEBAND = [-1,1]`, `CRPIX3 = 0.75`, `SPACECRAFT_ORBIT`, 0-row `SYSTEM_TEMPERATURE` |
| `2008_05_04_bw089_03.fits` | [`vlba_fits/bw089/2008_05_04_bw089_03.fits`](http://astrogeo.org/s0/vlba_fits/bw089/2008_05_04_bw089_03.fits) | 5 529 600 / `fc462650536002b22c5d5d71376ac86efce2807a` | none | 5 529 600 / `fc462650536002b22c5d5d71376ac86efce2807a` | VLBA **hardware** correlator with `SIDEBAND = -1`, nonzero LSB visibilities and a `NO_TONES = 1` `PHASE-CAL` |
| `2008_05_04_bw089_04.fits` | [`…/2008_05_04_bw089_04.fits`](http://astrogeo.org/s0/vlba_fits/bw089/2008_05_04_bw089_04.fits) | 5 673 600 / `cd3b71ac93a0e0d8a9a3cb716ea077c9b8c67514` | none | 5 673 600 / `cd3b71ac93a0e0d8a9a3cb716ea077c9b8c67514` | its sibling epoch, same structure |
| `VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.excerpt.idifits` | [`vlba_fits/bd152ie/VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.idifits`](http://astrogeo.org/s0/vlba_fits/bd152ie/VLBA_BD152IE_gatedie_BIN0_SRC0_0_121231T205433.idifits) | 370 641 600 / `15c7fa2bc3c5be91a4f36e137ce4c2f30bb8a369` | excerpt, 7 896 of 173 484 `UV_DATA` rows | 18 270 720 / `e26b6a0b74df1b2e9accbae0336f346824f5590f` | the duplicated-`ANTENNA` case: 50 rows = 10 antennas × 5 correlator jobs, plus a `GATEMODL` extension and a genuine `CORRVERS = DIFX-2.1` header |
| `2012_04_17_raes03v_C_01.excerpt.fits` | [`radik_fits/raes03v/2012_04_17_raes03v_C_01.fits`](http://astrogeo.org/s0/radik_fits/raes03v/2012_04_17_raes03v_C_01.fits) | 115 678 080 / `fa4c172f1b01ac925d990dc604e1f850692b562c` | excerpt, 9 354 of 27 599 `UV_DATA` rows | 39 487 680 / `1b72988fd03740c21958128ef126a619839a6966` | the file that pins the `DiFX-ra` LSB `PHASE-CAL` convention, and a high-SNR LSB visibility witness |
| `2011_06_28_rdv87_alt_01.excerpt.fits` | [`vlba_fits/rdv87/2011_06_28_rdv87_alt_01.fits`](http://astrogeo.org/s0/vlba_fits/rdv87/2011_06_28_rdv87_alt_01.fits) | 9 685 624 320 / `0f20f46859f7ed133e3025f5ac8b7f9f80f576a3` | excerpt, 389 of 293 750 `UV_DATA` rows | 39 916 800 / `5c6ab9cca75c811187ba6320bb4743ebf121a76d` | second, independent `DIFX-2.0.1` LSB witness (16 bands, `NO_POL = 1`, `PHASE-CAL` 12 494 rows) |

The excerpt selections are documented as code in `scripts/MAKE.sh`: raes03v keeps every record
of the three ground–ground baselines EF-MC/EF-YS/MC-YS plus every 10th autocorrelation;
rdv87 keeps the whole FD–PT scan on source 34 (2011-06-29 04:37:43…04:43:11) with the matching
autocorrelations plus a 1-in-2111 sample of everything else; bd152ie keeps the two strongest
source-blocks plus a 1-in-26 sample.

### `vlba-difx/` — NRAO VLBA archive (MOJAVE project BL178)

Both files come from <https://data.nrao.edu/portal/>, which serves them only through an
anonymous **staging request** — there is no direct URL. Give the portal the product locator
below (or search the project code), and it stages the original file and a `SHA1SUMS` at a
request-scoped `https://dl-dsoc.nrao.edu/anonymous/<request>/…` location that expires.

| file | original file name / locator | orig size / SHA1 | done | staged size / SHA1 | used by |
|---|---|---|---|---|---|
| `VLBA_BL178AC_bl178ac_BIN0_SRC0_0_111228T171125.excerpt.idifits` | `VLBA_BL178AC_bl178ac_BIN0_SRC0_0_111228T171125.idifits`, experiment **BL178AC**, `uid://vlba/correlation/fd2b205c-0f70-40a6-847e-1198becf2bf0` | 5 953 806 720 / `5d6515577b94107445719c3a0619830953292ef9` | excerpt, 5 797 of 1 385 432 `UV_DATA` rows | 60 004 800 / `490eac599ad4f7b527a0f77f398a0f5c778dc109` | `FITS-IDI lower-sideband acceptance (BL178AC)` |
| `VLBA_BL178AL_bl178al_BIN0_SRC0_0_120712T141309.excerpt.idifits` | `VLBA_BL178AL_bl178al_BIN0_SRC0_0_120712T141309.idifits`, experiment **BL178AL**, `uid://vlba/correlation/7c866aab-9bc3-40a4-ac54-b78f3dd2aa22` | 5 000 201 280 / `cdc2f0270fbf576380dac033c8aabb398018e3df` | excerpt, 3 801 of 1 162 555 `UV_DATA` rows | 50 005 440 / `e51d5eb5c767a7788f4489a509cf8124acd4dfd2` | `FITS-IDI lower-sideband acceptance, DiFX 2.1 (BL178AL)` |

The two are the same MOJAVE 15 GHz 8×LSB/USB setup five months apart, differing in the
difx2fits release that wrote them (`CORRVERS = DIFX-2.0.1` vs `DIFX-2.1`) — which is exactly
the distinction the `PHASE-CAL` version gate is about. Each excerpt keeps in full the scan its
testitem names: BL178AC the 3C 84 scan KP–LA 2011-12-12 02:09:30…02:12:44, BL178AL the
0923+392 scan FD–LA 2012-06-25 23:30:44…23:36:30.

### `jive/` — EVN, correlated at JIVE

| file | source URL | orig size / SHA1 | done | staged size / SHA1 | used by |
|---|---|---|---|---|---|
| `ep075f_WSRT.IDI1` | [`archive.jive.nl/exp/EP075F_130526/fits/ep075f_WSRT.IDI1`](https://archive.jive.nl/exp/EP075F_130526/fits/ep075f_WSRT.IDI1) | 77 771 520 / `8792ddd266d2bc25b94f9a49ee4cf71220a01d8a` | none | 77 771 520 / `8792ddd266d2bc25b94f9a49ee4cf71220a01d8a` | `FITS-IDI zero-based COMPLEX axis (JIVE)` |
| `n09q2_1_1-shortened.IDI1` | [`casatestdata/raw/fits/n09q2_1_1-shortened.IDI1`](https://open-bitbucket.nrao.edu/projects/CASA/repos/casatestdata/raw/fits/n09q2_1_1-shortened.IDI1) | 1 725 120 / `5af29bac3f7bf102fe4f0144bddb56faa13f1365` | none | 1 725 120 / `5af29bac3f7bf102fe4f0144bddb56faa13f1365` | `FITS-IDI zero-based COMPLEX axis (JIVE)` |

`ep075f` is WSRT/DZB output (`CORRELAT = 'DZB'`), which carries the lower sideband in the sign
of `CH_WIDTH` while writing `SIDEBAND = +1` throughout; `n09q2_1_1-shortened` is SFXC output
(the file is the shortened copy distributed in NRAO's CASA test-data repository, taken from
EVN experiment N09Q2). Both write the `UV_DATA` `COMPLEX` axis 0-based.

### `vsop/` — VSOP/HALCA space VLBI, VLBA hardware correlator, via JAXA DARTS

| file | source URL | orig size / SHA1 | done | staged size / SHA1 | used by |
|---|---|---|---|---|---|
| `v050c.fits.1-8` | [`data.darts.isas.jaxa.jp/…/halca/VSOP_CorrelatedData/v050c/event/v050c.fits.1-8`](https://data.darts.isas.jaxa.jp/pub/halca/VSOP_CorrelatedData/v050c/event/v050c.fits.1-8) | 1 699 200 / `d4ddb1a4277efb859a4ba5c56e9902e044969159` | none | 1 699 200 / `d4ddb1a4277efb859a4ba5c56e9902e044969159` | `FITS-IDI single-polarization aux tables (NO_POL=1)` |

`FXCORVER = 4.20`, observed 1999-04-01, single polarization (LL) with the full instrumental
table set — `PHASE-CAL` (`NO_TONES = 3`, non-monotonic tone frequencies), `SYSTEM_TEMPERATURE`,
`GAIN_CURVE` — all written with `_1` columns only.

### `misc/` — everything else

| file | source URL | orig size / SHA1 | done | staged size / SHA1 | used by |
|---|---|---|---|---|---|
| `K08161.0.FITS` | member of [`ftp.mpifr-bonn.mpg.de/vlbiarchive/DiFX_testdata/k08161/k08161.difx-1.5.0.outputfiles.tar.gz`](https://ftp.mpifr-bonn.mpg.de/vlbiarchive/DiFX_testdata/k08161/k08161.difx-1.5.0.outputfiles.tar.gz) (tarball 1 370 554 B) | 216 000 / `8628431e8fd0a94e006818bee3d29b294957ff15` | none (extracted from the tarball) | 216 000 / `8628431e8fd0a94e006818bee3d29b294957ff15` | `FITS-IDI single-polarization aux tables (NO_POL=1)`; also the "DiFX file with no `CORRVERS` card" branch |
| `emerlin_multiuv.IDI1` | [`casatestdata/raw/fits/emerlin_multiuv.IDI1`](https://open-bitbucket.nrao.edu/projects/CASA/repos/casatestdata/raw/fits/emerlin_multiuv.IDI1) | 2 128 320 / `811e6008d39087a58f9b238b3072b54fcc57b7bd` | none | 2 128 320 / `811e6008d39087a58f9b238b3072b54fcc57b7bd` | `duplicated table names (e-MERLIN)` — the file holds **two** `UV_DATA` HDUs of 63 rows each |
| `05BBA01_VENUS22.LTA_LL.1FITS.excerpt.fits` | [Zenodo 4529203](https://zenodo.org/records/4529203/files/05BBA01_VENUS22.LTA_LL.1FITS.fits?download=1) | 532 054 080 / `4f147ad15b3ed917a56a430748c371258eeb546b` | excerpt, 19 112 of 339 300 groups | 30 000 960 / `cbba34afa74bd8d8318a0252f720fe7f7d5509ea` | `UVFITS FQ sign conventions (real files)` — `CH WIDTH = -125 000` with `SIDEBAND = +1`, the AIPS encoding of a descending axis |
| `05BBA01_VENUS22.LTB_LL.1FITS.excerpt.fits` | [Zenodo 4529203](https://zenodo.org/records/4529203/files/05BBA01_VENUS22.LTB_LL.1FITS.fits?download=1) | 532 054 080 / `96b4e1f0ce90708df66e18b12e9534bb14e2a627` | excerpt, 19 112 of 339 300 groups | 30 000 960 / `c2299f8eaa4b4674b7cb5925ab4428fa1ee80ede` | same testitem: the ascending twin of the same observation, the control |
| `mirsplit.excerpt.UVFITS` | [`casatestdata/raw/uvfits/mirsplit.UVFITS`](https://open-bitbucket.nrao.edu/projects/CASA/repos/casatestdata/raw/uvfits/mirsplit.UVFITS) | 135 463 680 / `49e03a8fc019d4a659fadd65d737fca8e148e3c2` | excerpt, 3 983 of 18 000 groups | 30 000 960 / `11d538fa7f66d588d83cf75c13c96860906508bf` | same testitem: 16 IFs with `CH WIDTH < 0` **and** `SIDEBAND = -1`, so the rule must be OR, not XOR |
| `sma_masses/Per35.SWARM.1.3mm.s1.lsb.1.151006.uvfits` | [Harvard Dataverse datafile 3616840](https://dataverse.harvard.edu/api/access/datafile/3616840), dataset [10.7910/DVN/NGA7DX](https://doi.org/10.7910/DVN/NGA7DX) | 36 253 440 / `872c7202fb5bc85c92198848696f790bab223375` | none | 36 253 440 / `872c7202fb5bc85c92198848696f790bab223375` | same testitem: **negative `TOTAL BANDWIDTH`** (−1.664 GHz), which used to give a negative `nchan` |
| `sma_masses/Per35.SWARM.1.3mm.s1.usb.1.151006.uvfits` | [Harvard Dataverse datafile 3616842](https://dataverse.harvard.edu/api/access/datafile/3616842), same dataset | 36 253 440 / `5eed0adc47d3d5e29d45b8d6d452d9b2d655a740` | none | 36 253 440 / `5eed0adc47d3d5e29d45b8d6d452d9b2d655a740` | the all-positive upper-sideband twin of the file above, its control |
| `sma_masses/SVS13C.sub.SWARM.lsb.s3.170127.excerpt.uvfits` | [Harvard Dataverse datafile 3175052](https://dataverse.harvard.edu/api/access/datafile/3175052), dataset [10.7910/DVN/GQTCQR](https://doi.org/10.7910/DVN/GQTCQR) | 263 531 520 / `abdc3e5b75b21a5979e486deb79fc1f56a02ca6e` | excerpt, 152 of 1 340 groups | 29 923 200 / `a1fc17cfc91a0b075b54f09174088a4a24c9a684` | same testitem: 16 384 channels, `CH WIDTH < 0`, `TOTAL BANDWIDTH < 0`, `SIDEBAND = -1` |

### `pkg-data/` — the package's own fixtures, moved out of `VLBIFiles.jl/test/data/`

Nineteen small files (29 275 930 B together) that VLBIFiles.jl has always tested against: the
UVFITS/FITS-IDI readers, the image and difmap-model readers, the alist reader. They are
unchanged — copied byte for byte out of the package repository, no excerpting, no rewriting —
and the "source URL" column says what is *known* about each. Six were fetched on demand by the
test suite itself, so their URL is recorded in the code that fetched them; a seventh, the EHT
M87 image, is a published CDS catalogue file and was downloaded from there; the rest predate
any such record and say so.

| file | bytes / SHA1 | source | what it is / used by |
|---|---|---|---|
| `vis.fits` | 2 131 200 / `9869f076976bdc1881f3b7174311b0994d2d2b19` | legacy VLBIFiles test fixture, original source not re-verified | VLBA 15 GHz, `BL149CZ` 2010-12-24, J1033+6051, AIPS UVFITS, 8 IFs × 1 channel × 4 Stokes, 5 082 groups — the main UVFITS fixture (`uvf simple`, `closures calculations`, the three `grouphdu …` items, `uvtable_wide`, `prefetch!`, …) |
| `vis_multichan.vis` | 826 560 / `70c38e69b4ff67f098aeffdf4cc0c26922097c21` | legacy VLBIFiles test fixture, original source not re-verified | VLBA 4.6 GHz, `BH019` 1996-06-05, J0414+053A, 8 IFs × 16 channels, 515 groups — `uvf multichannel`, `frequency correctness CRPIX=1 multichan` |
| `BL146_1.fits` | 2 448 000 / `f4ab6eea1ece41483b3dc5ec247d69c342be633c` | [`fits.gsfc.nasa.gov/registry/fitsidi/BL146_1.fits`](https://fits.gsfc.nasa.gov/registry/fitsidi/BL146_1.fits) (NASA GSFC FITS Support Office, FITS-IDI registry sample) | VLBA hardware correlator (`FXCORVER = 4.22`) 2007-08-23, 4 bands × 8 channels × 4 Stokes, 1 000 rows, full aux-table set — the FITS-IDI fixture of `FITS IDI small`, `FITS-IDI auxiliary tables`, `mmap column read`, `RDATE fallback…`, and the two-polarization control of `FITS-IDI single-polarization aux tables (NO_POL=1)` |
| `DDTSUVDATA.fits` | 596 160 / `12e46c6deefa634b96065ed461e93d9d4eb1392c` | [`fits.gsfc.nasa.gov/samples/DDTSUVDATA.fits`](https://fits.gsfc.nasa.gov/samples/DDTSUVDATA.fits) | VLA 3C161, 1984-01-29, written by AIPS; `NAXIS = 6`, i.e. **no IF axis**, 28 antennas, 7 956 groups — `uvf NAXIS=6 no IF axis (DDTSUVDATA)` |
| `0332-391.uvfits` | 14 670 720 / `7e4e2a73864816ee1a21adfa0ba850e04df49da0` | [`purify/data/atca/0332-391.uvfits`](https://github.com/astro-informatics/purify/raw/development/data/atca/0332-391.uvfits) | ATCA 1.43 GHz 2001-05-20, Miriad `atlod`/`fits`; `NAXIS = 6`, descending `CDELT4` with no FQ table, Stokes I/Q/U/V, 13 channels — `uvf NAXIS=6 no IF axis (ATCA)` |
| `mwa_1061316296.uvfits` | 1 529 280 / `947eb742ae446f7414e43b9bc30d9365965639aa` | [`rasg-datasets v0.0.4 …/MWA/1061316296.uvfits`](https://github.com/RadioAstronomySoftwareGroup/rasg-datasets/raw/v0.0.4/visibility_data/MWA/1061316296.uvfits) (renamed) | MWA 167 MHz 2013-08-23, written by pyuvdata; linear feeds, every visibility flagged — `uvf linear polarization (MWA)` |
| `paper_zen.uvfits` | 66 240 / `136e6beaf0c02e11b7bf3b4ad4a8eb4770e70158` | [`rasg-datasets v0.0.4 …/PAPER/zen.2456865.60537.xy.uvcRREAAM.uvfits`](https://github.com/RadioAstronomySoftwareGroup/rasg-datasets/raw/v0.0.4/visibility_data/PAPER/zen.2456865.60537.xy.uvcRREAAM.uvfits) (renamed) | PAPER 100 MHz 2014-07-27, Miriad; `NAXIS = 6`, single `XY` product, 11 channels — `uvf NAXIS=6 linear pol (PAPER)`, `faithful warnings` |
| `J1256-0547_X_2020_10_18_pet_vis.fits` | 236 160 / `daa9bd688580ab5016caa2708ae57d24b8ca9fed` | [`astrogeo.org/images/J1256-0547/J1256-0547_X_2020_10_18_pet_vis.fits`](https://astrogeo.org/images/J1256-0547/J1256-0547_X_2020_10_18_pet_vis.fits) | VLBA X-band 2020-10-18 (`uh007b`), merged by `UVA_MERGE 2.1`: **three `AIPS AN` tables**, i.e. three subarrays in one file — `uvf multi-array baselines` |
| `SR1_3C279_2017_101_hi_hops_netcal_StokesI.uvfits` | 1 238 400 / `98c4fdcab7243b66ca02b8165ceebb0f6f8dd5d5` | EHT 2017 April public data release, HOPS/`netcal` product; legacy VLBIFiles test fixture, original download not re-verified | EHT 229 GHz 2017-04-11, 3C279, Stokes I, 14 455 groups — `uvf EHT 2`, `antenna catalog` (real ECEF cross-check) |
| `hops_3600_OJ287_LO+HI.medcal_dcal_full.uvfits` | 794 880 / `02bb180639a3dad2233be7d867a44ed9f2d4f57c` | EHT 2017 April HOPS product; legacy VLBIFiles test fixture, original download not re-verified | EHT 227 GHz 2017-04-09, OJ 287, LO+HI bands (2 IFs), 6 220 groups — `uvf EHT 1` |
| `datafile_01-01_230GHz.uvfits` | 178 560 / `c1ae1e63c2c297a9442a9eb57d28fee0c8e9694c` | EHT 2013 campaign product; legacy VLBIFiles test fixture, original download not re-verified | EHT 230 GHz 2013-01-01, M87, 1 772 groups — `uvf EHT 3` |
| `alist_v6.fsumm` | 127 814 / `77226072ae5dba628e2e855f68c130f2356c69f8` | HOPS `alist` version-6 fringe summary (header: processed 2016-07-26); legacy VLBIFiles test fixture, original source not re-verified | 318 fringe records, 228 GHz — the only fixture of the `Alist` reader (`alist`, `generic loading`) |
| `map.fits` | 1 071 360 / `9cba0872d2d8ea73bcc56dfdc84dbbfef7c5ad87` | legacy VLBIFiles test fixture, original source not re-verified | 512² CLEAN image of J0000+0248 (`bp192d3`, 2016-01-03) written by `PIMA 2.26`, with an `AIPS CC` table of 361 components — the image fixture (`img read data`, `img read clean`, `img clean/residual/combined`, `difmap model`) |
| `map_stacked.fits` | 2 234 880 / `132092bcf885761e3e88388ef1cb437407850e4b` | legacy VLBIFiles test fixture, original source not re-verified | 512² stacked CLEAN image, J0738+17 (`BR034`, 1996-01-19), difmap → AIPS, circular beam, **no CC table** — `img stacked` |
| `sampling_mean.fits` | 529 920 / `2689580af4d20ca33b98ac40afb2616423c6e920` | legacy VLBIFiles test fixture, original source not re-verified | 256² mean uv-sampling map, `TELESCOP = 'VLBI'`, `OBJECT = 'Unknown'`, `JY/PIXEL`, no `BMAJ` — the nonstandard-header image case (`img nonstandard header names`) |
| `M87_EHT_2018_3644_b3.fits` | 570 240 / `f46d3db9879c32da29afd3cd1f2c472f392dc8c9` | [`cdsarc J/A+A/681/A79 fits/M87_EHT_2018_3644_b3.fits`](https://cdsarc.cds.unistra.fr/ftp/J/A+A/681/A79/fits/M87_EHT_2018_3644_b3.fits) (the image attached to CDS catalogue [J/A+A/681/A79](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/681/A79), EHT Collaboration 2024, A&A 681, A79) | 128² representative EHT image of M 87* from the 2018 April 21 track (experiment `3644`), band 3, 227.1 GHz, 1.17 µas pixels, **`BUNIT = '10^9 K'`** and no `BMAJ`, with an `AIPS CC` table of 15 223 components — `img strange units` |
| `difmap_model.mod` | 532 / `7520d0c60635a889c766ba7b8e1cd4427c70715d` | legacy VLBIFiles test fixture, original source not re-verified | difmap model file, 4 components with `v`-marked free parameters — `difmap model`, `generic loading` |
| `difmap_model_clean.mod` | 24 964 / `80163e3eea24b0dc4489465bf81178d0b64566e4` | legacy VLBIFiles test fixture, original source not re-verified | difmap model file, 631 delta components — `difmap model` |
| `difmap_model_empty.mod` | 60 / `463d1702e22794fc0b1b68b86a6dd8e3cd6b5218` | legacy VLBIFiles test fixture, original source not re-verified | difmap model file with a phase-centre line and no components — `difmap model`, `generic loading` |

Two further fixtures are referenced by the test suite under `pkg-data/` but are **not**
published here. `J0840-5732_X_2010_03_11_dew_map.fits` is public — it is
<https://astrogeo.org/images/J0840-5732/J0840-5732_X_2010_03_11_dew_map.fits>, SHA1
`1574f886f4339c4670086a980388cb7f685f9fa5` — but its first of two `AIPS CC` tables holds
10 000 000 components, so the file is 124 217 280 B and exceeds GitHub's 100 MiB per-file
limit; it can only be fetched from astrogeo directly. `GOALS_GroupS2_Ref59_Cals_Avg.idi`, the
Obit-written MeerKAT FITS-IDI, has no located public source at all. Their testitems skip
themselves unless the file is dropped into `pkg-data/` by hand, exactly as they did while the
package still had a `test/data/`.

`scripts/` (4 files) holds `trim_idifits.py`, `trim_uvfits_groups.py`, `verify_excerpt.py` and
`MAKE.sh`; they are documentation and reproduction tools, not data.

## Provenance and acknowledgments

All data here are public. Please respect the source archives' own acknowledgment requests
when publishing anything derived from them — this repository is a test corpus, not a
re-publication of anyone's science.

* **NRAO / VLBA** — `vlba-difx/` (MOJAVE BL178AC and BL178AL). VLBA correlator products
  become public under the [NRAO data policy](https://science.nrao.edu/observing/proposal-types/data-management)
  after the proprietary period; both are served as `data_rights = PUBLIC` by the NRAO
  archive. They are not plain URLs: use <https://data.nrao.edu/portal/> and the product
  locators and original file names given above (anonymous staging request → `dl-dsoc.nrao.edu`
  download links plus a `SHA1SUMS` at the request root). The National Radio Astronomy
  Observatory is a facility of the National Science Foundation operated under cooperative
  agreement by Associated Universities, Inc.
* **astrogeo.org** — `astrogeo/` (leotest/r1482, rk01ak, bw089, bd152ie, raes03v, rdv87).
  Leonid Petrov's open archive of raw correlator output, plain HTTP, no login. Please credit
  the archive (<http://astrogeo.org/>) as the source of these observations.
* **EVN / JIVE** — `jive/`. The EVN
  [asks](https://www.evlbi.org/data-access) that publications using EVN data, "including that
  obtained from the EVN archive", carry the standard acknowledgment: *"The European VLBI
  Network is a joint facility of independent European, African, Asian, and North American
  radio astronomy institutes. Scientific results from data presented in this publication are
  derived from the following EVN project code(s): XXXXX"* — here **EP075** (`ep075f_WSRT.IDI1`)
  and **N09Q2** (`n09q2_1_1-shortened.IDI1`). EVN archive data enter the public domain after
  the proprietary period (normally one year after distribution to the PI).
* **Zenodo record [4529203](https://doi.org/10.5281/zenodo.4529203)** — the GMRT pair.
  GMRT 2004 Venus campaign data, published under **CC-BY**; cite the record.
* **Harvard Dataverse** — `misc/sma_masses/`. SMA observations from the MASSES survey
  (Ian Stephens, Center for Astrophysics | Harvard & Smithsonian); datasets
  [10.7910/DVN/NGA7DX](https://doi.org/10.7910/DVN/NGA7DX) ("Per-emb-35 (NGC 1333 IRAS1), uv
  data") and [10.7910/DVN/GQTCQR](https://doi.org/10.7910/DVN/GQTCQR) ("SVS 13C, uv data"),
  both released under **CC0 1.0**. The Submillimeter Array is a joint project between the
  Smithsonian Astrophysical Observatory and the Academia Sinica Institute of Astronomy and
  Astrophysics.
* **NRAO casatestdata** — `misc/emerlin_multiuv.IDI1` (e-MERLIN), `misc/mirsplit.excerpt.UVFITS`
  (CARMA, written by casacore) and `jive/n09q2_1_1-shortened.IDI1` (EVN/SFXC), from the public
  CASA test-data repository <https://open-bitbucket.nrao.edu/projects/CASA/repos/casatestdata>.
* **DARTS / ISAS, JAXA** — `vsop/v050c.fits.1-8`, from the VSOP/HALCA correlated-data archive
  <https://data.darts.isas.jaxa.jp/pub/halca/VSOP_CorrelatedData/>. VSOP was led by ISAS with
  the VLBA correlation done at NRAO.
* **MPIfR** — `misc/K08161.0.FITS`, a member of the DiFX 1.5.0 test-data tarball on the MPIfR
  public VLBI archive <https://ftp.mpifr-bonn.mpg.de/vlbiarchive/DiFX_testdata/>.
* **`pkg-data/`**, the fixtures moved out of the package repository. Where the source is known
  it is: **NASA GSFC FITS Support Office** sample files (`BL146_1.fits` from the FITS-IDI
  registry, `DDTSUVDATA.fits` from the samples directory, <https://fits.gsfc.nasa.gov/>);
  **astrogeo.org** (`J1256-0547_X_2020_10_18_pet_vis.fits`, credit the archive as above);
  the **purify** project's ATCA example (`0332-391.uvfits`,
  <https://github.com/astro-informatics/purify>, observed by the ATCA, an Australia Telescope
  National Facility instrument); and the **Radio Astronomy Software Group**'s `rasg-datasets`
  (`mwa_1061316296.uvfits`, `paper_zen.uvfits`,
  <https://github.com/RadioAstronomySoftwareGroup/rasg-datasets>, MWA and PAPER data
  redistributed there for pyuvdata's test suite); and the **CDS** (Strasbourg astronomical Data
  Center, <https://cds.unistra.fr/>), which publishes `M87_EHT_2018_3644_b3.fits` as the image
  attached to catalogue J/A+A/681/A79 of Event Horizon Telescope Collaboration 2024,
  A&A 681, A79. The three other EHT files
  (`SR1_3C279_…`, `hops_3600_OJ287_…`, `datafile_01-01_230GHz.uvfits`) are products of **Event
  Horizon Telescope** observations — they came into the package before any download record was
  kept, so the exact release they were taken from is stated as unverified rather than guessed;
  publications using EHT data should follow the collaboration's own acknowledgment policy
  (<https://eventhorizontelescope.org/>). The remaining files (`vis.fits`, `vis_multichan.vis`,
  `map*.fits`, `sampling_mean.fits`, `difmap_model*.mod`, `alist_v6.fsumm`) are VLBA/VLBI
  products of the same kind with no recorded provenance; the VLBA is an NRAO facility.

## Reproducing and checking

```sh
sha1sum -c SHA1SUMS                              # every file, as published here
python3 scripts/verify_excerpt.py FULL EXCERPT   # re-prove one excerpt against its source
SRC=/some/scratch/dir sh scripts/MAKE.sh         # re-download the sources and rebuild all excerpts
```

`MAKE.sh` needs python ≥ 3.11 with astropy and numpy, plus curl and ~17 GB of scratch space
for the source files it downloads; the two NRAO files must be staged by hand (it skips them
when they are not in `$SRC`). Rebuilt excerpts are bit-identical to the ones committed here —
that is what `SHA1SUMS` is for.

`MANIFEST.md` carries the per-file detail: what each file's header actually contains and which
reader behaviour it pins down.
