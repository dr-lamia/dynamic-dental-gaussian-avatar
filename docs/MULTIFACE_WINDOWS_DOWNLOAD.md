# Windows MultiFace downloader

The official MultiFace downloader shells out to Unix utilities such as `wget`,
`md5sum`, `touch`, and `rm`. This helper is intended for Windows PowerShell
and uses `curl.exe` plus Python's standard library instead.

## PowerShell quick start

From your existing MultiFace folder:

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/dr-lamia/dynamic-dental-gaussian-avatar/main/configs/multiface_dental_minimal.json" -OutFile "multiface_dental_minimal.json"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/dr-lamia/dynamic-dental-gaussian-avatar/main/scripts/download_multiface_windows.py" -OutFile "download_multiface_windows.py"
```

Then run **one line**:

```powershell
python .\download_multiface_windows.py --dest "D:\MultiFace-dental-minimal" --download_config ".\multiface_dental_minimal.json"
```

Do not use `^` as a PowerShell continuation character. If you want a multi-line
PowerShell command, use the backtick character instead.

## TLS/certificate note

The script uses Windows `curl.exe`, which normally uses the Windows certificate
trust mechanism and often works on institutional networks where an older Python
`pip` fails certificate verification.

If curl also reports a certificate-chain error, the secure solution is to install
or configure your institution's root CA certificate. The script also exposes
`--insecure` only as a last-resort temporary option; it disables certificate
verification and should not be the default.
