import cv2
from pyzbar.pyzbar import decode
import os
import time
import pygame
import json

# テキストファイルデータベースを読み込み
database = {}
database_file = 'database.json'

# 同じQRコードを再度読み取るまでの待機時間（秒）
ignore_period = 2

# QRコードの最後の読み取り時間を追跡する辞書
last_read_times = {}
"""
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
"""
# ウェブカメラを起動
cap = cv2.VideoCapture(0)

# pygameの初期化
pygame.mixer.init()

while True:
    # カメラフレームをキャプチャ
    ret, frame = cap.read()

    # QRコードの読み取り
    decoded_objects = decode(frame)

    # recorded.txt ファイルからデータを読み込む
    if not os.path.exists(database_file):
        print(f"データベースファイル '{database_file}' が見つかりません。")
        exit()

    with open(database_file, 'r') as file:
        database = json.load(file)

    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        current_time = time.time()
        if not data in last_read_times: #最後に読み込まれたのはいつか辞書に記載がない場合に追加する
            last_read_times[data] = ignore_period
        if  (current_time - last_read_times[data]) >= ignore_period: #最後に読み込まれたリストを参照して、ignore_preiod秒立っていない場合ははじく、
            last_read_times[data] = current_time
            if (data in database["haireru"] or data in database["haitta"]): #はいれるか読み取り済みかにかかわらず入っているか判定
                    if data in database["haireru"]: #はいれる場合はそのデータベースを入ったリストにコピーして、はいれるリストから削除
                        print("入場可能 - 顧客データ: " + database["haireru"][data])
                        database["haitta"][data] = database["haireru"][data]
                        database["haireru"].pop(data)
                        with open(database_file, "wt") as file:
                            json.dump(database, file, ensure_ascii=False, indent=4)  # ファイルを更新
                        # 入場が可能な場合、"ok.wav"を再生
                        pygame.mixer.music.load("ok.wav")
                        time.sleep(0.5)
                        pygame.mixer.music.play()
                    else:
                        print(f"このQRコードは既に読み取り済みです。(id={data})")
            else:
                print(f"入場不可(id={data})")

    # ウェブカメラの画像を表示（ESCキーで終了）
    cv2.imshow("QR Code Scanner", frame)
    if cv2.waitKey(1) == 27:
        break

# カメラリソースを解放
cap.release()
cv2.destroyAllWindows()
