# ConvertSjisToUtf8.ps1

param (
    [string]$inputFile,  # 入力ファイル（Shift JIS）
    [string]$outputFile   # 出力ファイル（UTF-8）
)

# Shift JISでファイルを読み込み、UTF-8で出力
$content = Get-Content -Path $inputFile -Encoding Default  # DefaultはShift JISを読み込む
Set-Content -Path $outputFile -Value $content -Encoding utf8

Write-Host "変換完了: $inputFile -> $outputFile"
