@echo off
setlocal enabledelayedexpansion
title Spexron Engine - Python Baslatici
cd /d "%~dp0"

:: 1. Python Kontrolu
where pythonw >nul 2>&1
if %errorlevel% == 0 (
    start "" pythonw spexron_main.py
    exit
)

where py >nul 2>&1
if %errorlevel% == 0 (
    start "" py -W spexron_main.py
    exit
)

set USER_PYTHON="%LocalAppData%\Programs\Python\Python314\pythonw.exe"
if exist %USER_PYTHON% (
    start "" %USER_PYTHON% spexron_main.py
    exit
)

set USER_PYTHON_OLD="%LocalAppData%\Programs\Python\Python312\pythonw.exe"
if exist %USER_PYTHON_OLD% (
    start "" %USER_PYTHON_OLD% spexron_main.py
    exit
)

:: 2. Eger Python yoksa, otomatik indirme ve Admin modunda kurulum baslat
cls
echo =======================================================================
echo              SPEXRON ENGINE v2.0 - OTOMATIK KURULUM
echo =======================================================================
echo.
echo  [i] Cihazinizda Python bulunamadi!
echo  [i] Spexron Engine'in calismasi icin Python 3.12.3 indiriliyor...
echo.
echo  Lutfen bekleyin, bu islem internet hiziniza bagli olarak 1-2 dakika
echo  surebilir.
echo.

:: TLS 1.2 aktif ederek resmi web sitesinden indir
set "INSTALLER=%TEMP%\python_312_installer.exe"
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; echo '  -> Python yukleyicisi indiriliyor...'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile '%INSTALLER%'"

if not exist "%INSTALLER%" (
    echo.
    echo  [!] HATA: Python yukleyicisi indirilemedi!
    echo  [!] Internet baglantinizi kontrol edin veya manuel kurun: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo  [i] Indirme tamamlandi!
echo  [i] Yonetici haklariyla UAC onayi isteniyor. Lutfen cikan uyarida EVET'e tiklayin.
echo  [i] Python arka planda sessizce kuruluyor, lutfen pencereyi kapatmayin...
echo.

:: Yonetici modunda (Admin) ve sessiz (/quiet) parametreleriyle kur, path'e ekle
powershell -Command "Start-Process -FilePath '%INSTALLER%' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0' -Verb RunAs -Wait"

:: Yükleyiciyi temizle
if exist "%INSTALLER%" del /f /q "%INSTALLER%"

echo  [i] Kurulum tamamlandi. Cevre degiskenleri guncelleniyor...
echo.

:: Ortam degiskenlerini anlik olarak yenile
for /f "tokens=2*" %%A in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYS_PATH=%%B"
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USR_PATH=%%B"
set "PATH=%SYS_PATH%;%USR_PATH%;%PATH%"

:: 3. Kurulum Sonrasi Son Kontrol ve Calistirma
where pythonw >nul 2>&1
if %errorlevel% == 0 (
    echo  [+] Python basariyla kuruldu ve algilandi!
    echo  [+] Spexron Engine baslatiliyor...
    timeout /t 2 >nul
    start "" pythonw spexron_main.py
    exit
)

:: Alternatif yollari tara
set "NEW_PY_PATH=%ProgramFiles%\Python312\pythonw.exe"
if exist "%NEW_PY_PATH%" (
    echo  [+] Python basariyla kuruldu!
    echo  [+] Spexron Engine baslatiliyor...
    timeout /t 2 >nul
    start "" "%NEW_PY_PATH%" spexron_main.py
    exit
)

set "NEW_PY_PATH2=%LocalAppData%\Programs\Python\Python312\pythonw.exe"
if exist "%NEW_PY_PATH2%" (
    echo  [+] Python basariyla kuruldu!
    echo  [+] Spexron Engine baslatiliyor...
    timeout /t 2 >nul
    start "" "%NEW_PY_PATH2%" spexron_main.py
    exit
)

echo  [!] UYARI: Kurulum yapildi fakat PATH yenilenemedigi icin doğrudan algilanamadi.
echo  [!] Bilgisayarinizi yeniden baslattiginizda aktif olacaktir.
echo  [!] Spexron Engine'i simdi manuel yoldan baslatmayi deniyorum...
echo.

:: Eger hicbiri olmazsa py launcher dene
where py >nul 2>&1
if %errorlevel% == 0 (
    start "" py -W spexron_main.py
    exit
)

echo  [!] HATA: Python baslatilamadi. Lutfen bu pencereyi kapatip programi tekrar acin.
pause
exit /b 1
