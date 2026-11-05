@echo off
chcp 65001 > nul
title Practica 1 (Entrega 1) - Sistema de Registro Horario

:MENU
cls
echo ===================================================================
echo     PRACTICA 1 (ENTREGA 1) - SISTEMA DE REGISTRO HORARIO
echo     (Backend REST API + BD MySQL + AppAdmin Ionic)
echo ===================================================================
echo.
echo Selecciona la opcion que deseas ejecutar:
echo.
echo   [1]  Arrancar Backend REST API (Express en puerto 8080 + Swagger UI)
echo   [2]  Arrancar AppAdmin (Ionic / Angular en http://localhost:8100)
echo   [3]  Abrir documentacion interactiva Swagger UI en el navegador
echo   [4]  Descomprimir librerias offline (si estas en clase sin internet)
echo   [5]  Instalar / Actualizar dependencias con npm (online)
echo.
echo   [X]  Salir
echo.
echo ===================================================================
set /p opt="Introduce tu opcion: "

if /i "%opt%"=="1" goto RUN_BACKEND
if /i "%opt%"=="2" goto RUN_APPADMIN
if /i "%opt%"=="3" goto OPEN_SWAGGER
if /i "%opt%"=="4" goto EXTRACT_OFFLINE
if /i "%opt%"=="5" goto INSTALL_ONLINE
if /i "%opt%"=="X" goto END
goto MENU

:RUN_BACKEND
cd /d "%~dp0backend-api"
if not exist "node_modules" (
    if exist "node_modules.tar.gz" (
        echo [INFO] Descomprimiendo dependencias offline de Backend...
        tar -xzf node_modules.tar.gz
    )
)
echo.
echo Arrancando Backend API REST en puerto 8080...
start http://localhost:8080/api-docs
call node server.js
pause
goto MENU

:RUN_APPADMIN
cd /d "%~dp0AppAdmin"
if not exist "node_modules" (
    if exist "node_modules.tar.gz" (
        echo [INFO] Descomprimiendo dependencias offline de AppAdmin...
        tar -xzf node_modules.tar.gz
    )
)
echo.
echo Arrancando aplicacion AppAdmin en Ionic / Angular...
where ionic >nul 2>nul
if %errorlevel% equ 0 (
    call ionic serve
) else (
    call npm start
)
pause
goto MENU

:OPEN_SWAGGER
start http://localhost:8080/api-docs
goto MENU

:EXTRACT_OFFLINE
echo.
echo ===================================================================
echo [1/2] Descomprimiendo librerias de backend-api...
echo ===================================================================
cd /d "%~dp0backend-api"
if exist "node_modules.tar.gz" (
    tar -xzf node_modules.tar.gz
    echo [OK] Backend librerias listas.
) else (
    echo [!] No se encontro node_modules.tar.gz en backend-api
)

echo.
echo ===================================================================
echo [2/2] Descomprimiendo librerias de AppAdmin...
echo ===================================================================
cd /d "%~dp0AppAdmin"
if exist "node_modules.tar.gz" (
    tar -xzf node_modules.tar.gz
    echo [OK] AppAdmin librerias listas.
) else (
    echo [!] No se encontro node_modules.tar.gz en AppAdmin
)

cd /d "%~dp0"
echo.
echo Todas las librerias han sido preparadas sin necesidad de conexion a internet.
pause
goto MENU

:INSTALL_ONLINE
echo.
echo ===================================================================
echo [1/2] Instalando con npm en backend-api...
echo ===================================================================
cd /d "%~dp0backend-api"
call npm install --no-audit --no-fund --strict-ssl=false

echo.
echo ===================================================================
echo [2/2] Instalando con npm en AppAdmin...
echo ===================================================================
cd /d "%~dp0AppAdmin"
call npm install --no-audit --no-fund --strict-ssl=false

cd /d "%~dp0"
echo.
echo Dependencias instaladas con exito mediante npm.
pause
goto MENU

:END
exit
