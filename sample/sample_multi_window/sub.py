import tkinter as tk


def create_sub_window(win_parent: tk.Tk) -> tk.Toplevel:
    def on_close() -> None:
        win_me.destroy()
        win_parent.deiconify()
        win_parent.focus_force

    win_me = tk.Toplevel()
    win_me.title(string="Sub Window")
    win_me.geometry(newGeometry="400x300")
    win_me.resizable(width=False, height=False)
    win_me.protocol(name="WM_DELETE_WINDOW", func=on_close)
    label = tk.Label(master=win_me, text="This is the sub window")
    label.pack(pady=20)
    return win_me


# お約束のおまじない
if __name__ == "__main__":

    def show_sub_window() -> None:
        win_root.withdraw()
        win_sub: tk.Toplevel = create_sub_window(win_parent=win_root)
        win_sub.focus_force()

    win_root = tk.Tk()
    win_root.title(string="Dummy Main Window")
    win_root.geometry(newGeometry="400x300")
    win_root.resizable(width=False, height=False)
    win_root.focus
    button = tk.Button(master=win_root, text="Open Sub Window", command=show_sub_window)
    button.pack(padx=10, pady=10)
    win_root.mainloop()
