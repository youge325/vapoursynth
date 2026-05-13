@echo off
REM Build VapourSynth documentation in both English and Chinese.
REM Chinese build uses direct rst sources from zh_CN_source and disables locale catalogs.

cd /d "%~dp0"

echo ========================================
echo Generating zh_CN_source from existing translations...
echo ========================================
python generate_zh_cn_source.py
if errorlevel 1 (
    echo ERROR: Failed to generate zh_CN_source!
    exit /b 1
)

echo ========================================
echo Building English documentation...
echo ========================================
sphinx-build -E -b html -d _build/doctrees/en -D language=en . _build/html/en
if errorlevel 1 (
    echo ERROR: English build failed!
    exit /b 1
)

echo.
echo ========================================
echo Building Chinese documentation from zh_CN_source...
echo ========================================
set VAPOURSYNTH_DISABLE_LOCALE=1
sphinx-build -E -b html -d _build/doctrees/zh_CN -D language=zh_CN -c . zh_CN_source _build/html/zh_CN
set VAPOURSYNTH_DISABLE_LOCALE=
if errorlevel 1 (
    echo ERROR: Chinese build failed!
    exit /b 1
)

REM Create a redirect index.html at root
echo ^<!DOCTYPE html^> > _build/html/index.html
echo ^<html^> >> _build/html/index.html
echo ^<head^>^<meta http-equiv="refresh" content="0; url=en/index.html"^>^</head^> >> _build/html/index.html
echo ^<body^>^<p^>Redirecting to ^<a href="en/index.html"^>English documentation^</a^>...^</p^>^</body^> >> _build/html/index.html
echo ^</html^> >> _build/html/index.html

echo.
echo ========================================
echo Build complete!
echo   English: _build/html/en/
echo   Chinese: _build/html/zh_CN/
echo   Root:    _build/html/index.html (redirects to English)
echo ========================================
