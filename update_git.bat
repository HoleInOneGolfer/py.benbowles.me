REM Set REPO_PATH to current directory on Windows, else to %USERPROFILE%\src
IF "%OS%"=="Windows_NT" (
    SET "REPO_PATH=%CD%"
) ELSE (
    SET "REPO_PATH=%USERPROFILE%\src"
)

REM Change to the repository directory
cd /d "%REPO_PATH%" || exit /b 1

git fetch origin main || exit /b 1
REM git reset --hard origin/main || exit /b 1
