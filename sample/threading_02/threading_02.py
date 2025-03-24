import datetime
import os
import random
import threading
from logging import Formatter, Logger, getLogger, handlers
from queue import Queue
from time import sleep
from tkinter import Tk, ttk
from typing import List


# メイン画面とイベントループ処理
def main() -> None:
    # -----------------------------------------------------------------
    # クロージャ
    # -----------------------------------------------------------------

    def start_button() -> None:
        if command[0]:
            return
        logger.debug(msg="start_button() が呼び出されました。")
        command[0] = True
        func_list.append(threading.Thread(target=thread_func_put, args=("func_put_1",)))
        func_list.append(threading.Thread(target=thread_func_put, args=("func_put_2",)))
        func_list.append(threading.Thread(target=thread_func_put, args=("func_put_3",)))
        func_list.append(threading.Thread(target=thread_func_put, args=("func_put_4",)))
        func_list.append(threading.Thread(target=thread_func_put, args=("func_put_5",)))
        func_list.append(threading.Thread(target=thread_func_get))
        for func in func_list:
            func.start()

    def stop_button() -> None:
        logger.debug(msg="stop_button() が呼び出されました。")
        command[0] = False

    def thread_func_put(name: str) -> None:
        logger.debug(msg=f"thread_func_put({name}) が呼び出されました。")
        while command[0]:
            sleep_time: float = random.random() * 5
            sleep(sleep_time)
            dt_now_jst_aware: datetime.datetime = datetime.datetime.now(
                tz=datetime.timezone(offset=datetime.timedelta(hours=9))
            )
            queue_data.put(
                item=(name, dt_now_jst_aware.strftime(format="%Y年%m月%d日 %H:%M:%S"), str(object=sleep_time))
            )
            logger.debug(msg=f"thread_func_put({name}) がキューへ put しました")

    def thread_func_get() -> None:
        logger.debug(msg="thread_func_get() が呼び出されました。")
        while command[0]:
            if queue_data.qsize() > 0:
                while queue_data.qsize() > 0:
                    (f_name, f_date, f_wait) = queue_data.get()
                    result_table.insert(parent="", index="end", values=(f_name, f_date, f_wait, queue_data.qsize()))
                result_table.yview_moveto(1.0)
            sleep(1)

    # -----------------------------------------------------------------
    # スレッド共有
    # -----------------------------------------------------------------

    command: List[bool] = [False]
    func_list: List[threading.Thread] = []
    queue_data: Queue = Queue(maxsize=20)

    # -----------------------------------------------------------------
    # ロガーの初期化
    # -----------------------------------------------------------------

    logger: Logger = getLogger(name=__name__)
    logger.setLevel(level="DEBUG")
    rotating_handler = handlers.RotatingFileHandler(
        os.path.splitext(os.path.abspath(__file__))[0] + ".log",
        mode="w",
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    format = Formatter(fmt="%(asctime)s : %(levelname)s : %(filename)s - %(message)s")
    rotating_handler.setFormatter(format)
    logger.addHandler(hdlr=rotating_handler)
    logger.debug(msg="起動しました。")

    # -----------------------------------------------------------------
    # GUI 組み立て (Tkinter.tk & ttk)
    # -----------------------------------------------------------------

    try:
        logger.debug("メインウィンドウを作成します。")

        root: Tk = Tk()
        root.title("Trhreding sample")

        frame1: ttk.Frame = ttk.Frame(master=root)
        frame1.pack(padx=10, pady=5)

        columns_list: List[List] = [
            ["thread name", 100, False],
            ["put date", 160, False],
            ["wait time", 80, False],
            ["queue length", 100, False],
        ]
        result_table: ttk.Treeview = ttk.Treeview(
            master=frame1, columns=[item[0] for item in columns_list], show="headings"
        )
        for col_namme, col_width, col_stretch in columns_list:
            result_table.heading(column=col_namme, text=col_namme)
            result_table.column(column=col_namme, width=col_width, stretch=col_stretch)
        result_table.grid(row=0, column=0, columnspan=len(columns_list), pady=5, sticky="nsew")

        scrollbar: ttk.Scrollbar = ttk.Scrollbar(master=frame1, orient="vertical", command=result_table.yview)
        result_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=len(columns_list), sticky="ns")

        frame2: ttk.Frame = ttk.Frame(master=root)
        frame2.pack(padx=10, pady=5)

        ttk.Button(master=frame2, text="開始", command=start_button).grid(row=1, column=0, pady=10, sticky="E")
        ttk.Button(master=frame2, text="停止", command=stop_button).grid(row=1, column=1, pady=10, sticky="E")

        logger.debug(msg="メインウィンドウを作成してイベントループを開始します。")

        # メインウィンドウのイベントループ
        root.mainloop()

    except Exception as e:
        msg: str = f"メインウィンドウの作成中にエラーが発生しました: {e}"
        logger.error(msg=msg)
        return


# お約束の main() 関数
if __name__ == "__main__":
    main()
