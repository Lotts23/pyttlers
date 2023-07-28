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
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=dist\
OutputBaseFilename=PyttlersInstall
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}
AppMutex={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Pyttlers.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\ikon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\*"; DestDir: "{userappdata}\{#MyAppName}\src"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram},{#MyAppName}"; Flags: nowait postinstall skipifsilent
