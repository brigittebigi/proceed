<!DOCTYPE html>
<html lang="en">
    
<head>
    <meta charset="utf-8">
    <meta name="description" content="Proceed - LPL" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Proceed</title>  
    <link rel="stylesheet" href="./etc/styles/style.css" />
    <link href="favicon.png" type="image/x-icon" rel="icon" />
    <link href="favicon.png" type="image/x-icon" rel="shortcut icon" />
</head>

<body> 

    <div class="cols12 section1">
        <div class="cols3"></div>
        <div class="cols7 mg-top1 ">

            <a href="index.php"><div class="maintitle mg-top4">PROCEED</div></a>
 
            <div class="menu">
                <a href="download.html"><img src="icon-menu/dl.png">Download</a>
                <a href="installation.html"><img src="icon-menu/install.png">Installation</a>
                <a href="documentation.html"><img src="icon-menu/doc.png">Documentation</a>
                <a href="http://github.com/brigittebigi/proceed/"><img src="icon-menu/dev.png">Development</a>
            </div> 
        </div>
    </div> 

    <div class="cols12 section2">
        <div class="cols2"></div>
        <div class="cols5 mg-top2 right">
            <h1>Proceed</h1>
            <p class="txt-justify cols10 left"> 
             Proceed is a computer software package written and maintained by Brigitte Bigi 
             of the Laboratoire Parole et Langage, in Aix-en-Provence, France. 
             Available for free, with open source code, there is simply no other package
             to allow the almost automatic generation of proceedings and book of abstracts. 
            </p>        
        </div>

        <div class="cols4 left mg-top3">
        <div class="slideshow">
        <ul>
            <li><img src="./etc/screenshots/OverallView.png" alt="" width="350" height="200" /></li>
        <?php
            $temp_files = glob('./etc/screenshots/*');
            foreach($temp_files as $file)
            {
                echo '        <li><img src="'.$file.'" alt="" width="350" height="200" /></li>';
                echo PHP_EOL;
            }
        ?>
        </ul>
        <script type="text/javascript" src="./etc/scripts/jquery.min.js"></script>
        <script type="text/javascript">
           $(function(){
              setInterval(function(){
                 $(".slideshow ul").animate({marginLeft:-350},800,function(){
                    $(this).css({marginLeft:0}).find("li:last").after($(this).find("li:first"));
                 })
              }, 3000);
           });
        </script>
        </div>
        </div>

    </div>    
    
    <div class="cols12 section3">
        <div class="cols2"></div>
        <div class="cols9 mg-top2 right">
            <h1>Download and install Proceed</h1>
            <p class="txt-justify cols10 left"> 
            Proceed is ready to run, so it does not need elaborate installation, except for 
            its dependencies (other software required for Proceed to work properly). 
            All you need to do is to copy the Proceed package from the web site to somewhere 
            on your computer. Preferably, choose a location without spaces nor accentuated 
            characters in the name of the path.
            </p>
            <p class="txt-justify cols10 left">
            The package is compressed and zipped, so you will need to decompress 
            and unpack it once you've got it.
            </p>        
        </div>
    </div>

    <div id="footer">
        <img src="image-general/gnu.png">       

        <p class="copyright">
            Brigitte Bigi © 2013-2015 
        </p>
    </div>
    
    <span class="scrollT"></span>
    <script type="text/javascript" src="./etc/scripts/fn.scrollT.js"></script>
    <script type="text/javascript" src="./etc/scripts/fn.center.js"></script>
    <script type="text/javascript" src="./etc/scripts/main.js"></script>
</body>
</html>
