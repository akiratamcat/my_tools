import sys
import tkinter as tk

from sub import create_sub_window


def main() -> None:
    def on_close() -> None:
        win_root.destroy()
        sys.exit()

    def show_sub_window() -> None:
        win_root.withdraw()
        win_sub: tk.Toplevel = create_sub_window(win_parent=win_root)
        win_sub.focus_force()

    win_root = tk.Tk()
    win_root.title(string="Main Window")
    win_root.geometry(newGeometry="400x300")
    win_root.resizable(width=False, height=False)
    win_root.protocol(name="WM_DELETE_WINDOW", func=on_close)
    win_root.focus_force

    button = tk.Button(master=win_root, text="Open Sub Window", command=show_sub_window)
    button.pack(padx=10, pady=10)

    win_root.mainloop()


# お約束のおまじない
if __name__ == "__main__":
    main()
