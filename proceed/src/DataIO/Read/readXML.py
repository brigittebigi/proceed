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

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import xml.dom.minidom
import codecs
import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(os.path.dirname( os.path.abspath(__file__))), "Documents") )

from documents import document, author, laboratory
from readgeneric import readGeneric


# ---------------------------------------------------------------------------
# Class
# ---------------------------------------------------------------------------

class readXML( readGeneric ):
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Read XML files from sciencesconf.org inheritance from readGeneric.

    """

    def __init__( self ):
        pass


    # overwrite
    def GetDocs ( self, filename, authorsfilename=None ):
        """
        Return a list of document instances from filename.

        @param filename is the XML submissions file name. This file contains all
        information required to import data.

        """
        self.dom = xml.dom.minidom.parse(filename)
        self.DocTab = self.createDocuments ()
        return self.DocTab


    def get_ByTagName ( self , tagName ):

        return self.dom.getElementsByTagName(tagName)


    def createDocuments ( self ):

        documentsTab = list()
        docTab = self.get_ByTagName ("document")

        for doc in docTab:

            newDoc = document( doc.getAttribute("docid") )
            newDoc.set_status( doc.getAttribute("status") )

            metaDataTab = self.get_ByTagName('metadata')

            for metadata in metaDataTab:

                if ( metadata.parentNode == doc ):

                    title = self.get_Info_Str(    metadata , 'title' )
                    abstract = self.get_Info_Str( metadata , 'abstract' )
                    subject = self.get_Info_Str(  metadata , 'subject' )
                    topics = self.get_Info_List(  metadata , 'topic' )
                    keywords = self.get_Info_List ( metadata , 'keyword' )

                    newDoc.set_title ( title )
                    newDoc.set_abstract ( abstract )
                    newDoc.set_subject ( subject )
                    newDoc.set_topics ( topics )
                    newDoc.set_keywords ( keywords )


            authorsTab = self.get_ByTagName( "authors" )

            for authors in authorsTab:

                if ( authors.parentNode == doc ):
                    authorList = self.get_Authors( authors , doc )
                    newDoc.set_authors( authorList )

            newDoc.set_laboratory(self.get_Labo(doc))

            documentsTab.append(newDoc)

        return documentsTab



    def get_Authors ( self , authorsTag , parentTag ):

        authorsList = list()
        authorTab =self.get_ByTagName( "author" )
        maxOrdre = self.get_AuthorsMaxOrder( authorsTag )

        i = 1

        while ( i <= maxOrdre ):

            for authors in authorTab:

                if ( authors.parentNode != authorsTag ):
                    continue

                if ( int(authors.getAttribute( 'order' ) ) != i ):
                    continue

                # i == int(author.getAttribute( 'order' ) )
                newAuthor = author( i )

                lastname    = self.get_Info_Str ( authors , 'lastname' )
                middlename  = self.get_Info_Str ( authors , 'middlename' )
                firstname   = self.get_Info_Str ( authors , 'firstname' )
                email       = self.get_Info_Str ( authors , 'email' )
                url         = self.get_Info_Str ( authors , 'url' )
                speaker     = self.get_Info_Str ( authors , 'speaker' )
                corresponding = self.get_Info_Str ( authors , 'corresponding' )
                researchTeam  = self.get_Info_Str ( authors , 'researchteam' )

                laboList = self.get_Author_labidx ( authors  )

                newAuthor.set_lastname(lastname)
                newAuthor.set_middlename(middlename)
                newAuthor.set_firstname(firstname)
                newAuthor.set_email(email)
                newAuthor.set_url(url)
                newAuthor.set_speaker(speaker)
                newAuthor.set_corresponding(corresponding)
                newAuthor.set_labos(laboList)
                newAuthor.set_researchTeam(researchTeam)

                authorsList.append(newAuthor)

            i += 1
        return authorsList


    def get_Author_labidx ( self , authorTag ):

        numLabo_Author = list()
        laboAuthorTab = self.get_ByTagName('labidx')

        for laboId in laboAuthorTab:

            if ( laboId.parentNode == authorTag ):
                numLabo_Author.append( self.getText(laboId.childNodes) )


        #return laboList
        return numLabo_Author


    def get_Labo ( self , docTag ):

        laboList = list()

        laboDoc = self.get_ByTagName("laboratory")

        for labo in laboDoc:

            if ( labo.parentNode.parentNode != docTag ):
                continue

            #else
            num = labo.getAttribute('labidx')
            name  = self.get_Info_Str ( labo , 'name')
            sigle  = self.get_Info_Str ( labo , 'sigle')
            country  = self.get_Info_Str ( labo , 'country')
            url  = self.get_Info_Str ( labo , 'url')
            address  = self.get_Info_Str ( labo , 'address')
            affiliationsList  = self.get_Info_List ( labo , 'affiliation')

            newLabo = laboratory ( num )
            newLabo.set_nom(name)
            newLabo.set_sigle(sigle)
            newLabo.set_country(country)
            newLabo.set_url(url)
            newLabo.set_address(address)
            newLabo.set_affiliations(affiliationsList)

            laboList.append(newLabo)

        return laboList


    def get_AuthorsMaxOrder ( self , authorTag ):

        authorTab =self.get_ByTagName( "author" )
        res = 0

        for author in authorTab:

            if ( author.parentNode == authorTag ):
                if ( int(author.getAttribute( 'order' ) ) > res ):
                    res = int(author.getAttribute( 'order' ) )

        return res


    def get_Info_Str ( self , parentTag , info ):


        res = ""
        tagTab = self.get_ByTagName(info)

        for tag in tagTab:

            if ( tag.parentNode == parentTag ):
                res = self.getText(tag.childNodes)
                if ( info == "abstract"):
                    res = tag.firstChild.wholeText

        return unicode(res)


    def get_Info_List ( self , parentTag , info ):

        res = list()

        tagTab = self.get_ByTagName(info)

        for tag in tagTab:

            if ( tag.parentNode.parentNode == parentTag ):
                res.append(self.getText(tag.childNodes))

        return res


    def getText(self ,nodelist):
        """
        Return the text contained by the nodes in nodelist.
        """

        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)



# DEBUG:
if ( __name__ == '__main__'):

    Obj = readXML( )

    with codecs.open ( 'test.txt' , 'w' , 'utf-8') as out:
        for doc in Obj.GetDocs('../soumissions-trasp.xml'):
            out.write('* Soumission: \n')
            out.write('    - Titre : '+unicode(doc.get_title()))
            out.write('\n')
            out.write('    - Auteurs: \n')
            for auth in doc.get_authors():
                out.write('         '+auth.get_lastname()+' '+auth.get_firstname()+' ; ')
                for lab in auth.get_labos():
                    labo = doc.get_laboratory()[int(lab)]
                    out.write(labo.get_nom()+', ')
                    #out.write(labo.get_address()+' ')
                    out.write(labo.get_country()+' ; ')

                out.write('\n')
            out.write('\n')

            #out.write ( unicode(doc) )

