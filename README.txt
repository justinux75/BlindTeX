DESCRIPTION:
This is a software which allows to convert LaTeX formulas to a natural language format. The main goal of it is to allow visual impaired people to access to mathematical content in documents writen in LaTeX format, with the help of a screen reader.

The program has two modes of use: the first one is by converting the LaTeX document to an xhtml format (with the help of an external software, LaTeXML program) with the mathematical equations translated with the BlindTeX engine. In this way, users can use their web browser to navigate through the document and read the equations in text mode (we  suggest that this navigation can be performed with ‘word navigation mode’ in the screen reader so that  each mathematical symbol can be read  on a single ‘key hit’).
The secon mode of use  is by transformin LaTeX equations individually. This mode  does not need of any external program.

IMPORTANT REMARK:
We re-write the blindtex project (http://www.github.com/blindtex/blindtex/) adding new features and leaving others, so that it be easier work with files. This changes have been done in a different repository due to the code in this one, is not so clean and stable as it is that in the original repository. So, for those who are interested in colaborate or to have a more professional code we suggest to go to that repositoy.
 
DIFFERENCES:

   The general differences with respect to the original BlindTeX proyect are:
1. We have omitted all references to the GUI and we leave all the functionality from the terminal.
2. We are not incorporating the AST implementation of the last version of the original 	 projec	t.
3. We have added features that allow to deal with user’s macros, including tex files from the main LaTeX document and we have extended the dictionaries and some other structures in the parsing.

Up to now, we have only support for spanish dictionaries, but  we hope that we can give support for english and  another languages.

BEFORE INSTALATION:

In order to work with this version of BTX  it is needed to have previously installed the following software:
1. Python 3. (www.python.org)
2. We make use of the python ply module (sudo pip install ply, or put the module into the ‘converter’ folder).
3. A LaTeX distribution (for instance MiKTeX in Windows or LiveTeX in Linux or MACOS).
4. We use the ‘LaTeXML’ project to convert LaTeX documents to xhtml format, so it is needed to have installed the latexml program (see, https://dlmf.nist.gov/LaTeXML/get.html)
The BlindTeX scripts make use of the two commands:
latexml -dest=file.xml file.tex
latexmlpost -dest=file.xhtml file.xml
So it is important to ensure that these commands can be executed from your terminal.
4. By default we assume that your  browser is ‘Mozilla Firefox’ in Windows or ‘Safari’ in MACOS. (This can be changed easily from the code)
INSTALLATION:
We are not providing packaging of the software, so it is neccsary to install the software manually. You may take the following steps:
1.- Download or clone the repository, and move the BlindTeX folder (that inside the main  folder), to a preferred place (we suggest to put it in the root, ‘C:\BlindTeX’, in Windows), and int the user's home folder in Linux or MacOS. If you decide to change the location, please change the  "BTX" variable  in the blt scripts appropriately. 
2. Move the blt.bat file for Windows  or blt  shell script for MacOS or Linux in a folder included in the user’s PATH. If you do not know what is this, we suggest to create a  ‘bin’ folder as following:
	a. Create a folder named ‘bin’ in a location into the user’s folder (for instance, ‘C:\Users\[Name of the user]\bin’ in Windows or ‘/Users/[Name of the user/bin’ for MacOS or Linux).
	b. Include the bin folder to the PATH. In Windows press Windows key and X, and afterwards press ‘a’ to open a Power Shell. Type ‘sysdm.cpl’ to open System preferences. Go to  ‘Advanced Options’ and User’s variables. Add  the exact path of the new ‘bin’ folder. In  Linux or MacOS open a terminal and open the file ‘.bash_profile’ and write at the end of the file 
	export PATH=“$PATH:~/bin”
	3. Put the blt.bat file (for windows) or the blt script (for Linux or MacOS) contained in the scripts folder of BLX into the ‘bin’ folder. In Linux or MacOS from the terminal move into the bin folder (‘cd ~/bin’) and give permission for executing:
	chmod a+x blt
   

If all has gone fine, by typing ‘blt -h’ in the terminal you should obtain some ‘warnings’ about the parser and a ‘help’ of the use of the ‘mainBlindTeX.py’ script.
 
USE:
We can use BTX in two ways:

1. Converting full LaTeX documents.
The general use of blindtex is the followin:
1.- Open a terminal (cmd) in the folder where the LaTeX document is located.
2. First it is important to ensuere that the TeX file is correct, so we emphasize to LaTeX compile it with the command (several times):
pdflatex file.tex
And, if there is no problems, then we proceed with the following command:
blt -abuo file.tex  
with file.tex is the  and name of the LaTeX file to convert. This command creates a number of files, but the one that we can be interested in is ‘file.xhtml’.
  The options ‘-abuo’ means:
1. -o: This is the option to produce the output file (it is not optional if we want a  translation of a full LaTeX document). With this option we make use of the ‘LaTeXML’ program.
-a: It reads the labels of equations wich are writen in the file.aux file when the LaTeX compiler processes the file.tex document. (So for this option we need to have compiled the TeX document previously). However this option is only optional.
 -u: This option allows to un-macros the original LaTeX document. It will only work with the user’s macros defined in the preamble of the document (between the LaTeX commands  ‘\documentclass’ or ‘\documentstyle’ and the ‘\begin{document}’). (optional)
-b: This option allows to open the browser with the resulting xhtml document.(optional)

Apart from the file.xhtml file and others files, BLT also produces a TroubleFormulas’s document where are lested all the formlas which have caused some problems in the translation. (in the resulting  xhtml file they will appear as ‘Bad Formula’).

If the -b option was included  after various secons the web browser should open showing the document with equations translated in natural language.

2. Command line conversion:
 This procedure allows to convert LaTeX formulas (without the ‘$’ symbols or others equation delimiters) in the command line. The option for this procedure is ‘-e’, and it can be used with the formula as an string argument, e.g.,
 blt -e "\frac{1}{2}\int_0^\infty f(x)\,dx"
 The result will be shown in the  stdout. Notice the double quotes at the begining and at the end of the formula.
 Also it is possible to use the '-e' option with pipes from a file, e.g.,

blt -e < file.txt
where 'file.txt' is an text file with the formula to be converted (without delimiters).
 Or in a prompt mode
blt -e "
>\frac{1}{2}
>\int_0^\infty f(x)\,dx
<"
Notice the inclussion of double quotes at the command line and at the end of the formula.


MORE ADVANCED USE:
 The program allows to manage the dictionaries for the different LaTeX symbols, so one can change the translation of already  existing symbols, adding new symbols, etc. See the documentation of the BTX.
