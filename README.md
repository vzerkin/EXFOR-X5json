## EXFOR-X5json
by V.Zerkin, 2021-2026

### Introduction
X5-JSON presents information from several data [`sources`](VERSION.TXT):

1. Original EXFOR:
   * explicitly named metadata with information relevant from EXFOR-CINDA dictionaries
   * structured numeric data in original form
2. Computational data:
   * numeric data from EXFOR translated to comparable form (basic units, laboratory system, etc.)
   * generalized data ~C5: y, &Delta;y, &Delta;y.*stat*, &Delta;y.*sys*, x1, &Delta;x1, x2, &Delta;x2, etc.
   * MF, MT for data compatible with ENDF evaluated data
3. Data for renormalization:
   * monitor cross sections from [EXFOR file and Archive] and [modern Standards]
   * decay data for renormalization from [EXFOR file] and [recent ENSDF]


### Content of this repository
1. Entire EXFOR library translated to X5 format: one json file per Entry
2. Data indexes
   * Index of Entries with Reference:author/title/DOI in [csv](x5json/X5-Entries.csv) and [json](x5json/X5-Entries.json) form
   * Index of Datasets with Reaction-codes and ENDF:MF/MT in [csv](x5json/X5-Datasets.csv) and [json](x5json/X5-Datasets.json) form
   * Python-codes to scan X5 files and produce [`Entry`](x5json/x5index2entries.py) and [`Datasets`](x5json/x5index2entries.py) index files
3. Examples of Python-codes:
   * Search datasets by reaction, extract computational data: [`x5data1.py`](x5json/x5data1.py)
   * Find, extract, filter and plot data of various quantities: 
     * SIG(Ei): [`x5data2.py`](x5json/x5data2.py) &rarr; [`png`](x5json/x5data2.png "plot") [`html`](x5json/x5data2.html.zip "interactive plot")
       cross sections
     * DA(Ao): [`x5data4a.py`](x5json/x5data4a.py) &rarr; [`png`](x5json/x5data4a.png) [`html`](x5json/x5data4a.html.zip "interactive plot")
       angular distributions
     * DA(Ei): [`x5data4e.py`](x5json/x5data4e.py) &rarr; [`png`](x5json/x5data4e.png) [`html`](x5json/x5data4e.html.zip "interactive plot")
       angular distributions
     * DAP(Ei): [`x5data4par.py`](x5json/x5data4par.py) &rarr; [`png`](x5json/x5data4par.png) [`html`](x5json/x5data4par.html.zip "interactive plot")
       partial angular distributions
     * DE(Eo): [`x5data5de.py`](x5json/x5data5de.py) &rarr; [`png`](x5json/x5data5de.png) [`html`](x5json/x5data5de.html.zip "interactive plot")
       emission spectra
     * DAE(Eo): [`x5data6dae.py`](x5json/x5data6dae.py) &rarr; [`png`](x5json/x5data6dae.png) [`html`](x5json/x5data6dae.html.zip "interactive plot")
       double differential cross sections
     * NU(Ei): [`x5data7nubar.py`](x5json/x5data7nubar.py) &rarr; [`png`](x5json/x5data7nubar.png) [`html`](x5json/x5data7nubar.html.zip "interactive plot")
       NUBAR - average number of neutrons per fission
     * FY(A): [`x5data8fy.py`](x5json/x5data8fy.py) &rarr; [`png`](x5json/x5data8fy.png) [`html`](x5json/x5data8fy.html.zip "interactive plot")
       total chain yield of fission products
   * Retrieve and renormalize cross section data: [`x5data3.py`](x5json/x5data3.py) &rarr;
     [`png`](x5json/x5data3.png) [`html`](x5json/x5data3.html.zip "interactive plot")
   * Export EXFOR data from X5 to pandas.DataFrame: [`x5data2pandas.py`](x5json/x5data2pandas.py) &rarr; [`txt`](x5json/x5data2pandas.tto)
   * Common modules:
     * search datasets by reaction code: [`x5subr.py`](x5json/x5subr.py)
     * automatically renormalize computational data: [`x5auto.py`](x5json/x5auto.py)

### Links
* X5-JSON: [about](https://nds.iaea.org/nrdc/nrdc_2023/present/zerkin1.pdf#page=40),
  [design](https://nds.iaea.org/nrdc/wksp_2024/present/zerkin2.pdf#page=6),
  [structure](https://nds.iaea.org/nrdc/wksp_2024/present/zerkin2.pdf#page=8)
* X5-JSON from the IAEA-NDS: [download](https://nds.iaea.org/cdroms/#x5json)
* EXFOR data renormalization/correction:
  [automatic](https://nds.iaea.org/nrdc/wksp_2022/present/zerkin5.pdf#page=3),
  [experts](https://nds.iaea.org/nrdc/wksp_2022/present/zerkin5.pdf#page=5),
  [syntax](https://nds.iaea.org/exfor/x4guide/x4corrections/x4corrections.pdf),
  [examples](https://github.com/vzerkin/x4corrections),
  [video](https://www.youtube.com/watch?v=n9P1Z134WYM)
* JSON Tree Editor: [about](https://vzerkin.github.io/), [start](https://vzerkin.github.io/edit-json-tree/#1)
