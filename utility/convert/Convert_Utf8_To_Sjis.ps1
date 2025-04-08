# ConvertUtf8ToSjis.ps1

param (
    [string]$inputFile,  # ���̓t�@�C���iUTF-8�j
    [string]$outputFile   # �o�̓t�@�C���iShift JIS�j
)

# UTF-8�Ńt�@�C����ǂݍ��݁AShift JIS�ŏo��
$content = Get-Content -Path $inputFile -Encoding utf8
Set-Content -Path $outputFile -Value $content -Encoding Default  # Default��Shift JIS�ŏo��

Write-Host "�ϊ�����: $inputFile -> $outputFile"
