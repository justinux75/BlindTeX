@echo off
SET BTX="%homepath%\blindtex\BlindTeX"
SET LOCAL=%cd%
SET var=%LOCAL%\
PUSHD %BTX%
if not "%~1"=="" goto :next
 python %BTX%\blindtexGUI.py && POPD
pause > nul
:next
if %~1== -h goto :val
if %~1== -e goto :val
python mainBlindtex.py %1 "%var%%~2"
POPD
pause > nul
:val
python mainBlindtex.py %1 "%~2"
popd
pause > nul
