import tkinter as tk


def create_sub_window(win_parent: tk.Tk) -> tk.Toplevel:
    def on_close():
        win_me.destroy()
        win_parent.deiconify()
        win_parent.focus_force

    win_me = tk.Toplevel()
    win_me.title("Sub Window")
    win_me.geometry("400x300")
    win_me.resizable(False, False)
    win_me.protocol("WM_DELETE_WINDOW", on_close)
    label = tk.Label(win_me, text="This is the sub window")
    label.pack(pady=20)
    return win_me


# お約束のおまじない
if __name__ == "__main__":

    def show_sub_window():
        win_root.withdraw()
        win_sub = create_sub_window(win_root)
        win_sub.focus_force()

    win_root = tk.Tk()
    win_root.title("Dummy Main Window")
    win_root.geometry("400x300")
    win_root.resizable(False, False)
    win_root.focus
    button = tk.Button(win_root, text="Open Sub Window", command=show_sub_window)
    button.pack(padx=10, pady=10)
    win_root.mainloop()
