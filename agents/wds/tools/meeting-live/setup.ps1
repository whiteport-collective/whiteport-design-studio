# setup.ps1: installs everything the recording and the transcription need on a Windows computer.
# Part of WDS (agents/wds/tools/meeting-live.md). Can be run again any number of times.
#
#   powershell -ExecutionPolicy Bypass -File <WDS>\agents\wds\tools\meeting-live\setup.ps1 [-Preload]
#
# Does:
#   1. Python 3 (winget) if it is missing
#   2. The packages for recording and live transcription: pyaudiowpatch, faster-whisper, numpy, pillow, python-socketio
#   3. ffmpeg (winget) for the screen video
#   4. The graphics card: Intel graphics gets openvino-genai and optimum-intel, NVIDIA gets the CUDA libraries (cuBLAS, cuDNN)
#   5. Downloads KB-Whisper small (the live transcription) in advance; -Preload also fetches medium and,
#      with Intel graphics, the conversion to OpenVINO (a few minutes)
#   6. Checks that the recording finds the screens, and says so if recordings: is missing in ~/.wds/me.md

param([switch]$Preload)
$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
function Step($t) { Write-Host "`n== $t" -ForegroundColor Cyan }
function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Refresh-Path { $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User") }

Step "1. Python"
$py = $null
foreach ($c in @("python", "py")) {
    if (Have $c) {
        try { $v = & $c -c "import sys; print(sys.version_info[0])" 2>$null; if ($v -eq "3") { $py = $c; break } } catch {}
    }
}
if (-not $py) {
    winget install --id Python.Python.3.13 -e --accept-source-agreements --accept-package-agreements
    Refresh-Path
    $py = "python"
}
& $py --version

Step "2. Packages for recording and live transcription"
& $py -m pip install --quiet --upgrade pyaudiowpatch faster-whisper numpy pillow "python-socketio[client]"

Step "3. ffmpeg (the screen video)"
if (Have "ffmpeg") { Write-Host "already installed" } else {
    winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
    Refresh-Path
    if (-not (Have "ffmpeg")) { Write-Host "ffmpeg installed; open a new terminal so that it is found." -ForegroundColor Yellow }
}

Step "4. The graphics card"
$gpus = (Get-CimInstance Win32_VideoController | ForEach-Object { $_.Name }) -join ", "
Write-Host "Graphics: $gpus"
$intel = $gpus -match "Intel"
if ($intel) {
    & $py -m pip install --quiet --upgrade openvino-genai "optimum-intel[openvino]" "httpcore>=1.0.9"
    & $py -c "import openvino as ov; d = ov.Core().available_devices; print('OpenVINO sees:', d); print('The graphics card is used' if 'GPU' in d else 'No GPU for OpenVINO: the processor is used')"
}
$nvidia = $gpus -match "NVIDIA"
if ($nvidia) {
    # faster-whisper (CTranslate2) on CUDA 12 needs cuBLAS and cuDNN 9; the pip packages are enough, no CUDA Toolkit
    & $py -m pip install --quiet --upgrade nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"
    & $py -c "import ctranslate2; n = ctranslate2.get_cuda_device_count(); print('CUDA devices:', n); print('The NVIDIA card is used' if n else 'CUDA not found: check the NVIDIA driver')"
}
if (-not $intel -and -not $nvidia) {
    Write-Host "No supported graphics card: the transcription runs on the processor." -ForegroundColor Yellow
}

Step "5. Models"
& $py -c "from faster_whisper import WhisperModel; WhisperModel('KBLab/kb-whisper-small', device='cpu', compute_type='int8'); print('KB-Whisper small ready (live transcription)')"
if ($Preload) {
    & $py -c "from faster_whisper import WhisperModel; WhisperModel('KBLab/kb-whisper-medium', device='cpu', compute_type='int8'); print('KB-Whisper medium ready (thorough transcription)')"
    if ($intel) {
        & $py -c "import sys; sys.path.insert(0, r'$here'); import refine; print('OpenVINO model:', refine.ov_model_dir('KBLab/kb-whisper-medium'))"
    }
} else {
    Write-Host "Medium and the OpenVINO conversion are downloaded the first time refine.py runs (or run with -Preload)."
}

Step "6. Check"
& $py (Join-Path $here "local.py") --list-screens
$me = Join-Path $HOME ".wds\me.md"
if (-not (Test-Path $me) -or -not (Select-String -Path $me -Pattern "^recordings:" -Quiet)) {
    Write-Host "Missing: a line 'recordings: <folder>' in $me (a private folder for audio and video). Otherwise the recording skill asks the first time." -ForegroundColor Yellow
} else {
    Write-Host ((Select-String -Path $me -Pattern "^recordings:").Line)
}
Write-Host "`nDone. Tell the agent 'record' (in Swedish: 'spela in')." -ForegroundColor Green
