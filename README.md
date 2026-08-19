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

The files are too large, and too numerous, to live inside the package repository, so the
gated testitems in `VLBIFiles.jl/test/runtests.jl` look for a clone of this repository
through `VLBIFILES_TEST_*` environment variables and skip themselves when it is absent.

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
