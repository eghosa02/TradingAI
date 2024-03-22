@echo off

REM Librerie da controllare
set librerie=scikit-learn pymongo gradio yfinance pandas_datareader cv2 sklearn keras joblib msgpack

REM Verifica se le librerie sono installate
for %%i in (%librerie%) do (
    python -c "import %%i" 2>nul
    if errorlevel 1 (
        echo Library %%i not found. installation...
        pip install %%i
    ) else (
        echo Library %%i found.
    )
)
echo All right.
cls
.\dist\launcher dist\main
pause