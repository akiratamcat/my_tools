"""
-----------------------------------------------------------------------
excel_oldtype.py
EXCEL 旧型式(.xls)ファイル 用処理
-----------------------------------------------------------------------

python.exe -m pip install --upgrade pip
pip install xlrd==1.2.0

"""

import os
from logging import Logger
from typing import Any, List, Tuple

import xlrd  # xlrd 1.2.0

from utility import normalize_string


# EXCEL 旧型式(.xls)ファイル をフルパスで受けて、そのファイル内を検索する
def search_in_excel_file_old_type(
    excel_file_path: str,
    search_term: str,
    case_sensitive: bool,
    width_sensitive: bool,
    progress_callback: Any,
    results: List[Tuple[str, str, str, str, str, str]],
    logger: Logger,
) -> None:
    """EXCEL 旧型式(.xls)ファイル をフルパスで受けて、そのファイル内を検索する

    Args:
        excel_file_path (str): 検索対象の EXCEL ファイル（旧型式）
        search_term (str): 検索したい語句（正規化済）
        case_sensitive (bool): 大文字/小文字を同一視するか否か
        width_sensitive (bool): 全角/半角を同一視するか否か
        progress_callback (Any): 進捗を更新するためのコールバック関数
        results (List[Tuple[str, str, str, str, str, str]]): 検索結果を格納するリスト
        logger (Logger): logging.Logger
    """
    logger.debug(msg="search_in_excel_file_old_type()")
    logger.debug(
        msg=f" --> excel_file_path={excel_file_path}"
        f" search_term={search_term}"
        f" case_sensitive={case_sensitive}"
        f" width_sensitive={width_sensitive}"
    )

    try:
        #
        # 対象ファイルの各シートの全てのセルを調べる
        #

        msg: str = "対象ファイルの各シートの全てのセルを調べる"
        logger.debug(msg=msg)

        # EXCEL ファイルを xlrd で開く
        logger.debug(msg=f"xlrd.open_workbook({excel_file_path})")
        with xlrd.open_workbook(filename=excel_file_path) as workbook:
            # シートごとに処理するループ
            logger.debug(msg=f"len(workbook.sheets())= {len(workbook.sheets())}")
            for sheet in workbook.sheets():
                # シート名を表示
                sheet_name: str = sheet.name
                msg = f"ファイル: {os.path.basename(p=excel_file_path)} シート: {sheet_name}"
                logger.debug(msg)
                progress_callback(msg)
                # シート内のすべてのセルを検索
                for row_index in range(sheet.nrows):
                    for col_index in range(sheet.ncols):
                        # セルの値を取得
                        cell_value: str = str(object=sheet.cell_value(row_index, col_index))
                        # セルが空なら loop continue
                        if len(cell_value) == 0:
                            continue
                        # セルから取得した値を検索条件に合わせて正規化
                        normalized_cell_value: str = normalize_string(
                            s=cell_value,
                            ignore_case=not case_sensitive,
                            ignore_width=not width_sensitive,
                            logger=logger,
                        )
                        # 検索語が含まれる場合は結果に追加
                        if search_term in normalized_cell_value:
                            # 列番号を列文字に変換
                            col_letter: str = ""
                            temp_col_index: int = col_index
                            while temp_col_index >= 0:
                                col_letter = chr(65 + (temp_col_index % 26)) + col_letter
                                temp_col_index = temp_col_index // 26 - 1
                            # セルのアドレスを組み立て
                            cell_address: str = f"{col_letter}:{row_index + 1}"
                            # 結果リストに追加
                            # 旧型式ファイルは図形検索に対応しないため、常に"セル"として追加
                            msg = f"{cell_address} : {normalized_cell_value} に {search_term} が含まれています。"
                            logger.debug(msg=msg)
                            results.append(
                                (
                                    os.path.basename(excel_file_path),
                                    sheet_name,
                                    cell_address,
                                    "セル",
                                    cell_value,
                                    excel_file_path,
                                )
                            )

        # xlrd は close がない。with ブロックを使い、ブロックを抜けると自動的に閉じるようにした。
    except Exception as e:
        msg = f"EXCEL 旧型式.xlsファイル grepエラー {os.path.basename(excel_file_path)}: {e}"
        logger.error(msg=msg)

    return
