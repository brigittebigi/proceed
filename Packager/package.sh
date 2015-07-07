#!/bin/bash

# ---------------------------------------------------------------------------
# File:    package.sh
# Author:  Brigitte Bigi
# Date:    May, 2015
# Brief:   Proceed packaging script.
# ---------------------------------------------------------------------------
#
# This script can perform 4 actions:
#
#  1. Diagnosis
#
#    - Execute all Unittests of the API
#
#  2. Manual and documentation
#
#    a/ Use epydoc to generate the API reference manual.
#       It results a "manual" folder in the web directory.
#    b/ Use pandoc to generate the User documentation (html and PDF),
#       from markdown files.
#
#  3. Package
#
#    Create a zip file with the public part of Proceed.
#
#  4. Clean
#
# ---------------------------------------------------------------------------


# ===========================================================================
# Fix global variables
# ===========================================================================

# Program to package
PROGRAM_DIR=".."
PROGRAM_NAME=$(grep -i program: $PROGRAM_DIR/README.txt | awk '{print $2}')
PROGRAM_AUTHOR=$(grep -i author: $PROGRAM_DIR/README.txt | awk -F":" '{print $2}')
PROGRAM_VERSION=$(grep -i version: $PROGRAM_DIR/README.txt | awk '{print $2}')
PROGRAM_COPYRIGHT=$(grep -i copyright: $PROGRAM_DIR/README.txt | awk -F":" '{print $2}')

# Files and directories to be used
BIN_DIR="unit"
DOC_DIR="doc"
ETC_DIR="etc"
WEB_DIR="web"
TEMP="/tmp/proceed_package.txt"

# Actions to perform in this script
DO_DIAGNOSIS="False"
DO_MANUAL="False"
DO_PACKAGE="False"
DO_CLEAN="False"

LOG_DIAGNOSIS="diagnosis.log"
LOG_MANUAL="manual.log"
LOG_PACKAGE="package.log"

# User-Interface
MSG_HEADER="${PROGRAM_NAME} Packager, a program written by ${PROGRAM_AUTHOR}."
TODAY=$(date "+%Y-%m-%d")

BLACK='\e[0;30m'
WHITE='\e[1;37m'
LIGHT_GRAY='\e[0;37m'
DARK_GRAY='\e[1;30m'
BLUE='\e[0;34m'
DARK_BLUE='\e[1;34m'
GREEN='\e[0;32m'
LIGHT_GREEN='\e[1;32m'
CYAN='\e[0;36m'
LIGHT_CYAN='\e[1;36m'
RED='\e[0;31m'
LIGHT_RED='\e[1;31m'
PURPLE='\e[0;35m'
LIGHT_PURPLE='\e[1;35m'
BROWN='\e[0;33m'
YELLOW='\e[1;33m'
NC='\e[0m' # No Color


# ===========================================================================
# Functions generic
# ===========================================================================


# Print a title message on stdout
# Parameters:
#  $1: message to print
function fct_echo_title {
    echo -e "${LIGHT_GREEN}-----------------------------------------------------------------------"
    echo -e "${BROWN}$1"
    echo -e "${LIGHT_GREEN}-----------------------------------------------------------------------${NC}"
}


# Print the header message on stdout
function fct_echo_header {
    echo
    echo -e "${LIGHT_GREEN}-----------------------------------------------------------------------"
    echo -e "${LIGHT_RED}$MSG_HEADER"
    echo -e "${LIGHT_GREEN}-----------------------------------------------------------------------${NC}"
    echo
}


# Print an error message, then exit
# Parameters:
#   $1: error message
function fct_exit_error {
    fct_echo_header
    echo -e "${RED}Error: $1${NC}"
    echo
    exit 1
}


# Is a program currently running? Stop this script if yes.
# Parameter:
#  $1: program name
function fct_test_running {
    isrun=`ps aux | grep -c "$1"`
    if [ $isrun -gt 1 ]; then
        fct_exit_error "${PROGRAM_NAME} must be stopped before using this script."
    fi
}


# ===========================================================================
# Functions to clean
# ===========================================================================


# Clean the current directory: remove temporary files
function fct_clean_temp {
    if [ -e $LOG_DIAGNOSIS ]; then rm $LOG_DIAGNOSIS; fi
    if [ -e $LOG_MANUAL ]; then rm $LOG_MANUAL; fi
    if [ -e $LOG_PACKAGE ]; then rm $LOG_PACKAGE; fi
    if [ -e $TEMP ];  then rm $TEMP;  fi

    rm $BIN_DIR/*/*.pyc &> /dev/null
    rm $BIN_DIR/*/*.dump &> /dev/null

}


# Clean the package
function fct_clean_proceed {
    rm  -r $PROGRAM_DIR/samples/*.log               &> /dev/null
    rm $PROGRAM_DIR/proceed/*/*.pyc                   &> /dev/null
    rm $PROGRAM_DIR/proceed/*/*/*.pyc                 &> /dev/null
    rm $PROGRAM_DIR/proceed/*/*/*/*.pyc               &> /dev/null
    rm $PROGRAM_DIR/proceed/*/*/*/*/*.pyc             &> /dev/null
    rm $PROGRAM_DIR/proceed/etc/settings.dump
}


# ===========================================================================
# Functions to extract the command-line
# ===========================================================================


# Print the Usage message on stdout
function fct_echo_usage {
    fct_echo_header
    echo -e "${CYAN}Usage: $0 [-p|-d|-m|-a]${NC}"
    echo -e "where:${LIGHT_CYAN}"
    echo -e "    -p: package"
    echo -e "    -d: diagnosis"
    echo -e "    -m: manual and documentation"
    echo -e "    -c: clean (remove all un-necessary files)"
    echo -e "    -a: all (package+diagnosis+manual)${NC}"
    echo
}

# Test if this scripts has the expected number of arguments
# Parameters:
#   $1: nb args
function fct_test_nb_args {
    local maxargs=1
    local minargs=1
    # The command is given without args: print usage
    if [ "$1" -eq 0 ]
    then
        echo -e "${DARK_BLUE}Help.${NC}"
        fct_echo_usage
        exit 0
    fi
    # Too many args: print error and usage
    if [ "$1" -gt $maxargs ]
    then
        echo -e "${DARK_BLUE}Too many arguments.${NC}"
        fct_echo_usage
        exit 1
    fi
    # Too few args: print error and usage
    if [ "$1" -lt $minargs ]
    then
        echo -e "${DARK_BLUE}Too few arguments.${NC}"
        fct_echo_usage
        exit 1
    fi
}


# Fix options from args
# Parameters:
#   $1: all the arguments
function fct_get_args {
    if [ "$1" == "-a" ];
    then
        DO_PACKAGE="True";
        DO_DISGNOSIS="True";
        DO_MANUAL="True";
        DO_CLEAN="True";
    elif [ "$1" == "-p" ];
    then
        DO_PACKAGE="True";
        DO_DISGNOSIS="False";
        DO_MANUAL="False";
        DO_CLEAN="False";
    elif [ "$1" == "-d" ];
    then
        DO_PACKAGE="False";
        DO_DISGNOSIS="True";
        DO_MANUAL="False";
        DO_CLEAN="False";
    elif  [ "$1" == "-m" ];
    then
        DO_PACKAGE="False";
        DO_DISGNOSIS="False";
        DO_MANUAL="True";
        DO_CLEAN="False";
    elif  [ "$1" == "-c" ];
    then
        DO_PACKAGE="False";
        DO_DISGNOSIS="False";
        DO_MANUAL="False";
        DO_CLEAN="True";
    else
        echo -e "${DARK_BLUE}Unregognized option $1.${NC}"
        fct_echo_usage
        exit 1
    fi
}


# ===========================================================================
# Functions for the DIAGNOSIS
# ===========================================================================

# Use unittest to check the API
function fct_test_api {
    echo -e "${BROWN} - Unittest of the API.${NC}"

    echo >> $LOG_DIAGNOSIS
    echo "##########  ${PROGRAM_NAME} API Diagnosis - $TODAY #########" >> $LOG_DIAGNOSIS
    echo >> $LOG_DIAGNOSIS

    echo " ... Test  "
    $BIN_DIR/test_all.py    >&  $TEMP

    local error=`grep -c '... ERROR' $TEMP`
    if [ $error -eq 0 ]; then
         echo " ... Tests: Success"
    else
         echo " ... Tests: $error error(s)."
    fi

    cat $TEMP >> $LOG_DIAGNOSIS
    echo >> $LOG_DIAGNOSIS
    echo " ######### ############################ ######### " >> $LOG_DIAGNOSIS
    echo >> $LOG_DIAGNOSIS

    rm $TEMP
}


# Main function for the diagnosis
function fct_diagnosis {
    fct_echo_title "${PROGRAM_NAME} - Diagnosis"
    fct_test_api
    echo "Check out the $LOG_DIAGNOSIS file for details."
}



# ===========================================================================
# DOCUMENTATION
# ===========================================================================

# Generate a new version of the API manual
function fct_api_manual {
    echo -e "${BROWN} - API Manual${NC}"

    if [ -e $WEB_DIR/manual ] ; then
        rm -rf $WEB_DIR/manual;
    fi

    # test if epydoc is ok.
    type epydoc >& /dev/null
    if [ $? -eq 1 ] ; then
        echo -e "${RED}epydoc is missing. Please, install it and try again.${NC}"
        return 1
    fi

    # OK... generate the API manual
    epydoc --config $BIN_DIR/epydoc.conf --css $ETC_DIR/styles/epydoc.css --output $WEB_DIR/manual $PROGRAM_DIR/proceed/src >& $LOG_MANUAL
    echo " The reference manual of the web directory was updated."
    echo " ... Check out the $LOG_MANUAL file for details."
}


function fct_uml_diagrams {
    echo -e "${BROWN} - $PROGRAM_NAME UML diagrams${NC}"
    # test if suml is ok.
    type suml >& /dev/null
    if [ $? -eq 1 ] ; then
        echo -e "${RED}suml is missing. Please, install it and try again.${NC}"
        return 1
    fi

    #TODO
    #suml --png --class -i $ETC_DIR/figures/proceed.yuml -o $ETC_DIR/figures/proceed.png
}


# Return a string indicating the list of files for a sub-folder of the
# documentation
# Parameters:
#  $1: sub-folder name (without path) of the documentation
function fct_get_md_idx {

    # Get all files mentionned in the idx
    local f="`cat $DOC_DIR/$1/${1}.idx`"

    # Add its path to each file name
    local files="`for i in $f; do echo "$DOC_DIR/$1/"$i; done`"

    # return the list of files
    echo $files
}


# Return the list of sub-folders of the documentation
function fct_get_docfolders {
    local folders="`cat $DOC_DIR/markdown.idx`"
    echo $folders
}


# Return a string indicating the list of files for the documentation
function fct_get_all_md {
    local folders=$(fct_get_docfolders)
    local files="$DOC_DIR/header.md"
    for folder in $folders;
    do
        files="$files $(fct_get_md_idx $folder)"
    done

    # return the list of files
    echo $files
}

# Generate a new version of the documentation
function fct_proceed_doc {
    echo -e "${BROWN} - $PROGRAM_NAME documentation${NC}"

    # test if pandoc is ok.
    type pandoc >& /dev/null
    if [ $? -eq 1 ] ; then
        echo -e "${RED}pandoc is missing. Please, install it and try again.${NC}"
        return 1
    fi

    echo ' Version for the web (add header and footer)'
    # An HTML file is generated for each sub-folder of the documentation
    local folders=$(fct_get_docfolders)
    for folder in $folders;
    do
        echo " ... $folder"
        local files="$DOC_DIR/header.md"
        files="$files $(fct_get_md_idx $folder)"
        files="$files $DOC_DIR/footer.md"
        pandoc -s --toc --mathjax -t html5 --css $ETC_DIR/styles/style.css -H $DOC_DIR/include-scripts.txt -B $DOC_DIR/header.txt -A $DOC_DIR/footer.txt $files --highlight-style haddock -o $WEB_DIR/documentation_${folder}.html
    done

    # A Unique file is generated from all files of the documentation
    local files=$(fct_get_all_md)

    echo ' Version PDF';
    pandoc -N --template=$DOC_DIR/mytemplate.tex -V geometry:a4paper -V geometry:"top=3cm, bottom=3cm, left=3cm, right=2.5cm" --variable documentclass="report" --variable classoption="twoside, openright" --variable mainfont="FreeSerif" --variable sansfont="FreeSans" --variable monofont="FreeMono" --variable fontsize=11pt --variable version="$PROGRAM_VERSION" --variable frontpage="`pwd`/doc/frontpage.pdf" $files --latex-engine=xelatex --toc -o $PROGRAM_DIR/documentation/documentation.pdf
    cp $PROGRAM_DIR/documentation/documentation.pdf $WEB_DIR

    # Package: erase old then copy new
    rm -rf $WEB_DIR/$ETC_DIR
    rm -rf $PROGRAM_DIR/documentation/$ETC_DIR
    cp -r $ETC_DIR $WEB_DIR
    cp -r $ETC_DIR $PROGRAM_DIR/documentation
    cp -r $DOC_DIR $PROGRAM_DIR/documentation/$ETC_DIR

    echo " The ${PROGRAM_NAME} documentation folder and the web directory were both updated."
}


# Main function for the documentation
function fct_documentation {
    fct_echo_title "${PROGRAM_NAME} - API Manual and Documentation (package and web)"
    fct_api_manual
    fct_uml_diagrams
    fct_proceed_doc
}


# ===========================================================================
# PACKAGE
# ===========================================================================

function fct_package {
    fct_echo_title "${PROGRAM_NAME} - Packaging"

    # Update Infos...
    if [ -e $TEMP ]; then rm $TEMP; fi
    cat $PROGRAM_DIR/README.txt | awk -v d=$TODAY '/[dD]ate/{printf "date:       %s\n",d; next} {print}' >> $TEMP
    mv $TEMP $PROGRAM_DIR/README.txt

    # Create the package

    local packagename=`pwd`/${PROGRAM_NAME}-${PROGRAM_VERSION}-${TODAY}.zip
    pushd $PROGRAM_DIR
    zip -q -r $packagename proceed.bat proceed.command bin etc documentation proceed *.txt
    if [ "$?" != 0 ]; then
        echo -e "${RED}No package created!${NC}"
        popd
        return 1
    else
        popd
        echo "  The file" $packagename "has been created."
    fi

}

# ===========================================================================
# CLEAN
# ===========================================================================

function fct_clean_all {
    fct_echo_title "${PROGRAM_NAME} - Clean all contents"
    fct_clean_temp
    fct_clean_proceed
    echo " The proceed folder now is clean!"

 }


# ===========================================================================
# MAIN
# ===========================================================================

fct_test_running "proceed.command"   # Is currently running?
fct_clean_temp            # Clean the current directory
fct_test_nb_args "$#"     # Test if this scripts has the expected number of arguments
fct_get_args "$@"         # Fix options from arguments
fct_echo_header           # Print the header message on stdout

if [ $DO_DISGNOSIS == "True" ]; then fct_diagnosis; fi
if [ $DO_MANUAL == "True" ];    then fct_documentation; fi
if [ $DO_PACKAGE == "True" ];   then fct_clean_proceed; fct_package; fi
if [ $DO_CLEAN == "True" ];   then fct_clean_all; fi

fct_echo_title "Terminated."

# ===========================================================================

