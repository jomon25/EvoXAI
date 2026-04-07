@echo off
echo =========================================
echo EvoXAI Auto-Sync tool
echo =========================================
echo.

git status
echo.

set /p msg="Enter your commit message for today's changes: "

echo.
echo Saving and uploading...
git add .
git commit -m "%msg%"
git push

echo.
echo Done! Your changes are live on GitHub.
pause
