@echo off
echo =================================================================
echo Cable Tag Printer - Creating EXE file
echo =================================================================

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo Creating exe file...
pyinstaller --onefile --windowed --name=CableTagPrinter main.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to create exe file!
    pause
    exit /b 1
)

echo Copying additional files...
if exist templates md dist\templates
if exist assets md dist\assets
if exist models md dist\models
if exist templates\*.* xcopy /E /I templates dist\templates
if exist assets\*.* xcopy /E /I assets dist\assets
if exist models\*.* xcopy /E /I models dist\models

echo =================================================================
echo EXE file created successfully!
echo File located in dist\CableTagPrinter.exe
echo =================================================================
pause