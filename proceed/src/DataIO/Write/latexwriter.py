#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
# SPPAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SPPAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPPAS. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------

import codecs
import os
import datetime
import subprocess
import shutil

from structs.prefs import Preferences
from structs.abstracts_themes import all_themes

from utils.commons import test_pdflatex, test_xetex
import utils.abstracts   as abstracts
import utils.unicode_tex as unicode_tex
import utils.fileutils   as fileutils

# ---------------------------------------------------------------------------

COMPILERS = ['pdflatex', 'xetex']

# ---------------------------------------------------------------------------

class LaTeXDiagnosis() :
    """
    Execute pdflatex on a document and return a diagnosis:
        -  1 means ok (no compilation error)
        - -1 means that an error occurred.
    """

    def __init__(self, texfilename):
        self._error = ""
        self.texfilename = texfilename

    def get_error(self):
        return self._error

    def run(self):
        tmpname = fileutils.set_tmpfilename() + ".tex"
        shutil.copy(self.texfilename, tmpname)
        try :
            subprocess.check_output(["pdflatex","-interaction=nonstopmode",tmpname])
            self._error = "OK"
        except subprocess.CalledProcessError as err :
            self._error = err.output
            ret = -1
        else:
            ret = 1
        self.clean( tmpname )
        return ret

    def clean(self, f):
        try:
            os.remove( f )
            os.remove( f.replace('.tex', '.log') )
            os.remove( f.replace('.tex', '.aux') )
            os.remove( f.replace('.tex', '.pdf') )
        except Exception:
            pass

# ---------------------------------------------------------------------------
# LaTeXWriter
# ---------------------------------------------------------------------------

class LaTeXWriter:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Write documents, one per LaTeX file with title, authors, abstract, or
    all documents title/authors in a single LaTeX file.

    To do: some <span> in abstracts are not properly removed.

    """

    def __init__( self, status=1, prefs=None ):
        self._status  = status
        self.prefs = prefs
        if prefs is None:
            self.prefs.SetValue('COMPILER', 'str', 'pdflatex')
            self._prefs.SetTheme( all_themes[0][1] )
        self.pdflatex_ok = test_pdflatex()
        self.xetex_ok = test_xetex()

    def write_as_list( self, docs, filename ):
        with codecs.open ( filename , 'w' , 'utf-8') as fp:

            self.__write_header(fp)
            self.__write_style(fp)
            self.__write_separator(fp)
            self.__write_begindoc(fp)
            fp.write('\\begin{tabular}{ll}\n')
            for doc in docs:
                if doc.get_status()==self._status:
                    for auth in doc.get_authors():
                        ln = unicode_tex.unicode_to_tex(auth.get_lastname())
                        fn = unicode_tex.unicode_to_tex(auth.get_firstname())
                        fp.write(ln+' '+fn+', ')
                    fp.write(' & ')
                    fp.write(doc.get_title())
                    fp.write(' \\\\ \n')
                    fp.write('\n')
            fp.write('\\end{tabular}\n')
            self.__write_end(fp)

    def write_doc( self, doc , filename, tocompile=True ):
        with codecs.open ( filename , 'w' , 'utf-8') as fp:
            self.__write_header(fp,doc.get_docid())
            self.__write_properties(fp)
            self.__write_style(fp)
            self.__write_separator(fp)
            self.__write_title(fp,doc.get_title())
            self.__write_authors(fp,doc)
            self.__write_separator(fp)
            self.__write_begindoc(fp)
            self.__write_maketitle(fp)
            if len(doc.get_keywords()) > 0:
                fp.write('\\keywords{ ')
                self.__write_keywords(fp,doc.get_keywords())
                fp.write('}\n')
                fp.write('\\abstract{}\n')
            self.__write_abstract(fp,doc.get_abstract())
            self.__write_end(fp)

        # Perform the diagnosis
        if self.pdflatex_ok:
            if self.prefs.GetValue('COMPILER') == 'pdflatex':
                diag = LaTeXDiagnosis( filename ).run()
            else:
                comp = self.prefs.GetValue('COMPILER')
                self.prefs.SetValue('COMPILER', 'str', 'pdflatex')
                tmpname = fileutils.set_tmpfilename()
                self.write_doc( doc, tmpname )
                diag = LaTeXDiagnosis( tmpname ).run()
                try:
                    os.remove( tmpname )
                except Exception:
                    pass
                self.prefs.SetValue('COMPILER', 'str', comp)
            doc.set_pdfdiagnosis(diag)

        if tocompile is True:
            if ( self.prefs.GetValue('COMPILER') == 'pdflatex' and self.pdflatex_ok ) or  ( self.prefs.GetValue('COMPILER') == 'xetex' and self.xetex_ok ):
                try :
                    tmpname = fileutils.set_tmpfilename() + ".tex"
                    shutil.copy(filename, tmpname)
                    subprocess.check_output([self.prefs.GetValue('COMPILER'),"-interaction=nonstopmode",tmpname])
                except Exception:
                    doc.set_pdfdiagnosis( 0 )
                try:
                    os.remove( tmpname )
                    os.remove( tmpname.replace('.tex', '.log') )
                    os.remove( tmpname.replace('.tex', '.aux') )
                    shutil.move(tmpname.replace('.tex', '.pdf'), filename.replace('.tex', '.pdf'))
                except Exception:
                    pass

    def __write_separator(self,fp):
        fp.write('% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %\n')

    def __write_header(self,fp,docid=None):
        now = datetime.datetime.now()
        self.__write_separator(fp)
        fp.write('% % Document generated automatically                                      % %\n')
        if docid is not None:
            fp.write('% % Abstract submission number '+str(docid)+ '                                      % %\n')
        fp.write('% % '+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'                                                             % %\n')
        self.__write_separator(fp)
        fp.write('\n')
        fp.write('\documentclass['+self.prefs.GetValue('FONT_SIZE')+']{article}\n')
        fp.write('\n')

        ## Fix included package depending the compiler (and the encoding...)
        if self.prefs.GetValue('COMPILER') == "pdflatex":
            fp.write('\usepackage['+self.prefs.GetValue('ENCODING')+']{inputenc}\n')
            fp.write('\usepackage[T1]{fontenc} %% this gets hyphenation and accented letters right for most of the European languages\n')
            fp.write('\usepackage{CJKutf8} %% for Chinese characters\n')
            fp.write('\usepackage[english]{babel}\n')
            fp.write('\usepackage{textcomp}\n')
            fp.write('\n')
            fp.write('\usepackage[pdftex]{graphicx}\n')
            fp.write('\usepackage{amsfonts}\n')
            fp.write('\usepackage{amssymb}\n')
            fp.write('\usepackage{amsmath}\n')
            fp.write('\usepackage{mathptmx}        %% use fitting times fonts also in formulas\n')

        elif self.prefs.GetValue('COMPILER') == "xetex":
            fp.write('\usepackage{fontspec}       %% we will use a specific font\n')
            fp.write('\usepackage{xunicode}       %% this file is UTF8 \n')
            fp.write('\usepackage{lmodern}        %%  \n')
            fp.write('\setmainfont{Times New Roman} \n')
            fp.write('\setsansfont{Arial} \n')
            fp.write('\setmonofont[Color={0019D4}]{Courier New} \n')
            #fp.write('\setmainfont{DejaVu Serif}  %%  \n')
            #fp.write('\setmainfont{WenQuanYi Zen Hei Sharp}  %% The choosed font \n')
            fp.write('\n')

        else:
            message  = "Unrecognized compiler name: %s."%self.prefs.GetValue('COMPILER')
            message += "Must be one of %s"%' '.join(COMPILERS)
            raise TypeError( message )
        fp.write('\usepackage{authblk}\n')
        fp.write('\usepackage{tipa}\n')
        fp.write('\n')

        self.__write_separator(fp)
        fp.write('\n')


    def __write_properties(self,fp):
        fp.write('% % set margins\n')
        fp.write('\usepackage['+self.prefs.GetValue('PAPER_SIZE')+',')
        fp.write('left='+str(self.prefs.GetValue('MARGIN_LEFT'))+'mm,')
        fp.write('right='+str(self.prefs.GetValue('MARGIN_RIGHT'))+'mm,')
        fp.write('top='+str(self.prefs.GetValue('MARGIN_TOP'))+'mm,')
        fp.write('bottom='+str(self.prefs.GetValue('MARGIN_BOTTOM'))+'mm,')
        fp.write('noheadfoot]{geometry}\n')
        fp.write('\n')
        fp.write('% % paragraph indentation\n')
        fp.write('\setlength{\parindent}{'+str(self.prefs.GetValue('PARINDENT'))+'cm}\n')
        fp.write('\setlength{\parskip}{'+str(self.prefs.GetValue('PARSKIP'))+'pt}\n')
        fp.write('\n')
        fp.write('% % no page numbers\n')
        fp.write('\\renewcommand\\thepage{}\n')
        fp.write('\n')


    def __write_style(self,fp):
        fp.write('% % fix title style\n')
        fp.write('\let\LaTeXtitle\\title\n')
        fp.write(self.prefs.GetValue('TITLE') + '\n')
        fp.write('\n')
        fp.write('% % Fix authors style\n')
        fp.write(self.prefs.GetValue('AUTHORS') + '\n')
        # Remove the "AND" between authors, replace by a comma
        fp.write('\\renewcommand\Authsep{, }\n')
        fp.write('\\renewcommand\Authand{, }\n')
        fp.write('\\renewcommand\Authands{, }\n')
        fp.write('\n')
        fp.write('% % Fix affiliation style\n')
        fp.write(self.prefs.GetValue('LABOS') + '\n')
        fp.write('\setlength{\\affilsep}{1em}\n')
        fp.write('\n')
        fp.write('% % fix e-mail style\n')
        fp.write(self.prefs.GetValue('EMAIL') + '\n')
        fp.write('\n')
        fp.write('% % fix keywords style\n')
        fp.write('\\newcommand{\smalllineskip}{\\baselineskip=15pt}\n')
        fp.write(self.prefs.GetValue('KEYWORDS') + '\n')
        fp.write('\n')
        fp.write(self.prefs.GetValue('ABSTRACT') + '\n')
        fp.write('\\renewcommand\paragraph[1]{\\vspace{1em}{\\bfseries #1}}\n\n')


    def __write_title(self,fp,title): # title is a string
        fp.write('\n')
        fp.write('% % Fix title\n')
        fp.write('\\title{'+unicode(title)+'}\n')
        fp.write('\date{}\n')
        fp.write('\n')


    def __write_authors(self,fp,doc): # authors is a list of authors instances
        fp.write('% % Fix authors then affiliation and email for each author\n')
        i = 0
        for auth in doc.get_authors():
            i = i+1
            ln = unicode(auth.get_lastname())
            mn = unicode(auth.get_middlename())
            fn = unicode(auth.get_firstname())
            fp.write('\\author['+str(i)+']{'+fn+' '+mn+' '+ln+'}\n')
        i = 0
        for auth in doc.get_authors():
            i = i+1
            for lab in auth.get_labos():
                labo = doc.get_laboratory()[int(lab)]
                fp.write('\\affil['+str(i)+']{')
                fp.write(unicode(labo.get_nom())+', ')
                #fp.write(unicode(labo.get_address())+' ')
                fp.write(unicode(labo.get_country())+' ')
                fp.write('\emailaddress{'+unicode_tex.unicode_to_tex(auth.get_email()))
                fp.write('}}\n')


    def __write_begindoc(self,fp):
        fp.write('\n')
        fp.write('% % BEGIN DOCUMENT % %\n')
        fp.write('\\begin{document}\n')
        fp.write('\n')


    def __write_maketitle(self,fp):
        fp.write('% % MAKE THE TITLE\n')
        fp.write('\maketitle\n')
        fp.write('\n')


    def __write_keywords(self,fp,kwds): # kwds is a list of strings
        for kwidx in range(len(kwds)-1):
            fp.write(unicode_tex.unicode_to_tex(kwds[kwidx]))
            fp.write(', ')
        fp.write(unicode_tex.unicode_to_tex(kwds[len(kwds)-1]))


    def __write_abstract(self,fp,abstract): # abstract is a string
        fp.write('% % ABSTRACT CONTENT\n')
        fp.write('\n')
        # Convert important HMTL Tag into LateX
        tmpa = abstracts.html_to_mytags(abstract)
        # Remove the other HTML tags
        parser = abstracts.HTMLCleaner()
        parser.feed(tmpa)
        a = parser.get_data()
        # Then, normalize the string
        a = unicode_tex.unicode_to_texipa(a)
        # Convert my tags to real tex
        a = abstracts.mytags_to_tex(abstract)
        # finally: write!
        fp.write(unicode(a))
        fp.write('\n')


    def __write_end(self,fp):
        fp.write('\n')
        fp.write('% % END DOCUMENT % %\n')
        fp.write('\end{document}\n')
        fp.write('% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %\n')
        fp.write('\n')


    def __write_figure(self,fp,filename):
        ##NOT USED FOR NOW!
        fp.write('\n')
        fp.write('% % FIGURE\n')
        fp.write('\\begin{figure}[h]\n')
        fp.write('   \centerline{\includegraphics[width=0.8\\textwidth]{'+filename+'}}\n')
        fp.write('\end{figure}\n')
        fp.write('\n')

