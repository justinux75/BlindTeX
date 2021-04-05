#-*-:coding:utf-8-*-

import os
import copy
import string
import subprocess
import mainBlindtex
import os
import re
from sys import argv

#HU1
#Method to open a file and return its content as a string.
def openFile(fileName):
	'''This function takes a file a return its content as a string.
		Args:
			fileName(str): The name of the file to be oppened.
		Returns:
			str: The content of the file.'''
	try:
		myFile = open(fileName)
		stringDocument = myFile.read()
		myFile.close()
		return stringDocument
	except IOError:
		print("File %s could not be openned."%(fileName))
		return ""
#EndOfFunction


## La funcion "inputFiles" obtiene la cadena del documento latex
## y sustituye los comandos "\include{archivo}" y "\input{archivo}" por el 
## contenido del archivo "archivo.tex" que se encuentre en la misma ubicacion que 
##el archivo fuernte inicial.
##	ARGS entrada:
##		documentString (str): la cadena del archivo inicial
##		currentPath: Ubicacion del archivo inicial.
##	Output:
##		inputList(lst): lista, cuyo primer elemento es el documento tex sustituido, y el segundo es la lista de archivos (path absoluto) de archivos revisados (incluyebndo el orginal) sin extension.. de archivos input/include invocados.
 
def inputFiles(documentString, fileName):
	currentPath=os.path.dirname(fileName)
	lista=[os.path.splitext(fileName)[0]]
	patron=re.compile(r"\\(input|include)\{([a-zA-Z0-9\.]*)\}")
	newDocumentString=documentString
	coinci=patron.finditer(documentString)
	for k in coinci:
		inputFileString=openFile(os.path.join(currentPath,k.groups()[1]+os.path.extsep+"tex"))
		newDocumentString=newDocumentString.replace(k.group(),"\n"+inputFileString+"\n")
		lista.append(os.path.join(currentPath,os.path.splitext(k.groups()[1])[0]))
	return [newDocumentString,lista]
 
 


##End of function


#Replace the document containing the LaTeX math with the output of the function seekAndReplace. Write the content in a new file.
def replaceAndWrite(contentList, replacedDocument, fileName):
	'''Replace the document containing the LaTeX math with the output of the function seekAndReplace. Write the content in a new file.
		Args:
			contentList(list[str,str,str]): The list generated by extractContent.
			replacedDocument(str): the LaTeX content without formulas, just markers.
			fileName(str): The name of the .tex file where the result will be written. '''
	newContentList = copy.deepcopy(contentList)
	newContentList[1] = replacedDocument
	try:
		myFile = open(fileName, 'w')#TODO Check if the file already exist, warn about that and decide if the user wants to replace it.
		myFile.write("".join(newContentList))
		myFile.close()
	except IOError:
		print("File could not be oppened.")
		return

	
#EndOfFunction

def convertToHtml(fileName, biblioName=None, translator="latexml"):
	'''This function uses LaTeXML to convert a .tex file in a html with accesible math formulas.
		Args:
			fileName(str): the name of the .tex file to be processed.
			(opt)biblioName(str): the name o a .bib file. '''

	noExtensionName = fileName.replace(".tex","")
	
	if(biblioName):
                if(os.name == 'nt'): #i.e is in windows
                        noExtensionBiblio = biblioName.replace(".bib","")
                        subprocess.call(["latexml","--dest=%s.xml"%(noExtensionName),"--quiet",fileName], shell=True)
                        subprocess.call(["latexml", "--dest=%s.xml"%(noExtensionBiblio),"--bibtex", biblioName], shell= True)
                        subprocess.call(["latexmlpost","-dest=%s.xhtml"%(noExtensionName),"--bibliography=%s.xml"%(noExtensionBiblio),noExtensionName+".xml"], shell=True)
                else: #TODO: Do not repeat
                        noExtensionBiblio = biblioName.replace(".bib","")
                        subprocess.call(["latexml","--dest=%s.xml"%(noExtensionName),"--quiet",fileName])
                        subprocess.call(["latexml", "--dest=%s.xml"%(noExtensionBiblio),"--bibtex", biblioName])
                        subprocess.call(["latexmlpost","-dest=%s.xhtml"%(noExtensionName),"--bibliography=%s.xml"%(noExtensionBiblio),noExtensionName+".xml"])
	else:
		if translator=="latexml":
			if(os.name == 'nt'):
				subprocess.call(["latexml","--dest=%s.xml"%(noExtensionName),"--quiet",fileName], shell = True)#Generates xml file.
				subprocess.call(["latexmlpost","-dest=%s.xhtml"%(noExtensionName),noExtensionName+".xml"], shell = True)#Generates xhtml file.
			else:
				subprocess.call(["latexml","--dest=%s.xml"%(noExtensionName),"--quiet",fileName])#Generates xml file.
				subprocess.call(["latexmlpost","-dest=%s.xhtml"%(noExtensionName),noExtensionName+".xml"])#Generates xhtml file.
		else:
			if(os.name == 'nt'):
				subprocess.call([translator,fileName], shell = True)#Generates html file.
			else:
				subprocess.call([translator,fileName])#Generates html file.
#EndOfFunction

def convertToPdf(filePath,fileName):
        if(os.name == 'nt'):
                subprocess.call(['pdflatex','-output-directory',filePath, fileName], shell = True)
                subprocess.call(['pdflatex','-output-directory',filePath, fileName], shell = True)
        else:
                subprocess.call(['pdflatex','-output-directory',filePath, fileName])
                subprocess.call(['pdflatex','-output-directory',filePath, fileName])
        

#EndOfFunction
        
#TODO ¿con alguna extensión o la extensión se da desde afuera?
def writeHtmlFile(htmlString, fileName):
	'''Function to write the html result in a final file.
		Args:
			htmlString(str): The string with the html content of the final result.
			fileName(str): The name of the file where the string will be written. '''
	try:
		htmlFile = open(fileName,'w')
		htmlFile.write(htmlString)
		htmlFile.close()
	except IOError:
		print('File could not be oppened.')
		return	
#EndOf Function



#This function works just when a .tex file is being converted.
def writeTroubles(strfileName, listtroubleFormulas):
        (filePath, name) = os.path.split(strfileName)
        try:
                registerFile = open(os.path.join(filePath, 'TroubleFormulasOf'+name.replace('.tex','.txt')),'w')
                for formula in listtroubleFormulas:
                        registerFile.write('I had troubles with:\n'+formula+'\n')
                registerFile.close()
        except IOError:
                return
#EndOfFunction