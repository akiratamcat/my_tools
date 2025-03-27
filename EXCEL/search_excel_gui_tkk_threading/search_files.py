"""
-----------------------------------------------------------------------
EXCELファイルに grep する GUI ツール
-----------------------------------------------------------------------

"""

import os
from logging import Logger
from typing import Any, List, Tuple

from excel_newtype import search_in_excel_file_new_type
from excel_oldtype import search_in_excel_file_old_type
from utility import normalize_string


def search_files(
    folder_path: str,
    search_term: str,
    recursive: bool,
    case_sensitive: bool,
    width_sensitive: bool,
    shape_search: bool,
    progress_callback: Any,
    logger: Logger,
) -> List[Tuple[str, str, str, str, str, str]]:
    """
    指定されたパスから EXCEL ファイルを探して、指定された検索語を含むセルを検索し、結果をリストで返す関数

    Args:
        folder_path (str): EXCELファイルを検索する起点となるフォルダのパス
        search_term (str): 検索したい語句
        recursive (bool): folder_path 以下を再帰的に検索するか否か
        case_sensitive (bool): 大文字/小文字を同一視するか否か
        width_sensitive (bool): 全角/半角を同一視するか否か
        shape_search (bool): 図形内のテキストも検索するか否か（但し 新形式 .xlsx, .xlsm ファイルのみ）
        progress_callback (Any): 進捗を更新するためのコールバック関数
        logger (Logger): logging.Logger

    Returns:
        List[Tuple[str, str, str, str, str]]: 検索結果をメインウィンドウのテーブル構造に合わせたリストで返す
    """

    logger.debug(msg="search_in_excel_files()")

    # 検索条件に従って検索語句を正規化
    normalized_search_term: str = normalize_string(
        s=search_term,
        ignore_case=not case_sensitive,
        ignore_width=not width_sensitive,
        logger=logger,
    )

    # 検索結果を格納するリストを初期化
    results: List[Tuple[str, str, str, str, str, str]] = []

    # 指定したフォルダ内のすべてのファイルを取得
    for root, dirs, files in os.walk(folder_path):
        msg: str = f"フォルダ: {root}"
        logger.debug(msg)
        progress_callback(msg)
        # ファイルごとに処理するループ
        for filename in files:
            if filename.endswith((".xlsx", ".xlsm", ".xls")):
                # ファイルのパスを組み立て
                file_path: str = os.path.join(root, filename).replace("/", os.sep)

                if filename.endswith(".xls"):
                    # EXCEL 旧型式.xlsファイル対応
                    logger.debug(msg=f"EXCEL 旧型式.xlsファイルが見つかりました {file_path}")
                    search_in_excel_file_old_type(
                        excel_file_path=file_path,
                        search_term=normalized_search_term,
                        case_sensitive=case_sensitive,
                        width_sensitive=width_sensitive,
                        progress_callback=progress_callback,
                        results=results,
                        logger=logger,
                    )
                elif filename.endswith(".xlsx") or filename.endswith(".xlsm"):
                    # EXCEL 新形式 .xlsx, .xlsm ファイル対応
                    logger.debug(msg=f"EXCEL 新形式 .xlsx, .xlsm ファイルが見つかりました {file_path}")
                    search_in_excel_file_new_type(
                        excel_file_path=file_path,
                        search_term=normalized_search_term,
                        case_sensitive=case_sensitive,
                        width_sensitive=width_sensitive,
                        shape_search=shape_search,
                        progress_callback=progress_callback,
                        results=results,
                        logger=logger,
                    )
                else:
                    pass  # 処理対象のファイルではない

        # 再帰的に検索しない場合は、フォルダ内のファイルをすべて検索したら終了
        if not recursive:
            logger.debug(msg="再帰的に検索しない。")
            break

    return results
