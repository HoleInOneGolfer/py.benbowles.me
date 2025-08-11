IF "%OS%"=="Windows_NT" (
    SET "REPO_PATH=%CD%"
) ELSE (
    SET "REPO_PATH=%USERPROFILE%\src"
)

cd /d "%REPO_PATH%" || exit /b 1

git fetch origin main || exit /b 1
git reset --hard origin/main || exit /b 1

IF EXIST "%REPO_PATH%\requirements.txt" (
    pip install --upgrade -r "%REPO_PATH%\requirements.txt" || exit /b 1
)
