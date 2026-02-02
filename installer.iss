[Setup]
AppName=ASD2CSV
AppVersion=1.0.0
DefaultDirName={pf}\ASD2CSV
DefaultGroupName=ASD2CSV
OutputDir=dist_installer
OutputBaseFilename=ASD2CSV_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\icon.ico

[Files]
Source: "dist\ASD2CSV\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\ASD2CSV"; Filename: "{app}\ASD2CSV.exe"
Name: "{commondesktop}\ASD2CSV"; Filename: "{app}\ASD2CSV.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\ASD2CSV.exe"; Description: "Launch ASD2CSV"; Flags: nowait postinstall skipifsilent
