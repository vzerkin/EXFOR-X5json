                      Nuclear Data Section (NDS)
             Department of Nuclear Sciences and Applications
                International Atomic Energy Agency (IAEA)
                Vienna International Centre, P.O. Box 100,
                        A-1400 Vienna, Austria
                Tel:(+43 1) 2600-21714; Fax:(+43 1) 26007
  
       "X5-json: comprehensive presentation of EXFOR in JSON format"
              by Viktor Zerkin, IAEA-NRDC, version 2026-07-01
_______________________________________________________________________________

CONTENT

    EXFOR data and relevant information presented as set of JSON files
 1) X5.json files (one file per Entry) include meta-data, dictionary-information,
    original and computational data, data for renormalization by monitor cross 
    sections and decay data.
 2) EXFOR-Entries.csv  - list of Entries (CSV: Comma Separated Values)
 3) EXFOR-Datasets.csv - list of Datasets
 4) Examples of usage  - programs on Python3
_______________________________________________________________________________

LICENSES

 1) See LICENSE.TXT
_______________________________________________________________________________

DOWNLOAD

 1) Download file "EXFOR-x5json-20260701.zip" from Internet:
    https://www-nds.iaea.org/cdroms/#x5json
_______________________________________________________________________________

INSTALL

 1) Uncompress file "EXFOR-x5json-20260701.zip" to HD disk
    (required free space on HD disk: ~3.5Gb)

    Windows: two options a) or b)
      a) right click on the file "EXFOR-x5json-20260701.zip" and follow
          --> "7-zip" --> "Extract files"
      b) Open command prompt window: <Windows/R> --> type "cmd<Enter>"
         C:\TMP1> "C:\Program Files\7-Zip\7z.exe" x EXFOR-x5json-20260701.zip

    Linux/MacOS:
      $ unzip EXFOR-x5json-20260701.zip
_______________________________________________________________________________

USAGE

 Prepared to be used by programs to build own database or procedures.
_______________________________________________________________________________

EXAMPLES

Required: Python3, Plotly

Programs:
 1) x5index2entries.py  scan dir recursively, load *.x5.json, produce Entry-index in JSON and CSV
 2) x5index2datasets.py scan dir recursively, load *.x5.json, produce Datasets-index in JSON and CSV
 3) x5data1.py          find datasets by reaction, extract data in computational form
 4) x5data2.py          find datasets by reaction, extract data, plot by Plotly -> png,html
 5) x5data3.py          find datasets, automatically renormalize cross sections, plot by Plotly -> png,html
 6) x5data4a.py         DA(Ang)   angular distributions: find, filter data by incident energy, plot -> png,html
 7) x5data4e.py         DA(Ein)   angular distributions: find, filter data by angle, plot -> png,html
 8) x5data4par.py       DAP(Ein)  partial angular distributions: find, filter data by angle, plot -> png,html
 9) x5data5de.py        DE(Eout)  emission spectra: find, filter data by incident energy, plot -> png,html
10) x5data6dae.py       DAE(Eout) double differential cross sections: find, filter data by incident energy, plot -> png,html
11) x5data7nubar.py     NUBAR(Ei) average number of neutrons per fission, plot -> png,html
12) x5data2pandas.py    extract X5json.x4.data --> pandas.DataFrame

Run:
 $ python3 -B x5index2entries.py
 $ python3 -B x5index2datasets.py
 $ python3 -B x5data1.py
 $ python3 -B x5data2.py
 $ python3 -B x5data3.py
 $ python3 -B x5data4a.py
 $ python3 -B x5data4e.py [ex1]
 $ python3 -B x5data4par.py
 $ python3 -B x5data5de.py
 $ python3 -B x5data6dae.py
 $ python3 -B x5data7nubar.py
 $ python3 -B x5data2pandas.py 23114 >x5data2pandas.tto
_______________________________________________________________________________

Please report setup/runtime errors to V.Zerkin@gmail.com
_______________________________________________________________________________

         ALL PRODUCTS ON THIS PACKAGE ARE PROVIDED IN GOOD FAITH AND 
                    WITHOUT A WARRANTY OF ANY KIND.
