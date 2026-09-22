# 2.2 Dependencies

```bash
$ tree ./Classification/Dprt/ | grep -Ev "Microsoft|System|Native|directory|Third|Format"
./Classification/Dprt/
├── Google.Protobuf.dll
├── ICSharpCode.SharpZipLib.dll
├── MimeKitLite.dll
├── Newtonsoft.Json.dll
├── pdfium.dll
├── RtfPipe.dll
├── SkiaSharp.dll
├── UtfUnknown.dll
└── x64
    └── 7z.dll

2 directories, 72 files
```

| Dependency                | DLL                           | Repo / URL                                                                    |
|:--------------------------|:------------------------------|:------------------------------------------------------------------------------|
| Google Protocol Buffers   | Google.Protobuf.dll           | [protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf)       |
| SharpZipLib               | ICSharpCode.SharpZipLib.dll   | [icsharpcode/SharpZipLib](https://github.com/icsharpcode/SharpZipLib)         |
| MimeKit                   | MimeKitLite.dll               | [jstedfast/MimeKit](https://github.com/jstedfast/MimeKit)                     |
| Newtonsoft.Json           | Newtonsoft.Json.dll           | [JamesNK/Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json)         |
| PDFium                    | pdfium.dll                    | [pdfium/pdfium](https://pdfium.googlesource.com/pdfium/)                      |
| RtfPipe                   | RtfPipe.dll                   | [erdomke/RtfPipe](https://github.com/erdomke/RtfPipe)                         |
| SkiaSharp                 | SkiaSharp.dll                 | [mono/SkiaSharp](https://github.com/mono/SkiaSharp)                           |
| UTF-unknown               | UtfUnknown.dll                | [CharsetDetector/UTF-unknown](https://github.com/CharsetDetector/UTF-unknown) |
| 7zip                      | 7z.dll                        | [https://www.7-zip.org](https://www.7-zip.org/)                               |

```bash
$ file * | grep -Ev "Microsoft|System|Native|directory|Third|Format"
Google.Protobuf.dll:                PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly, 3 sections
ICSharpCode.SharpZipLib.dll:        PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly, 3 sections
MimeKitLite.dll:                    PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly, 3 sections
Newtonsoft.Json.dll:                PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly, 3 sections
pdfium.dll:                         PE32+ executable for MS Windows 5.02 (DLL), x86-64, 9 sections
RtfPipe.dll:                        PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly, 3 sections
SkiaSharp.dll:                      PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly, 3 sections
UtfUnknown.dll:                     PE32 executable for MS Windows 4.00 (DLL), Intel i386 Mono/.Net assembly, 3 sections

$ file ./x64/7z.dll
./x64/7z.dll:                       PE32+ executable for MS Windows 5.02 (DLL), x86-64, 6 sections
```

| DLL                               | File Type                                                                 |
|:----------------------------------|:--------------------------------------------------------------------------|
| Google.Protobuf.dll               | PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly  |
| ICSharpCode.SharpZipLib.dll       | PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly  |
| MimeKitLite.dll                   | PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly  |
| Newtonsoft.Json.dll               | PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly  |
| pdfium.dll                        | PE32+ executable for MS Windows 5.02 (DLL), x86-64                        |
| RtfPipe.dll                       | PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly  |
| SkiaSharp.dll                     | PE32 executable for MS Windows 6.00 (DLL), Intel i386 Mono/.Net assembly  |
| UtfUnknown.dll                    | PE32 executable for MS Windows 4.00 (DLL), Intel i386 Mono/.Net assembly  |
| 7z.dll                            | PE32+ executable for MS Windows 5.02 (DLL), x86-64                        |

```bash
$ {
    printf 'File\tCompany\tProduct\tFileVersion\tProductVersion\tDescription\n'

    find . -maxdepth 1 -type f \
        \( -iname '*.dll' -o -iname '*.exe' -o -iname '*.sys' \) \
        -print0 |
    xargs -0 -r exiftool -T \
        -FileName \
        -CompanyName \
        -ProductName \
        -FileVersion \
        -ProductVersion \
        -FileDescription
} | column -t -s $'\t' | grep -Ev "Microsoft|System|Native|directory|Third|Format"

```

| File                          | FileVersion   | Description               |
|-------------------------------|---------------|---------------------------|
| Google.Protobuf.dll           | 3.27.3.0      | Google Protocol Buffers   |
| ICSharpCode.SharpZipLib.dll   | 1.3.3.11      | ICSharpCode.SharpZipLib   |
| MimeKitLite.dll               | 4.3.0.0       | MimeKit                   |
| Newtonsoft.Json.dll           | 13.0.3.27908  | Json.NET .NET 4.5         |
| pdfium.dll                    | -             | -                         |
| RtfPipe.dll                   | 2.0.7677.4303 | RtfPipe                   |
| UtfUnknown.dll                | 2.0.664       | UTF Unknown               |
| 7z.dll                        | 24.09         | 7z Plugin                 |