[CmdletBinding()]
param(
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $projectRoot "out\KitCode-Windows.zip"
} elseif (-not [System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath = Join-Path $projectRoot $OutputPath
}
$OutputPath = [System.IO.Path]::GetFullPath($OutputPath)

$requiredPaths = @(
    "launch.bat",
    "requirements.txt",
    ".env.example",
    ".github\download-windows.svg",
    ".github\kitcode-workspace.png",
    "README.md",
    "TROUBLESHOOTING.md",
    "scripts\launch.ps1",
    "backend\main.py",
    "frontend_dist\index.html"
)
foreach ($relativePath in $requiredPaths) {
    $sourcePath = Join-Path $projectRoot $relativePath
    if (-not (Test-Path -LiteralPath $sourcePath)) {
        throw "The release cannot be built because '$relativePath' is missing."
    }
}

$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$stagingRoot = [System.IO.Path]::GetFullPath(
    (Join-Path $tempBase ("kitcode-release-" + [guid]::NewGuid().ToString("N")))
)
if (-not $stagingRoot.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "The release staging folder was not created inside the system temporary folder."
}

$packageRoot = Join-Path $stagingRoot "KitCode"

try {
    New-Item -ItemType Directory -Path $packageRoot | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $packageRoot ".github") | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $packageRoot "scripts") | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $packageRoot "backend") | Out-Null

    foreach ($fileName in @("launch.bat", "requirements.txt", ".env.example", "README.md", "TROUBLESHOOTING.md")) {
        Copy-Item -LiteralPath (Join-Path $projectRoot $fileName) -Destination $packageRoot
    }
    Copy-Item -LiteralPath (Join-Path $projectRoot ".github\download-windows.svg") -Destination (Join-Path $packageRoot ".github")
    Copy-Item -LiteralPath (Join-Path $projectRoot ".github\kitcode-workspace.png") -Destination (Join-Path $packageRoot ".github")
    Copy-Item -LiteralPath (Join-Path $projectRoot "scripts\launch.ps1") -Destination (Join-Path $packageRoot "scripts")

    $backendFiles = Get-ChildItem -LiteralPath (Join-Path $projectRoot "backend") -File -Filter "*.py"
    if (-not $backendFiles) {
        throw "No backend Python files were found."
    }
    $backendFiles | Copy-Item -Destination (Join-Path $packageRoot "backend")

    Copy-Item -LiteralPath (Join-Path $projectRoot "frontend_dist") -Destination $packageRoot -Recurse

    $outputDirectory = Split-Path -Parent $OutputPath
    if (-not (Test-Path -LiteralPath $outputDirectory)) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }

    Push-Location $stagingRoot
    try {
        Compress-Archive -LiteralPath "KitCode" -DestinationPath $OutputPath -CompressionLevel Optimal -Force
    } finally {
        Pop-Location
    }

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [System.IO.Compression.ZipFile]::OpenRead($OutputPath)
    try {
        $entries = @($archive.Entries | ForEach-Object { $_.FullName.Replace("\", "/") })
        foreach ($requiredEntry in @(
            "KitCode/launch.bat",
            "KitCode/requirements.txt",
            "KitCode/.github/download-windows.svg",
            "KitCode/.github/kitcode-workspace.png",
            "KitCode/scripts/launch.ps1",
            "KitCode/backend/main.py",
            "KitCode/frontend_dist/index.html"
        )) {
            if ($entries -notcontains $requiredEntry) {
                throw "The built ZIP is missing '$requiredEntry'."
            }
        }

        $forbidden = $entries | Where-Object {
            $_ -match '(^|/)(\.env|data|\.git|\.venv|node_modules|__pycache__)(/|$)'
        }
        if ($forbidden) {
            throw "The built ZIP contains forbidden local or sensitive content: $($forbidden -join ', ')"
        }
    } finally {
        $archive.Dispose()
    }

    $sizeMiB = [math]::Round((Get-Item -LiteralPath $OutputPath).Length / 1MB, 2)
    $hash = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Host "Built $OutputPath ($sizeMiB MiB)" -ForegroundColor Green
    Write-Host "SHA-256: $hash"
} finally {
    if ((Test-Path -LiteralPath $stagingRoot) -and
        $stagingRoot.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase)) {
        Remove-Item -LiteralPath $stagingRoot -Recurse -Force
    }
}
