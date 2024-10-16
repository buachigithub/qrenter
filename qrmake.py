# 必要なライブラリのインポート
import qrcode
import random
from PIL import Image, ImageDraw, ImageFont
import os

# 保存先ディレクトリが存在しない場合、ディレクトリを作成
output_dir = "./qrcode"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# テキストファイルデータベースを作成
database = {}
for _ in range(10):
    customer_data = str(random.randint(1000000000, 9999999999))
    entry_code = str(random.randint(100000, 999999))
    database[entry_code] = customer_data

# フォント設定（Arialが無い場合はシステムにインストールされた他のフォントを指定してください）
try:
    font = ImageFont.truetype("MPLUS.ttf", 36)  # フォントサイズ36
except IOError:
    font = ImageFont.load_default()

# データベースをQRコードとして保存
for entry_code, customer_data in database.items():
    # QRコードの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(entry_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # QRコード画像を取得し、サイズを調整
    img = img.convert("RGB")
    img_width, img_height = img.size

    # テキスト用に新しい画像を作成（QRコード画像の下にスペースを作成）
    new_img = Image.new("RGB", (img_width, img_height + 50), "white")  # 50ピクセルの余白
    new_img.paste(img, (0, 0))  # QRコードを上に貼り付け

    # テキストを描画
    draw = ImageDraw.Draw(new_img)
    
    # 'textbbox' でテキストのサイズを取得 (左上と右下の座標)
    text_bbox = draw.textbbox((0, 0), entry_code, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    
    # テキストを中央に配置
    text_position = ((img_width - text_width) // 2, img_height + 5)  # 中央揃え
    draw.text(text_position, entry_code, font=font, fill="black")

    # 画像を保存
    new_img.save(f"{output_dir}/{entry_code}.png")

    # database.txt にエントリーコードを追記
    with open("database.txt", "a") as f:
        f.write(entry_code + ",\n")
