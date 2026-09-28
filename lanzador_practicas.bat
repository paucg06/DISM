@echo off
title Lanzador de Practicas DISM
:MENU
cls
echo ===================================================================
echo                     PANEL DE CONTROL DISM
echo ===================================================================
echo.
echo Selecciona la practica que deseas ejecutar:
echo.
echo   [0]  DISM0  - Proyecto Base Tabs (Ionic + Angular)
echo   [1]  DISM1  - Componentes Visuales Tabs (Botones, Listas, Toggles)
echo   [2]  DISM2  - Menu Lateral Side (ion-split-pane, ion-menu)
echo   [3]  DISM3  - Consumo API Externa (HttpClient, RandomUser)
echo   [4]  DISM4  - Backend Mock Fake API (json-server puerto 3000)
echo   [5]  DISM5  - App Cliente CRUD Completo (Fake REST API)
echo   [6]  DISM6  - Geolocalizacion GPS y Reverse Geocoding (Nominatim)
echo   [7]  DISM7  - Mapas Interactivos Leaflet (Marcadores Alicante/BCN)
echo   [8]  DISM8  - Ver Contrato OpenAPI 3.0 (HolaMundo.yaml)
echo   [9]  DISM9  - Servidor Express OpenAPI (Puerto 8080 /api-docs)
echo   [10] DISM10 - Servidor Express CRUD + MySQL (Puerto 8080 /api-docs)
echo.
echo   [T]  INSTALAR dependencias de TODAS las practicas de golpe
echo   [X]  Salir
echo.
echo ===================================================================
set /p opt="Introduce tu opcion: "

if /i "%opt%"=="0" goto RUN_DISM0
if /i "%opt%"=="1" goto RUN_DISM1
if /i "%opt%"=="2" goto RUN_DISM2
if /i "%opt%"=="3" goto RUN_DISM3
if /i "%opt%"=="4" goto RUN_DISM4
if /i "%opt%"=="5" goto RUN_DISM5
if /i "%opt%"=="6" goto RUN_DISM6
if /i "%opt%"=="7" goto RUN_DISM7
if /i "%opt%"=="8" goto RUN_DISM8
if /i "%opt%"=="9" goto RUN_DISM9
if /i "%opt%"=="10" goto RUN_DISM10
if /i "%opt%"=="T" goto INSTALL_ALL
if /i "%opt%"=="X" goto END
goto MENU

:RUN_DISM0
cd /d "%~dp0DISM0"
echo Arrancando DISM0...
call ionic serve
pause
goto MENU

:RUN_DISM1
cd /d "%~dp0DISM1"
echo Arrancando DISM1...
call ionic serve
pause
goto MENU

:RUN_DISM2
cd /d "%~dp0DISM2"
echo Arrancando DISM2...
call ionic serve
pause
goto MENU

:RUN_DISM3
cd /d "%~dp0DISM3"
echo Arrancando DISM3...
call ionic serve
pause
goto MENU

:RUN_DISM4
cd /d "%~dp0DISM4"
echo Arrancando json-server en puerto 3000...
call npx json-server db.json --port 3000
pause
goto MENU

:RUN_DISM5
cd /d "%~dp0"
echo Iniciando backend json-server en segundo plano...
start "DISM4 Fake Backend (Puerto 3000)" cmd /c "cd /d %~dp0DISM4 && npx json-server db.json --port 3000"
timeout /t 2 > nul
cd /d "%~dp0DISM5"
echo Arrancando cliente DISM5...
call ionic serve
pause
goto MENU

:RUN_DISM6
cd /d "%~dp0DISM6"
echo Arrancando DISM6...
call ionic serve
pause
goto MENU

:RUN_DISM7
cd /d "%~dp0DISM7"
echo Arrancando DISM7...
call ionic serve
pause
goto MENU

:RUN_DISM8
cd /d "%~dp0DISM8"
notepad HolaMundo.yaml
goto MENU

:RUN_DISM9
cd /d "%~dp0DISM9"
echo Arrancando Servidor Express OpenAPI en puerto 8080...
start http://localhost:8080/api-docs
call npm start
pause
goto MENU

:RUN_DISM10
cd /d "%~dp0DISM10"
echo Arrancando Servidor Express CRUD MySQL en puerto 8080...
start http://localhost:8080/api-docs
call npm start
pause
goto MENU

:INSTALL_ALL
cd /d "%~dp0"
echo ===================================================================
echo        INSTALANDO DEPENDENCIAS DE TODAS LAS PRACTICAS
echo ===================================================================
for %%P in (DISM0 DISM1 DISM2 DISM3 DISM5 DISM6 DISM7 DISM9 DISM10) do (
    echo.
    echo --- Instalando en %%P ---
    cd /d "%~dp0%%P"
    call npm install --no-audit --no-fund
)
cd /d "%~dp0"
echo.
echo ===================================================================
echo     TODAS LAS DEPENDENCIAS HAN SIDO INSTALADAS CON EXITO
echo ===================================================================
pause
goto MENU

:END
exit
