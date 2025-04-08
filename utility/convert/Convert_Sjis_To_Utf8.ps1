# ConvertSjisToUtf8.ps1

param (
    [string]$inputFile,  # ���̓t�@�C���iShift JIS�j
    [string]$outputFile   # �o�̓t�@�C���iUTF-8�j
)

# Shift JIS�Ńt�@�C����ǂݍ��݁AUTF-8�ŏo��
$content = Get-Content -Path $inputFile -Encoding Default  # Default��Shift JIS��ǂݍ���
Set-Content -Path $outputFile -Value $content -Encoding utf8

Write-Host "�ϊ�����: $inputFile -> $outputFile"
