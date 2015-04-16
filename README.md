# Proceed: A software to generate automatically conference proceedings


# Introduction

to be documented


# Importing/Exporting data of a conference

This step can only be performed by using the Command-Line User Interface (CLI).
There a 2 scripts to perform import/export: import.py and import-to-tex.py.
To get help and usage, use the --help option.


Both scripts take as input the conference output file:

- sciencesconf.org: Export submissions in XML;
- easychair.org: Get the "snapshot" XLSX file then save the pages "Submissions"
and "Authors" as CSV files with ";" as separator. Then convert both files to UTF8
encoding and replace '\n' by ' ~ '. Remarks: only OpenOffice/LibreOffice can perform
the required convertions (impossible with Excel).

The script *import.py* takes as input one of sciencesconf or easychair file(s)
and save some of the data in the form of:

- a single html file;
- a single latex file;
- a single index file.

The script *import-to-tex.py* save title, authors, laboratories, keywords,
and abstracts in a set of latex files, and create 3 CSV files:

- DOCUMENTS.csv
- SESSIONS.csv
- AUTHORS.csv

For now, all data are created in the current directory. You have to create a
destination directory and to move them in.


Examples of use:

1. Export Authors/Title of reviewed papers in HTML:

    > python import.py -i sample-data/trasp.xml -o trasp.html -s 4


2. Export accepted abstracts in csv from sciencesconf:

    > python import.py -i sample-data/trasp.xml -o csv


3. Export for Proceed:

    > python import-to-tex.py -i sample-data/submissions.csv -a sample-data/authors.csv -o confname -s 1 -r easychair -S taln
    > python import-to-tex.py -i sample-data/submissions.xml -o confname -s 1 -r sciencesconf -S simple





# Managing data

A Graphical User Interface is available to perform this step. It consists in managing
the conference data: Authors, Documents and Sessions. Such data will be used to generate
the conference program, and the proceedings.

[SCREENSHOT]


The GUI is made of 3 main areas:

- a toolbar;
- a notebook (left);
- a data panel.


## Toolbar

The toolbar includes icons to perform actions (from left to right):

- exit the program;
- load data: get data from a directory (authors, documents and sessions as CSV files, and PDF of the submissions);
- save data: save CSV files of the loaded data;
- check data: diagnosis to know if loaded data can be exported as PDF;
- export data: export loaded data as a PDF document;
- add: create a new entry in the data;
- edit: modify the selected entry;
- delete: remove definitively the selected entry;
- about: open an aboutbox.


## Notebook

The notebook contains 3 pages with:

- the list of documents;
- the list of sessions;
- the list of authors.

Clicking on one entry in the list allows to select it and print related information
in the data panel. Then, three actions can be performed on such data:

1. Add a new one.
2. Modify the selected one.
3. Delete the selected one.


## Data panel

This is an area to show the content of an entry. Nothing else!



# Exporting proceedings

to be documented.
