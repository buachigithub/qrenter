# テキストファイルデータベースの生成
import qrcode
import random

# テキストファイルデータベースを作成
database = {}
for _ in range(10):
    customer_data = str(random.randint(1000000000, 9999999999))
    entry_code = str(random.randint(100000, 999999))
    database[entry_code] = customer_data

# データベースをQRコードとして保存
for entry_code, customer_data in database.items():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(entry_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"./qrcode/{entry_code}.png")
