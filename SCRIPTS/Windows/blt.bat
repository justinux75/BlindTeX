@echo off
SET BTX="c:\BlindTeX"
SET LOCAL=%cd%
SET var=%LOCAL%\
cd %BTX%
if %~1== -h set  var=
if %~1== -e set var=
python mainBlindtex.py %1 "%var%%~2"
cd %LOCAL%
pause > nul

