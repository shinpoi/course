## 1. Linuxの仕組み

### 1-4.
* コンパイラ最適化（実行速度をはやくする）
  * ゆるい順：-O1(-O), -O2, -O3, -O4  
  * -O3からバグが出やすい

### 1-7.
* man [section] command

* section:
  1. ユーザーコマンド (man 1 git)
  2. システムコール (man 2 read)
  3. ライブラリ関数 (man 3 printf)
  4. デバイスファイルなど (man 4 tty)
  5. ファイルフォーマット (man 5 ext4)
  6. ゲーム
  7. 規格など
  8. システム管理用コマンド (man 8 useradd)

***

## 2. Linuxカーネルの世界

### 2-1.
厳密には「Linux」はカーネルだけを指していますが、普段も「Linux OS」の略として使われています。

### 2-2.
libc -> standard C library

***

## 3. Linuxを描き出す３つの概念

### 3-1. ファイルシステム

* ファイル
  * Regular File
  * Directory
  * Symbolic Link
    * Hard Link
    * Soft Link
  * Device File
    * Character Device File (keyboard, printer, etc...)
    * Block Device File (SSD, HDD, etc...)
  * Named Pipe (FIFO)
  * UNIX Domain Socket

### 3-2. プロセス

* Process ID: 一意（唯一）

### 3-3. ストリーム

* ストリームの意味
  * FILE型の値
  * STREAMSカーネルモジュール
* バイト列が出入りするものならば、何でもストリームです。
* パイプ：プロセスとプロセスを繋ぐストリーム

まとめ：

プロセス　＜---　ストリーム　---＞　プロセス  

　/\  
　 |

ストリーム

　 |  
　\/

ファイルシステム

***
