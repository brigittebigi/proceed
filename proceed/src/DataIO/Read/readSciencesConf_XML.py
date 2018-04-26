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
#       Copyright (C) 2013-2018  Brigitte Bigi
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

import xml.dom.minidom

from DataIO.Documents.documents import document, author, laboratory
from readgeneric import readGeneric

from threading import Thread

# ---------------------------------------------------------------------------


class readSciencesConfXML(readGeneric, Thread):
    """
    :authors: Bastien Herbaut, Brigitte Bigi
    :contact: brigitte.bigi@gmail.com
    :license: GPL
    
    Read XML files from sciencesconf.org inheritance from readGeneric.

    """
    def __init__(self, progressbar=None):
        Thread.__init__(self)
        self._progress = progressbar
        self.start()

    # -----------------------------------------------------------------------

    # overwrite
    def GetDocs(self, filename, authorsfilename=None):
        """
        Return a list of document instances from filename.

        :param filename: (str) the XML submissions file name.
        This file contains all information required to import data.

        """
        if self._progress:
            self._progress.set_new()
            self._progress.set_header("Read XML file")
            self._progress.update(0, "")

        self.dom = xml.dom.minidom.parse(filename)
        self.DocTab = self.createDocuments()

        return self.DocTab

    # -----------------------------------------------------------------------

    def get_ByTagName (self, tagName):

        return self.dom.getElementsByTagName(tagName)

    # -----------------------------------------------------------------------

    def createDocuments(self):

        documents_tab = list()
        doc_tab = self.get_ByTagName("document")
        total = len(doc_tab)

        for i, doc in enumerate(doc_tab):
            if self._progress:
                # Indicate the file to be processed
                self._progress.set_text("Paper id: " + doc.getAttribute("docid"))

            new_doc = document(doc.getAttribute("docid"))
            if doc.getAttribute("status"):
                new_doc.set_status(int(doc.getAttribute("status")))
            else:
                new_doc.set_status(1)

            metaDataTab = self.get_ByTagName('metadata')

            for metadata in metaDataTab:
                if metadata.parentNode == doc:
                    title = self.get_Info_Str(metadata, 'title')
                    abstract = self.get_Info_Str(metadata, 'abstract')
                    subject = self.get_Info_Str(metadata, 'subject')
                    topics = self.get_Info_List(metadata, 'topic')
                    keywords = self.get_Info_List(metadata, 'keyword')

                    new_doc.set_title(title)
                    new_doc.set_abstract(abstract)
                    new_doc.set_subject(subject)
                    new_doc.set_topics(topics)
                    new_doc.set_keywords(keywords)

            for authors in self.get_ByTagName("authors"):
                if authors.parentNode == doc:
                    new_doc.set_authors(self.get_Authors(authors, doc))

            new_doc.set_laboratory(self.get_Labo(doc))

            documents_tab.append(new_doc)
            if self._progress:
                self._progress.set_fraction(float((i+1))/float(total))

        # Indicate completed!
        if self._progress:
            self._progress.update(1, "Completed.")
            self._progress.set_header("")

        return documents_tab

    # -----------------------------------------------------------------------

    def get_Authors(self, authorsTag, parentTag):

        authorsList = list()
        authorTab = self.get_ByTagName("author")
        maxOrdre = self.get_AuthorsMaxOrder(authorsTag)

        i = 1
        while i <= maxOrdre:

            for authors in authorTab:

                if authors.parentNode != authorsTag:
                    continue

                if int(authors.getAttribute('order')) != i:
                    continue

                # i == int(author.getAttribute('order'))
                new_author = author(i)

                last_name = self.get_Info_Str(authors, 'lastname')
                middle_name = self.get_Info_Str(authors, 'middlename')
                first_name = self.get_Info_Str(authors, 'firstname')
                email = self.get_Info_Str(authors, 'email')
                url = self.get_Info_Str(authors, 'url')
                speaker = self.get_Info_Str(authors, 'speaker')
                corresponding = self.get_Info_Str(authors, 'corresponding')
                research_team = self.get_Info_Str(authors, 'researchteam')

                labs_list = self.get_Author_labidx(authors)

                new_author.set_last_name(last_name)
                new_author.set_middle_name(middle_name)
                new_author.set_first_name(first_name)
                new_author.set_email(email)
                new_author.set_url(url)
                new_author.set_speaker(speaker)
                new_author.set_corresponding(corresponding)
                new_author.set_labos(labs_list)
                new_author.set_research_team(research_team)

                authorsList.append(new_author)
            i += 1
            
        return authorsList

    # -----------------------------------------------------------------------

    def get_Author_labidx (self, authorTag):

        numLabo_Author = list()
        laboAuthorTab = self.get_ByTagName('labidx')

        for laboId in laboAuthorTab:
            if (laboId.parentNode == authorTag):
                numLabo_Author.append(self.getText(laboId.childNodes))

        #return labs_list
        return numLabo_Author

    # -----------------------------------------------------------------------

    def get_Labo(self, docTag):

        labs_list = list()
        labs_doct = self.get_ByTagName("laboratory")

        for labo in labs_doct:

            if labo.parentNode.parentNode != docTag:
                continue

            #else
            num = labo.getAttribute('labidx')
            name = self.get_Info_Str(labo, 'name')
            sigle = self.get_Info_Str(labo, 'sigle')
            country = self.get_Info_Str(labo, 'country')
            url = self.get_Info_Str(labo, 'url')
            address = self.get_Info_Str(labo, 'address')
            affiliations_list = self.get_Info_List(labo, 'affiliation')

            new_lab = laboratory (num)
            new_lab.set_nom(name)
            new_lab.set_sigle(sigle)
            new_lab.set_country(country)
            new_lab.set_url(url)
            new_lab.set_address(address)
            new_lab.set_affiliations(affiliations_list)

            labs_list.append(new_lab)

        return labs_list

    # -----------------------------------------------------------------------

    def get_AuthorsMaxOrder(self, authorTag):

        author_tab = self.get_ByTagName("author")
        res = 0
        for author in author_tab:
            if author.parentNode == authorTag:
                if int(author.getAttribute('order')) > res:
                    res = int(author.getAttribute('order'))

        return res

    # -----------------------------------------------------------------------

    def get_Info_Str(self, parentTag, info):

        res = ""
        tag_tab = self.get_ByTagName(info)

        for tag in tag_tab:
            if tag.parentNode == parentTag:
                res = self.getText(tag.childNodes)
                if info == "abstract":
                    res = tag.firstChild.wholeText

        return unicode(res)

    # -----------------------------------------------------------------------

    def get_Info_List(self, parentTag, info):

        res = list()

        tagTab = self.get_ByTagName(info)
        for tag in tagTab:
            if tag.parentNode.parentNode == parentTag:
                res.append(self.getText(tag.childNodes))

        return res

    # -----------------------------------------------------------------------

    def getText(self, nodelist):
        """
        Return the text contained by the nodes in nodelist.
        """
        rc = list()
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

