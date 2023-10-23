import cv2
from pyzbar.pyzbar import decode
import os
import time
import pygame

# テキストファイルデータベースを読み込み
database = {}
database_file = 'database.txt'

if not os.path.exists(database_file):
    print(f"データベースファイル '{database_file}' が見つかりません。")
    exit()

with open(database_file, 'r') as file:
    for line in file:
        parts = line.strip().split(',')
        if len(parts) == 2:
            entry_code, customer_data = parts
            database[entry_code] = customer_data
        else:
            print(f"無効な行: {line}")

# 同じQRコードを再度読み取るまでの待機時間（秒）
ignore_period = 2

# QRコードの最後の読み取り時間を追跡する辞書
last_read_times = {}

# 既に読み取ったQRコードを記録するファイル
recorded_file = 'recorded.txt'

# recorded.txt ファイルからデータを読み込む関数
def read_recorded_file():
    recorded_qr_codes = set()
    if os.path.exists(recorded_file):
        with open(recorded_file, 'r') as file:
            for line in file:
                recorded_qr_codes.add(line.strip())
        return recorded_qr_codes
    return set()

# recorded.txt ファイルにデータを書き込む関数
def write_recorded_file(recorded_qr_codes):
    with open(recorded_file, 'w') as file:
        for qr_code in recorded_qr_codes:
            file.write(f"{qr_code}\n")

# recorded.txt ファイルからデータを読み込む
recorded_qr_codes = read_recorded_file()

# ウェブカメラを起動
cap = cv2.VideoCapture(0)

# pygameの初期化
pygame.mixer.init()

while True:
    # カメラフレームをキャプチャ
    ret, frame = cap.read()

    # QRコードの読み取り
    decoded_objects = decode(frame)

    # recorded.txt ファイルからデータを再度読み込む
    recorded_qr_codes = read_recorded_file()

    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        if data in database:
            current_time = time.time()
            if data not in last_read_times or (current_time - last_read_times[data]) >= ignore_period:
                if data not in recorded_qr_codes:
                    print(f"入場可能 - 顧客データ: {database[data]}")
                    last_read_times[data] = current_time
                    recorded_qr_codes.add(data)
                    write_recorded_file(recorded_qr_codes)  # ファイルを更新
                    # 入場が可能な場合、"ok.wav"を再生
                    pygame.mixer.music.load("ok.wav")
                    pygame.mixer.music.play()
                else:
                    print(f"このQRコードは既に読み取り済みです。")
            else:
                print(f"同じQRコードを再度読み取る前に待機してください.")
        else:
            print("入場不可")

    # ウェブカメラの画像を表示（ESCキーで終了）
    cv2.imshow("QR Code Scanner", frame)
    if cv2.waitKey(1) == 27:
        break

# カメラリソースを解放
cap.release()
cv2.destroyAllWindows()
