@echo off
rem   Builds a zip containing stuff needed to link with the wxWindows DLL
rem   shipped with wxPython.  This should allow other developers to create apps
rem   or extensions that can share the same DLL.

setlocal
set BASE=_distrib_zip\wxPython-%1

set TYPE=h
if "%2" == "debug" set TYPE=d

set DELTYPE=d
if "%2" == "debug" set DELTYPE=h 

set DLLDIR=vc_dll
if "%CPU%" == "AMD64" set DLLDIR=vc_amd64_dll

set PLATFORM=win32
if "%CPU%" == "AMD64" set PLATFORM=win64


rem **** Make a directory to build up a distribution tree
mkdir _distrib_zip
mkdir %BASE%


rem *** copy files
copy distrib\README.devel.txt %BASE%\README.txt

mkdir %BASE%\build
mkdir %BASE%\build\bakefiles
mkdir %BASE%\build\bakefiles\wxpresets

copy /s %WXWIN%\build\bakefiles\wxpresets\*  %BASE%\build\bakefiles\wxpresets  

mkdir %BASE%\include
mkdir %BASE%\include\wx
copy /s %WXWIN%\include\wx\*                 %BASE%\include\wx

copy /s %WXWIN%\contrib\include\wx\gizmos    %BASE%\include\wx\gizmos
copy /s %WXWIN%\contrib\include\wx\ogl       %BASE%\include\wx\ogl
copy /s %WXWIN%\contrib\include\wx\stc       %BASE%\include\wx\stc

copy /s %WXWIN%\wxPython\include\wx\*        %BASE%\include\wx
mkdir %BASE%\include\wx\wxPython\i_files
copy  %WXWIN%\wxPython\src\*.i               %BASE%\include\wx\wxPython\i_files
copy  %WXWIN%\wxPython\src\*.py              %BASE%\include\wx\wxPython\i_files

mkdir %BASE%\lib
mkdir %BASE%\lib\%DLLDIR%
mkdir %BASE%\lib\%DLLDIR%\msw%TYPE%
mkdir %BASE%\lib\%DLLDIR%\mswu%TYPE%

copy /s %WXWIN%\lib\%DLLDIR%\msw%TYPE%\*       %BASE%\lib\%DLLDIR%\mswh
copy /s %WXWIN%\lib\%DLLDIR%\mswu%TYPE%\*      %BASE%\lib\%DLLDIR%\mswuh
copy %WXWIN%\lib\%DLLDIR%\*                    %BASE%\lib\%DLLDIR%


rem *** remove unneeded files
cd _distrib_zip

ffind /SB wx*%DELTYPE%_*.*		>  del-files
ffind /SB wx*%DELTYPE%.*		>> del-files
ffind /SB .#*				>> del-files
ffind /SB .cvsignore			>> del-files

for %f in (@del-files) do 	rm -fv %f
rem del /y @del-files


ffind /SB /A:D	CVS			>  del-dirs
echo  wxPython-%1\include\wx\cocoa 	>> del-dirs
echo  wxPython-%1\include\wx\gtk 	>> del-dirs
echo  wxPython-%1\include\wx\mac 	>> del-dirs
echo  wxPython-%1\include\wx\mgl 	>> del-dirs
echo  wxPython-%1\include\wx\motif 	>> del-dirs
echo  wxPython-%1\include\wx\os2 	>> del-dirs
echo  wxPython-%1\include\wx\univ 	>> del-dirs
echo  wxPython-%1\include\wx\unix 	>> del-dirs
echo  wxPython-%1\include\wx\x11 	>> del-dirs

for %d in (@del-dirs) do 	rm -rfv %d
rem del /sxzy @del-dirs

rm del-files
rm del-dirs

rem *** bundle it all up  TODO: don't hard-code the 2.8
set EXT=
if "%2" == "debug" set EXT="-debug"
tar cvf ../dist/wxPython2.8-%PLATFORM%-devel-%1%EXT%-msvc%MSVCVER%.tar wxPython-%1
bzip2 -9 ../dist/wxPython2.8-%PLATFORM%-devel-%1%EXT%-msvc%MSVCVER%.tar

rem *** cleanup
rem cd ..
rem rm -rf _distrib_zip

endlocal



