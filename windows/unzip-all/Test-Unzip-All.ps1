[CmdletBinding()]
param(
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
# 結果ファイルの指定がなければ、このスクリプトと同じフォルダに出力します。
if ([string]::IsNullOrEmpty($OutputPath)) {
    $OutputPath = Join-Path -Path $PSScriptRoot -ChildPath 'Unzip-All.Tests.txt'
}
$testScriptPath = Join-Path -Path $PSScriptRoot -ChildPath 'Unzip-All.ps1'
$powershellPath = (Get-Command powershell.exe -ErrorAction Stop).Source
# テストデータは一時フォルダに作成し、テスト終了後に削除します。
$testRoot = Join-Path -Path ([System.IO.Path]::GetTempPath()) -ChildPath ('Unzip-All.Tests.' + [guid]::NewGuid().ToString('N'))
$results = [System.Collections.Generic.List[string]]::new()
$passedCount = 0
$failedCount = 0

# 展開スクリプトを別プロセスで実行し、終了コードで成否を確認します。
function Invoke-UnzipAll {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ArchivePath
    )

    $output = & $powershellPath -NoProfile -ExecutionPolicy Bypass -File $testScriptPath $ArchivePath 2>&1 | Out-String
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        throw "Unzip-All.ps1 の終了コードが $exitCode でした。出力: $output"
    }
}

# テストを個別に実行し、成功・失敗とエラー内容を記録します。
function Invoke-Test {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [scriptblock]$Test
    )

    try {
        & $Test
        $script:passedCount++
        $script:results.Add("[成功] $Name")
    }
    catch {
        $script:failedCount++
        $script:results.Add("[失敗] $Name - $($_.Exception.Message)")
    }
}

# 指定した内容を含むテスト用ZIPファイルを作成します。
function New-TestArchive {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ArchiveDirectory,
        [Parameter(Mandatory = $true)]
        [string]$ArchiveName,
        [Parameter(Mandatory = $true)]
        [string]$ContentDirectory
    )

    New-Item -ItemType Directory -Path $ArchiveDirectory -Force | Out-Null
    New-Item -ItemType Directory -Path $ContentDirectory -Force | Out-Null
    $archivePath = Join-Path -Path $ArchiveDirectory -ChildPath "$ArchiveName.zip"
    Compress-Archive -Path (Join-Path -Path $ContentDirectory -ChildPath '*') -DestinationPath $archivePath -ErrorAction Stop
    return $archivePath
}

try {
    New-Item -ItemType Directory -Path $testRoot -Force | Out-Null

    # 出力先がない状態から展開し、ZIP内のファイル内容を確認します。
    Invoke-Test -Name '出力先フォルダがない場合にZIPを展開できる' -Test {
        $archiveDirectory = Join-Path -Path $testRoot -ChildPath 'new-output'
        $contentDirectory = Join-Path -Path $testRoot -ChildPath 'new-content'
        New-Item -ItemType Directory -Path $contentDirectory -Force | Out-Null
        Set-Content -LiteralPath (Join-Path -Path $contentDirectory -ChildPath 'fresh.txt') -Value 'fresh content' -ErrorAction Stop
        $archivePath = New-TestArchive -ArchiveDirectory $archiveDirectory -ArchiveName 'sample' -ContentDirectory $contentDirectory

        Invoke-UnzipAll -ArchivePath $archivePath

        $destinationPath = Join-Path -Path $archiveDirectory -ChildPath 'sample'
        $actualContent = Get-Content -LiteralPath (Join-Path -Path $destinationPath -ChildPath 'fresh.txt') -Raw -ErrorAction Stop
        if ($actualContent.Trim() -ne 'fresh content') {
            throw '展開されたファイルの内容がZIP内の内容と一致しません。'
        }
    }

    # 出力先に古いファイルを用意し、削除後に新しい内容が展開されることを確認します。
    Invoke-Test -Name '既存の出力先フォルダを削除してから展開できる' -Test {
        $archiveDirectory = Join-Path -Path $testRoot -ChildPath 'replace-output'
        $contentDirectory = Join-Path -Path $testRoot -ChildPath 'replace-content'
        $nestedContentDirectory = Join-Path -Path $contentDirectory -ChildPath 'nested'
        New-Item -ItemType Directory -Path $nestedContentDirectory -Force | Out-Null
        Set-Content -LiteralPath (Join-Path -Path $nestedContentDirectory -ChildPath 'fresh.txt') -Value 'replacement content' -ErrorAction Stop
        $archivePath = New-TestArchive -ArchiveDirectory $archiveDirectory -ArchiveName 'replace-me' -ContentDirectory $contentDirectory
        $destinationPath = Join-Path -Path $archiveDirectory -ChildPath 'replace-me'
        $staleDirectory = Join-Path -Path $destinationPath -ChildPath 'old-nested'
        New-Item -ItemType Directory -Path $staleDirectory -Force | Out-Null
        Set-Content -LiteralPath (Join-Path -Path $staleDirectory -ChildPath 'stale.txt') -Value 'stale content' -ErrorAction Stop

        Invoke-UnzipAll -ArchivePath $archivePath

        if (Test-Path -LiteralPath (Join-Path -Path $staleDirectory -ChildPath 'stale.txt')) {
            throw '以前の出力先にあった古いファイルが残っています。'
        }
        $actualContent = Get-Content -LiteralPath (Join-Path -Path $destinationPath -ChildPath 'nested\fresh.txt') -Raw -ErrorAction Stop
        if ($actualContent.Trim() -ne 'replacement content') {
            throw '置き換え後のファイルの内容がZIP内の内容と一致しません。'
        }
    }
}
catch {
    $failedCount++
    $results.Add("[失敗] テストの準備 - $($_.Exception.Message)")
}
finally {
    # テストで作成した一時ファイルを残さないようにします。
    if (Test-Path -LiteralPath $testRoot) {
        Remove-Item -LiteralPath $testRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}

$reportLines = @(
    'Unzip-All テスト結果'
    "実行日時: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    ''
) + $results.ToArray() + @(
    ''
    "成功: $passedCount"
    "失敗: $failedCount"
)

# 結果ファイルの保存先フォルダを作成してから、テスト結果を書き込みます。
try {
    $resolvedOutputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputPath)
    $outputDirectory = Split-Path -Path $resolvedOutputPath -Parent
    if (-not (Test-Path -LiteralPath $outputDirectory -PathType Container)) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }
    Set-Content -LiteralPath $resolvedOutputPath -Value $reportLines -Encoding UTF8 -ErrorAction Stop
    Write-Host "テスト結果を保存しました: $resolvedOutputPath"
}
catch {
    Write-Error "テスト結果を '$OutputPath' に保存できませんでした: $($_.Exception.Message)"
    exit 1
}

if ($failedCount -gt 0) {
    exit 1
}

exit 0
