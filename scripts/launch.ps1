[CmdletBinding()]
param(
    [ValidateRange(0, 65535)]
    [int]$Port = 0,
    [switch]$SkipBrowser
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$requirementsPath = Join-Path $projectRoot "requirements.txt"
$stampPath = Join-Path $venvPath ".kitcode-requirements.sha256"
$envFile = Join-Path $projectRoot ".env"
$frontendPath = Join-Path $projectRoot "frontend_dist"

function Write-Step([string]$Message) {
    Write-Host "`n  $Message" -ForegroundColor Cyan
}

function Test-Python([string]$Executable, [string[]]$Prefix = @()) {
    try {
        $version = & $Executable @Prefix -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
        if ($LASTEXITCODE -ne 0 -or -not $version) { return $false }
        $parts = $version.Trim().Split('.')
        return ([int]$parts[0] -eq 3 -and [int]$parts[1] -ge 10)
    } catch { return $false }
}

function Find-Python {
    $python = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($python -and (Test-Python $python.Source)) {
        return @{ Executable = $python.Source; Prefix = @() }
    }
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher -and (Test-Python $launcher.Source @("-3"))) {
        return @{ Executable = $launcher.Source; Prefix = @("-3") }
    }
    $knownLocations = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python313\python.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe")
    )
    foreach ($candidate in $knownLocations) {
        if ((Test-Path $candidate) -and (Test-Python $candidate)) {
            return @{ Executable = $candidate; Prefix = @() }
        }
    }
    return $null
}

function Install-Python {
    Write-Step "Python was not found. Installing Python 3.12 for this Windows account..."
    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if ($winget) {
        & $winget.Source install --exact --id Python.Python.3.12 --scope user --silent --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -eq 0) { return }
    }
    $installer = Join-Path $env:TEMP "kitcode-python-3.12.10-amd64.exe"
    $download = "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"
    Write-Host "  Downloading the official Python installer..." -ForegroundColor DarkGray
    Invoke-WebRequest -UseBasicParsing -Uri $download -OutFile $installer
    $signature = Get-AuthenticodeSignature -FilePath $installer
    if ($signature.Status -ne "Valid" -or $signature.SignerCertificate.Subject -notmatch "Python Software Foundation") {
        Remove-Item -LiteralPath $installer -Force -ErrorAction SilentlyContinue
        throw "The downloaded Python installer did not have a valid Python Software Foundation signature. Nothing was installed."
    }
    $installProcess = Start-Process -FilePath $installer -ArgumentList @(
        "/quiet", "InstallAllUsers=0", "PrependPath=0", "Include_pip=1", "Include_test=0", "Shortcuts=0"
    ) -PassThru -Wait
    if ($installProcess.ExitCode -ne 0) {
        throw "The Python installer returned exit code $($installProcess.ExitCode)."
    }
    Remove-Item -LiteralPath $installer -Force -ErrorAction SilentlyContinue
}

function Test-Java {
    $javaBin = Find-JavaBin
    $javac = if ($javaBin) { Join-Path $javaBin "javac.exe" } else { $null }
    $java = if ($javaBin) { Join-Path $javaBin "java.exe" } else { $null }
    if (-not $javac -or -not $java) { return $false }
    try {
        & $javac -version 2>$null | Out-Null
        return $LASTEXITCODE -eq 0
    } catch { return $false }
}

function Find-JavaBin {
    $bins = @()
    if ($env:JAVA_HOME) { $bins += (Join-Path $env:JAVA_HOME "bin") }
    $javac = Get-Command javac.exe -ErrorAction SilentlyContinue
    if ($javac) { $bins += (Split-Path -Parent $javac.Source) }
    $roots = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Eclipse Adoptium"),
        (Join-Path $env:ProgramFiles "Eclipse Adoptium")
    )
    foreach ($root in $roots) {
        if (Test-Path $root) { $bins += (Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue | ForEach-Object { Join-Path $_.FullName "bin" }) }
    }
    foreach ($bin in $bins) {
        if ((Test-Path (Join-Path $bin "javac.exe")) -and (Test-Path (Join-Path $bin "java.exe"))) { return $bin }
    }
    return $null
}

function Ensure-Java {
    if (Test-Java) { return }
    Write-Step "Java JDK was not found. Installing Temurin Java 21 for Java drills..."
    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if (-not $winget) {
        Write-Host "  Java setup was skipped because winget is unavailable. Python and SQL drills are ready; install a Java 17+ JDK later to enable Java." -ForegroundColor Yellow
        return
    }
    & $winget.Source install --exact --id EclipseAdoptium.Temurin.21.JDK --scope user --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -eq 0) {
        $bin = Find-JavaBin
        if ($bin) {
            $env:JAVA_HOME = Split-Path -Parent $bin
            $env:PATH = "$bin;$env:PATH"
            Write-Host "  Java is ready for this launch." -ForegroundColor Green
        } else {
            Write-Host "  Java was installed, but Windows has not exposed it yet. Restart KitCode to enable Java drills." -ForegroundColor Yellow
        }
    } else {
        Write-Host "  Java installation did not complete. Python and SQL drills are still ready; retry launch.bat or install a Java 17+ JDK." -ForegroundColor Yellow
    }
}

try {
    Write-Host ""
    Write-Host "  KitCode Interview Studio" -ForegroundColor White
    Write-Host "  Local-first Python, Java, and SQL interview practice" -ForegroundColor DarkGray

    if (Test-Path $envFile) {
        foreach ($line in Get-Content $envFile) {
            $trimmed = $line.Trim()
            if (-not $trimmed -or $trimmed.StartsWith("#") -or -not $trimmed.Contains("=")) { continue }
            $parts = $trimmed.Split("=", 2)
            $name = $parts[0].Trim()
            $value = $parts[1].Trim().Trim('"').Trim("'")
            if ($name -match '^[A-Za-z_][A-Za-z0-9_]*$') {
                [Environment]::SetEnvironmentVariable($name, $value, "Process")
            }
        }
    }

    $resolvedPort = 8765
    if ($env:KITCODE_PORT) {
        $parsedPort = 0
        if (-not [int]::TryParse($env:KITCODE_PORT, [ref]$parsedPort) -or $parsedPort -lt 1 -or $parsedPort -gt 65535) {
            throw "KITCODE_PORT must be a number from 1 to 65535."
        }
        $resolvedPort = $parsedPort
    }
    if ($Port -gt 0) { $resolvedPort = $Port }
    $appUrl = "http://127.0.0.1:$resolvedPort"

    $existing = $null
    try {
        $existing = Invoke-WebRequest -UseBasicParsing -Uri "$appUrl/api/health" -TimeoutSec 1
    } catch {
        # A refused connection means the port is available. An HTTP response with
        # an error status means another service already owns the port.
        if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
            throw "Port $resolvedPort is already used by another local service. Close it or run launch.bat -Port 8766."
        }
    }

    if ($existing) {
        $health = $null
        try { $health = $existing.Content | ConvertFrom-Json } catch { }
        if ($existing.StatusCode -eq 200 -and $health -and
            $health.service -eq "kitcode" -and $health.ok -eq $true) {
            Write-Host "`n  KitCode is already running at $appUrl" -ForegroundColor Green
            if (-not $SkipBrowser) { Start-Process $appUrl }
            exit 0
        }
        throw "Port $resolvedPort is already used by another local service. Close it or run launch.bat -Port 8766."
    }

    if (-not (Test-Path $venvPython)) {
        $python = Find-Python
        if (-not $python) {
            Install-Python
            $python = Find-Python
        }
        if (-not $python) {
            throw "Python 3.10 or newer could not be located after installation. Restart Windows, then open launch.bat again."
        }
        Write-Step "Preparing KitCode's private Python environment (first launch only)..."
        & $python.Executable @($python.Prefix) -m venv $venvPath
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $venvPython)) {
            throw "Python could not create the local .venv environment."
        }
    }

    if (-not (Test-Path $requirementsPath)) {
        throw "requirements.txt is missing. Restore it from the KitCode folder and try again."
    }

    if (-not (Test-Path (Join-Path $frontendPath "index.html"))) {
        throw "The packaged interface is missing. Restore the frontend_dist folder and try again."
    }
    $requirementsHash = (Get-FileHash -Algorithm SHA256 $requirementsPath).Hash
    $installedHash = if (Test-Path $stampPath) { (Get-Content -Raw $stampPath).Trim() } else { "" }
    if ($requirementsHash -ne $installedHash) {
        Write-Step "Installing the packages KitCode needs (first launch only)..."
        & $venvPython -m pip install --disable-pip-version-check --quiet -r $requirementsPath
        if ($LASTEXITCODE -ne 0) {
            throw "Python packages could not be installed. Check your internet connection, then open launch.bat again."
        }
        Set-Content -Path $stampPath -Value $requirementsHash -NoNewline
    }

    # Java is optional at runtime, but launch makes a best-effort one-click
    # setup so its practice rail is ready on a fresh Windows machine.
    Ensure-Java

    Write-Step "Starting your practice workspace..."
    $env:PRACTICE_FRONTEND_DIR = $frontendPath
    $env:KITCODE_DATA_DIR = (Join-Path $projectRoot "data")
    # The launcher intentionally stays loopback-only. Use -Port or
    # KITCODE_PORT customizes the port without exposing learner execution.
    $env:KITCODE_HOST = "127.0.0.1"
    $env:KITCODE_PORT = "$resolvedPort"
    if ($SkipBrowser) {
        $env:KITCODE_OPEN_BROWSER = "0"
    } elseif (-not $env:KITCODE_OPEN_BROWSER) {
        $env:KITCODE_OPEN_BROWSER = "1"
    }

    Write-Host "`n  Ready: $appUrl" -ForegroundColor Green
    Write-Host "  Keep this window open while you practise. Close it to stop KitCode." -ForegroundColor DarkGray
    & $venvPython -m backend.main
    exit $LASTEXITCODE
} catch {
    Write-Host "`n  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  If this keeps happening, see TROUBLESHOOTING.md." -ForegroundColor Yellow
    exit 1
}
