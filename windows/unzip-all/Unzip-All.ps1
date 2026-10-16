[CmdletBinding()]
param(
    # ZIPファイルまたは検索対象フォルダを、複数まとめて受け取ります。
    [Parameter(Mandatory = $true, Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$Path
)

$ErrorActionPreference = 'Stop'
$hadErrors = $false
# 展開対象のZIPと、重複して処理しないためのパス一覧を用意します。
$archives = [System.Collections.Generic.List[System.IO.FileInfo]]::new()
$seenPaths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)

# 入力ごとに、ZIP単体かフォルダかを判定して展開対象を集めます。
foreach ($inputPath in $Path) {
    try {
        $item = Get-Item -LiteralPath $inputPath -ErrorAction Stop
        if ($item.PSIsContainer) {
            # フォルダの場合は、配下のすべての階層からZIPを検索します。
            $foundArchives = @(Get-ChildItem -LiteralPath $item.FullName -Filter '*.zip' -File -Recurse -Force -ErrorAction Stop)
            foreach ($archive in $foundArchives) {
                # 同じZIPが複数の入力から見つかっても、一度だけ処理します。
                if ($seenPaths.Add($archive.FullName)) {
                    $archives.Add($archive)
                }
            }
            if ($foundArchives.Count -eq 0) {
                Write-Host "ZIPファイルが見つかりません: $($item.FullName)"
            }
        }
        elseif ([System.IO.Path]::GetExtension($item.Name) -ieq '.zip') {
            # ZIPファイル単体が指定された場合も、重複を避けて追加します。
            if ($seenPaths.Add($item.FullName)) {
                $archives.Add($item)
            }
        }
        else {
            Write-Warning "ZIPファイルまたはフォルダではありません: $inputPath"
            $hadErrors = $true
        }
    }
    catch {
        Write-Warning "入力を読み取れません: $inputPath ($($_.Exception.Message))"
        $hadErrors = $true
    }
}

# 展開対象がなければ、エラーの有無を終了コードに反映して終了します。
if ($archives.Count -eq 0) {
    if (-not $hadErrors) {
        Write-Host '展開するZIPファイルがありません。'
    }
    exit ([int]$hadErrors)
}

# 各ZIPの隣に同名フォルダを作り、その中へ展開します。
foreach ($archive in $archives) {
    try {
        $destinationPath = Join-Path -Path $archive.DirectoryName -ChildPath $archive.BaseName
        Write-Host "展開中: $($archive.FullName)"
        Expand-Archive -LiteralPath $archive.FullName -DestinationPath $destinationPath -ErrorAction Stop
        Write-Host "完了: $destinationPath"
    }
    catch {
        # 失敗したZIPを通知し、残りのZIPの処理は続けます。
        Write-Warning "展開に失敗しました: $($archive.FullName) ($($_.Exception.Message))"
        $hadErrors = $true
    }
}

# いずれかの入力・展開でエラーがあれば、失敗を示す終了コードを返します。
exit ([int]$hadErrors)
