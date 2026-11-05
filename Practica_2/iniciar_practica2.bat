@echo off
chcp 65001 > nul
title Practica 2 (Entrega 2) - Sistema Completo de Registro Horario

:MENU
cls
echo ===================================================================
echo     PRACTICA 2 (ENTREGA 2) - SISTEMA COMPLETO DE REGISTRO HORARIO
echo     (Backend REST API + BD MySQL + AppAdmin + AppUsuarios)
echo ===================================================================
echo.
echo Selecciona la opcion que deseas ejecutar:
echo.
echo   [1]  ARRANCAR TODO (Backend 8080 + AppAdmin 8100 + AppUsuarios 8101)  [RECOMENDADO]
echo.
echo   [2]  Arrancar solo Backend REST API (Node.js en puerto 8080)
echo   [3]  Arrancar solo AppAdmin (Modo Rapido en puerto 8100)
echo   [4]  Arrancar solo AppUsuarios (Modo Rapido en puerto 8101)
echo   [5]  Arrancar AppAdmin en Modo Desarrollo (Ionic Serve)
echo   [6]  Arrancar AppUsuarios en Modo Desarrollo (Ionic Serve)
echo   [7]  Abrir Swagger UI en el navegador (http://localhost:8080/api-docs/)
echo.
echo   [8]  Descomprimir librerias offline (para ordenadores sin internet)
echo   [9]  Instalar / Actualizar dependencias con npm (online)
echo.
echo   [X]  Salir
echo.
echo ===================================================================
set /p opt="Introduce tu opcion: "

if /i "%opt%"=="1" goto RUN_ALL
if /i "%opt%"=="2" goto RUN_BACKEND
if /i "%opt%"=="3" goto RUN_FAST_ADMIN
if /i "%opt%"=="4" goto RUN_FAST_USUARIOS
if /i "%opt%"=="5" goto RUN_DEV_ADMIN
if /i "%opt%"=="6" goto RUN_DEV_USUARIOS
if /i "%opt%"=="7" goto OPEN_SWAGGER
if /i "%opt%"=="8" goto EXTRACT_OFFLINE
if /i "%opt%"=="9" goto INSTALL_ONLINE
if /i "%opt%"=="X" goto END
goto MENU

:RUN_ALL
cls
echo ===================================================================
echo   ARRANCANDO SISTEMA COMPLETO DE PRACTICA 2...
echo ===================================================================
echo.
echo [1/3] Iniciando Backend REST API en puerto 8080...
cd /d "%~dp0backend-api"
if not exist "node_modules" (
    if exist "node_modules.tar.gz" (
        tar -xzf node_modules.tar.gz
    )
)
start "Backend REST API (Puerto 8080)" cmd /k "cd /d "%~dp0backend-api" && node server.js"

timeout /t 2 /nobreak > nul

echo [2/3] Iniciando Servidor Web para AppAdmin y AppUsuarios...
cd /d "%~dp0"
start "Servidor Web Apps (Puertos 8100 y 8101)" cmd /k "cd /d "%~dp0" && node servidor_estatico.js"

timeout /t 2 /nobreak > nul

echo [3/3] Abriendo aplicaciones en tu navegador...
start http://localhost:8080/api-docs/
start http://localhost:8100
start http://localhost:8101

echo.
echo ===================================================================
echo   SERVICIOS INICIADOS CORRECTAMENTE:
echo   - Backend y Swagger UI: http://localhost:8080/api-docs/
echo   - AppAdmin:            http://localhost:8100
echo   - AppUsuarios:         http://localhost:8101
echo.
echo   Los servicios estan ejecutandose en sus ventanas dedicadas.
echo ===================================================================
echo.
pause
goto MENU

:RUN_BACKEND
echo.
echo [INFO] Arrancando Backend REST API en nueva ventana...
cd /d "%~dp0backend-api"
if not exist "node_modules" (
    if exist "node_modules.tar.gz" (
        tar -xzf node_modules.tar.gz
    )
)
start "Backend REST API (Puerto 8080)" cmd /k "cd /d "%~dp0backend-api" && node server.js"
timeout /t 2 /nobreak > nul
start http://localhost:8080/api-docs/
goto MENU

:RUN_FAST_ADMIN
echo.
echo [INFO] Arrancando AppAdmin en nueva ventana...
cd /d "%~dp0"
start "Servidor Web Apps" cmd /k "cd /d "%~dp0" && node servidor_estatico.js"
timeout /t 2 /nobreak > nul
start http://localhost:8100
goto MENU

:RUN_FAST_USUARIOS
echo.
echo [INFO] Arrancando AppUsuarios en nueva ventana...
cd /d "%~dp0"
start "Servidor Web Apps" cmd /k "cd /d "%~dp0" && node servidor_estatico.js"
timeout /t 2 /nobreak > nul
start http://localhost:8101
goto MENU

:RUN_DEV_ADMIN
echo.
echo [INFO] Arrancando AppAdmin en Modo Desarrollo (Ionic Serve)...
cd /d "%~dp0AppAdmin"
if not exist "node_modules" (
    if exist "node_modules.tar.gz" (
        tar -xzf node_modules.tar.gz
    )
)
start "AppAdmin (Ionic Serve - 8100)" cmd /k "cd /d "%~dp0AppAdmin" && ionic serve --port 8100"
goto MENU

:RUN_DEV_USUARIOS
echo.
echo [INFO] Arrancando AppUsuarios en Modo Desarrollo (Ionic Serve)...
cd /d "%~dp0AppUsuarios"
if not exist "node_modules" (
    if exist "node_modules.tar.gz" (
        tar -xzf node_modules.tar.gz
    )
)
start "AppUsuarios (Ionic Serve - 8101)" cmd /k "cd /d "%~dp0AppUsuarios" && ionic serve --port 8101"
goto MENU

:OPEN_SWAGGER
echo.
echo Abriendo Swagger UI en el navegador...
start http://localhost:8080/api-docs/
goto MENU

:EXTRACT_OFFLINE
echo.
echo ===================================================================
echo [1/3] Descomprimiendo librerias de backend-api...
echo ===================================================================
cd /d "%~dp0backend-api"
if exist "node_modules.tar.gz" (
    tar -xzf node_modules.tar.gz
    echo [OK] Backend librerias listas.
)

echo.
echo ===================================================================
echo [2/3] Descomprimiendo librerias de AppAdmin...
echo ===================================================================
cd /d "%~dp0AppAdmin"
if exist "node_modules.tar.gz" (
    tar -xzf node_modules.tar.gz
    echo [OK] AppAdmin librerias listas.
)

echo.
echo ===================================================================
echo [3/3] Descomprimiendo librerias de AppUsuarios...
echo ===================================================================
cd /d "%~dp0AppUsuarios"
if exist "node_modules.tar.gz" (
    tar -xzf node_modules.tar.gz
    echo [OK] AppUsuarios librerias listas.
)

cd /d "%~dp0"
echo.
echo Todas las librerias han sido preparadas sin necesidad de conexion a internet.
pause
goto MENU

:INSTALL_ONLINE
echo.
echo ===================================================================
echo [1/3] Instalando dependencias en backend-api...
echo ===================================================================
cd /d "%~dp0backend-api"
call npm install --no-audit --no-fund --strict-ssl=false

echo.
echo ===================================================================
echo [2/3] Instalando dependencias en AppAdmin...
echo ===================================================================
cd /d "%~dp0AppAdmin"
call npm install --no-audit --no-fund --strict-ssl=false

echo.
echo ===================================================================
echo [3/3] Instalando dependencias en AppUsuarios...
echo ===================================================================
cd /d "%~dp0AppUsuarios"
call npm install --no-audit --no-fund --strict-ssl=false

cd /d "%~dp0"
echo.
echo Dependencias instaladas con exito mediante npm.
pause
goto MENU

:END
exit
