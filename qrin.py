import cv2
from pyzbar.pyzbar import decode
import os
import time
import pygame
import threading 

# テキストファイルデータベースを読み込みする関数
def load_database():
    database = {}
    if not os.path.exists(database_file):
        print(f"データベースファイル '{database_file}' が見つかりません。")
        exit()

    with open(database_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                entry_code, customer_data = parts
                database[entry_code] = customer_data
    return database

# ファイル名の定義
database_file = 'database.txt'
recorded_file = 'recorded.txt'

# 最初にデータベースを読み込む
database = load_database()

# 同じQRコードを再度読み取るまでの待機時間（秒）
ignore_period = 2

# QRコードの最後の読み取り時間を追跡する辞書
last_read_times = {}

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

# pygameの初期化
pygame.mixer.init()

# ユーザー入力を処理する関数
def check_manual_input():
    while True:
        user_input = input()
        
        # 手入力時にデータベースを再読み込み
        database = load_database()

        if user_input in database:
            if user_input not in recorded_qr_codes:
                print(f"OK ({user_input}) - 顧客データ: {database[user_input]}")
                recorded_qr_codes.add(user_input)
                write_recorded_file(recorded_qr_codes)
                pygame.mixer.music.load("ok.wav")
                pygame.mixer.music.play()
            else:
                print("このコードは既に読み取り済みです。")
        else:
            print("入力したコードは無効です。")

# 別スレッドでユーザー入力を待機するスレッドを開始
input_thread = threading.Thread(target=check_manual_input)
input_thread.daemon = True  # メインスレッドが終了したらこのスレッドも終了する
input_thread.start()

# ウェブカメラを起動
cap = cv2.VideoCapture(0)

while True:
    # カメラフレームをキャプチャ
    ret, frame = cap.read()

    # QRコードの読み取り
    decoded_objects = decode(frame)

    # recorded.txt ファイルからデータを再度読み込む
    recorded_qr_codes = read_recorded_file()

    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        
        # QRコードスキャン時にもデータベースを再読み込み
        database = load_database()

        if data in database:
            current_time = time.time()

            # QRコードが一定期間内に再度読み取られていないか確認
            if data not in last_read_times or (current_time - last_read_times[data]) >= ignore_period:
                if data not in recorded_qr_codes:
                    print(f"OK ({data}) - 顧客データ: {database[data]}")
                    last_read_times[data] = current_time
                    recorded_qr_codes.add(data)
                    write_recorded_file(recorded_qr_codes)  # ファイルを更新
                    # 入場が可能な場合、"ok.wav"を再生
                    pygame.mixer.music.load("ok.wav")
                    pygame.mixer.music.play()
                else:
                    # このQRコードがすでに読み取り済みであれば、再度処理しない
                    print(f"このQRコードは既に読み取り済みです。")
                    last_read_times[data] = current_time
            else:
                # 同じQRコードを一定期間内に再度読み取った場合、処理しない
                continue
        else:
            print("入場不可")

    # ウェブカメラの画像を表示（ESCキーで終了）
    cv2.imshow("QR Code Scanner", frame)
    if cv2.waitKey(1) == 27:
        break

# カメラリソースを解放
cap.release()
cv2.destroyAllWindows()
