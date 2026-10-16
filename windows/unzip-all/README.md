# ZIP一括展開ツール

指定したZIPファイル、またはフォルダ内のZIPファイルを、それぞれZIPと同じ場所にある同名フォルダへ展開するPowerShellツールです。

## ファイル構成

| ファイル | 説明 |
| --- | --- |
| `Unzip-All.ps1` | ZIPファイルの検索と展開を行うスクリプト |
| `Unzip-All.bat` | ZIPファイルまたはフォルダをドラッグ＆ドロップして実行するためのバッチファイル |
| `Test-Unzip-All.ps1` | 展開処理を検証するテストスクリプト |
| `Unzip-All.Tests.txt` | テスト実行時に生成・更新されるテスト結果 |

## 動作環境

- Windows
- Windows PowerShell（`powershell.exe`）

Windows PowerShellの実行ポリシーによってスクリプトを直接起動できない場合は、以下の実行例のように `-ExecutionPolicy Bypass` を指定してください。これはその起動に限って適用され、システムの実行ポリシーを変更しません。

## ZIPを展開する

このフォルダでPowerShellを開き、ZIPファイルまたは検索対象のフォルダを指定して実行します。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\Unzip-All.ps1" "C:\files\archive.zip"
```

フォルダを指定すると、そのフォルダ以下の階層から `.zip` ファイルを再帰的に検索して展開します。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\Unzip-All.ps1" "C:\files\archives"
```

複数のZIPファイルやフォルダも一度に指定できます。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\Unzip-All.ps1" "C:\files\first.zip" "C:\files\archives"
```

または、`Unzip-All.bat` にZIPファイルやフォルダをドラッグ＆ドロップして実行できます。

### 展開時の動作

- ZIPごとに、ZIPファイルと同じ場所へZIPと同名のフォルダを作成して展開します。たとえば `C:\files\archive.zip` は `C:\files\archive\` に展開されます。
- 展開先に同名のフォルダがすでにある場合、そのフォルダと中身を削除してから展開します。必要なファイルがないか確認してから実行してください。
- あるZIPの展開に失敗しても、残りのZIPの処理を続けます。警告を出力し、いずれかの入力または展開でエラーがあれば終了コード `1` を返します。エラーがなければ `0` を返します。
- フォルダ内にZIPが見つからない場合は、その旨を表示します。

## テストを実行する

このフォルダで次のコマンドを実行します。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\Test-Unzip-All.ps1"
```

テストは一時フォルダにテスト用ファイルとZIPを作成し、実際の `Unzip-All.ps1` を起動して検証します。テスト後、一時データは削除されます。

現在のテスト項目:

1. 展開先が存在しない場合に、ZIPの内容を展開できること。
2. 既存の展開先フォルダを削除し、ZIPの新しい内容に置き換えられること。

テスト結果は既定でこのフォルダの `Unzip-All.Tests.txt` に日本語で出力されます。別の保存先を指定する場合は、`-OutputPath` を使用します。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\Test-Unzip-All.ps1" -OutputPath "C:\temp\Unzip-All.Tests.txt"
```

テスト成功時は終了コード `0`、失敗時は `1` を返します。結果ファイルには実行日時、各テストの成否、および成功・失敗件数が記録されます。
