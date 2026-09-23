# 2.1 General Metadata

## Versions & Descriptions

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
} | column -t -s $'\t'
```

| File                      | File Version          | Description                                                                   |
|---------------------------|-----------------------|-------------------------------------------------------------------------------|
| SenseNdr.exe              | 4.0.0.15              | Windows Defender Advanced Threat Protection - Sense NDR module                |
| SenseSampleUploader.exe   | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection Sample Upload module              |
| SenseTracer.exe           | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection Sense Event Tracer module         |
| SenseTVM.exe              | 1.4.0-0               | Windows Defender Advanced Threat Protection Sense TVM module                  |
| WATPCSP.dll               | 10.8804.27858.1000    | Windows Defender Advanced Threat Protection Manageability module              |
| aadrt.dll                 | 1.1009.0.0            | AAD Runtime                                                                   |
| MipDlp.dll                | 1.0.0.0               | Microsoft Defender RMS Label Protection DLL                                   |
| MsSense.dll               | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection Sense Library                     |
| MsSense.exe               | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection Service Executable                |
| RunPsScript.dll           | 10.8805.27858.1000    | Run PS Script                                                                 |
| SenseAP.exe               | 0.3.9-4               | Windows Defender Advanced Threat Protection - Sense AP module                 |
| SenseAPToast.exe          | 0.1.0-11              | Windows Defender Advanced Threat Protection - Sense AP notification module    |
| SenseCM.exe               | 2.1037.0.0            | Windows Defender Advanced Threat Protection Security Configuration Module     |
| SenseDlpProcessor.exe     | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection Sense Dlp Processor module        |
| SenseGPParser.exe         | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection Sense Group Policy module         |
| SenseIdentity.exe         | 3.0.6-405             | Windows Defender Advanced Threat Protection Sense Identity module             |
| SenseImdsCollector.exe    | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection IMDSCollector module              |
| SenseIR.exe               | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection Sense IR module                   |


```bash
$ cd ./Classification
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
} | column -t -s $'\t'

```

| File                      | File Version          | Description                                                   |
|---------------------------|-----------------------|---------------------------------------------------------------|
| cmicarabicwordbreaker.dll | 1.0.0.1               | `TODO: <File description>`                                    |
| mce.dll                   | 15.20.8835.000        | Classification Engine Implementation                          |
| MpGear.dll                | 1.1.25050.5           | Microsoft Antimalware Utility Library                         |
| OPCTextExtractorWin.dll   | 1.1001.0.0            | OPC files text extractor                                      |
| SenseCE.exe               | 10.8805.27858.1000    | Windows Defender Advanced Threat Protection Sense CE module   |

## File Dump

```bash
$ eza -l -T --no-permissions --no-user
   - 22 Sep 12:01 .
1.6M 21 Nov  2025 ├── aadrt.dll
   - 21 Sep 13:12 ├── Classification
1.2M 21 Nov  2025 │   ├── cmicarabicwordbreaker.dll
   - 21 Nov  2025 │   ├── Dprt
6.1M  7 Mar  2025 │   │   ├── DocumentFormat.OpenXml.dll
483k 21 Nov  2025 │   │   ├── Google.Protobuf.dll
215k 21 Nov  2025 │   │   ├── ICSharpCode.SharpZipLib.dll
236k 21 Nov  2025 │   │   ├── Microsoft.Ceres.ContentUnderstanding.SemanticDocument.dll
122k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.External.ExternalClient.dll
 22k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.External.ExternalCore.dll
 19k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.External.FormatDetectionClient.dll
 44k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Common.Configuration.dll
 46k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Common.Interop.dll
129k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Common.JpegInterop.dll
 52k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Common.Metro.dll
 23k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Common.Rms.dll
 21k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Designer.dll
175k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Docx.dll
 21k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Dwg.dll
 27k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.EncOffMetro.dll
199k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.ExcelGeneric.dll
 47k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.ExcelLegacy.dll
157k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Filter.dll
 60k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Fluid.dll
 21k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Gif.dll
 20k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.GZip.dll
445k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Html.dll
 25k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Image.dll
 19k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.ImageWithoutMeta.dll
 20k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Jpeg.dll
 39k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Json.dll
 27k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Lnk.dll
 35k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Mime.dll
 30k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Msg.dll
 96k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Ocr.dll
 32k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.OfficeXml.dll
 54k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.OneNote.dll
4.5M 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Pdf.dll
 25k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.PFile.dll
 20k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Plaintext.dll
 28k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Png.dll
 39k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.PointPublishing.dll
165k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Pptx.dll
 19k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.RmsOfficeLegacy.dll
1.2M 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Rtf.dll
 45k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.SevenZip.dll
 24k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.SimpleXml.dll
 21k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Tar.dll
 21k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Vtt.dll
 28k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Xps.dll
 28k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.FormatHandlers.Zip.dll
184k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.Runtime.Client.dll
 59k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.Runtime.Common.dll
203k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.Runtime.Core.dll
 77k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.Runtime.FormatDetector.dll
 66k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.Runtime.FormatHandler.dll
 20k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.Runtime.LanguageDetector.dll
 21k 21 Nov  2025 │   │   ├── Microsoft.Ceres.DocParsing.Runtime.Plugin.dll
863k 21 Nov  2025 │   │   ├── MimeKitLite.dll
 11k 21 Nov  2025 │   │   ├── NativeDocumentParsers.cat
 40k 21 Nov  2025 │   │   ├── NativeDocumentParsers.dll
759k 21 Nov  2025 │   │   ├── NativeDprt.dll
710k 21 Nov  2025 │   │   ├── Newtonsoft.Json.dll
4.5M 21 Nov  2025 │   │   ├── pdfium.dll
195k 21 Nov  2025 │   │   ├── RtfPipe.dll
800k 21 Nov  2025 │   │   ├── SkiaSharp.dll
 21k  7 Mar  2025 │   │   ├── System.Buffers.dll
253k 21 Nov  2025 │   │   ├── System.Collections.Immutable.dll
 53k 21 Nov  2025 │   │   ├── System.Drawing.Common.dll
142k  7 Mar  2025 │   │   ├── System.Memory.dll
116k  7 Mar  2025 │   │   ├── System.Numerics.Vectors.dll
 18k  7 Mar  2025 │   │   ├── System.Runtime.CompilerServices.Unsafe.dll
 79k  7 Mar  2025 │   │   ├── System.Text.Encodings.Web.dll
 91k 21 Nov  2025 │   │   ├── ThirdPartyNotice.txt
261k 21 Nov  2025 │   │   ├── UtfUnknown.dll
   - 21 Nov  2025 │   │   └── x64
1.9M 21 Nov  2025 │   │       └── 7z.dll
3.6M 21 Nov  2025 │   ├── fastmorph.dll
2.3M 21 Nov  2025 │   ├── korwbrkr.dll
6.7M 21 Nov  2025 │   ├── mce.dll
679k 21 Nov  2025 │   ├── MpGear.dll
1.3M 21 Nov  2025 │   ├── mswb7.dll
3.4M 21 Nov  2025 │   ├── mswb7001e.dll
3.4M 21 Nov  2025 │   ├── mswb70011.dll
3.4M 21 Nov  2025 │   ├── mswb70011_v2.dll
3.4M 21 Nov  2025 │   ├── mswb70404.dll
3.4M 21 Nov  2025 │   ├── mswb70804.dll
2.6M 21 Nov  2025 │   ├── nl7data001e.dll
 12M 21 Nov  2025 │   ├── nl7data0011.dll
 12M 21 Nov  2025 │   ├── nl7data0011_v2.dll
4.7M 21 Nov  2025 │   ├── nl7data0404.dll
5.7M 21 Nov  2025 │   ├── nl7data0804.dll
985k 21 Nov  2025 │   ├── nl7lexicons001e.dll
3.7M 21 Nov  2025 │   ├── nl7lexicons0011.dll
3.7M 21 Nov  2025 │   ├── nl7lexicons0011_v2.dll
1.2M 21 Nov  2025 │   ├── nl7lexicons0404.dll
1.2M 21 Nov  2025 │   ├── nl7lexicons0804.dll
2.1M 21 Nov  2025 │   ├── nl7models001e.dll
9.1M 21 Nov  2025 │   ├── nl7models0011.dll
9.1M 21 Nov  2025 │   ├── nl7models0011_v2.dll
 12M 21 Nov  2025 │   ├── nl7models0404.dll
4.3M 21 Nov  2025 │   ├── nl7models0804.dll
6.1k  1 Apr  2024 │   ├── NOTICE.txt
1.1M 21 Nov  2025 │   ├── npe.dll
4.7M 21 Nov  2025 │   ├── OPCTextExtractorWin.dll
3.9M 21 Nov  2025 │   ├── SenseCE.exe
1.1k  7 Mar  2025 │   └── SenseCe.exe.config
   - 21 Nov  2025 ├── en-US
 51k 21 Nov  2025 │   └── MsSense.exe.mui
 87M 22 Sep 08:25 ├── MDE_RE.zip
9.3M 21 Nov  2025 ├── MipDlp.dll
 13M 21 Nov  2025 ├── MsSense.dll
803k 21 Nov  2025 ├── MsSense.exe
1.4M 21 Nov  2025 ├── RunPsScript.dll
3.6M 21 Nov  2025 ├── SenseAP.exe
3.2M 21 Nov  2025 ├── SenseAp.ThirdPartyNotice.txt
501k 21 Nov  2025 ├── SenseAPToast.exe
7.7M 21 Nov  2025 ├── SenseCM.exe
4.3M 21 Nov  2025 ├── SenseDlpProcessor.exe
399k 21 Nov  2025 ├── SenseGPParser.exe
3.9M 21 Nov  2025 ├── SenseIdentity.exe
1.0M 21 Nov  2025 ├── SenseImdsCollector.exe
5.6M 21 Nov  2025 ├── SenseIR.exe
 22M 21 Nov  2025 ├── SenseNdr.exe
2.9M 21 Nov  2025 ├── SenseSampleUploader.exe
4.5M 21 Nov  2025 ├── SenseTracer.exe
3.1M 21 Nov  2025 ├── SenseTVM.exe
 11k  1 Apr  2024 ├── ThirdPartyNotice
423k 21 Nov  2025 └── WATPCSP.dll
```