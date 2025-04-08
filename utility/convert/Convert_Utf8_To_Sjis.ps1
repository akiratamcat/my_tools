# ConvertUtf8ToSjis.ps1

param (
    [string]$inputFile,  # 入力ファイル（UTF-8）
    [string]$outputFile   # 出力ファイル（Shift JIS）
)

# UTF-8でファイルを読み込み、Shift JISで出力
$content = Get-Content -Path $inputFile -Encoding utf8
Set-Content -Path $outputFile -Value $content -Encoding Default  # DefaultはShift JISで出力

Write-Host "変換完了: $inputFile -> $outputFile"
