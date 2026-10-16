$ErrorActionPreference = 'Stop'

$scriptPath = Join-Path -Path $PSScriptRoot -ChildPath 'Unblock-DownloadedFiles.ps1'
$resultPath = Join-Path -Path $PSScriptRoot -ChildPath 'TestResults.txt'
$testRoot = Join-Path -Path ([System.IO.Path]::GetTempPath()) -ChildPath ('ClearBlockTests_' + [guid]::NewGuid().ToString('N'))
$testScriptPath = Join-Path -Path $testRoot -ChildPath 'Unblock-DownloadedFiles.ps1'
$powerShellExe = Join-Path -Path $PSHOME -ChildPath 'powershell.exe'
$script:testResults = New-Object 'System.Collections.Generic.List[object]'

function Add-TestResult {
    param(
        [string]$Name,
        [bool]$Passed,
        [string]$Details
    )

    $status = if ($Passed) { 'PASS' } else { 'FAIL' }
    $script:testResults.Add([pscustomobject]@{
        Status = $status
        Name = $Name
        Details = $Details
    })
}

function New-BlockedTestFile {
    param([string]$Path)

    $parentDirectory = Split-Path -Parent $Path
    New-Item -ItemType Directory -Path $parentDirectory -Force | Out-Null
    Set-Content -LiteralPath $Path -Value 'ClearBlock test file'
    Set-Content -LiteralPath $Path -Stream Zone.Identifier -Value ("[ZoneTransfer]`r`nZoneId=3")
}

function Test-HasZoneIdentifier {
    param([string]$Path)

    return $null -ne (Get-Item -LiteralPath $Path -Stream Zone.Identifier -ErrorAction SilentlyContinue)
}

function Invoke-UnblockScript {
    param([string[]]$Arguments)

    $output = @(& $powerShellExe -NoLogo -NoProfile -ExecutionPolicy Bypass -File $testScriptPath @Arguments 2>&1)
    return [pscustomobject]@{
        ExitCode = $LASTEXITCODE
        Output = ($output | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
    }
}

function Get-LatestTestLog {
    $logDirectory = Join-Path -Path $testRoot -ChildPath 'Logs'
    $logs = @(Get-ChildItem -LiteralPath $logDirectory -Filter 'UnblockFiles_*.log' -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending)

    if ($logs.Count -eq 0) {
        return $null
    }

    return $logs[0]
}

try {
    if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
        throw "対象スクリプトが見つかりません: $scriptPath"
    }

    New-Item -ItemType Directory -Path $testRoot -Force | Out-Null
    Copy-Item -LiteralPath $scriptPath -Destination $testScriptPath

    # 対象スクリプトがWindows PowerShell 5.1で構文解析できることを確認します。
    $tokens = $null
    $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($scriptPath, [ref]$tokens, [ref]$parseErrors) | Out-Null
    $syntaxDetails = if ($parseErrors.Count -eq 0) {
        '構文エラーなし'
    }
    else {
        ($parseErrors | ForEach-Object { $_.Message }) -join '; '
    }
    Add-TestResult -Name 'PowerShell構文' -Passed ($parseErrors.Count -eq 0) -Details $syntaxDetails

    # 個別ファイルを指定したときにブロック属性が解除され、ログが作成されることを確認します。
    $singleFile = Join-Path -Path $testRoot -ChildPath 'single.txt'
    New-BlockedTestFile -Path $singleFile
    $singleRun = Invoke-UnblockScript -Arguments @($singleFile)
    $singleLog = Get-LatestTestLog
    $singleLogText = if ($singleLog) { Get-Content -LiteralPath $singleLog.FullName -Raw -Encoding UTF8 } else { '' }
    $singlePassed = (
        $singleRun.ExitCode -eq 0 -and
        -not (Test-HasZoneIdentifier -Path $singleFile) -and
        $singleLogText.Contains('処理成功:') -and
        $singleLogText.Contains('成功: 1 件')
    )
    Add-TestResult -Name '個別ファイルのブロック解除' -Passed $singlePassed -Details "終了コード=$($singleRun.ExitCode)、Zone.Identifier解除と成功ログを確認"

    # フォルダーを指定したときに、直下とサブフォルダーのファイルが処理されることを確認します。
    $folder = Join-Path -Path $testRoot -ChildPath 'folder'
    $folderFile = Join-Path -Path $folder -ChildPath 'top.txt'
    $nestedFile = Join-Path -Path $folder -ChildPath 'nested\child.txt'
    New-BlockedTestFile -Path $folderFile
    New-BlockedTestFile -Path $nestedFile
    $folderRun = Invoke-UnblockScript -Arguments @($folder)
    $folderLog = Get-LatestTestLog
    $folderLogText = if ($folderLog) { Get-Content -LiteralPath $folderLog.FullName -Raw -Encoding UTF8 } else { '' }
    $folderPassed = (
        $folderRun.ExitCode -eq 0 -and
        -not (Test-HasZoneIdentifier -Path $folderFile) -and
        -not (Test-HasZoneIdentifier -Path $nestedFile) -and
        $folderLogText.Contains('成功: 2 件')
    )
    Add-TestResult -Name 'フォルダーの再帰処理' -Passed $folderPassed -Details "終了コード=$($folderRun.ExitCode)、直下とサブフォルダーの2ファイルを確認"

    # ファイルと、そのファイルを含むフォルダーを同時指定しても重複処理しないことを確認します。
    $duplicateFolder = Join-Path -Path $testRoot -ChildPath 'duplicate'
    $duplicateFile = Join-Path -Path $duplicateFolder -ChildPath 'same.txt'
    New-BlockedTestFile -Path $duplicateFile
    $duplicateRun = Invoke-UnblockScript -Arguments @($duplicateFile, $duplicateFolder)
    $duplicateLog = Get-LatestTestLog
    $duplicateLogText = if ($duplicateLog) { Get-Content -LiteralPath $duplicateLog.FullName -Raw -Encoding UTF8 } else { '' }
    $successLines = @($duplicateLogText -split '\r?\n' | Where-Object { $_ -match '\[SUCCESS\] 処理成功:' }).Count
    $duplicatePassed = (
        $duplicateRun.ExitCode -eq 0 -and
        -not (Test-HasZoneIdentifier -Path $duplicateFile) -and
        $successLines -eq 1 -and
        $duplicateLogText.Contains('成功: 1 件')
    )
    Add-TestResult -Name '重複指定の一度だけの処理' -Passed $duplicatePassed -Details "終了コード=$($duplicateRun.ExitCode)、成功ログ=$successLines 件"

    # 存在しないパスを指定した場合に、失敗終了コードとエラー記録が得られることを確認します。
    $missingRun = Invoke-UnblockScript -Arguments @((Join-Path -Path $testRoot -ChildPath 'missing.txt'))
    $missingLog = Get-LatestTestLog
    $missingLogText = if ($missingLog) { Get-Content -LiteralPath $missingLog.FullName -Raw -Encoding UTF8 } else { '' }
    $missingPassed = ($missingRun.ExitCode -ne 0 -and $missingLogText.Contains('対象を開けません'))
    Add-TestResult -Name '存在しないパスのエラー処理' -Passed $missingPassed -Details "終了コード=$($missingRun.ExitCode)、エラーをログに記録"

    # 対象未指定の場合も、失敗終了コードとエラー記録が得られることを確認します。
    $emptyRun = Invoke-UnblockScript -Arguments @()
    $emptyLog = Get-LatestTestLog
    $emptyLogText = if ($emptyLog) { Get-Content -LiteralPath $emptyLog.FullName -Raw -Encoding UTF8 } else { '' }
    $emptyPassed = ($emptyRun.ExitCode -ne 0 -and $emptyLogText.Contains('対象が指定されていません'))
    Add-TestResult -Name '対象未指定のエラー処理' -Passed $emptyPassed -Details "終了コード=$($emptyRun.ExitCode)、エラーをログに記録"

    # ログが既定のLogsフォルダーに日時入りのファイル名で作成されることを確認します。
    $logNamePassed = (
        $emptyLog -and
        $emptyLog.Directory.Name -eq 'Logs' -and
        $emptyLog.Name -match '^UnblockFiles_\d{8}_\d{6}_\d{3}\.log$'
    )
    Add-TestResult -Name 'Logsフォルダーと日時付きログ名' -Passed ([bool]$logNamePassed) -Details $(if ($emptyLog) { "Logs\$($emptyLog.Name) を確認" } else { 'ログファイルが見つかりません' })
}
catch {
    Add-TestResult -Name 'テスト実行中の予期しないエラー' -Passed $false -Details $_.Exception.Message
}
finally {
    $passCount = @($script:testResults | Where-Object { $_.Status -eq 'PASS' }).Count
    $failCount = @($script:testResults | Where-Object { $_.Status -eq 'FAIL' }).Count
    $lines = New-Object 'System.Collections.Generic.List[string]'
    $lines.Add("実行日時: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
    $lines.Add("実行PowerShell: $($PSVersionTable.PSVersion)")
    $lines.Add("結果: $passCount 件成功 / $failCount 件失敗")
    $lines.Add('')
    foreach ($testResult in $script:testResults) {
        $lines.Add("[$($testResult.Status)] $($testResult.Name) - $($testResult.Details)")
    }

    [System.IO.File]::WriteAllLines($resultPath, $lines, [System.Text.UTF8Encoding]::new($true))

    if (Test-Path -LiteralPath $testRoot) {
        Remove-Item -LiteralPath $testRoot -Recurse -Force
    }
}

Get-Content -LiteralPath $resultPath -Encoding UTF8
if (@($script:testResults | Where-Object { $_.Status -eq 'FAIL' }).Count -gt 0) {
    exit 1
}

exit 0
