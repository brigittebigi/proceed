## Getting and installing


### Website

The source code with recent stable releases and the development version is 
available at:

<https://github.com/brigittebigi/proceed>

From this website, anyone can download the development version, 
contribute, send comments and/or declare an issue.


### Dependencies

Other programs are required for PROCEED to operate. Of course,
they must be installed before using PROCEED, and *only once*.
This operation doesn't take too long, duration depending on the operating system.
The following software are required:

1. Python, version 2.7.x
2. wxPython >= 3.0
3. pdftk
4. pdflatex

Administrator rights are required to perform these installations. 


### Download and install SPPAS

PROCEED is ready to run, so it does not need elaborate installation, except for
its dependencies (other software required for PROCEED to work properly).
All you need to do is to copy the PROCEED package from github to somewhere
on your computer. Preferably, choose a location without spaces nor accentuated 
characters in the name of the path.  

![Download GitHUB](./etc/screenshots/github.png)

The PROCEED package is compressed and zipped, so you will need to
*decompress and unpack* it once you've got it.

### The SPPAS package

The package of PROCEED is a folder with content as files and sub-folders. 

![PROCEED Package content](./etc/screenshots/explorer-PROCEED-folder.png)

The PROCEED package contains:

- the `README.txt` file, which aims to be read by users!
- the files `proceed.bat` and `proceed.command` to execute the Graphical User Interface of PROCEED
- the `samples` are sets of submissions freely distributed to test PROCEED
- the `proceed` directory contains the program itself
- the `documentation`, which contains:

    - a copy of the licenses.
    - the `documentation` in PDF.
    - a file INSTALL with the list of requirements to use the software.
    - the `etc` directory is for internal use. Do not modify or remove it.


### Update

Updating PROCEED is very (very very!) easy and fast:

1. Optionally, put the old package into the Trash,
2. Download and unpack the new version.
