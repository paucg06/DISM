@echo off
chcp 65001 > nul
title Practica 2 COMPILADA - Control Horario PWA

echo ===================================================================
echo     PRACTICA 2 COMPILADA - SISTEMA DE CONTROL HORARIO (PWA)
echo     (Ejecucion Inmediata - Cero Dependencias y Cero Instalaciones)
echo ===================================================================
echo.

:: Liberar puertos si habia procesos anteriores
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8100 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1

echo [1/3] Arrancando Servidor Backend REST API (Puerto 8080)...
start "Backend REST API (Puerto 8080)" cmd /k "cd /d "%~dp0backend-api" && node server.js"

timeout /t 2 /nobreak > nul

echo [2/3] Arrancando Servidor Web PWA (Puerto 8100)...
start "Servidor Web PWA (Puerto 8100)" cmd /k "cd /d "%~dp0" && node servidor_estatico.js"

timeout /t 2 /nobreak > nul

echo [3/3] Abriendo aplicacion PWA en tu navegador...
start http://localhost:8080/api-docs/
start http://localhost:8100/?fresh=%RANDOM%

echo.
echo ===================================================================
echo   SISTEMA EN EJECUCION EXITOSA:
echo   - Swagger UI:   http://localhost:8080/api-docs/
echo   - App PWA:      http://localhost:8100
echo.
echo   Roles y Temas visuales:
echo   - Login (Sin sesion):   TEMA GRIS
echo   - Administrador (admin): TEMA VERDE (Gestion integral)
echo   - Empleado (sergio):     TEMA AZUL  (Fichaje y consultas)
echo.
echo   Credenciales disponibles:
echo   - Administrador: usuario "admin",  clave "admin123"
echo   - Empleados:     usuario "sergio", clave "1234"
echo                    usuario "lucia",  clave "1234"
echo.
echo   Para detener los servicios, simplemente cierra las ventanas de consola.
echo ===================================================================
echo.
pause
