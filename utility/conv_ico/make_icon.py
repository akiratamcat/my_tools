import io

import cairosvg
from PIL import Image

# SVGからICOを生成
svg_path = "app_icon.svg"
output_path = "app_icon.ico"
# SVG→PNG（256x256）
sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
imgs = []
for w, h in sizes:
    png_data = cairosvg.svg2png(url=svg_path, output_width=w, output_height=h)
    if not isinstance(png_data, bytes):
        print(f"サイズ {w}x{h} のPNGデータ生成に失敗しました")
        continue
    img = Image.open(io.BytesIO(png_data)).convert("RGBA")
    imgs.append(img)
imgs[0].save(output_path, format="ICO", sizes=sizes)
print("app_icon.ico created")
