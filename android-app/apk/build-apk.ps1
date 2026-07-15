$ErrorActionPreference = "Stop"
$apkRoot = "C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\android-app\apk"
$SRC     = Join-Path $apkRoot "src"
$RES     = Join-Path $apkRoot "res"
$MAN     = Join-Path $apkRoot "AndroidManifest.xml"
$OUT     = "C:\Users\lionn\AppData\Local\Temp\kilo\apkout"
New-Item -ItemType Directory -Force -Path $OUT, "$OUT\obj", "$OUT\rjava" | Out-Null
Get-ChildItem $OUT -Exclude keystore.jks | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

$JDK = "C:\Program Files\Android\openjdk\jdk-21.0.8"
$SDK = "C:\Program Files (x86)\Android\android-sdk"
$BT  = "$SDK\build-tools\36.0.0"
$AJAR = "$SDK\platforms\android-34\android.jar"

$env:JAVA_HOME = $JDK
$env:PATH = "$JDK\bin;" + $env:PATH

$javac    = "$JDK\bin\javac.exe"
$jar      = "$JDK\bin\jar.exe"
$keytool  = "$JDK\bin\keytool.exe"
$aapt2    = "$BT\aapt2.exe"
$d8       = "$BT\d8.bat"
$zipalign = "$BT\zipalign.exe"
$apksign  = "$BT\apksigner.bat"

Write-Host "== aapt2 compile resources =="
& $aapt2 compile --dir $RES -o "$OUT\res.zip" 2>&1 | Select-Object -Last 5

Write-Host "== aapt2 link (resources + R.java) =="
& $aapt2 link -o "$OUT\app-unsigned.apk" -I $AJAR --manifest $MAN -R "$OUT\res.zip" --java "$OUT\rjava" --auto-add-overlay 2>&1 | Select-Object -Last 8

Write-Host "== javac (MainActivity + R.java) =="
& $javac -cp $AJAR -d "$OUT\obj" "$SRC\com\xcaliburcuts\app\MainActivity.java" "$OUT\rjava\com\xcaliburcuts\app\R.java" 2>&1 | Select-Object -Last 10

Write-Host "== d8 -> classes.dex =="
New-Item -ItemType Directory -Force -Path "$OUT\dex" | Out-Null
& $jar -cf "$OUT\classes.jar" -C "$OUT\obj" .
& $d8 --lib $AJAR --output "$OUT\dex" "$OUT\classes.jar" 2>&1 | Select-Object -Last 10

Write-Host "== add classes.dex into apk =="
$py = @"
import zipfile
src=r'$OUT\app-unsigned.apk'
dst=r'$OUT\app-nodx.apk'
dex=r'$OUT\dex\classes.dex'
z=zipfile.ZipFile(src,'r')
nz=zipfile.ZipFile(dst,'w')
for it in z.infolist():
    if it.filename=='classes.dex': continue
    ni=zipfile.ZipInfo(it.filename); ni.compress_type=it.compress_type
    nz.writestr(ni, z.read(it.filename))
nz.writestr('classes.dex', open(dex,'rb').read())
nz.close()
print('dex added')
"@
py -3 -c $py

Write-Host "== zipalign =="
& $zipalign -p 4 "$OUT\app-nodx.apk" "$OUT\app-aligned.apk" 2>&1 | Select-Object -Last 3

Write-Host "== keystore =="
if (-not (Test-Path "$OUT\keystore.jks")) {
  & $keytool -genkeypair -v -keystore "$OUT\keystore.jks" -keyalg RSA -keysize 2048 -validity 10000 -alias xcalibur -storepass android -keypass android -dname "CN=Xcalibur Cuts, OU=App, O=Xcalibur, L=Gasparillo, C=TT" 2>&1 | Select-Object -Last 3
} else {
  Write-Host "keystore exists, reusing"
}

Write-Host "== apksigner =="
& $apksign sign --ks "$OUT\keystore.jks" --ks-key-alias xcalibur --ks-pass pass:android --key-pass pass:android --out "$OUT\XcaliburCuts.apk" "$OUT\app-aligned.apk" 2>&1 | Select-Object -Last 5

Write-Host "== verify =="
& $apksign verify --verbose "$OUT\XcaliburCuts.apk" 2>&1 | Select-Object -Last 6

Write-Host "APK: $OUT\XcaliburCuts.apk"
Get-Item "$OUT\XcaliburCuts.apk" | Select-Object Length
