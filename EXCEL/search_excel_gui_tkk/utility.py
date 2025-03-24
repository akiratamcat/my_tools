"""
-----------------------------------------------------------------------
utility.py
共通処理など
-----------------------------------------------------------------------

"""

import unicodedata
from logging import Logger


# 文字列を正規化する関数
def normalize_string(
    s: str,
    ignore_case: bool,
    ignore_width: bool,
    logger: Logger,
) -> str:
    """文字列を正規化する関数

    Args:
        s (str): 正規化したい文字列
        ignore_case (bool): 大文字/小文字を同一視するか否か
        ignore_width (bool): 全角/半角を同一視するか否か
        logger (Logger): logging.Logger

    Returns:
        str: 条件に従って正規化した結果の文字列
    """
    logger.debug(msg="normalize_string()")
    msg: str = ""
    out_s: str = s
    try:
        if ignore_case:
            out_s = s.lower()  # 大文字・小文字を同一視（小文字に変換）
        if ignore_width:
            out_s = unicodedata.normalize("NFKC", s)  # 全角・半角を同一視
        msg = f"正規化 {s} -> {out_s}"
        logger.debug(msg=msg)
    except Exception as e:
        msg = f"文字列 {s} 正規化中にエラーが発生しました: {e}"
        logger.error(msg=msg)
    #
    return out_s
