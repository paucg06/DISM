@echo off
chcp 65001 > nul
title Abrir Aplicacion PWA - Control Horario

echo ===================================================================
echo           ABRIR APLICACION PWA (MODO APLICACION NATIVA)
echo ===================================================================
echo.
echo Abriendo Control Horario PWA en ventana dedicada...
start "" "chrome.exe" --app="http://localhost:8100/?fresh=%RANDOM%" 2>nul || start "" "msedge.exe" --app="http://localhost:8100/?fresh=%RANDOM%" 2>nul || start http://localhost:8100/?fresh=%RANDOM%
