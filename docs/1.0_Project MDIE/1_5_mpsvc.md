# 1.5 MpSVC

## Initialization Process


## InitMpService

```cpp
// Init vftable for CMpServiceCallback in mpsvc.dll
v8 = CommonUtil::CreateNewRefObject<CMpServiceCallback>(&this);
...
v12 = *this; // Set pointer
v13 = (*(__int64 (**)(void))(v12 + 24))(); // Call
```

```
ServiceCrtMain
└── ServiceCrtMainImpl
    └── CMpServiceCallback::OnStartup
        └── InitMpService
```

### ETW Provider Initialization
```cpp
LogInitializingComponent((wchar_t *)L"InitializeETWEventProviders");
McGenEventRegister_EventRegister(
    &Microsoft_Antimalware_Service, // {751EF305-6C6E-4FED-B847-02EF79D26AEF}
    McGenControlCallbackV2,
    &Microsoft_Antimalware_Service_Context,
    &Microsoft_Antimalware_Service_Context);
AddressOfEventSetInformation();
// CommonUtils Init
if ( (Microsoft_Antimalware_ServiceEnableBits & 1) != 0 )
    McGenEventWrite_EventWriteTransfer(&Microsoft_Antimalware_Service_Context, &ServiceSync_Start, v9, 1, v32);
`MpService::AccessMpServiceFactory'::`2'::gs_pfnMpCreateInstance = MpEncodeVoidPointer(MpServiceCreateInstance);
```

ETW Provider for `Microsoft-Antimalware-Service` is being Initialized.

### InitMpServiceAsync

```
ServiceCrtMain
└── ServiceCrtMainImpl
    └── CMpServiceCallback::OnAsyncStartup
        └── InitMpService
```

## Security Features

### Real-time Protection Initialization

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
v27 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginStop");
v28 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginSetState");
v29 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginSetUserInformation");
v30 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginFlushLogData");
v31 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginSignatureChange");
v32 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginNotifySetupProgress");
v33 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginIsSuspended");
v34 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginUpdateMonitoringInfo");
v35 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginUpdateMonitoringInfoEx");
v36 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginUpdateProcessTaintInfo");
v37 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginNotifyFeatureControlUpdated");
v38 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginQueryRtpMonitoringInfoEx");
v39 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginRegisterFriendlyProcess");
v40 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetHeartBeatData");
v41 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginConfigChange");
v42 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginUpdateFolderGuardData");
v43 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginUpdateModuleMonitorData");
v44 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginConfigSyncMonitoring");
v45 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginConfigDirectoryMonitoring");
v46 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetConfigOperations");
v47 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginSetDefaultConfigs");
v48 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginUpdateTPState");
v49 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginUpdateTPExclusionsState");
v50 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetTPRegs");
v51 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginFreeTPRegs");
v52 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginRefreshConfigsinRTP");
v53 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginCheckExclusion");
v54 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginRefreshPlatformKillbits");
v55 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginRefreshPlatformKillbitsEx");
v56 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetThreatCategory");
v57 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetThreatExecInfo");
v58 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetThreatInfo");
v59 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginSetDriverUnloadInProgress");
v60 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginNotifySessionStateChange");
v61 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginNotifyRpcServerStateChange");
v62 = GetProcAddress(*((HMODULE *)v80 + 1), (LPCSTR)"MpPluginGetCopyAcceleratorState");
v63 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginSendUserModeRegistryData");
v64 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginFilterManagerNotifyUpdatePlatformInProgress");
v65 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginSetHybridModeState");
v66 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginPurgeFilterCache");
v70 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetOSCopyAcceleratorStatus");
v71 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginGetDevVolumesState");
v75 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginQueryDevVolumeProtectionState");
v76 = GetProcAddress(*((HMODULE *)v80 + 1), "MpPluginUpdateProcessTaintInfo");
```

**`mprtp.dll` has the `Real-time Protection` feature**:
```cpp
v7 = CommonUtil::NewSprintfW((CommonUtil *)&lpLibFileName, (wchar_t **)L"%ls\\%ls", v82, L"mprtp.dll");
```

### AMSI Register
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

```
EnableIOAVWorker
├── Software\\Microsoft\\AMSI\\Providers
├── MpIsWindowsCobalt
|   └── Software\\Microsoft\\AMSI\\Providers2
├── Software\\Wow6432Node\\Microsoft\\AMSI\\Providers
└── MpIsWindowsCobalt
    └── Software\\Wow6432Node\\Microsoft\\AMSI\\Providers2
```