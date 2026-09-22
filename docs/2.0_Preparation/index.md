# Reverse Engineering Preparation

## Data Format Parsers
Below are the file format parsers that MDE can parse (based on MDE's dependency DLLs):

### Document & Text Formats

| DLL                  | Parsing Format             | File Extension          |
|----------------------|----------------------------|-------------------------|
| Pdf.dll              | PDF                        | .pdf                    |
| Docx.dll             | Word OOXML                 | .docx, .docm            |
| ExcelGeneric.dll     | Excel OOXML                | .xlsx, .xlsm, .xlsb     |
| ExcelLegacy.dll      | Excel Legacy               | .xls                    |
| Pptx.dll             | PowerPoint OOXML           | .pptx, .pptm            |
| Rtf.dll              | Rich Text Format           | .rtf                    |
| Html.dll             | HTML                       | .html, .htm             |
| Plaintext.dll        | Plain Text                 | .txt, .log              |
| SimpleXml.dll        | XML                        | .xml                    |
| Json.dll             | JSON                       | .json                   |
| OfficeXml.dll        | Office XML                 | .xml                    |
| OneNote.dll          | OneNote                    | .one                    |
| Xps.dll              | XPS                        | .xps, .oxps             |
| Dwg.dll              | AutoCAD Drawing            | .dwg                    |
| Vtt.dll              | WebVTT                     | .vtt                    |

### Archive & Compression Formats

| DLL                  | Parsing Format             | File Extension          |
|----------------------|----------------------------|-------------------------|
| Zip.dll              | ZIP Archive                | .zip                    |
| SevenZip.dll         | 7-Zip Archive              | .7z                     |
| GZip.dll             | GZIP Archive               | .gz                     |
| Tar.dll              | TAR Archive                | .tar                    |

### Image Formats

| DLL                  | Parsing Format             | File Extension          |
|----------------------|----------------------------|-------------------------|
| Jpeg.dll             | JPEG Image                 | .jpg, .jpeg             |
| Png.dll              | PNG Image                  | .png                    |
| Gif.dll              | GIF Image                  | .gif                    |

### Email & Windows File Formats

| DLL                  | Parsing Format             | File Extension          |
|----------------------|----------------------------|-------------------------|
| Lnk.dll              | Windows Shortcut           | .lnk                    |
| Msg.dll              | Outlook Message            | .msg                    |
| Mime.dll             | MIME / Email               | .eml                    |

### Encrypted & Protected Formats

| DLL                  | Parsing Format             | File Extension          |
|----------------------|----------------------------|-------------------------|
| PFile.dll            | MIP Protected File         | .pfile                  |
| RmsOfficeLegacy.dll  | RMS Protected Office       | Protected Office Files  |
| EncOffMetro.dll      | Encrypted Office           | Encrypted Office Files  |