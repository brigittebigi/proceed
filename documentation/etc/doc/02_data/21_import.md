## Importing/Exporting data of a submission web site

Proceed can take as input the files of some conference submission web
sites:

- sciencesconf.org: Export submissions in XML or CSV;
- easychair.org: Get the "snapshot" XLSX file then save the pages "Submissions"
and "Authors" as CSV files with ";" as separator. Then convert both files to UTF8
encoding and replace carriage returns of the abstracts by ' ~ '. 
Remarks: only OpenOffice/LibreOffice can perform
the required convertions (impossible with Excel).

Proceed will import some of the data and create the following files:

- CONFERENCE.csv
- DOCUMENTS.csv
- SESSIONS.csv
- AUTHORS.csv

