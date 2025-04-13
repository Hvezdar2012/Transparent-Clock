@echo off
set /p input=Name of file you want to export. (make sure your icon is named icon.ico):

if x%input:.py=%==x%input% (
    set "str=%input%.py"
) else (
    set "str=%input%"
)

pyinstaller --onefile --noconsole --icon="icon.ico" "%str%"
exit
