#!/usr/bin/python
# -*- coding: UTF-8 -*-
# For sciencesconf input only.
#
# extract-reviews.py
#
# 2013-05-28
# Extract a set of csv files (each one from one abstract) from a directory,
# then save data in a file
# The output file is the equivalent of the "eval.csv"

import os
import sys
import getopt
import csv
import os.path

# ----------------------------------------------------------------------
# USEFUL FUNCTIONS
# ----------------------------------------------------------------------

def usage(output):
    """ Print the usage on an output.
        Parameters:
           - output is a string representing the output (for example: sys.stdout)
        Return:      none
        Exceptions:  none
    """
    output.write('extract-reviews.py [options] where options are:\n')
    output.write('      -i directory       Input directory name     [required] \n')
    output.write('      -o file            Output file name         [required] \n')
    output.write('      --quiet            Do not print messages, except errors or warnings\n')
    output.write('      --help             Print this help\n\n')

# End usage
# ----------------------------------------------------------------------


def quit(message, status):
    """ Quit the program with the appropriate exit status.
        Parameters:
           - message is a text to communicate to the user on sys.stderr.
           - status is an integer of the status exit value
        Return:      none
        Exceptions:  none
    """
    sys.stderr.write('extract-reviews.py '+message)
    sys.exit(status)

# End quit
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# TASK FUNCTIONS...
# ----------------------------------------------------------------------


# --------------------------------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------------------------------


if __name__:

    # ----------------------------------------------------------------------
    # Get all arguments, verify inputs.
    # ----------------------------------------------------------------------

    # Verify the program name and possibly some arguments
    if len(sys.argv) == 1:
        # stop the program and print an error message
        usage(sys.stderr)
        sys.exit(1)

    # Get options (if any...)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["help","quiet"])
    except getopt.GetoptError, err:
        # Print help information and exit:
        quit("Error: "+str(err)+".\nUse option -h for any help.\n", 1)

    dirinput   = None
    fileoutput = None
    verbose    = True

    # Extract options
    for o, a in opts:
        if o == "-i":
            dirinput = a
        elif o == "-o":
            fileoutput = a
        elif o == "--quiet":
            verbose = False
        elif o == "--help": # need help
            print 'Help'
            usage(sys.stdout)
            sys.exit()

    # Verify args

    if dirinput is not None:
        if not os.path.exists(dirinput):
            quit("Error: BAD input directory name: "+dirinput+"\n", 1)
    else:
        sys.stderr.write('Error: an input directory is required.\n')
        usage(sys.stderr)
        sys.exit(1)

    if fileoutput is None:
        sys.stderr.write('Error: an output file name is required.\n')
        usage(sys.stderr)
        sys.exit(1)

    if os.path.dirname(os.path.abspath(fileoutput)) == os.path.abspath(dirinput):
        sys.stderr.write('ERROR: the output file **CAN NOT** be inside the input directory.\n')
        sys.exit(1)

    if verbose is True:
        print "INPUT:  "+os.path.abspath(dirinput)
        print "OUTPUT: "+os.path.abspath(fileoutput)


    # ----------------------------------------------------------------------
    # Load input data / Write output
    # ----------------------------------------------------------------------

    # Open output file (erase existing file without warning!)
    try:
        fdo = open(fileoutput, "w")
    except Exception, e:
        sys.stderr.write('ERROR: unable to open'+fileoutput+'.\n')
        sys.exit(1)


    # Explore each csv input file, then write selected content in the output
    firstline = True
    for f in sorted( [csvf for csvf in os.listdir(dirinput) if csvf.endswith('.csv')] ):

        if verbose is True:
            print "FILE: ",f

        try:
            with open(os.path.join(dirinput,f), 'rb') as csvfile:
                datareader = csv.reader(csvfile, delimiter=';')
                rownum = 0
                for row in datareader:
                    # Keep only once the first line
                    if firstline is True and rownum==0:
                        # add an empty column
                        r = '"docid" ; ' + ' ; '.join( row )
                        firstline = False
                        # write data
                        fdo.write( r+'\n' )
                    elif rownum>0:
                        # Get the file name, remove extension
                        docid = os.path.basename( f ).replace(".csv","")+ ' ; '
                        docid = docid.replace('.eval', '')
                        r = docid + " ; ".join( row )
                        # write data
                        fdo.write( r+'\n' )
                    rownum = rownum + 1

        except Exception, e:
            sys.stderr.write('---- WARNING. File: '+f+' ignored:'+str(e)+'\n')

    fdo.close()

    # ----------------------------------------------------------------------

