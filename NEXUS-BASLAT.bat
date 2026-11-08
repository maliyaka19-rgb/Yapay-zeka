@echo off
chcp 65001 >nul
setlocal
title NEXUS-CORE Launcher

rem =====================================================
rem  NEXUS-CORE tek tiklama baslatici
rem  - Ollama (yerel model) servisini acar
rem  - Backend'i (FastAPI :8000) acar
rem  - Tarayicida http://127.0.0.1:8000/ acar
rem  Zaten calisiyorsa tekrar acmaz.
rem =====================================================

set "ROOT=%~dp0"
set "BACKEND=%ROOT%multimodal-studio\backend"
set "OPEN_URL=http://127.0.0.1:8000/"
set "LOGDIR=%TEMP%\nexus-logs"

if not exist "%LOGDIR%" mkdir "%LOGDIR%"

echo.
echo   NEXUS-CORE baslatiliyor...
echo.

rem ---- 1) Ollama (port 11434) ----
netstat -ano | findstr /r /c:":11434 .*LISTENING" >nul 2>nul
if errorlevel 1 (
    where ollama >nul 2>nul
    if errorlevel 1 (
        echo   [atla] Ollama bulunamadi, yerel model kapali kalacak.
    ) else (
        start "" /min ollama serve
        echo   [ok] Ollama baslatildi.
    )
) else (
    echo   [ok] Ollama zaten calisiyor.
)

rem ---- 2) Backend (port 8000) ----
netstat -ano | findstr /r /c:":8000 .*LISTENING" >nul 2>nul
if errorlevel 1 (
    if not exist "%BACKEND%\run_server.py" (
        echo   [HATA] Backend bulunamadi: "%BACKEND%\run_server.py"
        goto :end
    )
    start "NEXUS-CORE Backend" /min cmd /c "cd /d "%BACKEND%" && python run_server.py > "%LOGDIR%\backend.log" 2> "%LOGDIR%\backend.err.log""
    echo   [ok] Backend baslatildi.
) else (
    echo   [ok] Backend zaten calisiyor.
)

rem ---- 3) Hazir olana kadar bekle ----
echo   [..] Sunucu hazirlaniyor
set /a tries=0
:waitloop
set /a tries+=1
netstat -ano | findstr /r /c:":8000 .*LISTENING" >nul 2>nul
if not errorlevel 1 goto :ready
if %tries% geq 30 goto :timeout
timeout /t 1 /nobreak >nul
echo   ....
goto :waitloop

:ready
echo   [ok] NEXUS-CORE hazir: %OPEN_URL%
start "" "%OPEN_URL%"
echo.
echo   Kapatmak icin acilan penceredeki Ctrl+C tuslarini kullanin.
echo.
goto :end

:timeout
echo   [HATA] Sunucu 30 saniyede acilmadi.
echo          Loglar: %LOGDIR%\backend.err.log
echo          Manuel deneyin: cd /d "%BACKEND%" ^&^& python run_server.py
echo.

:end
endlocal
