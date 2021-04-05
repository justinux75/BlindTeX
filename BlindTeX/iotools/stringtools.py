#-*-:coding:utf-8-*-

import re
import string
import collections
import copy
#import blindtex.converter.parser 

#Regular expression to match anything in math mode. Altough there are better regex to do the same, this allows add new options easily.
#If you want to proove it before,  you can do it in https://regex101.com/r/dSxw4f/2/
#TODO The repetition of code is a signal it can be made in a more elegant way.

inlineMath = re.compile(r'''(?<!\\)( #Exclude escaped symbols
								((\$)(.*?)(?<!\\)(\$))| #Single $ formulas
								((\\\()(.*?)(?<!\\)(\\\))) #\(
							)''', re.DOTALL|re.UNICODE|re.X)
displayMath = re.compile(r'''(?<!\\)( #Exclude escaped symbols
										((\${2})(.*?)(?<!\\)(\${2}))| #Identify double $ formulas
										((\\\[)(.*?)(?<!\\)(\\\]))| #\[
										((\\begin\{equation\})(.*?)(?<!\\)(\\end\{equation\}))|
										((\\begin\{equation\*\})(.*?)(?<!\\)(\\end\{equation\*\}))| #begin equation with and without *
										((\\begin\{align\})(.*?)(?<!\\)(\\end\{align\}))|
										((\\begin\{align\*\})(.*?)(?<!\\)(\\end\{align\*\}))| # align and align*
										((\\begin\{flalign\})(.*?)(?<!\\)(\\end\{flalign\}))| 
										((\\begin\{flalign*\})(.*?)(?<!\\)(\\end\{flalign*\}))| # flalign and flalign*
										((\\begin\{eqnarray\})(.*?)(?<!\\)(\\end\{eqnarray\}))|
										((\\begin\{eqnarray\*\})(.*?)(?<!\\)(\\end\{eqnarray\*\})) #eqnarray and eqnarray*
									)''',re.DOTALL|re.UNICODE|re.X)


#Label regex
label = re.compile(r'\\label\{(.*?)\}',re.DOTALL|re.UNICODE|re.X)
newLabel = re.compile(r'\\newlabel\{(.*?)\}\{\{(.*?)\}\{(.*?)\}',re.DOTALL|re.UNICODE|re.X)
#List of possible equation delimiters.
delimiters = [r'\(', r'\)', r'\[', r'\]', r'\begin{equation}',r'\begin{equation*}',r'\begin{align}',r'\begin{align*}',r'\begin{flalign}', r'\end{flalign}', r'\begin{flalign*}', r'\end{flalign*}', r'\end{equation}',r'\end{equation*}',r'\end{align}',r'\end{align*}',r'\begin{eqnarray}', r'\begin{eqnarray*}', r'\end{eqnarray}', r'\end{eqnarray*}',]
#Strings to replace the found formulas.
inlineMathString = "(inlineLaTeXStringNumber%d)"
displayMathString = "(displayLaTeXStringNumber%d)"

#Auxiliar function to be used in seekAndReplaceFormulas to clean the equation from the delimiters.
def cleanDelimiters(equation):
	'''This method clean a string from the possible LaTeX equation delimiters to avoid future conflicts.
		Args:
			equation(str): The LaTeX equation.
		Returns
			str: The same equation without the delimiters in the delimiters list. '''
	newEquation = equation
	if(newEquation[0] == '$'):
	#This part is for the case with delimiters $ or $$, since in the equation could be a \$ we did this to avoid cleaning those to.
		newEquation = newEquation[1:len(newEquation)-1]
		#Already cleaned the first and last $ if there is other we pass the cleaner again.
		return cleanDelimiters(newEquation)
	else:
		for delim in delimiters:
			newEquation = newEquation.replace(delim, '')
		return newEquation
		
#EndOfFunction

#Function to separate the document from the preamble(LaTeX formating) and the information after the document.
#It returns an array of strings with the parts.
def extractContent(completeDocument):
    '''The method takes a string representing a LaTeX document and separates its preamble (the portion before "\\begin{document}"), its content and its epilogue (after \\end{document}) and returns them in a list.
        Args:
            completeDocument(str): The LaTeX document as a string.
        Returns:
            list[str,str,str]: A list of three strings, the first one the portion before \\begin{document}(inclusive), the second one the document, the last one the part after \\end{document}.'''
    
    preamble = ""
    document = ""
    epilogue = ""

    try:
        preamble = completeDocument[:completeDocument.index(r'\begin{document}')]
        document = completeDocument[completeDocument.index(r'\begin{document}'): completeDocument.index(r'\end{document}')+ len(r'\end{document}')]
        epilogue = completeDocument[completeDocument.index(r'\end{document}')+ len(r'\end{document}'):]
    except ValueError:
        print("\\begin{document} or \end{document} not found.\n")
    return [preamble, document, epilogue]
#EndOfFunction

#HU2 HU8 HU3
#Function to find all the math in the document, copy then in a file and replace then by  markers.
#The input is a strign with the document content, and a string with a name of the file where all the math will be writen.
def seekAndReplaceFormulas(document):
	'''Search for all the math formulas in the document, when one is found first, the function copies the formula in a list; then the function replace the formula for a marker to future uses.
		Args:
			document(str): the LaTeX content.
		Returns:
			namedTuple:A named Tuple called documentAndLists where:
						replacedDocument is the string with all the formulas replaced by markers.
						inline/displayList  is the list with all the inline/display formulas found.'''
	
	otherDocument = copy.deepcopy(document)

	displayIterator = displayMath.finditer(otherDocument)
	displayIndex = 0
	displayList =[]

	while(True):
		try:
			currentMatch = next(displayIterator)
			otherDocument = otherDocument.replace(currentMatch.group(0), displayMathString%(displayIndex),1)
			currentMatch = cleanDelimiters(currentMatch.group(0))+" " #The blank space at the end is for tokenization purposes.
			displayList.append(currentMatch)
			displayIndex += 1
		except StopIteration:
			break

	inlineIterator = inlineMath.finditer(otherDocument)
	inlineIndex = 0 #Index to keep track of which equation is being replaced.
	inlineList = []
	
	while(True):
		try:
			currentMatch = next(inlineIterator)
			otherDocument = otherDocument.replace(currentMatch.group(0), inlineMathString%(inlineIndex), 1)
			currentMatch = cleanDelimiters(currentMatch.group(0))+" " #The blank space at the end is for tokenization purposes.
			inlineList.append(currentMatch)
			inlineIndex += 1
		except StopIteration:
			break

	

	return collections.namedtuple('documentAndLists', 'replacedDocument, inlineList, displayList')(otherDocument, inlineList, displayList)
#EndOfFunction



#HU2 HU8 HU3
#Function to find all the math labels  in the auxiliary  document.
#The input is a strign with the aux document content.
def seekLabels(document):
	'''Search for all the equation labels  in the aux document, the result is a  dictionary with  the labels as its keys and numbers of equations as its values.
		Args:
			document(str): the aux    content.
		Returns:
			labelDictionary:A dictionary where:
						labels are the keys and  its corresponding number are its values.'''
	
	newLabelIterator = newLabel.finditer(document)
	labelDictionary = {}
	
	while(True):
		try:
			currentMatch = next(newLabelIterator)
			labelDictionary[str(currentMatch.group(1))]=str(currentMatch.group(2))
		except StopIteration:
			break

	

	return labelDictionary
#EndOfFunction



#HU6
#Insert all the LaTeX formulas in the file formulaFile, already converted, the replacement is done in order of appearance with the marker put before.
def insertConvertedFormulas(htmlString, inlineList, displayList,format=0):
	'''Insert all the LaTeX formulas in the lists, already converted, the replacement is done in order of appearance with the marker put before.
		Args:
			htmlString(str): the html document, product of the conversion from LaTeX to html.
			inlineList(str): the list with all the inline formulas written in LaTeX.
			displayList(str): the list with all the  display formulas written in LaTeX.
			format(int): this option indicates the begining and the end of the formula
				 suitable for each format. 0 and 2  for html,1for txt and 3 for tex
		Returns:
			str: the html document but with all the formulas inserted. '''
	if format==1:
		BEGINFORMAT=""
		ENDFORMAT=""
	elif format==3:
		BEGINFORMAT="%eqn: "
		ENDFORMAT=""
	else:
		BEGINFORMAT='\n<div> <p>'
		ENDFORMAT='</p></div>\n'
	
	output = ""	
	newString = copy.deepcopy(htmlString)
	inlineIndex = 0
	for line in inlineList:
		output = newString.replace(inlineMathString%(inlineIndex), (line) )
		newString = output
		inlineIndex += 1
	
	output = ""
	displayIndex = 0
	for line in displayList:
		output = newString.replace(displayMathString%(displayIndex),(BEGINFORMAT+line+ENDFORMAT) )
		newString = output
		displayIndex += 1
	
	return newString
#EndOfFunction

#This list contains all the trouble formulas. ¿Is there a way to avoid the global variable?
#TODO: Distinguish between file convertion and unique formula convertion.
troubleFormulas =[]
def reportProblem(strBadFormula):
        '''This function gathers all the formulas the lexer or parser had problems with and then send it to being writed in a file.
                Args:
                        strBadFormula(str): The guilty string. Sended by Parser.'''
        global troubleFormulas
        troubleFormulas.append(strBadFormula)

#EndOfFunction

def generateListOfLabels(listDisplay):
        '''Searchs all the labels and puts them in a list to be look for the references later.
                Args:
                        listDisplay(list(str)): A list with all the display formulas.
                Returns:
                        (list(str)): A list with all the labels found.'''
        labelList =[]
        for formula in listDisplay:
                if(label.search(formula)):
                        labelList.append(label.search(formula).group(1))
                else:
                        continue

        return labelList

#EndOfFunction
def generateLabelsDict(auxiliarDocumentString, labelsList):
	"""This function builds a dictionary with keys the labels  of the display formulas in the document and 
		values the number  that LaTeX asigns, which is taken from the newlist command in the .aux 
		document 
		that LaTeX generates when compiling
			Args:
				auxiliarDocumentString (str): the content of the .aux document.
				labelsList (lst): the list of labels of display formulas in the .tex document"""
	labelsDict={}
	newLabelsDict=seekLabels(auxiliarDocumentString)
	for label in labelsList:
		if label in newLabelsDict.keys():
			labelsDict[label]=newLabelsDict[label]
		else:
			labelsDict[label]=label
	return labelsDict
# END of FUNCTION
        
def replaceRefs(stringDocument, listLabels):
        '''Replaces the references in the document for easy to find flags.
                Args:
                        stringDocument(str): The document to look for.
                        listLabels(list(str)): The list with all the labels found.
                Returns:
                        (str):The document with all the references replaced.'''
        replacedDocument = copy.deepcopy(stringDocument)
        output =""
        for label in listLabels:
                output = replacedDocument.replace('\\ref{'+label+'}', '(refTo:'+label+')')
                replacedDocument = output


        return replacedDocument
#EndOfFunction

def replaceLabels(stringDocument, dictLabels):
        '''Replaces the labels of the math equations in the document with the numbering and the html id, for hyperreference.  
                Args:
                        stringDocument(str): The document to look for.
                        dictLabels(dictionary(str)): The dictionary  with all the labels as keys and  numbering as values.
                Returns:
                        (str):The document with all the labels replaced.'''
        replacedDocument = copy.deepcopy(stringDocument)
        output =""
        for label in dictLabels.keys():
                output = replacedDocument.replace('label: '+label, '<a tabindex="0" href="'+label+'" aria-label="Ecuaci&oacute;n '+str(dictLabels[label])+'"><span id="'+label+'">  Ecuaci&oacute;n '+str(dictLabels[label])+'</span></a>')
                replacedDocument = output


        return replacedDocument
#EndOfFunction



def insertReferences(stringDocument, dictLabels):
        '''Inserts the references changed in the  document.
                Args:
                        stringDocument(str):The document whre the replacement will be done.
                        dictLabels(dict(str)): The dict with  the labels   in the formulas as keys and its numbers as the values.
                Returns
                        (str): The document with all the references inserted.'''
        replacedDocument = copy.deepcopy(stringDocument)
        output = ""
        for label in dictLabels.keys():
                output = replacedDocument.replace('(refTo:'+label+')','<a tabindex="0" href="#'+label+'" aria-label="'+dictLabels[label]+'">r</a>')
                replacedDocument = output


        return replacedDocument
#EndOfFunction
        

