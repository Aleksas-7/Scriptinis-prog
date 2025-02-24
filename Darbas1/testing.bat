::https://stackoverflow.com/questions/10166386/arrays-linked-lists-and-other-data-structures-in-cmd-exe-batch-script/10167990#10167990


@REM First loop
    @REM Create batch script which
    @REM  reads all files of given extension
    @REM  from given directory and its sub directories 
    @REM into array or list, 

@REM Second loop
    @REM then iterate this array 
    @REM and form log file in the same directory. 
    @REM Log file should have this format:
        @REM current date 
        @REM current time
        @REM filename1
        @REM filepath1
        @REM filename2
        @REM filepath2 ...

@REM C:\Users\aluba\OneDrive\Desktop\VUmif\Year3_part2\ScriptinisProgramavimas

@echo off
setlocal EnableDelayedExpansion

set fo=file_output.txt
set default_dir=C:\Users
set default_ext=.bat

set /p "direc=Enter file directory (C:\smth\smth):  " 
if not defined direc set direc=%default_dir%

set /p "ext=Enter file ext (.txt .png):  "
if not defined ext set ext=%default_ext%

set index=0
(for /r %direc% %%f in (*%ext%) do (
    set /A index=index+1
    set file[!index!].path=%%f
    set file[!index!].name=%%~nxf
))

echo. > %direc%\%fo%
echo %date%>>%direc%\%fo%
echo %time%>>%direc%\%fo%
echo. >> %direc%\%fo%

(for /L %%i in (1,1,%index%) do (
    echo !file[%%i].name! >> %direc%\%fo%
    echo !file[%%i].path! >> %direc%\%fo%
))

start %direc%\%fo%
pause
taskkill /im notepad.exe /f
:: ^ not the most optimal way to close notepad
del %direc%\%fo%






