@echo off
echo =================================================================
echo Cable Tag Printer - Automatic Installation
echo =================================================================

echo Step 1: Updating pip...
python -m pip install --upgrade pip

echo Step 2: Installing dependencies...
pip install -r requirements.txt

echo Step 3: Creating needed folders...
if not exist templates md templates
if not exist assets md assets
if not exist models md models
if not exist output md output

echo Step 4: Creating exe file...
pyinstaller --onefile --windowed --name=CableTagPrinter main.py

echo Step 5: Copying files...
if exist templates\*.* xcopy /E /I templates dist\templates
if exist assets\*.* xcopy /E /I assets dist\assets
if exist models\*.* xcopy /E /I models dist\models

echo =================================================================
echo SUCCESS! Cable Tag Printer installed!
echo EXE file: dist\CableTagPrinter.exe
echo =================================================================
echo NOTE: Place your PDF templates in templates/ folder
echo NOTE: Place app icon in assets/ folder
echo NOTE: Run dist\CableTagPrinter.exe to start the app
echo =================================================================
pause