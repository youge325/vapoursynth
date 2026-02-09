@echo off
echo Building multilingual VapourSynth documentation...

REM Build English documentation
echo Building English version...
sphinx-build -b html doc doc/_build/html/en
if errorlevel 1 goto :error

REM Build Chinese documentation
echo Building Chinese version...
sphinx-build -D language=zh_CN -b html doc doc/_build/html/zh_CN
if errorlevel 1 goto :error

REM Create main index page
echo Creating main index page...
echo ^<!DOCTYPE html^> > doc/_build/html/index.html
echo ^<html^> >> doc/_build/html/index.html
echo ^<head^> >> doc/_build/html/index.html
echo ^<meta charset="utf-8"^> >> doc/_build/html/index.html
echo ^<title^>VapourSynth Documentation^</title^> >> doc/_build/html/index.html
echo ^<style^> >> doc/_build/html/index.html
echo body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; } >> doc/_build/html/index.html
echo .language-selector { margin: 20px; } >> doc/_build/html/index.html
echo .language-selector a { display: inline-block; padding: 20px 40px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; font-size: 18px; } >> doc/_build/html/index.html
echo .language-selector a:hover { background: #0056b3; } >> doc/_build/html/index.html
echo ^</style^> >> doc/_build/html/index.html
echo ^</head^> >> doc/_build/html/index.html
echo ^<body^> >> doc/_build/html/index.html
echo ^<h1^>VapourSynth Documentation^</h1^> >> doc/_build/html/index.html
echo ^<p^>Please choose your language / 请选择语言:^</p^> >> doc/_build/html/index.html
echo ^<div class="language-selector"^> >> doc/_build/html/index.html
echo ^<a href="en/index.html"^>English^</a^> >> doc/_build/html/index.html
echo ^<a href="zh_CN/index.html"^>中文^</a^> >> doc/_build/html/index.html
echo ^</div^> >> doc/_build/html/index.html
echo ^</body^> >> doc/_build/html/index.html
echo ^</html^> >> doc/_build/html/index.html

echo.
echo Build completed successfully!
echo English documentation: doc\_build\html\en\
echo Chinese documentation: doc\_build\html\zh_CN\
echo Main index page: doc\_build\html\index.html
goto :end

:error
echo.
echo Build failed!
exit /b 1

:end

pause