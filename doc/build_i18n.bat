@echo off
REM Build VapourSynth documentation in both English and Chinese
REM Output: _build/html/en/ and _build/html/zh_CN/

cd /d "%~dp0"

echo ========================================
echo Building English documentation...
echo ========================================
sphinx-build -b html -D language=en . _build/html/en
if errorlevel 1 (
    echo ERROR: English build failed!
    exit /b 1
)

echo.
echo ========================================
echo Building Chinese documentation...
echo ========================================
sphinx-build -b html -D language=zh_CN . _build/html/zh_CN
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
