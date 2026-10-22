@echo off
title Lanzador de la Entrega 1 - Sistema de Registro Horario (Admin, BD y Servicios Web)

:MENU
cls
echo ===================================================================
echo     ENTREGA 1 - SISTEMA DE REGISTRO HORARIO (DISM 2026-2027)
echo ===================================================================
echo.
echo Selecciona la opcion que deseas ejecutar:
echo.
echo   [1]  Arrancar Backend REST API (Node.js/Express en puerto 8080)
echo   [2]  Arrancar AppAdmin (Ionic/Angular en http://localhost:8100)
echo   [3]  Abrir documentacion interactiva Swagger UI en el navegador
echo   [4]  Instalar dependencias (npm install en Backend y AppAdmin)
echo.
echo   [X]  Salir
echo.
echo ===================================================================
set /p opt="Introduce tu opcion: "

if /i "%opt%"=="1" goto RUN_BACKEND
if /i "%opt%"=="2" goto RUN_APPADMIN
if /i "%opt%"=="3" goto OPEN_SWAGGER
if /i "%opt%"=="4" goto INSTALL_ALL
if /i "%opt%"=="X" goto END
goto MENU

:RUN_BACKEND
cd /d "%~dp0backend-api"
echo.
echo Arrancando Backend API REST en puerto 8080...
echo Se abrira Swagger UI en tu navegador...
start http://localhost:8080/api-docs
call npm start
pause
goto MENU

:RUN_APPADMIN
cd /d "%~dp0AppAdmin"
echo.
echo Arrancando aplicacion AppAdmin en Ionic...
call ionic serve
pause
goto MENU

:OPEN_SWAGGER
start http://localhost:8080/api-docs
goto MENU

:INSTALL_ALL
echo.
echo ===================================================================
echo [1/2] Instalando dependencias de backend-api...
echo ===================================================================
cd /d "%~dp0backend-api"
call npm install --no-audit --no-fund --strict-ssl=false

echo.
echo ===================================================================
echo [2/2] Instalando dependencias de AppAdmin...
echo ===================================================================
cd /d "%~dp0AppAdmin"
call npm install --no-audit --no-fund --strict-ssl=false

cd /d "%~dp0"
echo.
echo Dependencias instaladas con exito.
pause
goto MENU

:END
exit
