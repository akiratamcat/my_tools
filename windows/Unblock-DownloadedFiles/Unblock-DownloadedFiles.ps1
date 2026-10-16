param(
    # バッチファイルから渡されたファイルまたはフォルダーのパスを受け取ります。
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Path
)

$ErrorActionPreference = 'Stop'
# ログ保存先を変更する場合は、次の値を希望するフォルダーのパスに変更してください。
$logDirectory = Join-Path -Path $PSScriptRoot -ChildPath 'Logs'

# 保存先フォルダーがなければ作成し、ログの上書きを避ける日時付きファイルを用意します。
New-Item -ItemType Directory -Path $logDirectory -Force -ErrorAction Stop | Out-Null
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
$logPath = Join-Path -Path $logDirectory -ChildPath "UnblockFiles_$timestamp.log"

New-Item -ItemType File -Path $logPath -ErrorAction Stop | Out-Null

# 同じ形式のメッセージを画面とログの両方に出力します。
function Write-Log {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,

        [ValidateSet('INFO', 'SUCCESS', 'ERROR')]
        [string]$Level = 'INFO'
    )

    $line = '{0} [{1}] {2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Level, $Message
    Write-Host $line
    Add-Content -LiteralPath $logPath -Value $line -Encoding UTF8
}

# 対象ファイルを集約し、重複処理と成功・エラー件数を管理します。
$files = New-Object 'System.Collections.Generic.List[System.IO.FileInfo]'
$seenPaths = @{}
$errorCount = 0
$successCount = 0

Write-Log -Message "処理を開始します。ログ: $logPath"

# 入力された各パスを検証し、ファイルまたはフォルダー内のファイルを収集します。
if (-not $Path -or $Path.Count -eq 0) {
    Write-Log -Level ERROR -Message '対象が指定されていません。ファイルまたはフォルダーをこのスクリプトのバッチファイルにドラッグ＆ドロップしてください。'
    $errorCount++
}
else {
    foreach ($inputPath in $Path) {
        try {
            $item = Get-Item -LiteralPath $inputPath -Force -ErrorAction Stop
        }
        catch {
            Write-Log -Level ERROR -Message "対象を開けません: $inputPath - $($_.Exception.Message)"
            $errorCount++
            continue
        }

        if ($item.PSIsContainer) {
            Write-Log -Message "フォルダーを検索します: $($item.FullName)"
            $scanErrors = @()
            # 隠しファイルも含めてサブフォルダーを再帰検索し、アクセスできない項目のエラーも記録します。
            $folderFiles = Get-ChildItem -LiteralPath $item.FullName -File -Recurse -Force -ErrorAction SilentlyContinue -ErrorVariable +scanErrors

            foreach ($scanError in $scanErrors) {
                Write-Log -Level ERROR -Message "フォルダーの検索中にエラー: $($scanError.ToString())"
                $errorCount++
            }

            foreach ($file in $folderFiles) {
                if (-not $seenPaths.ContainsKey($file.FullName)) {
                    $seenPaths[$file.FullName] = $true
                    $files.Add($file)
                }
            }
        }
        elseif ($item -is [System.IO.FileInfo]) {
            if (-not $seenPaths.ContainsKey($item.FullName)) {
                $seenPaths[$item.FullName] = $true
                $files.Add($item)
            }
        }
        else {
            Write-Log -Level ERROR -Message "ファイルまたはフォルダーではありません: $inputPath"
            $errorCount++
        }
    }
}

# 収集したファイルのブロック属性を解除し、ファイルごとの結果を記録します。
foreach ($file in $files) {
    Write-Log -Message "ブロック解除を実行します: $($file.FullName)"
    try {
        Unblock-File -LiteralPath $file.FullName -ErrorAction Stop
        $successCount++
        Write-Log -Level SUCCESS -Message "処理成功: $($file.FullName)"
    }
    catch {
        $errorCount++
        Write-Log -Level ERROR -Message "処理失敗: $($file.FullName) - $($_.Exception.Message)"
    }
}

# 集計結果を記録し、エラーがあった場合は失敗を示す終了コードを返します。
Write-Log -Message "処理終了。成功: $successCount 件 / エラー: $errorCount 件 / 対象ファイル: $($files.Count) 件"
Write-Log -Message "ログファイル: $logPath"

if ($errorCount -gt 0) {
    exit 1
}

exit 0
