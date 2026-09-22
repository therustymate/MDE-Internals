# 1.3 MpDetours

## `MpDetoursHookAll`
```cpp
__int64 __fastcall MpDetoursHookAll(bool a1)
{
  __int64 v2; // rdi
  HANDLE ProcessHeap; // rax
  _QWORD *i; // rbx
  int v5; // eax
  int v6; // ebx
  _QWORD *v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // r9
  DWORD LastError_0; // eax
  _QWORD *v11; // rdx
  const char *v13; // rdx
  DWORD flOldProtect; // [rsp+20h] [rbp-39h] BYREF
  DWORD CurrentThreadId; // [rsp+28h] [rbp-31h] BYREF
  char v16; // [rsp+2Ch] [rbp-2Dh]
  __int64 v17; // [rsp+30h] [rbp-29h]
  _BYTE pExceptionObject[24]; // [rsp+38h] [rbp-21h] BYREF
  _QWORD v19[7]; // [rsp+50h] [rbp-9h] BYREF
  _QWORD *v20; // [rsp+88h] [rbp+2Fh]

  v2 = *((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)tls_index);
  v17 = *(_QWORD *)(v2 + 16);
  ProcessHeap = CppSwitchHeapScope::s_defaultHeap;
  if ( !CppSwitchHeapScope::s_defaultHeap )
    ProcessHeap = GetProcessHeap();
  *(_QWORD *)(v2 + 16) = ProcessHeap;
  CurrentThreadId = GetCurrentThreadId();
  v16 = 0;
  if ( dword_180023890 || _InterlockedCompareExchange(&dword_180023890, GetCurrentThreadId_0(), 0) )
  {
    LastError_0 = 4317;
    goto LABEL_40;
  }
  qword_180023858 = 0;
  qword_180023868 = 0;
  qword_180023880 = 0;
  for ( i = lpBaseAddress; i; i = (_QWORD *)i[1] )
  {
    flOldProtect = 0;
    if ( !VirtualProtect(i, 0x10000u, 0x40u, &flOldProtect) )
    {
      LastError_0 = GetLastError_0();
      dword_180023894 = LastError_0;
      if ( !LastError_0 )
        goto LABEL_10;
LABEL_40:
      Trace((char **)"DetourTransactionBegin failed, err:%u\n", LastError_0);
      std::runtime_error::runtime_error((std::runtime_error *)pExceptionObject, v13);
      CxxThrowException(pExceptionObject, (_ThrowInfo *)&TI2_AVruntime_error_std__);
    }
  }
  dword_180023894 = 0;
LABEL_10:
  if ( HIBYTE(word_180022CCC) )
  {
    v5 = MpDetoursHookFunctions((struct DetourInfos *)&g_DetourTable, 0);
    v6 = v5;
    if ( v5 < 0 )
    {
      v8 = 16;
      goto LABEL_15;
    }
  }
  if ( (_BYTE)word_180022CCF )
  {
    v5 = MpDetoursHookFunctions((struct DetourInfos *)&g_DetourCopyFileTable, 0);
    v6 = v5;
    if ( v5 < 0 )
    {
      v8 = 17;
      goto LABEL_15;
    }
  }
  if ( !byte_180022CCE )
  {
    if ( (_BYTE)word_180022CCC )
    {
      v5 = MpDetoursHookFunctions((struct DetourInfos *)&g_DetourPrintTable, a1);
      v6 = v5;
      if ( a1 && v5 < 0 )
      {
        v8 = 18;
LABEL_15:
        v9 = (unsigned int)v5;
      }
    }
  }
  v19[0] = off_18001B090;
  v20 = v19;
  v6 = DetourTransaction::Commit(&CurrentThreadId, v19);
  if ( v20 )
  {
    v11 = v19;
    LOBYTE(v11) = v20 != v19;
    (*(void (__fastcall **)(_QWORD *, _QWORD *))(*v20 + 32LL))(v20, v11);
  }
  if ( v6 < 0 )
  {
    v8 = 19;
    v9 = (unsigned int)v6;
  }
  *(_QWORD *)(v2 + 16) = v17;
  return 0;
}
```

Tracking `MpDetoursHookFunctions`:
```cpp
v5 = MpDetoursHookFunctions((struct DetourInfos *)&g_DetourTable, 0);           // user32.dll
v5 = MpDetoursHookFunctions((struct DetourInfos *)&g_DetourCopyFileTable, 0);   // kernelbase.dll
v5 = MpDetoursHookFunctions((struct DetourInfos *)&g_DetourPrintTable, a1);     // winspool.drv
```

```
.data:0000000180022220 ; struct DetourInfos g_DetourTable
.data:0000000180022220 ?g_DetourTable@@3PAUDetourInfos@@A dq offset aUser32Dll_0
.data:0000000180022220                                         ; DATA XREF: MpDetoursHookAll(bool)+EE↑o
.data:0000000180022220                                         ; "user32.dll"
```

```
.data:0000000180022180 ; struct DetourInfos g_DetourCopyFileTable
.data:0000000180022180 ?g_DetourCopyFileTable@@3PAUDetourInfos@@A dq offset aKernelbaseDll
.data:0000000180022180                                         ; DATA XREF: MpDetoursHookAll(bool)+14E↑o
.data:0000000180022180                                         ; "kernelbase.dll"
```

```
.data:0000000180022000 ; struct DetourInfos g_DetourPrintTable
.data:0000000180022000 ?g_DetourPrintTable@@3PAUDetourInfos@@A dq offset LibFileName
.data:0000000180022000                                         ; DATA XREF: MpDetoursHookAll(bool)+19D↑o
.data:0000000180022000                                         ; MpDetoursInitialize(HINSTANCE__ *)+11B↑o
.data:0000000180022000                                         ; "winspool.drv"
```

Hooked Functions:

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