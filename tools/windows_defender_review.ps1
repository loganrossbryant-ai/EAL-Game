# Scanner-only validation on an ephemeral GitHub Windows runner.
# Never runs the game or disables/allow-lists antivirus protection.
param(
    [string]$Candidate = "review-candidate/far-horizon",
    [string]$Manifest = "review-candidate/manifest.json",
    [string]$Report = "security-reports/defender-review.json"
)

$ErrorActionPreference = "Stop"
if ($env:GITHUB_ACTIONS -ne "true") {
    throw "This script is restricted to a temporary GitHub Actions runner."
}
$workspace = [IO.Path]::GetFullPath($env:GITHUB_WORKSPACE)
$target = [IO.Path]::GetFullPath((Join-Path $workspace $Candidate))
if (-not $target.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar)) {
    throw "The scan target must be inside the checked-out candidate."
}
$reportPath = Join-Path $workspace $Report
$result = [ordered]@{
    status = "not_scanned"
    source_commit = $env:GITHUB_SHA
    run_id = $env:GITHUB_RUN_ID
    run_attempt = $env:GITHUB_RUN_ATTEMPT
    started_utc = [DateTime]::UtcNow.ToString("o")
    completed_utc = $null
    files_verified_before_scan = $false
    files_verified_after_scan = $false
    defender = $null
    preferences = $null
    scan_exit_code = $null
    detections = @()
    error = $null
    automatic_sample_submission = "disabled; no file uploads for sample analysis"
    limitation = "A clean scan is evidence, not a guarantee of absence of malware."
}
$passed = $false

function Test-CandidateHashes($list) {
    $expected = @($list.files | ForEach-Object { $_.path.Replace("/", "\") } | Sort-Object)
    $actual = @(Get-ChildItem -LiteralPath $target -Recurse -File | ForEach-Object {
        $_.FullName.Substring($target.Length + 1)
    } | Sort-Object)
    if ((Compare-Object $expected $actual)) { throw "Candidate file inventory changed." }
    foreach ($entry in $list.files) {
        $file = Join-Path $target $entry.path
        if ((Get-Item -LiteralPath $file).Length -ne $entry.bytes) {
            throw "File size mismatch: $($entry.path)"
        }
        if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) {
            throw "File hash mismatch: $($entry.path)"
        }
    }
}

try {
    $manifestData = Get-Content -Raw -LiteralPath (Join-Path $workspace $Manifest) | ConvertFrom-Json
    Test-CandidateHashes $manifestData
    $result.files_verified_before_scan = $true
    $result.manifest_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $workspace $Manifest)).Hash.ToLowerInvariant()

    Import-Module Defender -ErrorAction Stop
    $service = Get-Service WinDefend -ErrorAction Stop
    if ($service.Status -ne "Running") { Start-Service WinDefend -ErrorAction Stop }

    # GitHub's runner image disables scanning and excludes C:/D: by default.
    # Only strengthen protection on this disposable runner; never change a PC.
    Set-MpPreference -DisableArchiveScanning $false -DisableScriptScanning $false `
        -DisableIOAVProtection $false -DisableBehaviorMonitoring $false `
        -DisableRealtimeMonitoring $false -DisableAutoExclusions $true `
        -SubmitSamplesConsent 2 -MAPSReporting 1 -ErrorAction Stop
    $preferences = Get-MpPreference
    foreach ($field in @("ExclusionPath", "ExclusionExtension", "ExclusionProcess")) {
        $values = @($preferences.$field | Where-Object { $_ })
        if ($values.Count -gt 0) {
            $remove = @{}; $remove[$field] = $values
            Remove-MpPreference @remove -ErrorAction Stop
        }
    }
    Update-MpSignature -ErrorAction Stop
    $status = Get-MpComputerStatus -ErrorAction Stop
    $preferences = Get-MpPreference -ErrorAction Stop
    $result.defender = $status | Select-Object AMRunningMode, AMServiceEnabled,
        AntivirusEnabled, RealTimeProtectionEnabled, AMEngineVersion,
        AMProductVersion, AntivirusSignatureVersion, AntivirusSignatureLastUpdated
    $result.preferences = $preferences | Select-Object DisableArchiveScanning,
        DisableScriptScanning, DisableRealtimeMonitoring, DisableAutoExclusions,
        ExclusionPath, ExclusionExtension, ExclusionProcess, MAPSReporting, SubmitSamplesConsent
    if (-not $status.AMServiceEnabled -or -not $status.AntivirusEnabled -or
        -not $status.RealTimeProtectionEnabled -or $status.AMRunningMode -ne "Normal") {
        throw "Defender is not active in normal protection mode. No scan clearance."
    }
    if ($preferences.DisableArchiveScanning -or $preferences.DisableScriptScanning -or
        $preferences.DisableRealtimeMonitoring -or @($preferences.ExclusionPath | Where-Object { $_ }).Count -gt 0 -or
        @($preferences.ExclusionExtension | Where-Object { $_ }).Count -gt 0 -or
        @($preferences.ExclusionProcess | Where-Object { $_ }).Count -gt 0) {
        throw "Scanning is disabled or exclusions remain. No scan clearance."
    }
    if (([DateTime]::UtcNow - $status.AntivirusSignatureLastUpdated.ToUniversalTime()).TotalDays -gt 2) {
        throw "Defender signatures are stale. No scan clearance."
    }
    $platformRoot = Join-Path $env:ProgramData "Microsoft\Windows Defender\Platform"
    $program = Get-ChildItem -LiteralPath $platformRoot -Directory | Sort-Object Name -Descending |
        ForEach-Object { Join-Path $_.FullName "MpCmdRun.exe" } |
        Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $program) { $program = Join-Path $env:ProgramFiles "Windows Defender\MpCmdRun.exe" }
    $signature = Get-AuthenticodeSignature -LiteralPath $program
    if ($signature.Status -ne "Valid" -or $signature.SignerCertificate.Subject -notmatch "Microsoft") {
        throw "Cannot verify the installed Microsoft scan executable."
    }
    $outLog = Join-Path $env:RUNNER_TEMP "fh-defender-out.txt"
    $errLog = Join-Path $env:RUNNER_TEMP "fh-defender-err.txt"
    $process = Start-Process -FilePath $program `
        -ArgumentList @("-Scan", "-ScanType", "3", "-File", "`"$target`"") `
        -NoNewWindow -PassThru -RedirectStandardOutput $outLog -RedirectStandardError $errLog
    if (-not $process.WaitForExit(300000)) {
        $process.Kill()
        throw "Defender scan timed out. No scan clearance."
    }
    $process.WaitForExit()
    $result.scan_exit_code = $process.ExitCode
    $result.scan_output = ((Get-Content -Raw -LiteralPath $outLog -ErrorAction SilentlyContinue) +
        (Get-Content -Raw -LiteralPath $errLog -ErrorAction SilentlyContinue))
    $detections = @(Get-MpThreatDetection -ErrorAction SilentlyContinue | Where-Object {
        (@($_.Resources) -join " ").IndexOf($target, [StringComparison]::OrdinalIgnoreCase) -ge 0
    })
    foreach ($detection in $detections) {
        $threat = Get-MpThreat -ThreatID $detection.ThreatID -ErrorAction SilentlyContinue
        $result.detections += [ordered]@{
            threat_id = $detection.ThreatID
            name = $threat.ThreatName
            resources = @($detection.Resources)
            action_success = $detection.ActionSuccess
        }
    }
    if ($detections.Count -gt 0) {
        $result.status = "detected"
        throw "Defender reported detections in the candidate. Release remains blocked."
    }
    if ($process.ExitCode -ne 0) { throw "Defender scan failed; exit $($process.ExitCode)." }
    Test-CandidateHashes $manifestData
    $result.files_verified_after_scan = $true
    $result.status = "scan_passed"
    $passed = $true
} catch {
    $result.error = $_.Exception.Message
    if ($result.status -ne "detected") { $result.status = "not_cleared" }
} finally {
    $result.completed_utc = [DateTime]::UtcNow.ToString("o")
    New-Item -ItemType Directory -Force -Path (Split-Path $reportPath) | Out-Null
    $json = $result | ConvertTo-Json -Depth 15
    [IO.File]::WriteAllText($reportPath, $json, (New-Object Text.UTF8Encoding($false)))
    Write-Output $json
}
if (-not $passed) { exit 1 }
