# 1.4 MpRTP

## `RealtimeProtection::CAgentsManager::Initialize`
`RealtimeProtection::CAgentsManager::Initialize` is a function that initializes all real-time detection modules. The functions it calls are as follows:

* `RealtimeProtection::NewFileSystemAgent`
* `RealtimeProtection::NewRegistryAgent`
* `RealtimeProtection::NewProcessAgent`
* `RealtimeProtection::NewWmiAgent`

It calls file, registry, process, and WMI agents. These functions are highly likely to be initialization functions that perform tasks to start real-time detection.

### RealtimeProtection Agents

```
RealtimeProtection::NewFileSystemAgent
└── RealtimeProtection::CFileSystemAgent::CFileSystemAgent
```

```cpp
RealtimeProtection::CFileSystemAgent *__fastcall RealtimeProtection::CFileSystemAgent::CFileSystemAgent(
        RealtimeProtection::CFileSystemAgent *this)
{
  *(_QWORD *)this = &RealtimeProtection::CFileSystemAgent::`vbtable'{for `CommonUtil::CRefVirtualObject'};
  *((_QWORD *)this + 25) = &RealtimeProtection::CProcessAgent::`vbtable'{for `RealtimeProtection::IProtectionAgentBase'};
  *((_QWORD *)this + 28) = &RealtimeProtection::CRegistryAgent::`vbtable'{for `RealtimeProtection::IRtpAgent'};
  *((_QWORD *)this + 31) = &RealtimeProtection::CProcessAgent::`vbtable'{for `RealtimeProtection::IProcessRequestHandler'};
  *((_QWORD *)this + 34) = &RealtimeProtection::CFileSystemAgent::`vbtable'{for `RealtimeProtection::IAsyncFileNotificationHandler'};
  *((_QWORD *)this + 22) = &CommonUtil::IRefObject::`vftable';
  *((_QWORD *)this + 24) = &RealtimeProtection::IProtectionAgentBase::`vftable'{for `RealtimeProtection::IProtectionAgentBase'};
  *(_QWORD *)((char *)this + *(int *)(*((_QWORD *)this + 25) + 4LL) + 200) = &RealtimeProtection::IProtectionAgentBase::`vftable'{for `CommonUtil::IRefObject'};
  *((_QWORD *)this + 27) = &RealtimeProtection::IRtpAgent::`vftable';
  *(_QWORD *)((char *)this + *(int *)(*((_QWORD *)this + 28) + 4LL) + 224) = &RealtimeProtection::IRtpAgent::`vftable'{for `CommonUtil::IRefObject'};
  *(_QWORD *)((char *)this + *(int *)(*((_QWORD *)this + 28) + 8LL) + 224) = &RealtimeProtection::IRtpAgent::`vftable'{for `RealtimeProtection::IProtectionAgentBase'};
  *((_QWORD *)this + 30) = &RealtimeProtection::IFileSystemRequestHandler::`vftable'{for `RealtimeProtection::IFileSystemRequestHandler'};
  *(_QWORD *)((char *)this + *(int *)(*((_QWORD *)this + 31) + 4LL) + 248) = &RealtimeProtection::IFileSystemRequestHandler::`vftable'{for `CommonUtil::IRefObject'};
  *((_QWORD *)this + 33) = &RealtimeProtection::IAsyncFileNotificationHandler::`vftable'{for `RealtimeProtection::IAsyncFileNotificationHandler'};
  *(_QWORD *)((char *)this + *(int *)(*((_QWORD *)this + 34) + 4LL) + 272) = &RealtimeProtection::IAsyncFileNotificationHandler::`vftable'{for `CommonUtil::IRefObject'};
  *(_QWORD *)((char *)this + *(int *)(*(_QWORD *)this + 4LL)) = &CommonUtil::CRefVirtualObject::`vftable';
  *(_DWORD *)((char *)this + *(int *)(*(_QWORD *)this + 4LL) - 4) = *(_DWORD *)(*(_QWORD *)this + 4LL) - 24;
  *((_DWORD *)this + 2) = 0;
  *(_QWORD *)((char *)this + *(int *)(*(_QWORD *)this + 4LL)) = &RealtimeProtection::CFileSystemAgent::`vftable'{for `CommonUtil::CRefVirtualObject'};
  *(_QWORD *)((char *)this + *(int *)(*(_QWORD *)this + 8LL)) = &RealtimeProtection::CFileSystemAgent::`vftable'{for `RealtimeProtection::IProtectionAgentBase'};
  *(_QWORD *)((char *)this + *(int *)(*(_QWORD *)this + 12LL)) = &RealtimeProtection::CFileSystemAgent::`vftable'{for `RealtimeProtection::IRtpAgent'};
  *(_QWORD *)((char *)this + *(int *)(*(_QWORD *)this + 16LL)) = &RealtimeProtection::CFileSystemAgent::`vftable'{for `RealtimeProtection::IFileSystemRequestHandler'};
  *(_QWORD *)((char *)this + *(int *)(*(_QWORD *)this + 20LL)) = &RealtimeProtection::CFileSystemAgent::`vftable'{for `RealtimeProtection::IAsyncFileNotificationHandler'};
  *(_DWORD *)((char *)this + *(int *)(*(_QWORD *)this + 4LL) - 4) = *(_DWORD *)(*(_QWORD *)this + 4LL) - 176;
  *(_DWORD *)((char *)this + *(int *)(*(_QWORD *)this + 8LL) - 4) = *(_DWORD *)(*(_QWORD *)this + 8LL) - 192;
  *(_DWORD *)((char *)this + *(int *)(*(_QWORD *)this + 12LL) - 4) = *(_DWORD *)(*(_QWORD *)this + 12LL) - 216;
  *(_DWORD *)((char *)this + *(int *)(*(_QWORD *)this + 16LL) - 4) = *(_DWORD *)(*(_QWORD *)this + 16LL) - 240;
  *(_DWORD *)((char *)this + *(int *)(*(_QWORD *)this + 20LL) - 4) = *(_DWORD *)(*(_QWORD *)this + 20LL) - 264;
  *((_DWORD *)this + 4) = 1;
  CommonUtil::CMpReadWriteLock::CMpReadWriteLock((RealtimeProtection::CFileSystemAgent *)((char *)this + 24));
  *((_QWORD *)this + 11) = 0;
  CommonUtil::CMpReadWriteLock::CMpReadWriteLock((RealtimeProtection::CFileSystemAgent *)((char *)this + 96));
  *((_DWORD *)this + 40) = 0;
  RealtimeProtection::CFileSystemAgent::InitializeSyncDssCapLimitCounter(this);
  return this;
}
```

These appear to be vftable constructors for file system detection, and the common functions in all agents are as follows:

* `CommonUtil::CRefVirtualObject`
* `RealtimeProtection::IProtectionAgentBase`
* `RealtimeProtection::IRtpAgent`

The investigation confirmed that all four identified agents are vftable constructors.

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
└──  RealtimeProtection::NewWmiAgent
    └── RealtimeProtection::CWmiAgent::CWmiAgent
        └── N/A
```

Then, it requests a filter using the four IRtpAgent values as parameters, as shown below:

```cpp
CommonUtil::AutoRef<RealtimeProtection::IFilterRequest>::~AutoRef<RealtimeProtection::IFilterRequest>(&inited);
CommonUtil::AutoRef<RealtimeProtection::IFilterRequest>::~AutoRef<RealtimeProtection::IFilterRequest>(&v20);
CommonUtil::AutoRef<RealtimeProtection::IFilterRequest>::~AutoRef<RealtimeProtection::IFilterRequest>(&v21);
CommonUtil::AutoRef<RealtimeProtection::IFilterRequest>::~AutoRef<RealtimeProtection::IFilterRequest>(&v22);
```







---

## Possible Real-time Protection Classes

### File System

* `RealtimeProtection::CFileSystemAgent`
* `RealtimeProtection::CFileSystemWatcher`
* `RealtimeProtection::CFileSystemNotification`
* `RealtimeProtection::CFileSystemScanRequest`
* `RealtimeProtection::CAutoDestroyFileSystemScanRequest`

### Process

* `RealtimeProtection::CProcessAgent`
* `RealtimeProtection::CProcessWatcher`
* `RealtimeProtection::CProcessNotification` / `CProcessNotificationWorkItem`
* `RealtimeProtection::CRtpProcessInfoMap` / `ProcessInfoMapEntry`

### Registry

* `RealtimeProtection::CRegistryAgent`
* `RealtimeProtection::CRegistryWatcher`
* `RealtimeProtection::CRegNotificationManager`
* `RealtimeProtection::CRegistryNotification` / `CRegistryNotificationSyncWrapper`

### WMI

* `RealtimeProtection::CWmiAgent`
* `RealtimeProtection::CWmiWatcher` / `CWmiEventAsyncWatcher` / `CWmiEventSyncWatcher`
* `RealtimeProtection::CWmiEventSink` / `CWmiEventSinkRefCount`

---

### Alert/Identification

* `RealtimeProtection::CWorkItemThreatDetection`
* `RealtimeProtection::CRtpThreatDetectionNotification`
* `RealtimeProtection::CWorkItemSuspiciousDetectionNotification`
* `RealtimeProtection::CAutoFreeSuspiciousDetectionData`

---

### Mini-Filter

* `RealtimeProtection::CRtpFilterManager` / `CRtpFilterManagerBase`
* `RealtimeProtection::CThreadPoolIoFilterPort`
* `RealtimeProtection::CThreadPoolIoPortHandler` / `CThreadPoolIoPortHandlerBase`
* `RealtimeProtection::CThreadPoolIoFilterRequest`
* `RealtimeProtection::CFileFilterRequest` / `CFileFilterReply`
* `RealtimeProtection::CAsynchronousFilterRequest` / `CAsynchronousFilterReply`
* `RealtimeProtection::IFilterRequest / IFilterRequestHandler`