#!/usr/bin/env python
#-*-coding:utf-8-*-
import re
from sys import argv
## Esta funcion recibe una cadena, y retorna  lo que se encuentra entre llaves
## (dl, dr), salvo si vienen precedidas por el simbolo \
## La funcion busca a partir de la posicion "start" e ignora 
## los espacios en blanco antes de la primera llave.
## la salida es una lista con dos items: el primero 
## es el propio argumento y el segundo es la parte de la cadena
## desde la posicion start hasta el final del argumento, incluyendo la llave final.
def entreLlaves(cadena,start=0,dl="{",dr="}"):
 longitud=len(cadena[start:])
 contador=0
 letra=cadena[start]
 letraAnt=""
 nivel=0
 nivelAnt=0
 argumento=""
 while not(letra==dr and letraAnt!="\\" and nivel==1):
  if (letra==dl and letraAnt!="\\"):
   nivel+=1
   if nivel>1:
    argumento+=letra
   else:
    pass
  elif (letra==dr and letraAnt!="\\"):
   nivel-=1
   if nivel!=0:
    argumento+=letra
   else:
    pass
  elif (letra==" " and nivel==0):
   pass
  elif ((letra!=" " or letra!=dl) and nivel==0):
   break
  else:
   argumento+=letra
  letraAnt=letra
  if longitud> contador+1:
   contador+=1
   letra=cadena[start+contador]
  else:
   break
 return [argumento,cadena[start:start+contador+1]]

#END of function
## La funcion comando toma una cadena y un entero start, y busca
## en la cadena a partir de la posicion start un patron que comienza con barraInvertida
## precediendo a una cadena de letras. La funcion
## devuelve una lista con dos items: el primero  es 
## el comando encontrado, y el segundo la parte de la cadena desde la poscion start
## hasta el final del comando.
def comando(cadena,start=0):
 patron=r"(\s*(\\([0-9]|[a-zA-Z]+)))"
 m=re.match(patron,cadena[start:])
 if m!=None:
  resultado = [m.groups(0)[1],m.groups(0)[0]]
 else:
  resultado=["",""]
 return resultado

#End of function

## La funcion argus recibe una cadena, y los siguientes argumentos:
## numero: indica el numero de argumentos que 
##    va a buscar.
## opciones: los valores pueden ser, -1,0, 1 o 2. Sirve
## para indicar si el comando a buscar tendra argumentos que empiezan por el
## simbolo "#" o argumentos entre corchetes "[", "]".
## salida: indica si queremos una salida "literal", es decir la cadena
## completa con lo buscado, o "argumentos", que  implica
## una salida que es una lista con los argumentos, opciones(argumentos entre 
## corchetes), y las posiciones donde empiezan dichos  argumentos.
## La funcion argus, busca en la cadena un numero de argumentos indicado por 
## el parametro "numero". Estos argumentos pueden ser digitos simples,
## caracteres simples, argumentos entre llaves, o comandos de LaTeX que 
## empiezan por el simbolo \ y siguen una serie de letras.
## La funcion es capaz de detectar si hay argumentos que empeizan por 
## el simbolo"#", o tiene argumentos entre corchetes "[", "]", que se
## usan en las definiciones de macros, o en comandos
## LaTeX con argumentos opcionales.

def argus(cadena,numero=1,opciones=0,salida="argumentos"):
 start=0
 contador=start
 letra=cadena[start]
 longitud=len(cadena[start:])
 lista=["" for k in range(numero)]
 listaOpciones= []
 posOpciones=[]
 listaNumeral=[]
 listaPosNumeral=[]
 argum=0
 literal=""
 while (numero>argum and longitud>contador+1):
  letra=cadena[contador]
  if letra==" " or letra=="\n":
   contador+=1
   literal+=letra
  elif letra=="\\":
   listaComando=comando(cadena,start=contador)
   lista[argum]=listaComando[0]
   contador+=len(listaComando[1])
   literal+=listaComando[1]
   argum+=1
  elif letra=="{":
   listaLlaves=entreLlaves(cadena,start=contador)
   lista[argum]=listaLlaves[0]
   contador+=len(listaLlaves[1])
   literal+=listaLlaves[1]
   argum+=1
  elif opciones!=0 and letra=="[":
   listaCorchetes=entreLlaves(cadena,start=contador,dl="[",dr="]")
   listaOpciones.append(listaCorchetes[0])
   posOpciones.append(argum)
   contador+=len(listaCorchetes[1])
   literal+=listaCorchetes[1]
  elif letra=="#" and opciones==-1:
   listaNumeral.append(cadena[contador+1])
   listaPosNumeral.append(argum)
   literal+=cadena[contador:contador+2]
   contador+=2
  else:
   lista[argum]=letra
   literal+=letra
   contador+=1
   argum+=1
 while (longitud > contador+1 and numero==argum and opciones==2):
  if cadena[contador]=="[":
   listaCorchetes=entreLlaves(cadena,start=contador,dl="[",dr="]")
   listaOpciones.append(listaCorchetes[0])
   literal+=listaCorchetes[1]
   contador+=len(listaCorchetes[1])
   posOpciones.append(argum)
  else:
   break
 if salida!="literal":
  if opciones==0:
   return lista
  else:
   return [lista,listaOpciones,posOpciones,listaNumeral,listaPosNumeral]
 else:
  return literal

#End of function

## La funcion s"suustituye" toma una "macro" y la  sustituye
## en la cadena que se pasa como argumento. Una "macro" consiste en una lista
## cuyos items son:
## 0: el nombre que define la macro
## 1: el número de argumentos que tiene
## 2: La cadena que define la macro.
## 3: el valor por defecto, si lo hubiere, del primer argumento.
## Asi la funcion "sustituye" busca en "cadena" comandos que
## correspondan a la macro, e identifica sus argumentos. Luego toma esos 
## argumentos y los sustituye en la cadena que define la macro. Y
## finalmente sustituye en "cadena" la macro y sus argumentos por la 
## cadena que define la macro con sus argumentos puestos
## en su lugar.
def sustituye(macro,cadena):
 if macro[3]!="":
  parametros=macro[1]-1
  defaultFlag=1
 else:
  parametros=macro[1]
  defaultFlag=0
 patron="\\\\"+macro[0]+"[^a-zA-Z]"
 m=re.search(patron,cadena)
 if m == None:
  return cadena
 else:
  pass
 inicio=m.start()
 fin=m.end()-1
 argumentosCompletos=argus(cadena[fin:],parametros,opciones=1)
 argumentos=argumentosCompletos[0]
 argumentosLiteral=argus(cadena[fin:],parametros,opciones=1,salida="literal")
 longitud=len(argumentosLiteral)
 sustituto=macro[2]
 if defaultFlag==1:
  if len(argumentosCompletos[1])!=0 and argumentosCompletos[2][0]==0:
   sustituto=re.sub("\\#1",argumentosCompletos[1][0].replace("\\","\\\\"),sustituto)
  else:
   sustituto=re.sub("\\#1",macro[3].replace("\\","\\\\"),sustituto)
 else:
  paramInicio=0
 for k in range(defaultFlag,macro[1]):
  patronNum="\\#"+str(k+1)
  sustituto=re.sub(patronNum,argumentos[k-defaultFlag].replace("\\","\\\\"),sustituto)
 resultado1=cadena[:inicio]
 resultado2=cadena[inicio+longitud+len(macro[0])+1:]
 resultado=resultado1+sustituto+resultado2
 return resultado
#end of function

## La funcion "encuentraMacros" busca en "cadena"
## todas las macros que esten definidas mediante "\def" o
## \newcommand, devolviendo una lista de "macros" (tal y como
## fueron definidas en la funcion anterior).
def encuentraMacros(cadena):
 lista=[]
 patron="\\\\(newcommand|def)[^a-zA-Z]"
 listaMacros=re.finditer(patron,cadena)
 for macro in listaMacros:
  parametros=0
  defecto=""
  inicio=macro.end()-1
  macroCompleta=argus(cadena[inicio:],2,opciones=-1)
  if len(macroCompleta[4])!=0:
   parametros=len(macroCompleta[4])
  elif len(macroCompleta[4])==0 and len(macroCompleta[1])==0:
   parametros=0
  elif len(macroCompleta[4])==0 and len(macroCompleta[1])==1:
   parametros=int(macroCompleta[1][0])
  elif len(macroCompleta[4])==0 and len(macroCompleta[1])==2:
   parametros=int(macroCompleta[1][0])
   defecto=macroCompleta[1][1]
  else:
   pass
  macroNueva=[macroCompleta[0][0].replace("\\",""),parametros,macroCompleta[0][1],defecto]
  lista.append(macroNueva)
 return lista
#End of Function

## La funcion "sustituyeTodas" busca las macros definidas en 
## la cadena "preambulo", y las sustituye en la cadena "body".
## La funcion devuelve la cadena "body" con las macros de "preambulo" 
## convenientemente sustituidas.
def sustituyeTodas(preambulo,body):
 lista=encuentraMacros(preambulo)
 for k in lista:
  macroNum=len(re.findall("\\\\"+k[0]+"[^a-zA-Z]",body))
  while(macroNum!=0):
   body=sustituye(k,body)
   macroNum-=1
 return body


#End of Function

## La funcion "cleanLatex" toma el contenido de un archivo LaTeX que esta
## especificado en su argumento, y devuelve una cadena con el 
## contenido del mismo sin los comentarios.
def cleanLatex(cadena):
 patron=re.compile(r"%+.*")
 cadenaLimpia=patron.sub("",cadena)
 return cadenaLimpia
#End of Function

## la funcion "splitLatex" toma una cadena de un 
## codigo LaTeX, y lo divide en el preambulo y en el cuerpo del documento.
## La funcion devuelve una lista de 2 elementos, el primero es la cadena
## que corresponde al preambulo y la segunda al cuerpo.

def splitLatex(cadena):
 patronPreambleBegin=re.compile(r"\\documentclass")
 patronPreambleEnd=re.compile(r"\\begin{document}")
 patronBodyEnd=re.compile(r"\\end{document}")
 startPreamble=patronPreambleBegin.search(cadena).start()
 endPreamble=patronPreambleEnd.search(cadena).start()
 endBody=patronBodyEnd.search(cadena).end()
 preamble=cadena[startPreamble:endPreamble]
 body=cadena[endPreamble:endBody]
 return [preamble,body]
#End of Function

## La funcion "undo" toma el contenido de un archivo LaTeX
## y devuelve la cadena del archivo, con las macros convenientemente
## sustituidas.
def undo(documentContent):
 #cadena=cleanLatex(documentString)
 #preambulo,bodyOrigen = splitLatex(cadena)
 body=sustituyeTodas(documentContent[0],documentContent[1])
 return [documentContent[0], body, documentContent[2]]

##END of function

