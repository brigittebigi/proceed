#!/usr/bin/env python
# -*- coding: utf8 -*-
# ---------------------------------------------------------------------------
#         ___    __    ___    ___  ____  ____   __
#         |  \  |  \  |   |  /     |     |     |  \   Automatic
#         |__/  |__/  |   |  |     |__   |__   |   |    Conference
#         |     |\_   |   |  |     |     |     |   |    Proceedings
#         |     |  \  |___|  \___  |___  |___  |__/   Generator
#        ==========================================================
#
#           http://www.lpl-aix.fr/~bigi/
#
# ---------------------------------------------------------------------------
# developed at:
#
#       Laboratoire Parole et Langage
#
#       Copyright (C) 2013-2014  Brigitte Bigi
#
#       Use of this software is governed by the GPL, v3
#       This banner notice must not be removed
# ---------------------------------------------------------------------------
#
# Proceed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Proceed is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Proceed. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------

__docformat__ = "epytext"

# ---------------------------------------------------------------------------

import sys
import codecs
import getopt
import logging

# ---------------------------------------------------------------------------

class GenLaTeXFile:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Class to generate an empty latex file.

    Class to generate an empty latex file.
    An header and a footer can be specified.
    Default is a PDF with 1 blank page, containing only the page number.

    """

    def __init__(self):
        """
        Creates a new GenLaTeXFile instance.

        Fix default options that mostly will be overridden.

        """
        self.__papersformat = ["a4paper", "letterpaper", "b5paper", "a5paper" ]

        self.__textstyles = ["\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"]

        self.__options = {}
        self.__options["paper"]        = "a4paper"
        self.__options["topmargin"]    = 30 # millimeters
        self.__options["bottommargin"] = 20 # millimeters
        self.__options["headsize"]     = 20 # pt
        self.__options["footsize"]     = 10 # pt
        self.__options["leftheader"]   = ""
        self.__options["centerheader"] = ""
        self.__options["rightheader"]  = ""
        self.__options["leftfooter"]   = ""
        self.__options["centerfooter"] = "\\thepage"
        self.__options["rightfooter"]  = ""
        self.__options["headercolor"]  = "20,20,20"
        self.__options["footercolor"]  = "20,20,20"
        self.__options["headerrule"]   = False
        self.__options["footerrule"]   = False
        self.__options["headerstyle"]  = ""
        self.__options["footerstyle"]  = ""
        self.__options["pagenumber"]   = "1"
        self.__options["numberofpages"] = 1
        # For TALN:
        #self.__options["color1"] = "30,120,200" # cyan (= light blue)
        #self.__options["color2"] = "0,60,150"   # blue
        #self.__options["color3"] = "190,70,30"  # dark orange
        # For others:
        self.__options["color1"] = "139,53,49"   # for session codes
        self.__options["color2"] = "85,85,240"   # for the date
        self.__options["color3"] = "190,70,30"   # for session names: dark orange

        # A possible text to add into the file
        self.__content = None

    # End __init__
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Setters and Getters for Header/Footer options
    # ------------------------------------------------------------------------


    def set_paper_format(self, pformat):
        """
        Fix the paper format.

        @param format (string): paper format is one of a4paper, letterpaper, b5paper, a5paper

        """
        if pformat not in self.__papersformat:
            raise TypeError
        self.__options["paper"] = pformat

    # End set_paper_format
    # ------------------------------------------------------------------------


    def set_top_margin(self, margin):
        """
        Fix the top margin, in millimeters.

        @param margin (int)

        """
        self.__options["topmargin"] = int(margin)

    # End set_top_margin
    # ------------------------------------------------------------------------


    def set_bottom_margin(self, margin):
        """
        Fix the bottom margin, in millimeters.
        @param margin (int)

        """
        self.__options["bottommargin"] = int(margin)

    # End set_bottom_margin
    # ------------------------------------------------------------------------


    def set_head_size(self, head):
        """
        Fix the head size, in points.

        @param head (int)

        """
        self.__options["headsize"] = int(head)

    # End set_head_size
    # ------------------------------------------------------------------------


    def set_foot_size(self, foot):
        """
        Fix the foot size, in points.

        @param head (int)

        """
        self.__options["footsize"] = int(foot)

    # End set_foot_size
    # ------------------------------------------------------------------------


    def set_left_header(self, text):
        """
        Fix the left header text.

        @param text (string)

        """
        self.__options["leftheader"] = text

    # End set_left_header
    # ------------------------------------------------------------------------


    def set_center_header(self, text):
        """
        Fix the center header text.

        @param text (string)

        """
        self.__options["centerheader"] = text

    # End set_center_header
    # ------------------------------------------------------------------------


    def set_right_header(self, text):
        """
        Fix the right header text.

        @param text (string)

        """
        self.__options["rightheader"] = text

    # End set_right_header
    # ------------------------------------------------------------------------


    def set_left_footer(self, text):
        """
        Fix the left footer text.

        @param text (string)

        """
        self.__options["leftfooter"] = text

    # End set_left_footer
    # ------------------------------------------------------------------------


    def set_center_footer(self, text):
        """
        Fix the center footer text.

        @param text (string)

        """
        self.__options["centerfooter"] = text

    # End set_center_header
    # ------------------------------------------------------------------------


    def set_right_footer(self, text):
        """
        Fix the right footer text.

        @param text (string)

        """
        self.__options["rightfooter"] = text

    # End set_right_footer
    # ------------------------------------------------------------------------


    def set_header_color(self, RGB):
        """
        Fix the header color (by using rgb values).

        @param RGB (string). Default is "100,100,100" (Gray).

        """
        self.__options["headercolor"] = RGB

    # End set_header_color
    # ------------------------------------------------------------------------


    def set_footer_color(self, RGB):
        """
        Fix the footer color (by using rgb values).

        @param RGB (string). Default is "100,100,100" (Gray).

        """
        self.__options["footercolor"] = RGB

    # End set_footer_color
    # ------------------------------------------------------------------------


    def set_header_style(self, style):
        """
        Fix the header style.

        @param style (string). style is one of:
            - \\rm - Roman
            - \\it - Italics
            - \\em - Emphasis (toggles between \it and \rm)
            - \\emph (LaTeX2e emphasis command)
            - \\bf - Boldface
            - \\sl - Slanted
            - \\sf - Sans serif
            - \\sc - Small caps
            - \\tt - Typewriter

        """
        if len(style)>0 and style not in self.__textstyles:
            raise TypeError('Style %s not supported.'%style)
        self.__options["headerstyle"] = style

    # End set_header_style
    # ------------------------------------------------------------------------


    def set_footer_style(self, style):
        """
        Fix the footer style.

        @param style (string). style is one of:
            - \\rm - Roman
            - \\it - Italics
            - \\em - Emphasis (toggles between \it and \rm)
            - \\emph (LaTeX2e emphasis command)
            - \\bf - Boldface
            - \\sl - Slanted
            - \\sf - Sans serif
            - \\sc - Small caps
            - \\tt - Typewriter

        """
        if len(style)>0 and style not in self.__textstyles:
            raise TypeError('Style %s not supported.'%style)
        self.__options["footerstyle"] = style

    # End set_footer_style
    # ------------------------------------------------------------------------


    def set_page_number(self, pagenumber):
        """
        Fix the first page number.

        @param pagenumber (string/int): page number of the 1st page

        """
        self.__options["pagenumber"] = str(pagenumber)

    # End set_page_number
    # ------------------------------------------------------------------------


    def set_number_of_pages(self, number):
        """
        Fix the expected number of pages.

        @param number (int): number of pages

        """
        self.__options["numberofpages"] = int(number)
        if self.__options["numberofpages"] < 1:
            self.__options["numberofpages"] = 1
            raise Exception('Bad number of pages.')

    # End set_number_of_pages
    # ------------------------------------------------------------------------


    def set_tex_content(self, text):
        """
        Fix the LaTeX text to add into the file.

        @param text (string): text

        THE OPTION "NUMBER OF PAGES" WILL BE IGNORED.

        """
        self.__content = text

    # End set_text_content
    # ------------------------------------------------------------------------


    def set_header_rule(self, boolean):
        """
        Activate/Disable the header rule.

        @param boolean (bool)

        """
        self.__options["headerrule"] = boolean

    # End set_header_rule
    # ------------------------------------------------------------------------


    def set_footer_rule(self, boolean):
        """
        Activate/Disable the footer rule.

        @param boolean (bool)

        """
        self.__options["footerrule"] = boolean

    # End set_footer_rule
    # ------------------------------------------------------------------------


    def set_option(self, optionname, optionvalue):
        """
        Fix the value of an existing option.

        Do not use this funtion if you dont exactly know what you are doing!

        - optionname (string)
        - optionvalue (any type)

        """
        if optionname not in self.__options.keys():
            raise TypeError('Unrecognized option')
        self.__options[optionname] = optionvalue

    # End set_option
    # ------------------------------------------------------------------------


    def get_list_paper_format(self):
        """
        Return the list of supported paper formats.
        """
        return self.__papersformat

    # End get_list_paper_format
    # ------------------------------------------------------------------------


    def get_list_textstyles(self):
        """
        Return the list of supported text styles.
        """
        return self.__textstyles

    # End get_list_textstyles
    # ------------------------------------------------------------------------


    def get_page_number(self):
        """
        Return the first page number.
        """
        return self.__options["pagenumber"]

    # End get_page_number
    # ------------------------------------------------------------------------


    def get_option(self, optionname):
        """
        Return any option from its name.
        """
        return self.__options[optionname]

    def get_options(self):
        """
        Return a dictionary of all options.
        """
        return self.__options


    # ------------------------------------------------------------------------
    # Write LaTeX document
    # ------------------------------------------------------------------------


    def exportLaTeX(self,filename):
        """
        Save the LaTeX file.

        @param filename (string): the output file pointer

        """
        if filename is not None:
            encoding='utf-8'
            fp = codecs.open(filename, 'w', encoding)
        else:
            fp = sys.stdout

        self.save(fp)
        fp.close()

    # End export_LaTeX
    # -------------------------------------------------------------------------


    def save(self,fp):
        """
        Save the LaTeX file.

        @param fp (filepointer): the output file

        """
        fp.write( " % This file was automatically generated by Proceed. \n" )
        fp.write( " % A program written by Brigitte Bigi \n" )
        fp.write( " % License: GPL.\n\n" )
        fp.write( " \\documentclass[12pt," )
        fp.write( self.__options["paper"] )
        fp.write( "]{article} \n\n")
        fp.write( " \\usepackage[utf8]{inputenc}\n")
        fp.write( " \\usepackage[T1]{fontenc} %% get hyphenation and accented letters right\n")
        fp.write( " \\usepackage{tipa} \n" )
        fp.write( " \\usepackage{xcolor} \n" )
        fp.write( " \\usepackage{longtable} \n" )
        fp.write( " \\usepackage{fancyhdr} \n" )
        fp.write( " \\usepackage[left=20mm,right=20mm,top="+str(self.__options['topmargin'])+"mm,bottom="+str(self.__options['bottommargin'])+"mm,head="+str(self.__options['headsize'])+"pt,foot="+str(self.__options['footsize'])+"pt]{geometry} \n")
        fp.write( " \\fancyhead{} \n")
        fp.write( " \\fancyfoot{} \n")

        # Fix Header and Footer color
        fp.write( " \\definecolor{HeaderColor}{RGB}{"+self.__options["headercolor"]+"} \n")
        fp.write( " \\definecolor{FooterColor}{RGB}{"+self.__options["footercolor"]+"} \n")

        # Define 3 other colors to be used as needed in the content
        fp.write( " \\definecolor{color1}{RGB}{"+self.__options["color1"]+"} \n")
        fp.write( " \\definecolor{color2}{RGB}{"+self.__options["color2"]+"} \n")
        fp.write( " \\definecolor{color3}{RGB}{"+self.__options["color3"]+"} \n")

        # Fix the Header Rule (YES/NO)
        if self.__options["headerrule"] == True:
            fp.write( " \\renewcommand{\\headrulewidth}{0.5pt} \n")
        else:
            fp.write( " \\renewcommand{\\headrulewidth}{0pt} \n")

        # Fix the Footer Rule (YES/NO)
        if self.__options["footerrule"] == True:
            fp.write(" \\renewcommand{\\footrulewidth}{0.5pt} \n")
        else:
            fp.write(" \\renewcommand{\\footrulewidth}{0pt} \n")

        fp.write( " \\begin{document} \n" )
        fp.write( " \\setcounter{page}{"+str(self.__options["pagenumber"])+"} \n")
        fp.write( "    \\pagestyle{fancy} \n" )

        # Then, fix Header (Left,Center,Right)
        if len(self.__options["leftheader"])>0:
            fp.write( "    \\lhead{\\color{HeaderColor}{"+self.__options["headerstyle"]+"{\small "+self.__options["leftheader"]+"}}}\n")
        if len(self.__options["centerheader"])>0:
            fp.write( "    \\chead{\\color{HeaderColor}{"+self.__options["headerstyle"]+"{\small "+self.__options["centerheader"]+"}}}\n")
        if len(self.__options["rightheader"])>0:
            fp.write( "    \\rhead{\\color{HeaderColor}{"+self.__options["headerstyle"]+"{\small "+self.__options["rightheader"]+"}}}\n")

        # Then, fix Footer (Left,Center,Right)
        if len(self.__options["leftfooter"])>0:
            fp.write( "    \\lfoot{\\color{FooterColor}{"+self.__options["footerstyle"]+"{"+self.__options["leftfooter"]+"}}}\n")
        if len(self.__options["centerfooter"])>0:
            fp.write( "    \\cfoot{\\color{FooterColor}{"+self.__options["footerstyle"]+"{"+self.__options["centerfooter"]+"}}}\n")
        if len(self.__options["rightfooter"])>0:
            fp.write( "    \\rfoot{\\color{FooterColor}{"+self.__options["footerstyle"]+"{"+self.__options["rightfooter"]+"}}}\n")

        # Create pages!
        if self.__content is None:
            # Create as many empty pages as it is fixed by "numberofpages"
            fp.write( "    \\  \\cleardoublepage\n"*self.__options["numberofpages"] )
        else:
            # Simply put the LaTeX content.
            fp.write( self.__content )
        fp.write( " \n" )
        fp.write( " \end{document} \n" )

    # End save
    # -------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Main program to be used inline
# -----------------------------------------------------------------------------


def usage(output):
    """
    Print the usage on an output.

    @param output is a string representing the output (for example: sys.stdout)

    """
    output.write('genLaTeX.py [options] where options are:\n')
    output.write('      -o outputfile           Output file name (Default: stdout) \n')
    output.write('      -l "left header"        Left Header Text\n')
    output.write('      -c "center header"      Center Header Text \n')
    output.write('      -r "right header"       Right Header Text \n')
    output.write('      -L "left footer"        Left Footer Text \n')
    output.write('      -C "center footer"      Center Footer Text \n')
    output.write('      -R "right footer"       Right Footer Text (Default: \\thepage) \n')
    output.write('      -p "paper"              Paper format\n')
    output.write('      -n number               First page number\n')
    output.write('      -N number               Number of pages\n')
    output.write('      -s "style"              Header style\n')
    output.write('      -S "style"              Footer style\n')
    output.write('      -g "R,G,B"              Header color; Red,Green,Blue (Default: "100,100,100") \n')
    output.write('      -G "R,G,B"              Footer colot; Red,Green,Blue (Default: "100,100,100") \n')
    output.write('      --hrule                 Add a rule to separate the header\n')
    output.write('      --frule                 Add a rule to separate the footer\n')
    output.write('      --help                  Print this help\n\n')

# End usage
# ----------------------------------------------------------------------


def Quit(message, status):
    """
    Quit the program with the appropriate exit status.

    @param message is a text to communicate to the user on sys.stderr.
    @param status is an integer of the status exit value

    """
    sys.stderr.write('genLaTeX.py '+message)
    sys.exit(status)

# End Quit
# ----------------------------------------------------------------------


if __name__ == "__main__":
    # Example of use:
    #   python genLaTeX.py
    #       -l "left header"
    #       -c "center header"
    #       -r "right header"
    #       -L "left footer"
    #       -C "center footer"
    #       -R "\\thepage"
    #       -p "letterpaper"
    #       -n 4
    #       -N 2
    #       -s "\\emph"
    #       -S "\\bf"
    #       -g "255,150,50"
    #       -G "150,250,50"
    #       --hrule
    #       -o outputfile

    # -------------------------------------------------------------------------
    # Verify and extract args:
    # -------------------------------------------------------------------------

    # Verify the program name and possibly some arguments
    if len(sys.argv) == 1:
        # stop the program and print an error message
        usage(sys.stderr)
        sys.exit(1)

    # Get options (if any...)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:c:r:L:C:R:p:n:N:s:S:g:G:o:", ["help","hrule","frule"])
    except getopt.GetoptError, err:
        # Print help information and exit:
        Quit("Error: "+str(err)+".\nUse option --help for any help.\n", 1)

    # Create object
    try:
        latexfile = GenLaTeXFile()
    except Exception, e:
        Quit('Error when creating the LaTeX object: \n'+str(e)+'\n', 1)

    filename = None
    # Extract options
    for o, a in opts:
        try:
            if o == "-l":
                latexfile.set_left_header(a)
            elif o == "-c":
                latexfile.set_center_header(a)
            elif o == "-r":
                latexfile.set_right_header(a)
            elif o == "-L":
                latexfile.set_left_footer(a)
            elif o == "-C":
                latexfile.set_center_footer(a)
            elif o == "-R":
                latexfile.set_right_footer(a)
            elif o == "-p":
                latexfile.set_paper_format(a)
            elif o == "-n":
                latexfile.set_page_number(a)
            elif o == "-N":
                latexfile.set_number_of_pages(a)
            elif o == "-s":
                latexfile.set_header_style(a)
            elif o == "-S":
                latexfile.set_footer_style(a)
            elif o == "--hrule":
                latexfile.set_header_rule(True)
            elif o == "--frule":
                latexfile.set_footer_rule(True)
            elif o == "-g":
                latexfile.set_header_color(a)
            elif o == "-G":
                latexfile.set_footer_color(a)
            elif o == "-o":
                filename = a
            elif o == "--help": # need help
                print 'Help'
                usage(sys.stdout)
                sys.exit()
        except Exception,e:
            usage(sys.stderr)
            sys.stderr.write('List of accepted paper formats: \n')
            for i in latexfile.get_list_paper_format():
                sys.stderr.write("        "+i+"\n")
            sys.stderr.write("\n")
            sys.stderr.write('List of accepted text styles: \n')
            for i in latexfile.get_list_textstyles():
                sys.stderr.write("        \\"+i+"\n")
            sys.stderr.write("\n")
            sys.exit(1)

    latexfile.exportLaTeX( filename )

# ---------------------------------------------------------------------------
