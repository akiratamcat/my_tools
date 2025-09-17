import os
import tkinter as tk
from tkinter import filedialog, messagebox

import cairosvg
from PIL import Image


def make_square_with_transparency(img: Image.Image) -> Image.Image:
    w, h = img.size
    if w == h:
        return img.convert("RGBA")
    size = max(w, h)
    new_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    left = (size - w) // 2
    top = (size - h) // 2
    new_img.paste(img.convert("RGBA"), (left, top))
    return new_img


def convert_svg_to_png(svg_path: str) -> Image.Image:
    png_data = cairosvg.svg2png(url=svg_path)
    return Image.open(io.BytesIO(png_data))


def convert_to_ico(src_path: str, dst_path: str):
    ext = os.path.splitext(src_path)[1].lower()
    if ext == ".svg":
        img = convert_svg_to_png(src_path)
    else:
        img = Image.open(src_path)
    img = make_square_with_transparency(img)
    sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
    imgs = [img.resize(size, Image.LANCZOS) for size in sizes]
    imgs[0].save(dst_path, format="ICO", sizes=sizes)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("画像→アイコン変換ツール")
        self.src_dir = tk.StringVar()
        self.dst_dir = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="元画像フォルダ:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.src_dir, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="選択", command=self.select_src_dir).grid(row=0, column=2)
        tk.Label(self.root, text="保存先フォルダ:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.dst_dir, width=40).grid(row=1, column=1)
        tk.Button(self.root, text="選択", command=self.select_dst_dir).grid(row=1, column=2)
        tk.Button(self.root, text="変換開始", command=self.start_conversion).grid(
            row=2, column=0, columnspan=3, pady=10
        )

    def select_src_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.src_dir.set(d)

    def select_dst_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.dst_dir.set(d)

    def start_conversion(self):
        src = self.src_dir.get()
        dst = self.dst_dir.get()
        if not src or not dst:
            messagebox.showerror("エラー", "両方のフォルダを選択してください")
            return
        exts = [".png", ".bmp", ".svg"]
        files = [f for f in os.listdir(src) if os.path.splitext(f)[1].lower() in exts]
        if not files:
            messagebox.showinfo("情報", "変換対象の画像がありません")
            return
        for f in files:
            try:
                src_path = os.path.join(src, f)
                dst_path = os.path.join(dst, os.path.splitext(f)[0] + ".ico")
                convert_to_ico(src_path, dst_path)
            except Exception as e:
                messagebox.showerror("変換エラー", f"{f}: {e}")
        messagebox.showinfo("完了", "変換が完了しました")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
