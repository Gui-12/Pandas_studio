@echo off
title Instalando Dependencias do Pandas Studio
echo.
echo ==================================================
echo   Instalando dependencias necessarias (Python)...
echo ==================================================
echo.
echo As seguintes bibliotecas serao instaladas:
echo - pandas (Manipulacao de dados)
echo - streamlit (Interface grafica)
echo - openpyxl (Ler Excel .xlsx)
echo - xlsxwriter (Salvar Excel)
echo.

pip install pandas streamlit openpyxl xlsxwriter

echo.
echo ==================================================
echo   Instalacao finalizada! 
echo   Agora voce pode executar o arquivo 'iniciar.bat'
echo ==================================================
echo.
pause