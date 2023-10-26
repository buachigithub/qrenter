
# QRで入場できるやつ

本当は学園祭とかで使えたらなーとか思ってたんですけど、当日トラブルだらけになりそうなので小規模のものに活用していきたいなとか思ってたり思ってなかったり。

## これはなに

入場チケット1枚1枚に違うQRコードを印刷し、**一度入ったチケットでの再度入場**や**チケット複製**、**存在しないチケット**での入場を防ぐことができるようなものです。

`recorded.txt`はリアルタイム更新に対応しているため、このプログラムをファイルサーバー上に置き、複数のPCで起動すると、2つ以上の入場口を設置することができます。

（改造してくれても、いいんですよ）

## インストール方法

Pythonがインストールされている前提です。

### 1.依存関係をインストールする

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

### 2.Zbarライブラリをインストールする

Linux(Debian系):
```
sudo apt-get install libzbar0
```
macOS:
```
brew install zbar
```
Windowsの人は自分でダウンロードしてね。

※追記　プリインストールされている場合が多いようです。エラーが出た時だけ入れてもいいかも

http://zbar.sourceforge.net/


## 使い方

すでに割り当てられそうな番号があるときは、その番号をそのままQRコード化して、`databese.txt`の中に`番号,顧客データ`のように１行ずつ入力してね。

まだ割り当てられそうな番号がないときは、`qrmake.py`を適当に実行して、生成された画像ファイルの番号を`databese.txt`の中に`番号,顧客データ`のように１行ずつ入力してね。

（ちなみに顧客データってのはなんでもいいです。「生徒」だったり「特別客」とか。空白だとエラーが出ます。）


## 簡単に（真面目に）言うと

`database.txt`の中には、全ての顧客データを`123456,一般客`のような形式で1行ずつ入力し、

`recorded.txt`の中には、勝手にスキャン済みの番号が`123456`のように記録されていきます。

なお、`recorded.txt`内のスキャン済みの番号を消すと、リセットされます。（一部を削除することもできます。）

### つまりどういうこと

一度読み取ったQRコード（番号）は、`recorded.txt`に記録されるため、再度読み取ることはできませんが、`recorded.txt`はリアルタイムで読み込んでいるため、番号を消せば、再度読み取ることができるようになります。


## Special Thanks

一部コード協力：たくんま @takunnma5286


## ライセンス

このコードはMITライセンスだよ。詳しくは[ライセンス全文](LICENSE)を見てね。

※同梱している音声ファイルは適用されません。

© 2023 Sotaro Shimada

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
