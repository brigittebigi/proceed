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
    </div>    <div class="cols12 section2">
        <!-- Espacement latérale -->
        <div class="cols2"></div>
        <div class="cols5 mg-top1 left">
            <h1 class="title0 left cols10">Proceed</h1>
            <p class="txt-justify cols10 left"> 
             Proceed is a computer software package written and maintained by Brigitte Bigi of the Laboratoire Parole et Langage, in Aix-en-Provence, France. Available for free, with open source code, there is simply no other package. Proceed is developed to allow the almost automatic generation of proceedings and book of abstracts. 
            </p>        
        </div>
    </div>    
    <div class="cols12 section3">
        <!-- Espacement latérale -->
        <div class="cols2"></div>
        <div class="cols5 mg-top2 right">
            <h1 class="title0 left cols10">Download and install Proceed</h1>
            <p class="txt-justify cols10 left"> 
            Proceed is ready to run, so it does not need elaborate installation, except for its dependencies (other software required for Proceed to work properly). All you need to do is to copy the Proceed package from the web site to somewhere on your computer. Preferably, choose a location without spaces nor accentuated characters in the name of the path.

            The package is compressed and zipped, so you will need to decompress and unpack it once you've got it.
            </p>        
        </div>
        <div class="cols4 left mg-top3">
            <img id="js-diapo" src="" alt="diapo-exemple">           
        </div>
    </div>
    <!-- On réupére le nom des images à faire défiler en JS -->
        <script type="text/javascript">
        var TabFiles = [".","..","Export1.png","LatexGen.png"]; 
    </script>    
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