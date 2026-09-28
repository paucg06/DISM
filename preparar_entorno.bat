@echo off
chcp 65001 > nul
title Preparar Entorno DISM - Instalacion de Dependencias

echo ===================================================================
echo     PREPARACION AUTOMATICA DE TODAS LAS PRACTICAS DISM (0 A 10)
echo ===================================================================
echo.
echo Este script instalara automaticamente las dependencias de Node.js
echo necesarias para ejecutar cada proyecto de forma independiente.
echo.
pause

echo -------------------------------------------------------------------
echo [1/9] Instalando dependencias DISM0...
cd /d "%~dp0DISM0"
call npm install --no-audit --no-fund

echo -------------------------------------------------------------------
echo [2/9] Instalando dependencias DISM1...
cd /d "%~dp0DISM1"
call npm install --no-audit --no-fund

echo -------------------------------------------------------------------
echo [3/9] Instalando dependencias DISM2...
cd /d "%~dp0DISM2"
call npm install --no-audit --no-fund

echo -------------------------------------------------------------------
echo [4/9] Instalando dependencias DISM3...
cd /d "%~dp0DISM3"
call npm install --no-audit --no-fund

echo -------------------------------------------------------------------
echo [5/9] Instalando dependencias DISM5...
cd /d "%~dp0DISM5"
call npm install --no-audit --no-fund

echo -------------------------------------------------------------------
echo [6/9] Instalando dependencias DISM6...
cd /d "%~dp0DISM6"
call npm install --no-audit --no-fund

echo -------------------------------------------------------------------
echo [7/9] Instalando dependencias DISM7...
cd /d "%~dp0DISM7"
call npm install --no-audit --no-fund

echo -------------------------------------------------------------------
echo [8/9] Instalando dependencias DISM9 (Servidor Express OpenAPI)...
cd /d "%~dp0DISM9"
call npm install --no-audit --no-fund

echo -------------------------------------------------------------------
echo [9/9] Instalando dependencias DISM10 (API CRUD MySQL OpenAPI)...
cd /d "%~dp0DISM10"
call npm install --no-audit --no-fund

cd /d "%~dp0"
echo.
echo ===================================================================
echo     TODAS LAS DEPENDENCIAS HAN SIDO INSTALADAS CON EXITO
echo ===================================================================
echo Ahora puedes ejecutar cualquier practica (ej: cd DISM5 && ionic serve)
echo o pedirle a Antigravity que te lance la que quieras mostrar.
echo.
pause
