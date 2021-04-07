#-*-:coding:utf-8-*-
import iotools.iotools
import iotools.stringtools
import iotools.macros
from iotools.stringtools import troubleFormulas
import converter.parser
import argparse
import os
import os.path
from sys import argv
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

def convertDocument(fileName, format=0,aux='no',undo='no',transl="latexml"):
	#Let's deal with path and fileNames, actually fileName is the path of the file.
	(filePath,name) = os.path.split(fileName)
	if transl=="latexml": # or transl=="htlatex":
		HTML="xhtml"
	else:
		HTML="html"

	#Get the document in a string.
	documentString = iotools.iotools.openFile(fileName)
	#if option "undo" is "yes"  cleans string  off commentaries and include strings of related files.
	if undo=="yes" or aux=="yes":
		includedFiles=iotools.iotools.inputFiles(documentString,fileName)
		documentString=includedFiles[0]
	if undo=="yes":
		documentString = iotools.macros.cleanLatex(documentString)
	#Get the content in a list with three elements.
	documentContent = iotools.stringtools.extractContent(documentString)
	if undo=='yes':
		documentContentUndo = iotools.macros.undo(documentContent)
		documentContent=documentContentUndo

	#This generates a list(a named tuple) with the document content (all formulas replaced) named replacedDocument, inline formulas named inlineList and display formulas named displayList.
	documentAndLists = iotools.stringtools.seekAndReplaceFormulas(documentContent[1])
	newDocumentContent = documentAndLists.replacedDocument
	
	#Generate the labels list.
	labelsList = iotools.stringtools.generateListOfLabels(documentAndLists.displayList)
	# generates  a dictionary with the labels as keys and numbering as values. In case of option 'aux="no"' its a redundant dictionary.
	if aux=="yes":
		auxiliarDocumentString=""
		for inputFilesIncluded in includedFiles[1]:
			auxiliarDocumentString+= iotools.iotools.openFile(inputFilesIncluded+os.path.extsep+"aux")
		labelsDict=iotools.stringtools.generateLabelsDict(auxiliarDocumentString, labelsList)
	else:
		labelsDict={label: label for label in labelsList}
	#Replace the references.
	newDocumentContent = iotools.stringtools.replaceRefs(newDocumentContent, labelsList)
	#Write another tex file without formulas.
	iotools.iotools.replaceAndWrite(documentContent,newDocumentContent,os.path.join(filePath,'noFormula_'+name))
	
	converter.parser.setOption(0)
	#Convert the formulas
	for index in range(len(documentAndLists.inlineList)):
		documentAndLists.inlineList[index] = converter.parser.convert(documentAndLists.inlineList[index])

	for index in range(len(documentAndLists.displayList)):
		documentAndLists.displayList[index] = converter.parser.convert(documentAndLists.displayList[index])
	if format==0:
		iotools.iotools.convertToHtml(os.path.join(filePath,'noFormula_'+name),translator=transl)
		#Get the html in a string
		htmlString = iotools.iotools.openFile(os.path.join(filePath,'noFormula_'+name.replace('.tex','.'+HTML)))
		#Insert converted formulas.
		htmlString = iotools.stringtools.insertConvertedFormulas(htmlString, documentAndLists.inlineList, documentAndLists.displayList)
		#Insert References
		htmlString = iotools.stringtools.insertReferences(htmlString,labelsDict)
		iotools.iotools.writeHtmlFile(htmlString, os.path.join(filePath,name.replace('.tex','.'+HTML)))
		#Insert labels with numbering in formulas
		htmlString = iotools.stringtools.replaceLabels(htmlString,labelsDict)
		iotools.iotools.writeHtmlFile(htmlString, os.path.join(filePath,name.replace('.tex','.'+HTML)))
		#Remove Residues
		try:
			os.remove(os.path.join(filePath,'noFormula_'+name.replace('.tex','.'+HTML)))
			if transl=="latexml":
				os.remove(os.path.join(filePath,'noFormula_'+name.replace('.tex','.xml')))
		except OSError:
			print("noFormula  files could not be removed/found")
	else:
		## For  the txt format:
		latexString=iotools.iotools.openFile(os.path.join(filePath,'noFormula_'+name))
		latexString = iotools.stringtools.insertConvertedFormulas(latexString, documentAndLists.inlineList, documentAndLists.displayList,format=1)
				#Insert References
		#latexString = iotools.stringtools.insertReferences(latexString,labelsDict)
		iotools.iotools.writeHtmlFile(latexString, os.path.join(filePath,name.replace('.tex','.txt')))
	#Remove Residues
	os.remove(os.path.join(filePath,'noFormula_'+name))


        #Write the trouble formulas
	iotools.iotools.writeTroubles(fileName, troubleFormulas)
	
#EndOfFunction

def convertToPdf(fileName):
        #Get the document in a string.
	documentString = iotools.iotools.openFile(fileName)
	#Get the content in a list with three elements.
	documentContent = iotools.stringtools.extractContent(documentString)
	#This generates a list(a named tuple) with the document content (all formulas replaced) named replacedDocument, inline formulas named inlineList and display formulas named displayList.
	documentAndLists = iotools.stringtools.seekAndReplaceFormulas(documentContent[1])
	newDocumentContent = documentAndLists.replacedDocument
	#Generate the labels list
	labelsList = iotools.stringtools.generateListOfLabels(documentAndLists.displayList)
	
	#Let's deal with path and fileNames, actually fileName is the path of the file.
	(filePath,name) = os.path.split(fileName)
	
	converter.parser.setOption(3)#For the LaTeX Accents
	#Convert the formulas
	for index in range(len(documentAndLists.inlineList)):
                #Here we take the risk of the sign ~ being used in the formula.
		documentAndLists.inlineList[index] = "\# %s \#"%converter.parser.convert(documentAndLists.inlineList[index])

	for index in range(len(documentAndLists.displayList)):
		documentAndLists.displayList[index] = "Ecuaci\\'on\\\\%s\\\\ Fin Ecuaci\\'on\\\\"%converter.parser.convert(documentAndLists.displayList[index])
        #insert converted formulas
	newDocumentContent = iotools.stringtools.insertConvertedFormulas( newDocumentContent, documentAndLists.inlineList, documentAndLists.displayList)
	
	#Write the .tex file with the modified formulas
	iotools.iotools.replaceAndWrite(documentContent,newDocumentContent,os.path.join(filePath,'Accessible_'+name))
	iotools.iotools.convertToPdf(filePath ,os.path.join(filePath,'Accessible_'+name))
	#Write the trouble formulas
	iotools.iotools.writeTroubles(fileName, troubleFormulas)
#EndOfFunction
def convertFormula(strFormula,intOption = 1):

        converter.parser.setOption(intOption)
        return converter.parser.convert(strFormula)
#EndOfFunction


if __name__=='__main__':
	parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
	parser.add_argument('-e','--equation', dest='equation',
		help = 'Latex format equation to convert',
		default="")
	parser.add_argument('-o','--output', dest='document',
		action='store', help = '',
		default="")
	parser.add_argument('-a','--aux', dest='aux',
		action='store_true', help = 'wWith .aux document', default=False)
	parser.add_argument('-u','--unmacros', dest='undo',
		action='store_true', help = 'un-macros', default=False)
	parser.add_argument('-b','--browser', dest='browser',
		action='store_true', help ='open a browser', default=False)
	#parser.add_argument('-f','--file', dest='file',
	#	help = 'un-macrosized file',
	#	default="")
	#parser.add_argument('-t','--text', dest='text',
	#	help = 'text output',
	#	default="")
	#parser.add_argument('-p','--pdf', dest='pdf',
	#	help = 'PDF output',
	#	default="")
	args = parser.parse_args()
	format, aux, undo, browser = 0, "no", "no", "off"
	if args.aux:
		aux="yes"
	if args.undo:
		undo="yes"
	if args.browser:
		browser="on"
	if args.equation:
		print("Equation: ", converter.parser.convert(args.equation))
		print("Equation: ", args.equation)
	else:
		if args.document:
			print('Converting to xhtml...')
			convertDocument(args.document,format,aux,undo)
			if browser=="on":
				if os.name=='nt':
					browserOn=os.system('start firefox "'+ args.document[:-4]+'.xhtml"')
				else:
					browserOn=os.system('open -a  Safari "'+ args.document[:-4]+'.xhtml"')
				if browserOn==0:
					print("The document  is ready  on your browser.")
				else:
					print("I couldn't open your browser")
		#elif args.text:
		#	print('Converting to text...')
		#	convertDocument(args.document,format,aux,undo)
		#else:
		#	convertToPdf(args.pdf)

	if len(troubleFormulas)!=0:
		print(str(len(troubleFormulas)) + " formulas have had troubles!")
	else:
		print("No trouble formulas!")
#EndOfMain

