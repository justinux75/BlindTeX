#-*-:coding:utf-8-*-
#Parser

import ply.yacc as yacc
from converter.dictionary import *
from converter.lexer import tokens
import converter.lexer as lexer
import ply.lex
import converter.formulate as formulate
import os
import sys
import re
import copy
#TODO: Avoid this.
try:
    sys.path.insert(0, 'blindtex')
    from iotools.stringtools import reportProblem
except ValueError:
    from iotools.stringtools import reportProblem

#--------------------------------------------------------------------------
#Variables dirección del los json


#Lista de objetos diccionario:
dOrdinary = dictionary(os.path.join('converter','dicts','Ordinary.json'))
dLargeOperators = dictionary(os.path.join('converter','dicts','LargeOperators.json'))
dBinaryOperators = dictionary(os.path.join('converter','dicts','BinaryOperators.json'))
dBinaryRelations = dictionary(os.path.join('converter','dicts','BinaryRelations.json'))
dMathFunctions = dictionary(os.path.join('converter','dicts','MathFunctions.json'))
dArrows = dictionary(os.path.join('converter','dicts','Arrows.json'))
dDelimiters = dictionary(os.path.join('converter','dicts','Delimiters.json'))
dAccents = dictionary(os.path.join('converter','dicts','Accents.json'))
dStyles = dictionary(os.path.join('converter','dicts','Styles.json'))
dDots = dictionary(os.path.join('converter','dicts','Dots.json'))
dUser = dictionary(os.path.join('converter', 'dicts', 'UserDict.json'))
#-------------------------------------------------------------------------------
#TODO Find a way to avoid global variables.
OPTION = 1 #This option are for the formulate function. 0 is for span and &nbsp , 1 is for literal translation and 2 is for math and nbsp.

def getOption():
    '''Function to get the current value of OPTION.
        return(int): The value of OPTION'''
    return OPTION
    
def setOption(intOption):
    '''Function to change the value of OPTION.
        Args:
            intOption(int): The value the user wants for OPTION.'''
    global OPTION
    OPTION = intOption

#precedence=(
#('right','NUM'), ('right','SUP', 'SUB'),('left','SNUM')
#)
#-------------------------------------------------------------------------------
def p_start(p):
	'''start : formula
			| start formula'''
	if(len(p) == 2):
		p[0] = p[1]
	else:
		p[0] = p[1] + p[2]

def p_formula(p):
	'''formula : simple
				| block 
				| command
				| scriptable
				| shortscriptable'''
	p[0] = p[1] 

def p_block(p):
	'''block : BEGINBLOCK start ENDBLOCK'''
	p[0] = p[2]

def p_scriptable(p):
	'''scriptable : frac'''
	p[0] = p[1]

def p_shortscriptable(p):
	'''shortscriptable : style'''
	p[0] = p[1]
	
#This generates a shift reduce conflict.
def p_symBlock(p):
	'''symBlock  : BEGINBLOCK symbol ENDBLOCK
	|  BEGINBLOCK  ENDBLOCK '''
	if (len(p)==4):
		p[0] = p[2]
	else:
		p[0]=" "
def p_symbol(p):
	'''symbol : CHAR
	| NUM
			| VERT
			| DOLLAR
			| ord
			| symbLarOp
			| binOp
			| binRel
			| arrow
			| dots
			| delimiter
			| mathFunc
			| not
			| unknown
			| user
			| factorial
			| punctuation
			| lnbrk'''
	p[0] =  p[1] + ' '


def p_simple(p):
	'''simple : symbol 
			| symBlock  '''
	p[0] = p[1]

def p_commands(p):
	''' command : accent
				| pmod
				| phantom
				| mathop
				| 	root
				| combi
				| script
				| scrLarop 
				| lim
				| textBlock
				| label
				| array
				| col'''
	p[0] = p[1]

#---------------rules for symbols-----------------
def p_symbLarOp(p):
	'''symbLarOp : LARGEOP '''
	p[0] = formulate.formulate(dLargeOperators.showReading(p[1]), OPTION)

def p_ord(p):
	'''ord : ORD'''
	p[0] = formulate.formulate(dOrdinary.showReading(p[1]),OPTION)

def p_binOp(p):
    '''binOp : BINOP
                | KBINOP '''
    p[0] = formulate.formulate(dBinaryOperators.showReading(p[1]),OPTION)

def p_binRel(p):
    '''binRel : BINREL
                | KBINREL'''
    p[0] = formulate.formulate(dBinaryRelations.showReading(p[1]),OPTION)

def p_arrow(p):
    '''arrow : ARROW'''
    p[0] = formulate.formulate(dArrows.showReading(p[1]),OPTION)

def p_dots(p):
    '''dots : DOTS '''
    p[0] = formulate.formulate(dDots.showReading(p[1]),OPTION)

def p_delimiter(p):
    '''delimiter : DELIMITER
                    | KDELIMITER '''
    p[0] = formulate.formulate(dDelimiters.showReading(p[1]),OPTION)

def p_function(p):
    '''mathFunc : FUNC '''
    p[0] = formulate.formulate(dMathFunctions.showReading(p[1]),OPTION)

def p_not(p):
    '''not : NOT '''
    p[0]= formulate.formulate('no',OPTION)  

def p_unknown(p):
    '''unknown : UNKNOWN'''
    p[0] = formulate.formulate(p[1],OPTION)

def p_userCommand(p):
    '''user : USER'''
    p[0] = formulate.formulate(dUser.showReading(p[1]), OPTION)

def p_factorial(p):
    '''factorial : '!' '''
    p[0] = formulate.formulate('factorial',OPTION)

#def p_prime(p):
#    '''prime : "'" '''
#    p[0] = formulate.formulate('prima',OPTION)


def p_punctuation(p):
	'''punctuation : "'"
		| ','
		| '.'
		| ':'
		| ';'
		| '|'
		| '"' '''
	if p[1]=="'":
		p[0] = formulate.formulate('prima',OPTION)
	elif p[1]==',':
		p[0] = formulate.formulate('coma',OPTION)
	elif p[1]=='.':
		p[0] = formulate.formulate('punto',OPTION)
	elif p[1]==':':
		p[0] = formulate.formulate('dosPuntos',OPTION)
	elif p[1]==';':
		p[0] = formulate.formulate('puntoYcoma',OPTION)
	elif p[1]=='|':
		p[0] = formulate.formulate('lineaVertical',OPTION)
	else:
		p[0] = formulate.formulate('comillas',OPTION)

def p_linebreak(p):
    '''lnbrk : LINEBREAK'''
    p[0] = formulate.formulate('saltoDeL&iacute;nea',OPTION)

#-------------------------------Argument commands-------------------------------
def p_simpleAccent(p):
    '''accent : ACCENT simple'''
    p[0] = p[2].rstrip()+ formulate.formulate(dAccents.showReading(p[1]),OPTION).title()


def p_complexAccent(p):
    '''accent : ACCENT block'''
    p[0] = formulate.formulate(dAccents.showReading(p[1]),OPTION) + p[2] + formulate.formulate('fin' + dAccents.showReading(p[1]),OPTION,)

def p_style(p):
    '''style : STYLE simple'''
    p[0] =  p[2].rstrip() + formulate.formulate(dStyles.showReading(p[1]),OPTION).title()

def p_complexStyle(p):
    '''style : STYLE block '''
    p[0] = formulate.formulate(dStyles.showReading(p[1]),OPTION) + p[2] + formulate.formulate('fin' + dStyles.showReading(p[1]),OPTION)

def p_pmod(p):
    '''pmod : PMOD simple'''
    p[0] = formulate.formulate('m&oacute;dulo',OPTION) + p[2]

def p_complexPmod(p):
    '''pmod : PMOD block'''
    p[0] = formulate.formulate('m&oacute;dulo', OPTION) + p[2] + formulate.formulate('finMod', OPTION)

def p_phantom(p):
    '''phantom : PHANTOM simple
                | PHANTOM block'''
    p[0] = ''

def p_mathop(p):
    '''mathop : MATHOP simple
    | MATHOP block 
    | MATHOP simple mathopScript
                | MATHOP block mathopScript'''
    if len(p) >3:
        p[0] = p[2] + p[3]
    else:
        p[0]= p[2]
        


def p_mathopScript(p):
	'''mathopScript : smathopScript
			| cmathopScript
			| sbmathopScript '''
	p[0] = p[1]

def p_smathopScript(p):
	'''smathopScript : SUP simple
				| SUB simple 
				| SUB shortscriptable
				| SUP shortscriptable'''
	if(p[1] == '^'):
		p[0] = formulate.formulate('arriba', OPTION) + p[2] + formulate.formulate(' ',OPTION)
	else:
		p[0] = formulate.formulate('abajo', OPTION) + p[2]+formulate.formulate(' ',OPTION) 

def p_sbmathopScript(p):
	'''sbmathopScript : SUP block
				| SUB block
				| SUP scriptable
				|  SUB scriptable '''
	if(p[1] == '^'):
		p[0] = formulate.formulate('encima', OPTION) + p[2] + formulate.formulate('finEncima',OPTION)
	else:
		p[0] = formulate.formulate('debajo', OPTION) + p[2] + formulate.formulate('finDebajo',OPTION)


def p_cmathopScript(p):
	'''cmathopScript : SUP simple SUB simple
				| SUP simple SUB block
				| SUP block SUB simple
				| SUP block SUB block
				| SUB simple SUP simple
				| SUB simple SUP block
				| SUB block SUP simple
				| SUB block SUP block 
				| SUB scriptable SUP simple
				| SUB simple SUP scriptable
				| SUB scriptable SUP block
				| SUB block SUP scriptable
				| SUB scriptable SUP scriptable
				| SUB shortscriptable SUP simple
				| SUB simple SUP shortscriptable
				| SUB shortscriptable SUP block
				| SUB block SUP shortscriptable
				| SUB scriptable SUP shortscriptable
				| SUB shortscriptable SUP scriptable
				| SUB shortscriptable SUP shortscriptable '''
	if(p[1] =='^'):
		p[0] = formulate.formulate('encima',OPTION) + p[2] + formulate.formulate('yDebajo',OPTION) + p[4] + formulate.formulate('finDebajo',OPTION)
	else:
		p[0] = formulate.formulate('debajo',OPTION) + p[2] +  formulate.formulate('yEncima',OPTION) + p[4] + formulate.formulate('finEncima',OPTION)





def p_root(p):
    '''root : ROOT simple
            | ROOT KDELIMITER start KDELIMITER simple '''#Conflicts here
    if(len(p) == 3):
        p[0] = formulate.formulate('ra&iacute;zcuadradade',OPTION) + p[2]
    else:
        p[0] = formulate.formulate('ra&iacute;z',OPTION) + p[3] + formulate.formulate('de',OPTION) + p[5]

def p_complexRoot(p):
    '''root :  ROOT block
            | ROOT KDELIMITER start KDELIMITER block '''#Conflicts here
    if(len(p) == 3):
        p[0] = formulate.formulate('ra&iacute;zCuadradaDe',OPTION) + p[2] + formulate.formulate('terminaRa&iacute;z',OPTION)
    else:
        p[0] = formulate.formulate('ra&iacute;z',OPTION) + p[3] + formulate.formulate('de',OPTION) + p[5] + formulate.formulate('terminaRa&iacute;z',OPTION)

def p_frac(p):
    '''frac : FRAC simple  simple'''
    p[0] = p[2] + formulate.formulate('sobre',OPTION) + p[3] + formulate.formulate(' ',OPTION)

def p_cFrac(p):
	'''frac : FRAC block block
			| FRAC simple block
			| FRAC block simple '''
	p[0] = formulate.formulate('comienzaFracci&oacute;n',OPTION) + p[2] + formulate.formulate('sobre',OPTION) + p[3] + formulate.formulate('finFracci&oacute;n',OPTION)

def p_combi(p):
    '''combi : choose
            | binom '''
    p[0] = p[1]

def p_choose(p):
    '''choose : simple CHOOSE simple'''
    p[0] = formulate.formulate('combinacionesDe', OPTION) + p[1] + formulate.formulate('en',OPTION) + p[3]

def p_cChoose(p):
	'''choose : simple CHOOSE block
			| block CHOOSE block
			| block CHOOSE simple '''
	p[0] = formulate.formulate('combinacionesDe', OPTION) + p[1] + formulate.formulate('en',OPTION) + p[3] + formulate.formulate('finCombinaci&oacute;n',OPTION)
def p_binom(p):
    '''binom : BINOM simple simple''' 
    p[0] = formulate.formulate('combinacionesDe', OPTION) + p[2] + formulate.formulate('en',OPTION) + p[3]

def p_cBinom(p):
	'''binom : BINOM simple block
			| BINOM block block 
            | BINOM block simple '''
	p[0] = formulate.formulate('combinacionesDe', OPTION) + p[2] + formulate.formulate('en',OPTION) + p[3] + formulate.formulate('finCombinaci&oacute;n',OPTION)


def p_script(p):
	'''script : sScript
			| cScript
			| sbScript '''
	p[0] = p[1]

def p_sScript(p):
	'''sScript : SUP simple
				| SUB simple 
				| SUB shortscriptable
				| SUP shortscriptable'''
	if(p[1] == '^'):
		p[0] = formulate.formulate('supra', OPTION) + p[2]+formulate.formulate(' ',OPTION) 
	else:
		p[0] = formulate.formulate('sub', OPTION) + p[2]+formulate.formulate(' ',OPTION) 

def p_sbScript(p):
	'''sbScript : SUP block
				| SUB block
				| SUP scriptable
				|  SUB scriptable '''
	if(p[1] == '^'):
		p[0] = formulate.formulate('s&uacute;per', OPTION) + p[2] + formulate.formulate('finS&uacute;per',OPTION)
	else:
		p[0] = formulate.formulate('abreSub', OPTION) + p[2] + formulate.formulate('finSub',OPTION)


def p_cScript(p):
	'''cScript : SUP simple SUB simple
				| SUP simple SUB block
				| SUP block SUB simple
				| SUP block SUB block
				| SUB simple SUP simple
				| SUB simple SUP block
				| SUB block SUP simple
				| SUB block SUP block 
				| SUB scriptable SUP simple
				| SUB simple SUP scriptable
				| SUB scriptable SUP block
				| SUB block SUP scriptable
				| SUB scriptable SUP scriptable
				| SUB shortscriptable SUP simple
				| SUB simple SUP shortscriptable
				| SUB shortscriptable SUP block
				| SUB block SUP shortscriptable
				| SUB scriptable SUP shortscriptable
				| SUB shortscriptable SUP scriptable
				| SUB shortscriptable SUP shortscriptable
				| SUP scriptable SUB simple
				| SUP simple SUB scriptable
				| SUP scriptable SUB block
				| SUP block SUB scriptable
				| SUP scriptable SUB scriptable
				| SUP shortscriptable SUB simple
				| SUP simple SUB shortscriptable
				| SUP shortscriptable SUB block
				| SUP block SUB shortscriptable
				| SUP scriptable SUB shortscriptable
				| SUP shortscriptable SUB scriptable
				| SUP shortscriptable SUB shortscriptable '''
	if(p[1] =='^'):
		p[0] = formulate.formulate('s&uacute;per',OPTION) + p[2] + formulate.formulate('finS&uacute;per',OPTION) + formulate.formulate('sub',OPTION) + p[4] + formulate.formulate('finSub',OPTION)
	else:
		p[0] = formulate.formulate('sub',OPTION) + p[2] + formulate.formulate('finSub',OPTION) + formulate.formulate('s&uacute;per',OPTION) + p[4] + formulate.formulate('finS&uacute;per',OPTION)
	
def p_scrLarop(p):
	'''scrLarop : LARGEOP sLaropScript
				| LARGEOP cLaropScript '''
	p[0] = formulate.formulate(dLargeOperators.showReading(p[1]),OPTION) + p[2] + formulate.formulate('de',OPTION)


def p_cLaripScript(p):
	'''cLaropScript : SUP simple SUB simple
				| SUP simple SUB block
				| SUP block SUB simple
				| SUP block SUB block
				| SUB simple SUP simple
				| SUB simple SUP block
				| SUB block SUP simple
				| SUB block SUP block
				| SUB scriptable SUP simple
				| SUB simple SUP scriptable
				| SUB scriptable SUP block
				| SUB block SUP scriptable
				| SUB scriptable SUP scriptable
				| SUB shortscriptable SUP simple
				| SUB simple SUP shortscriptable
				| SUB shortscriptable SUP block
				| SUB block SUP shortscriptable
				| SUB scriptable SUP shortscriptable
				| SUB shortscriptable SUP scriptable
				| SUB shortscriptable SUP shortscriptable 
				| SUP scriptable SUB simple
				| SUP simple SUB scriptable
				| SUP scriptable SUB block
				| SUP block SUB scriptable
				| SUP scriptable SUB scriptable
				| SUP shortscriptable SUB simple
				| SUP simple SUB shortscriptable
				| SUP shortscriptable SUB block
				| SUP block SUB shortscriptable
				| SUP scriptable SUB shortscriptable
				| SUP shortscriptable SUB scriptable
				| SUP shortscriptable SUB shortscriptable '''
	if(p[1] =='^'):
		p[0] = formulate.formulate('desde',OPTION) + p[4] + formulate.formulate('hasta',OPTION) + p[2] 
	else:
		p[0] = formulate.formulate('desde',OPTION) + p[2] + formulate.formulate('hasta',OPTION) + p[4]

def p_sLaropScript(p):
	''' sLaropScript : SUP simple
					| SUB simple
					| SUP shortscriptable
					| SUB shortscriptable
					| SUP block
					| SUB block
					| SUP scriptable
					| SUB scriptable '''
	if(p[1] =='^'):
		p[0] = formulate.formulate('hasta',OPTION) + p[2] 
	else:
		p[0] = formulate.formulate('sobre',OPTION) + p[2]
	

def p_lim(p):
    '''lim : LIM
            | LIM limScript'''
    if(len(p) == 3):
        p[0] = formulate.formulate('l&iacute;mitePara',OPTION) + p[2] + formulate.formulate('de',OPTION)
    else:
        p[0] = formulate.formulate('l&iacute;miteDe',OPTION)

def p_limScript(p):
	'''limScript : SUB simple
				| SUB block
				| SUB shortscriptable
				| SUB scriptable '''
	p[0] = p[2]

def p_textBlock(p):
    '''textBlock : TEXT any '''
    p[0] = formulate.formulate(' ',OPTION) + p[2] + formulate.formulate(' ', OPTION)

def p_sBlock(p):
	''' block : BEGINBLOCK SSTYLE any '''
	if  p[2]=="bf":
		p[0] = p[3] + formulate.formulate('Negrita', OPTION)
	elif p[2]=="cal":
			p[0] =  p[3] + formulate.formulate('Caligr&aacute;fica', OPTION)
	else:
		p[0] = formulate.formulate(' ',OPTION) + p[3] + formulate.formulate(' ', OPTION)



def p_label(p):
    '''label : LABEL any '''
    p[0] = formulate.formulateLabel(p[2], OPTION)

def p_ARRAYTEXT(p):
    '''textBlock : ARRAYTEXT any'''
    p[0] = p[2] + ' '

def p_any(p):
    '''any : ANYTHING
            | ANYTHING any'''
    if(len(p) == 3):
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_array(p):
    '''array : BEGARRAY arrayContent ENDARRAY '''
    if p[1]=="begin{cases}":
        p[0] = formulate.formulate('definidoEnCasos\n', OPTION) + p[2] + formulate.formulate('finCasos\n', OPTION)
    else:
        p[0] = formulate.formulate('Arreglo\n', OPTION) + p[2] + formulate.formulate('finArreglo\n', OPTION)



def p_arrayContent(p):
    '''arrayContent : start'''
    p[0] = p[1]

#
def p_col(p):
    '''col : COL'''
    p[0] = ''


def p_number(p):
	''' number : NUM NUM
	| number NUM'''
	if (len(p)==2):
		p[0]=p[1]
	else:
		p[0]=p[1]+p[2]
def  p_simple_number(p):
	'''simple : BEGINBLOCK number ENDBLOCK'''
	p[0]= p[2]
def p_number_formula(p):
	''' formula : number '''
	p[0]=p[1] + " "
 
#----------------------------Error Handling------------------------------------
class syntaxError(Exception):
        def __init__(self):
                pass
                
def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        raise syntaxError
        parser.errok()
    else:
        print("Syntax error at EOF")
        raise syntaxError

#-------------------------------------------------------------------------------    

parser = yacc.yacc()
arrayRegex = re.compile(r'''((?<!\\)((\\begin\{array\}(\{.*?\})?)))
(.*?)
(?<!\\)(\\end\{array\})|
((?<!\\)\\begin\{[pbBvV]?matrix(\*)?\}(\[.*?\])?(\{.*?\})?)
(.*?)
((?<!\\)\\end\{[pbBvV]?matrix(\*)?\})''',re.DOTALL|re.UNICODE|re.X)
#Be careful with these constants, if you change the arrayRegex they could change.
ARRAY_CONTENT_GROUP = 5
MATRIX_CONTENT_GROUP = 11
def convert(String):
        newString = seekAndReplaceMatrices(String)
        try:
                return parser.parse(newString)
        except ply.lex.LexError:
            reportProblem('LexError in:\n'+newString)
            return('Bad Formula')
        except syntaxError:
            reportProblem('Syntax Error in:\n' + newString)
            return('Bad Formula')
        except lexer.illegalCharacter:
            reportProblem('illegal character in:\n' +newString)
            return('Bad Formula')
#EndOfFunction

def seekAndReplaceMatrices(String):

    otherString = copy.deepcopy(String)
    iterator = arrayRegex.finditer(otherString)
    while(True):
        try:
            currentMatch = next(iterator)
            if(currentMatch.group(ARRAY_CONTENT_GROUP) != None):
                GROUP = ARRAY_CONTENT_GROUP
            elif(currentMatch.group(MATRIX_CONTENT_GROUP) != None):
                GROUP = MATRIX_CONTENT_GROUP
            #Else, why are you here?
            arrayStringContent = currentMatch.group(GROUP)
            arrayRows = arrayStringContent.split(r'\\')
            myArray =[]
            for row in arrayRows:
                myArray.append(row.split('&'))
            curRow = 1
            curCol = 1
            newContent = ''
            for row in myArray:
                for col in row:
                    newContent = newContent + r'~text{Elemento%da%da;}'%(curRow, curCol) + col + ';'
                    curCol = curCol + 1
                curCol = 1
                curRow = curRow +1
            
            otherString = otherString.replace(currentMatch.group(GROUP), newContent)

        except StopIteration:
            break
    return otherString
#EndOFunction
