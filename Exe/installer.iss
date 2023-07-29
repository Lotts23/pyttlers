; Script for building the installer with Inno Setup

#define MyAppName "Pyttlers"
#define MyAppVersion "1.0"
#define MyAppPublisher "Lotts"
#define MyAppURL "https://github.com/Lotts23/pyttlers"
#define MyAppExeName "Pyttlers.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=dist\
OutputBaseFilename=PyttlersInstall
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\{#MyAppExeName}
AppMutex={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Pyttlers.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "data\ikon.ico"; DestDir: "{app}\data"; Flags: ignoreversion
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram},{#MyAppName}"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{pf}\{#MyAppName}"; Flags: uninsneveruninstall
