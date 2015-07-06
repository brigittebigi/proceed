<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="description" content="Proceed - LPL" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Proceed</title>  
    <link rel="stylesheet" href="style.css" />
    <link href="favicon.png" type="image/x-icon" rel="icon" />
    <link href="favicon.png" type="image/x-icon" rel="shortcut icon" />
</head>
<body> 
    <!-- Div principale -->
    <div class="cols12 section1">
        <!-- Espacement latérale -->
        <div class="cols3"></div>
        <div class="cols7 mg-top3 ">
            <a id="title-proceed" href="index.php"><h1>PROCEED</h1></a>
            <div class="menu">
                <a href="#"><img src="icon-menu/dl.png">Download</a>
                <a href="install.php"><img src="icon-menu/install.png">Installation</a>
                <a href="doc.php"><img src="icon-menu/doc.png">Documentation</a>
                <a href="#"><img src="icon-menu/dev.png">Development</a>
            </div>          
        </div>
    </div>    <div class="cols12 section3">
        <!-- Espacement latérale -->
        <div class="cols2"></div>
        <div class="cols5 mg-top1 left">
            <h1 class="title0 left cols10">Installation</h1>
<p>SPPAS installation only consists to unpack the package.

    <p>
        In order to work, external programs must be installed <b>before</b>
        installing SPPAS.
        <i>Administrator rights are required to perform these installations.</i>
        Follow <b>carefully</b> instructions of this page to download and install all of them:
    </p>
    <ul>
        <li> Python 2.7</li>
        <li> wxPython </li>
        <li> Julius </li>
    </ul>


    <h1>Installing dependencies on Windows</h1>

        <h4>How to know if my computer is a 32-bits or 64-bits architecture?</h4>

        <h5>Method 1: automatically </h5>
        <p>
        <a href="http://support.microsoft.com/kb/827218">Just follow this link...</a> and
        it will be printed in blue color in the page.
        </p>

        <h5>Method 2: manually </h5>
        <p>
        <i>Windows >= 8:</i>
        Go to start and search for this pc and go to properties.
        Then you can find the architecture in section "System", line "System type:".
        </p>
        <p>
        <i>Windows Vista or Windows 7: </i>
        Click on Start, type system in the Start Search box, and then click system in the Programs list.
        For a 64-bits version operating system: 64-bits Operating System appears for the System type under System.
        For a 32-bits version operating system: 32-bits Operating System appears for the System type under System.
        </p>
        <p>
        <i>Windows XP: </i>
        Click on Start and then click on Run.
        Type sysdm.cpl, and then click on OK.
        Click on the General tab.
        For a 64-bits version operating system: Windows XP Professional x64 Edition Version appears under System.
        For a 32-bits version operating system: Windows XP Professional Version appears under System.
        </p>

        <h2>Python</h2>

        <p>
            <a href="https://www.python.org/downloads/release/python-2710/">Click here to download <b> Python </b></a>
        </p>
        <ul>
            <li> If you have a 32-bits computer, download and execute Python 2.7.9 "Windows x86 MSI Installer".</li>
            <li> Else if you have a 64-bits computer, download and execute Python 2.7.9 "Windows x86-64 MSI Installer". </li>
        </ul>
        <p>
        During  the installation, click three times on the "Next" button and then on "Finish".
        </p>

        <h2>WxPython</h2>

        <p>
            <a href="http://www.wxpython.org/download.php#msw">Click here to download <b> wxPython </b></a>
        </p>
        <ul>
            <li>If you have a 32-bits computer, download and execute wxPython with version name: "-win32-py27". </li>
            <li>Else if you have a 64-bits computer, download and execute wxPython with version name: "-win64-py27". </li>
        </ul>
        <p>
            During  the installation, click on the "Next" button and then on "Finish".
        </p>

        <h2>Julius installation:</h2>

        <p>
            <a href="http://sourceforge.jp/projects/julius/downloads/60273/julius-4.3.1-win32bin.zip/">Click here to download <b> Julius (release >= 4.1)</b></a>
        </p>

        <p>
            Open the Explorer and go to into the julius installation directory.
            Open the "bin" directory then select the file "julius.exe".
            <b>Copy this file into C:\WINDOWS\ </b><br>
            Take care: the file name must be STRICTLY julius.exe, and nothing else
            (you'll have to rename it by removing the version number if any).
        </p>


    <h1>Dependencies installation on Linux</h1>

        <p>
            For <b>Linux Ubuntu</b> users, there are <i>deb</i> packages for
            all dependencies (python2.7, wxpython, julius). <br>

            python-wxgtk-media and gstreamer must be installed too.
        </p>

        <p>
            For <b>Linux Fedora</b> users, there are <i>rpm</i> packages for
            python2.7 and wxpython. The Julius tool will have to be installed
            from sources.
        </p>


    <h1>Dependencies installation on MacOS</h1>
    <!-- <img src="images/macos.png" width="40"/> -->

        <h2>Python</h2>

            <p>
                <a href="https://www.python.org/downloads/release/python-2710/">Click here to download <b> Python </b></a>
            </p>
            <p>
              Click on the package and follow instructions.
            </p>

        <h2>WxPython</h2>
            <p>
              <a href="http://downloads.sourceforge.net/wxpython/wxPython3.0-osx-3.0.2.0-cocoa-py2.7.dmg">Click here to download <b> wxPython </b></a>
            </p>
            <p>
              Click on the package and follow instructions.
            </p>

        <h2>Julius installation: </h2>

            <p>
            I compiled a 64-bits version which include a ready-to-use version of Julius for MacOS.
            This version is available here:
            </p>
            <p>
            <a href="http://hdl.handle.net/11041/sldr000800/Julius-MacOS-10.7.3.tgz">Julius for MacOS (515Ko)</a>
            </p>
            <p>
            Download, extract the archive and drag-and-drop the package content into the <b>/usr/local/bin</b> directory.
            </p>

    <hr />     
        </div>
    </div>    
    <div id="footer">
        <img src="image-general/gnu.png">       

        <p class="copyright">
            Brigitte Bigi © 2011-2015 
        </p>
    </div>    
    <span class="scrollT"></span>
    <script type="text/javascript" src="jquery.min.js"></script>
    <script type="text/javascript" src="fn.scrollT.js"></script>
    <script type="text/javascript" src="fn.center.js"></script>
    <script type="text/javascript" src="diapo.js"></script>    
    <script type="text/javascript" src="main.js"></script>
</body>
</html>