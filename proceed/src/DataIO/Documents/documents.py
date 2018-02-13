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

__docformat__ = "epytext"


class document:
    """
    @authors: Bastien Hebaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Data for a document.

    Each document requires an identifier, corresponding to the name
    of the pdf (without the extension). This id is commonly the paper number.
    A document instance contains a title, an abstract, a subject, a list of
    topics, a list of key words, a list of authors, a list of laboratories,
    and a status value (from 0 to 4).

    """

    def __init__( self , docid):
        self._docid    = docid
        self._title    = ""
        self._abstract = ""
        self._subject  = ""
        self._topics   = list()
        self._keywords = list()
        self._authors  = list()
        self._laboratory = list()
        self._status = 1
        self._pdfdiagnosis = -2 # 0=missing; 1=valid; -1=invalid; -2:unknown


    def __repr__(self):

        authorList = list()
        for author in self._authors :
            authorList.append(unicode(author))

        laboList = list()
        for labo in self._laboratory :
            laboList.append(unicode(labo))

        return u"Document:\nId: {0}\nTitle: {1}\nAbstract: {2}\nSubject: {3}\nTopics: {4}\nKeywords: \n{5}\nAuthors: \n{6}\nLaboratories:\n{7}".format(self._docid , self._title , self._abstract , self._subject , '\n'.join(self._topics) , '\n'.join(self._keywords) , '\n'.join(authorList) , '\n'.join(laboList))


    def __str__(self):

        authorList = list()
        for author in self._authors :
            authorList.append(unicode(author))

        laboList = list()
        for labo in self._laboratory :
            laboList.append(unicode(labo))

        return u"Document:\nId: {0}\nTitle: {1}\nAbstract: {2}\nSubject: {3}\nTopics: {4}\nKeywords: \n{5}\nAuthors: \n{6}\nLaboratories:\n{7}".format(self._docid , self._title , self._abstract , self._subject , '\n'.join(self._topics) , '\n'.join(self._keywords) , '\n'.join(authorList) , '\n'.join(laboList))


    def __iter__(self):
        return self


    def get_docid(self):
        return self._docid

    def get_title(self):
        return self._title

    def get_subject(self):
        return self._subject

    def get_topics(self):
        return self._topics

    def get_abstract(self):
        return self._abstract

    def get_keywords(self):
        return self._keywords

    def get_authors(self):
        return self._authors

    def get_laboratory(self):
        return self._laboratory

    def get_status(self):
        return self._status

    def get_pdfdiagnosis(self):
        return self._pdfdiagnosis


    def set_docid(self , docid):
        self._docid = docid

    def set_title(self , title ):
        self._title = title

    def set_subject(self , subject):
        self._subject = subject

    def set_topics(self , topics):
        self._topics = topics

    def set_abstract(self , abstract ):
        self._abstract = abstract

    def set_keywords(self , keywords):
        self._keywords = keywords

    def set_authors(self , authors):
        self._authors = authors

    def append_author(self, author):
        self._authors.append( author )

    def set_laboratory(self , laboratory):
        self._laboratory = laboratory

    def append_laboratory(self, laboratory):
        self._laboratory.append( laboratory )

    def set_status(self , s):
#         try:
#             ints = int(status)
#         except Exception,e:
#             raise TypeError('The status value must be an integer value (0-4).')
        if s < 0 or s > 4:
            raise ValueError('The status value is not in an appropriate range (0 to 4): %s - %s'%(s,type(s)))
        self._status = s

    def set_pdfdiagnosis(self, v):
        if v<-2 or v>1:
            raise ValueError('The diagnosis value is not in an appropriate range (-2 to 1): %s - %s'%(v,type(v)))
        self._pdfdiagnosis = v


class author:

    def __init__( self , ordre ):
        self.ordre         = ordre
        self.lastname      = ""
        self.middlename    = ""
        self.firstname     = ""
        self.email         = ""
        self.url           = ""
        self.speaker       = ""
        self.researchTeam  = ""
        self.corresponding = ""
        self.labidx        = list()


    def __iter__(self):
        return self


    def __repr__(self):

        laboList = list()
        for labo in self.labidx :
            laboList.append(unicode(labo.get_nom()))
        return u"Author:\nOrder: {0}\nLastname: {1}\nMiddlename: {2}\nFirstanme: {3}\nEmail: {4}\nUrl: {5}\nSpeaker: {6}\nresearchTeam: {7}\ncorresponding: {8}\nLaboratory: {9}\n".format( self.ordre , self.lastname , self.middlename , self.firstname , self.email , self.url , self.speaker , self.researchTeam , self.corresponding , '\n'.join(laboList))


    def __str__(self):

        laboList = list()
        for labo in self.labidx:
            laboList.append(unicode(labo.get_nom()))

        return u"Author:\nOrder: {0}\nLastname: {1}\nMiddlename: {2}\nFirstanme: {3}\nEmail: {4}\nUrl: {5}\nSpeaker: {6}\nresearchTeam: {7}\ncorresponding: {8}\nLaboratory: {9}\n".format( self.ordre , self.lastname , self.middlename , self.firstname , self.email , self.url , self.speaker , self.researchTeam , self.corresponding , '\n'.join(laboList))


    def get_ordre(self):
        return self.ordre

    def get_lastname(self):
        return self.lastname

    def get_middlename(self):
        return self.middlename

    def get_firstname(self):
        return self.firstname

    def get_email(self):
        return self.email

    def get_url(self):
        return self.url

    def get_speaker(self):
        return self.speaker

    def get_researchTeam(self):
        return self.researchTeam

    def get_corresponding(self):
        return self.corresponding

    def get_labos(self):
        return self.labidx


    def set_ordre(self , ordre):
        self.ordre = ordre

    def set_lastname(self , lastname ):
        self.lastname = lastname

    def set_middlename(self , middlename):
        self.middlename = middlename

    def set_firstname(self , firstname):
        self.firstname = firstname

    def set_email(self , email ):
        self.email = email

    def set_url(self , url):
        self.url = url

    def set_speaker(self,speaker):
        self.speaker = speaker

    def set_researchTeam(self , researchTeam ):
        self.researchTeam = researchTeam

    def set_corresponding(self , corresponding):
        self.corresponding = corresponding

    def set_labos(self,labidx):
        self.labidx = labidx


class laboratory:

    def __init__( self , num ):
        self.num     = num
        self.nom     = ""
        self.sigle   = ""
        self.country = ""
        self.url     = ""
        self.address = ""
        self.affiliations = list()

    def __repr__(self):
        return u"Laboratory :\nNumber: {6}\nName: {0}\nSigle: {1}\nCountry: {2}\nurl: {3}\naddress: {4}\nAffiliations: \n{5}\n".format( self.nom , self.sigle , self.country , self.url , self.address , '\n'.join(self.affiliations) , self.num )

    def __str__(self):
        return u"Laboratory :\nNumber: {6}\nName: {0}\nSigle: {1}\nCountry: {2}\nurl: {3}\naddress: {4}\nAffiliations: \n{5}\n".format( self.nom , self.sigle , self.country , self.url , self.address , '\n'.join(self.affiliations) , self.num )

    def __iter__(self):
        return self


    def get_num(self):
        return self.num

    def get_nom(self):
        return self.nom

    def get_sigle(self):
        return self.sigle

    def get_country(self):
        return self.country

    def get_url(self):
        return self.url

    def get_address(self):
        return self.address

    def get_affiliations(self):
        return self.affiliations


    def set_nom(self , nom):
        self.nom = nom

    def set_sigle(self , sigle ):
        self.sigle = sigle

    def set_country(self , country):
        self.country = country

    def set_address(self , address):
        self.address = address

    def set_affiliations(self , affiliations ):
        self.affiliations = affiliations

    def set_url(self , url):
        self.url = url
