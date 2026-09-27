@echo off
setlocal
cd /d "%~dp0"

echo =================================================== >> data\scheduler_output.log
echo Run started at %date% %time% >> data\scheduler_output.log

:: Detect Python executable (prefer py -3.13 or system python)
where py >nul 2>&1
if %errorlevel% equ 0 (
    set "PYCMD=py -3.13"
) else (
    set "PYCMD=python"
)

echo [*] Running scraper with %PYCMD%... >> data\scheduler_output.log
%PYCMD% run_scraper.py --origin DEL --dest HYD >> data\scheduler_output.log 2>&1
if %errorlevel% neq 0 (
    echo [!] Initial scraper attempt failed, retrying with python fallback... >> data\scheduler_output.log
    python run_scraper.py --origin DEL --dest HYD >> data\scheduler_output.log 2>&1
)

echo [*] Updating CPI price indices and syncing dashboard... >> data\scheduler_output.log
%PYCMD% calculate_index.py >> data\scheduler_output.log 2>&1

echo Run finished at %date% %time% >> data\scheduler_output.log
echo =================================================== >> data\scheduler_output.log
endlocal
