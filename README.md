
# QRで入場できるやつ

本当は学園祭とかで使えたらなーとか思ってたんですけど、当日トラブルだらけになりそうなので小規模のものに活用していきたいなとか思ってたり思ってなかったり。

## 依存関係のインストール

### ・パッケージをインストールする

```
pip install qrcode
```

```
pip install pygame
```

```
pip install opencv-python-headles
```

```
pip install pyzbar
```

### ・Zbarライブラリをインストールする

Linux(Debian系):
```
sudo apt-get install libzbar0
```
macOS:
```
brew install zbar
```
Windowsの人は自分でダウンロードしてね。

http://zbar.sourceforge.net/


## How To Use

すでに割り当てられそうな番号があるときは、その番号をそのままQRコード化して、`databese.txt`の中に`番号,顧客データ`のように１行ずつ入力してね。

まだ割り当てられそうな番号がないときは、`qrmake.py`を適当に実行して、生成された画像ファイルの番号を`databese.txt`の中に`番号,顧客データ`のように１行ずつ入力してね。

（ちなみに顧客データってのはなんでもいいです。「生徒」だったり「特別客」とか。空白だとエラーが出ます。）


## 簡単に（真面目に）言うと

`database.txt`の中には、全ての顧客データを`123456,一般客`のような形式で1行ずつ入力し、

`recorded.txt`の中には、勝手にスキャン済みの番号が`123456`のように記録されていきます。

なお、`recorded.txt`内のスキャン済みの番号を消すと、リセットされます。（一部を削除することもできます。）


## Special Thanks

一部コード協力：たくんま @takunnma5286


## ライセンス

このコードはMITライセンスだよ。詳しくは[ライセンス全文](LICENSE)を見てね。

※同梱している音声ファイルは適用されません。

© 2023 Sotaro Shimada

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
