# Project MDIE

Maybe Defender Isn't Enough? - Microsoft Defender [REDACTED]


**MDIE (Maybe Defender Isn't Enough?) [REDACTED] is a [REDACTED] specifically designed for red team operations and research to [REDACTED]**. The goal of this project is to study the detection techniques used by Defender and methods to [REDACTED] them, demonstrating Defender's limitations. By integrating [REDACTED] techniques from the research, the [REDACTED] will be developed for [REDACTED] and research. By open-sourcing this project, [REDACTED].


This project is designed to be [REDACTED] itself. In this way, even if [REDACTED], it will be developed to remain [REDACTED] ensuring it cannot be exploited in the future.

## Disclaimer
This document and all associated materials are provided strictly for **legitimate security research, education, and authorized antivirus detection capability testing purposes only.**
The techniques and concepts described herein involve advanced software security, malware analysis, and development methods, and **any unauthorized use, reproduction, distribution, or malicious deployment against systems without explicit permission is strictly prohibited.**


By accessing and utilizing this material, you acknowledge and agree to comply with all applicable laws and regulations,
and to obtain proper authorization before conducting any security testing or research activities.


The author and affiliated parties **expressly disclaim all legal liability and responsibility for any misuse, unauthorized actions, or damages arising from the use of this information.**


Furthermore, this research was conducted to study current antivirus detection limitations, develop evasion techniques for educational purposes, and enhance cybersecurity expertise.
The disclosure of this technology is purely for advancing the security industry and academic research.


Therefore, all risks, legal responsibilities, and consequences resulting from the use or misuse of this document rest solely with the user.
The author and related parties are fully indemnified from any direct or indirect damages.


By reading or using this document, you are deemed to have accepted all the above conditions.

## Research Scope
**The scope of this research is limited to MDAV (Microsoft Defender Antivirus)**. MDE (Microsoft Defender for Endpoint) is **not included**, and the scope is restricted to the core Defender product, excluding EDR-related technologies.
### MDE vs MDAV
![MDE Detection Layer](https://learn.microsoft.com/en-us/defender-endpoint/media/next-gen-protection-engines.png)
MDE provides a significantly more robust detection system compared to MDAV. It is classified as an EDR (Endpoint Detection and Response) software, not a traditional antivirus solution.
Details: [Advanced technologies at the core of Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav)
## MDAV Investigation
First, I'll check the official Microsoft Learn documentation to see if there are other detection technologies not found in the Security UI.
Microsoft Learn: [Microsoft Defender Antivirus in Windows Overview](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows)
### Documented MDAV Services
Based on the official Microsoft Learn documentation, here are the services for Microsoft Defender:

| Service Type                              | Service Name                  | Service Identifier    |
|:------------------------------------------|:------------------------------|:----------------------|
| MDAV Core Service                         | MpDefenderCoreService.exe     | MdCoreSvc             |
| MDAV Service                              | MsMpEng.exe                   | WinDefend             |
| MDAV Network Realtime Inspection Service  | NisSrv.exe                    | WdNisSvc              |
| Microsoft Endpoint DLP Service            | MpDlpService.exe              | MDDlpSvc              |

```ps
PS C:\WINDOWS\system32> Get-Service -Name MdCoreSvc,WinDefend,WdNisSvc,MDDlpSvc -ErrorAction SilentlyContinue | Select-Object Name,Status,StartType | Format-Table -AutoSize
Name       Status StartType
----       ------ ---------
MDCoreSvc Running Automatic
WdNisSvc  Running    Manual
WinDefend Running Automatic
```

In MDAV, the settings related to malware (virus and threat protection) are as follows:
* Real-time protection
* Dev Drive protection
* Cloud-delivered protection
* Tamper protection

---

### ETW Providers
| ETW Provider Name                             | ETW Provider GUID                         |
|:----------------------------------------------|:------------------------------------------|
| Microsoft-Antimalware-AMFilter                | cfeb0608-330e-4410-b00d-56d8da9986e6      |
| Microsoft-Antimalware-Engine                  | 0a002690-3839-4e3a-b3b6-96d8df868d99      |
| Microsoft-Antimalware-Engine-Instrumentation  | 68621c25-df8d-4a6b-aabc-19a22e296a7c      |
| Microsoft-Antimalware-NIS                     | 102aab0a-9d9c-4887-a860-55de33b96595      |
| Microsoft-Antimalware-Protection              | e4b70372-261f-4c54-8fa6-a5a7914d73da      |
| Microsoft-Antimalware-RTP                     | 8e92deef-5e17-413b-b927-59b2f06a3cfc      |
| Microsoft-Antimalware-Scan-Interface          | 2a576b87-09a7-520e-c21a-4942f0271d67      |
| Microsoft-Antimalware-Service                 | 751ef305-6c6e-4fed-b847-02ef79d26aef      |
| Microsoft-Antimalware-UacScan                 | d37e7910-79c8-57c4-da77-52bb646364cd      |

[REDACTED]

### Log File
By analyzing the Xref of the function `MpLogMessageWithTime`, we can infer subsequent actions and reduce analysis time.
#### **Log Message**
We confirmed that logs are being recorded via the `MpLogMessageWithTime` function in the `C:\ProgramData\Microsoft\Windows Defender\Support\MPLog-[TIME].log` file:

```cpp
v26 = (unsigned int)MpReinforceServiceAcls(0);
MpLogMessageWithTime(0, L"[Security] MpReinforceServiceAcls(). hr=%#lx", v26);
```

```
OS install time not retrieved: hr = 0x8007000d
Current time: 12/06/2025 12:43:43.931399500 UTC (111640 ms since boot)
2025-12-06T12:43:43.929Z MpEnsureProcessMitigationPolicy(0x7) returns 0x1
2025-12-06T12:43:43.929Z [HybridMode] isHybridModePolicyEnabled: 0, isVerifiedAndReputableTrustModeEnabled: 0
...
2025-12-06T12:43:43.960Z [Security] MpReinforceServiceAcls(). hr=0
...

```
#### **Initialization Process**

* [RbM] Rollback Manager
* [PlatUpd] Platform Updater
* [TS] Trouble Shooting
* **[TP] Tamper Protection**
* [Service] Service Initialization
* [N/A] Cache Manager
* [N/A] Trust Verification
  * [N/A] License File Verification
  * [Plugin] Plugin Verification
* **[RTP] Real-time Protection**
* [KSL] Kernel Service Layer
* [Engine] Load "Engine"
  * [N/A] Load `mpengine.dll`
  * **[N/A] Attack Surface Reduction**
  * **[N/A] Process Enumeration**
* [SCC] Security Center Connector
* [DLP] Data Loss Prevention
* **[Cloud] Cloud-delivered Protection**

### Reverse Engineering: `MpDefenderCoreService.exe`

[MpDefenderCoreService Reverse Engineering Report](./1_1_MpDefenderCoreService/)

Here are the functions traversed to access the initialization function of MpDefenderCoreService:

1. `entry` or `wmainCRTStartup`
2. `_scrt_common_main_seh`
3. `main`
4. `HrExeMain`
5. `ServiceCrtMain`
6. `CMpServiceCallback::vftable`
7. **`CMpServiceCallback::OnStartUp`**

Tracking the data named `PTR_WdConfigManagerInitialize_140143258` inside the `CMpServiceCallback::OnStartUp` function revealed various sensors from `MpWatchDog` such as:

* **WdAnomalyDetector**
* **CMpWdPerfCPUSensor**
* **CWdServiceCrashSensor**

They are sensors belonging to MpWatchDog and are responsible for the overall monitoring of Defender. In particular, sensors like `WdAnomalyDetector` and others can be considered closer to **behavior-based  monitoring components**. They perform a large volume of monitoring tasks such as **HeartBeat checks on the protected target processes (MsMpEng.exe)**, **HeartBeat checks on servers (such as ECS)**, and more. Additionally, when protected target processes terminate or crash based on behavior (CrashSensor), it appears that they immediately report this and attempt to restore or restart the affected service.
Based on the analysis of those sensors and other `MpDefenderCoreService` components, the discovered sensors are:

* CrashSensor
* CpuSensor
* MemorySensor
* DiskSensor

These 4 sensors or more in `MpDefenderCoreService` are responsible for monitoring system resources and stability, specifically targeting the MsMpEng.exe process, as configured through the function `MpWatchDog::WdConfigManager::PopulateMonitoredTargets`.
**In conclusion, `MpDefenderCoreService.exe` is responsible for the overall stability, performance enhancement, and process protection of Defender, among other functions.**

### Reverse Engineering: `MsMpEng.exe`

[MsMpEng Reverse Engineering Report](./1_2_MsMpEng/)


The entry point of MsMpEng.exe is closely related to MpDefenderCoreService. First, MsMpEng.exe loads **`mpsvc.dll`** via `MpCheckPlatformUpdate` → `LoadMpSvcFrom`. Subsequently, it calls `ServiceCrtMain` from that DLL. This function receives CMpServiceCallback from MpDefenderCoreService and calls CMpServiceCallback::OnStartUp. Through this, MsMpEng.exe ensures that Defender checks for updates upon startup and **initializes and coordinates MpDefenderCoreService via the shared mpsvc.dll service framework**.

```cpp
long LoadMpSvcFrom(HMODULE *hmodule,wchar_t *param_2,uint param_3) {
    uVar3 = (ulong)param_2;
    library_obj = (HMODULE)0x0;
    pWCHAR_0x0 = (wchar_t *)0x0;
    lVar1 = CommonUtil::NewSprintfW(
        &pWCHAR_0x0,
        L"%ls\\mpsvc.dll"
    );
    target_library = pWCHAR_0x0;
    ...
    lVar1 = CommonUtil::UtilLoadLibraryEx(
        &library_obj,
        target_library,
        0
    );
    hLibModule = library_obj;
    ...
    // LAB_14000890d:
    *hmodule = hLibModule;
    ...
}
```

### Reverse Engineering: `mpsvc.dll`
[MpSvc Reverse Engineering Report](./1_5_mpsvc/)

The primary purpose of `MpSvc.dll` is to load, initialize, and execute Defender's plugins. Currently identified initialization-related functionalities include Real-time Protection, ETW, AMSI, and the "Engine". `InitMpService` and `InitMpServiceAsync` are responsible for initializing and executing these functions, serving as the main entry points.

```
InitMpServiceAsync
├── TurnOnRtpIfApplicable
└── InitPluginModules
    └── InitPluginModule
```

```cpp
v80 = &g_RTPPlugin; // Real Time Protection Plugin
v23 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginShutdown");
v24 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginSetEngine");
v25 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginReportThreadStatus");
v26 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetState");
...
```

```
InitMpServiceAsync
└── EnableIOAVWorker
```

```cpp
MpLogMessageWithTime(0, (__int64)L"[Service] %ls AMSI registration ...", v28);
v51 = UtilUpdateRegistrationKey(
    (HKEY *)0xFFFFFFFF80000002LL,
    (wchar_t *)L"Software\\Microsoft\\AMSI\\Providers",
    v4,
    cbSecurityDescriptor,
    0);
...
```

### Reverse Engineering: `mprtp.dll`
[MpRtp Reverse Engineering Report](./research/mprtp.dll/README.md)

```
RealtimeProtection::CAgentsManager::Initialize
├── RealtimeProtection::NewFileSystemAgent
|   └── RealtimeProtection::CFileSystemAgent::CFileSystemAgent
|       ├── RealtimeProtection::IFileSystemRequestHandler
|       └── RealtimeProtection::IAsyncFileNotificationHandler
├── RealtimeProtection::NewRegistryAgent
|   └── RealtimeProtection::CRegistryAgent::CRegistryAgent
|       └── RealtimeProtection::IRegistryRequestHandler
├── RealtimeProtection::NewProcessAgent
|   └── RealtimeProtection::CProcessAgent::CProcessAgent
|       └── RealtimeProtection::IProcessRequestHandler
└── RealtimeProtection::NewWmiAgent
    └── RealtimeProtection::CWmiAgent::CWmiAgent
        └── N/A
```

### Reverse Engineering: `MpDetours.dll`

[MpDetours Reverse Engineering Report](./1_3_MpDetours/)

Below are the target functions that `MpDetours.dll` hooks using `Detours`:

* **user32.dll**
    * `OpenClipboard` → `MpClipboardDetours::MpDetoursOpenClipboard`
    * `SetClipboardData` → `MpClipboardDetours::MpDetoursSetClipboardData`
    * `GetClipboardData` → `MpClipboardDetours::MpDetoursGetClipboardData`
    * `CloseClipboard` → `MpClipboardDetours::MpDetoursCloseClipboard`
    * `EmptyClipboard` → `MpClipboardDetours::MpDetoursEmptyClipboard`
    * `IsClipboardFormatAvailable` → `MpClipboardDetours::MpDetoursIsClipboardFormatAvailable`
    * `CountClipboardFormats` → `MpClipboardDetours::MpDetoursCountClipboardFormats`
    * `EnumClipboardFormats` → `MpClipboardDetours::MpDetoursEnumClipboardFormats`
    * `GetPriorityClipboardFormat` → `MpClipboardDetours::MpDetoursGetPriorityClipboardFormat`
    * `GetUpdatedClipboardFormats` → `MpClipboardDetours::MpDetoursGetUpdatedClipboardFormats`
* **ole32.dll**
    * `OleSetClipboard` → `MpClipboardDetours::MpDetoursOleSetClipboard`
    * `OleFlushClipboard` → `MpClipboardDetours::MpDetoursOleFlushClipboard`
    * `DoDragDrop` → `MpDetoursDoDragDrop`
* **kernelbase.dll**
    * `CopyFileExW` → `MpDetoursCopyFileExW`
    * `CopyFile2` → `MpDetoursCopyFile2`
* **winspool.drv**
    * `StartDocPrinterW` → `MpPrintDetours::MpDetoursStartDocPrinter`
    * `EndDocPrinter` → `MpPrintDetours::MpDetoursEndDocPrinter`
    * `StartPagePrinter` → `MpPrintDetours::MpDetoursStartPagePrinter`
    * `EndPagePrinter` → `MpPrintDetours::MpDetoursEndPagePrinter`
    * `WritePrinter` → `MpPrintDetours::MpDetoursWritePrinter`
    * `DocumentEvent` → `MpPrintDetours::MpDetoursDocumentEvent`
    * `StartDocDlgW` → `MpPrintDetours::MpDetoursStartDocDlg`


## In-Scope Security Features

### Real-time Protection
Real-time Protection is extremely difficult to analyze (there are hundreds of vftable initialization paths, all of which are hard to track), so after performing a certain level of analysis, the functionality was inferred.
Located In:

* `MpLog-[DATE].log`
* `mprtp.dll`

---

#### **File Real-time Protection**
`RealtimeProtection::CFileSystemAgent`

1. DLP (Data Loss Prevention) access inspection and detection
2. Volume / boot sector inspection and detection
3. Real-time file modification detection

#### **Process Real-time Protection**
`RealtimeProtection::CProcessAgent`

1. Detours-based user-mode hooking inspection and detection
2. Direct process inspection (handle-based) inspection and detection
3. Thread inspection and detection
4. DLL inspection and detection

#### **Registry**
`RealtimeProtection::CRegistryAgent` (provides detection context and support)

1. Provides registry event context

#### **WMI**
`RealtimeProtection::CWmiAgent` (provides detection context and support)

1. WMI real-time monitoring sensor

**The information above is not definitive.**

### Tamper Protection
`MpDefenderCoreService`

* Installation location verification
* Protection of MsMpEng process
* Performance monitoring
* Heartbeat monitoring

`mpsvc`
* Digital signature verification of additional components

### Cloud-delivered Protection
[REDACTED]
## Sub-Scope Security Features
### Attack Surface Reduction
Located In:
* `MpLog-[DATE].log`
---
* Block use of copied or impersonated system tools
* Block executable files from running unless they meet a prevalence, age, or trusted list criteria
* Block credential stealing from the Windows local security authority subsystem (lsass.exe)
* Block Office applications from injecting code into other processes
* Controlled folder access
* Block untrusted and unsigned processes that run from USB
* Block Adobe Reader from creating child processes
* Block Office applications from creating executable content
* Block Webshell creation for Servers
* Block Office communication application from creating child processes
* Block Win32 API calls from Office macro
* Block abuse of in-the-wild exploited vulnerable signed drivers
* Block all Office applications from creating child processes
* Use advanced protection against ransomware
* Block Process Creations originating from PSExec & WMI commands
* Block Launching of executable content from email attachment
* Block JavaScript or VBScript from launching downloaded executable content
* Block persistence through WMI event subscription
* Block rebooting machine in Safe Mode
* Block execution of potentially obfuscated scripts
### MpEngine Emulation
* [Windows Offender: Reverse Engineering Windows Defender's Antivirus Emulator](https://i.blackhat.com/us-18/Thu-August-9/us-18-Bulazel-Windows-Offender-Reverse-Engineering-Windows-Defenders-Antivirus-Emulator.pdf)
* [Recon 2018 - Reverse Engineering Windows Defender Part II](https://www.youtube.com/watch?v=ikEaPPyGIgk)
* [Recon 2018 Brussels - Reverse Engineering Windows Defender’s JavaScript Engine](https://www.youtube.com/watch?v=yrFVvrX0jgQ)
* [Black Hat USA 2018 - Windows Offender Reverse Engineering Windows Defender's Antivirus Emulator](https://www.youtube.com/watch?v=LvW68czaEGs)
## MDIE Stages & Techniques
[REDACTED]
## References
* [Advanced technologies at the core of Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav)
* [Engineering detection around Microsoft Defender](https://blog.sekoia.io/engineering-detection-around-microsoft-defender/)
* [Microsoft Defender Antivirus full scan considerations and best practices](https://learn.microsoft.com/en-us/defender-endpoint/mdav-scan-best-practices)
* [AMSI.fail - PowerShell AMSI Disable Script Generator](https://amsi.fail/)
* [Microsoft Defender Antivirus in Windows Overview](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows)
* [Requirements for Microsoft Defender Antivirus to run in passive mode](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility#requirements-for-microsoft-defender-antivirus-to-run-in-passive-mode)
* [Better know a data source: Antimalware Scan Interface](https://redcanary.com/blog/threat-detection/better-know-a-data-source/amsi/)
* [An unexpected journey into Microsoft Defender's signature World](https://key08.com/usr/uploads/2024/08/363846053.pdf)
* [Windows Offender: Reverse Engineering Windows Defender's Antivirus Emulator](https://i.blackhat.com/us-18/Thu-August-9/us-18-Bulazel-Windows-Offender-Reverse-Engineering-Windows-Defenders-Antivirus-Emulator.pdf)
* [Recon 2018 - Reverse Engineering Windows Defender Part II](https://www.youtube.com/watch?v=ikEaPPyGIgk)
* [Recon 2018 Brussels - Reverse Engineering Windows Defender’s JavaScript Engine](https://www.youtube.com/watch?v=yrFVvrX0jgQ)
* [Black Hat USA 2018 - Windows Offender Reverse Engineering Windows Defender's Antivirus Emulator](https://www.youtube.com/watch?v=LvW68czaEGs)
* [Gurpreet06/ETW-Patcher](https://github.com/Gurpreet06/ETW-Patcher/)