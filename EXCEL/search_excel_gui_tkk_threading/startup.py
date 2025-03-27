"""
-----------------------------------------------------------------------
EXCELファイルを対象とした grep gui ツール
-----------------------------------------------------------------------

"""

import os
from logging import Formatter, Logger, getLogger, handlers

from gui import gui_main


def main() -> None:
    """
    ロガーを初期化して、GUI画面を表示する。
    """

    # ロガーの初期化
    my_logger: Logger = getLogger(name=__name__)
    my_logger.setLevel(level="DEBUG")  # 開発中はログレベルを DEBUG に上書き設定
    rotating_handler = handlers.RotatingFileHandler(
        filename=os.path.splitext(os.path.abspath(__file__))[0] + ".log",
        mode="w",
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    format = Formatter(fmt="%(asctime)s : %(levelname)s : %(filename)s - %(message)s")
    rotating_handler.setFormatter(format)
    my_logger.addHandler(hdlr=rotating_handler)

    # GUI 画面表示
    gui_main(logger=my_logger)

    return


if __name__ == "__main__":
    """
    お約束の boot up 処理
    """
    main()
