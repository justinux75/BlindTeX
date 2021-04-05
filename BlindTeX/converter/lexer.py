#-*-:coding:utf-8-*-
#Lexer of LaTeX math content

import ply.lex as lex
from ply.lex import TOKEN
import json
import re
import os
import sys

tokens = ('CHAR', 'SUP', 'SUB','BEGINBLOCK','ENDBLOCK', 'ORD', 'FRAC', 'ROOT', 'LARGEOP',
          'BINOP','KBINOP','KBINREL', 'BINREL', 'NOT', 'FUNC', 'ARROW', 'KDELIMITER', 'DELIMITER',
          'ACCENT','STYLE','DOTS','LIM', 'UNKNOWN', 'BEGARRAY', 'ENDARRAY', 'LINEBREAK', "VERT", "DOLLAR", 'COL','CHOOSE',
          'BINOM', 'PMOD','PHANTOM','MATHOP','SSTYLE','TEXT','LABEL','ANYTHING','ARRAYTEXT', 'USER', 'NUM')

states = (('command', 'exclusive'), ('anything', 'exclusive'), )
      
try:
         myFile = open(os.path.join("converter",'dicts','regexes.json'), 'r')
         dictOfDicts = json.load(myFile)
         myFile.close()
except IOError:
        print('File could not be oppened.')
#def commandEnding(cadena):
# lista=cadena.split("|")
# for k in range(len(lista)):
#  lista[k]=lista[k]+r"[^a-zA-Z]"
# return "|".join(lista)
dictOfDictsExt={}
for k in dictOfDicts.keys():
 dictOfDictsExt[k]=r"("+dictOfDicts[k]+r")(?![a-zA-Z])"
dictOfDictsExt["Delimiters"]="({|})|("+dictOfDictsExt["Delimiters"]+")"

literals = [ '!',"'", '.', ',', ':', ';', '"', '|', ]


t_BEGINBLOCK = r'\{'

t_ENDBLOCK= r'\}'

t_SUP = r'\^'

t_SUB = r'_'


def t_COMMENTS(t):
	r'%(.)*'





	
def t_COMMAND(t):
	r'\\'
	t.lexer.begin('command')
	return

def t_command_ignore_mathstyle(t):
	r'(textstyle|displaystyle)'
	t.lexer.begin('INITIAL')
	pass



@TOKEN(dictOfDictsExt['UserDict'])
def t_command_USER(t):
	
	t.lexer.begin('INITIAL')
	return t



def t_command_PMOD(t):
	r'pmod'
	t.lexer.begin('INITIAL')
	return t

def t_command_PHANTOM(t):
	r'([hv]?phantom)|([hv]space(\*)?)'
	t.lexer.begin('INITIAL')
	return t

def t_command_MATHOP(t):
	r'mathop'
	t.lexer.begin('INITIAL')
	return t



def t_command_BEGARRAY(t):
	r'(begin\{array\}|begin\{cases\}|begin\{[pbBvV]?matrix(\*)?\})(\[.*?\])?(\{.*?\})?'
	t.lexer.begin('INITIAL')
	return t




def t_command_ENDARRAY(t):
	r'end\{array\}|end\{cases\}|end\{[pbBvV]?matrix(\*)?\}'
	t.lexer.begin('INITIAL')
	return t

def t_command_LINEBREAK(t):
	r'\\'
	t.lexer.begin('INITIAL')
	return t


def t_command_VERT(t):
	r'\|'
	t.lexer.begin('INITIAL')
	return t


def t_COL(t):
	r'[&]'
	return t




@TOKEN(dictOfDictsExt['LargeOperators'])
def t_command_LARGEOP(t):
	
	t.lexer.begin('INITIAL')
	return t

@TOKEN(dictOfDictsExt['Ordinary'])
def t_command_ORD(t):
	
	t.lexer.begin('INITIAL')
	return t

def t_command_FRAC(t):
	r'frac|tfrac|dfrac'
	t.lexer.begin('INITIAL')
	return t

def t_command_ROOT(t):
	r'sqrt'
	t.lexer.begin('INITIAL')
	return t

@TOKEN(dictOfDictsExt['Arrows'])
def t_command_ARROW(t):
	
	t.lexer.begin('INITIAL')
	return t

def t_command_leftRight(t):
	r'((left|right|bigl|bigr)(?![a-zA-Z\.]))|left\.|right\.'
	t.lexer.begin('INITIAL')
	pass
#Binary operators that can be made from the keyboard.
t_KBINOP = r'\+|-|\*|/'

@TOKEN(dictOfDictsExt['Dots'])
def t_command_DOTS(t):
	
	t.lexer.begin('INITIAL')
	return t

@TOKEN(dictOfDictsExt['BinaryOperators'])	
def t_command_BINOP(t):
	
	t.lexer.begin('INITIAL')
	return t


def t_KBINREL(t):
	r'[=<>]'	
	t.lexer.begin('INITIAL')
	return t

@TOKEN(dictOfDictsExt['BinaryRelations'])
def t_command_BINREL(t):
		
	t.lexer.begin('INITIAL')
	return t

@TOKEN(dictOfDictsExt['MathFunctions'])
def t_command_FUNC(t):
	
	t.lexer.begin('INITIAL')
	return t

def t_command_NOT(t):
	r'not'
	t.lexer.begin('INITIAL')
	return t

def t_KDELIMITER(t):
	r'\(|\)|\[|\]'
	return t


@TOKEN(dictOfDictsExt['Delimiters'])
def t_command_DELIMITER(t):
	
	t.lexer.begin('INITIAL')
	return t

@TOKEN(dictOfDictsExt['Accents'])
def t_command_ACCENT(t):

	t.lexer.begin('INITIAL')
	return t

@TOKEN(dictOfDictsExt['Styles'])
def t_command_STYLE(t):
	
	t.lexer.begin('INITIAL')
	return t

def t_command_LIM(t):
	r'lim'
	t.lexer.begin('INITIAL')
	return t

def t_command_CHOOSE(t):
	r'choose'
	t.lexer.begin('INITIAL')
	return t

def t_command_BINOM(t):
	r'binom'
	t.lexer.begin('INITIAL')
	return t

def t_command_MATHSPACE(t):
	r'[,!:; /\n]|quad|qquad'
	t.lexer.begin('INITIAL')
	pass

def t_command_DOLLAR(t):
	r'\$'
	t.lexer.begin('INITIAL')
	return t

# some user's macros have the symbol of dollar to work in math mode as in text mode.
# Hence, if using a un-macros script it is needed to ignore  the symbol. 
def t_ignore_dollar(t):
	r'\$'
	t.lexer.begin('INITIAL')
	pass
def t_command_SSTYLE(t):
	r'(rm|bf|cal|tt) '
	t.lexer.begin('anything')
	return t


		

def t_command_TEXT(t):
        r'((text(rm)?)|mbox|hbox)\{'
        t.lexer.begin('anything')
        return t

def t_command_LABEL(t):
        r'label\{'
        t.lexer.begin('anything')
        return t
def t_ARRAYTEXT(t):
        r'~text\{'
        t.lexer.begin('anything')
        return t


def t_anything_ANYTHING(t):
        r'[^\}]'
        return t
def t_anything_ignore_commands(t):
		r"\\([a-zA-Z])+ "
		pass
def t_anything_ENDANY(t):
        r'(?<!\\)\}'
        t.lexer.begin('INITIAL')
        pass
        
def t_blank(t):
	r'~'
#	return t

def t_CHAR(t):
	r'[A-Za-z]+?'
	return t
	

def t_NUM(t):
        r'[0-9]'
        return t


def t_command_UNKNOWN(t):
	r'[A-Za-z]+'
	t.lexer.begin('INITIAL')
	return t

t_ignore_SPACE=r'[ \t\n]+'
#---------------Error Handling-----------------
class illegalCharacter(Exception):
        def __init__(self):
                return
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	raise illegalCharacter

#---------------------------------------------
lexer= lex.lex()

if __name__ =="__main__":
	while True:
		s = raw_input()
		lexer.input(s)
		while True:
			tok = lexer.token()
			if not tok:
				break
			print(tok)
