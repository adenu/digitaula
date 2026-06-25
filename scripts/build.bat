@echo off
setlocal
cd /d "%~dp0.."

echo Instalando dependencias de build...
pip install -r requirements.txt -r requirements-dev.txt

echo.
echo Gerando executavel...
pyinstaller digitaula.spec --noconfirm

set DIST=dist\DigitAula
if not exist "%DIST%\sources" mkdir "%DIST%\sources"
if not exist "%DIST%\examples" mkdir "%DIST%\examples"
xcopy /E /I /Y examples "%DIST%\examples\"
copy /Y GUIA-PROFESSOR.md "%DIST%\"
copy /Y README.md "%DIST%\"

echo.
echo Pronto: %DIST%\DigitAula.exe
echo Envie a pasta inteira "dist\DigitAula" para o professor.
pause
