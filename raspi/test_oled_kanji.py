#!/usr/bin/env python3
# coding: utf-8

# Raspberry Pi の動作確認 I2C OLED SD1306 に文字を表示する
# Copyright (c) 2023 Wataru KUNINO

##############################
# SD1306  # RasPi # GPIO
##############################
#    SDA  #   3   # GP4
#    SCL  #   5   # GP5
##############################

disp_port = [\
'こんにちは　　　','　ラズベリーパイ','　　　　　　　　','ＯＬＥＤドライバ',\
'　　ｆｏｒ　　　','　Ｃパイソン　　','　　　　　　　　','ｈｔｔｐｓ：／／',\
'ｇｉｔ．ｂｏｋｕ','ｎｉｍｏ．ｃｏｍ','／ｏｌｅｄ／　　','　　　　　　　　',\
'　ｂｙ　国野　亘','　　くにのわたる','　　Ｗａｔａｒｕ','　　ＫＵＮＩＮＯ',\
]

disp_land = [\
'こんにちはラズベリーパイＯＬＥＤ','美咲フォントを使った日本語表示に',\
'対応したデバイスドライバです。　','詳細は下記サイトをご覧ください。',\
'ｈｔｔｐｓ：／／ｇｉｔ．ｂｏｋｕ','ｎｉｍｏ．ｃｏｍ／ｏｌｅｄ／　　',\
'　ｂｙ　国野　亘　くにの　わたる','　　　Ｗａｔａｒｕ　ＫＵＮＩＮＯ',\
]

sd1306 = 0x3C                           # OLED SD1306のI2Cアドレス
d_mode_i = 0x00                         # OLED設定モード
d_mode_w = 0x40                         # OLED描画モード
d_init = b'\xAE\xD5\x80\x8D\x14\x20\x00\xDA\x12\x81\x00\xD9\xF1\xDB\x40\xA4\xA6\xAF'
d_home = b'\x21\x00\x7F\x22\x00\x07'
d_fontx2_map = list()                   # 美咲フォント用メモリマップ

import smbus                            # I2Cインタフェース
from time import sleep                  # timeからsleepを組み込む

def main():
    i2c = smbus.SMBus(1)                    # I2C用オブジェクト生成
    i2c.write_i2c_block_data(sd1306, d_mode_i, list(d_init)) 
    i2c.write_i2c_block_data(sd1306, d_mode_i, list(d_home))
    for x in range(8)[::-1]:
        for y in range(16):
            b = disp_port[y][x].encode('CP932') # シフトJISコードに変換
            c = int.from_bytes(b, 'big')        # 整数に変換
            p_min = 0
            p_max = len(d_fontx2_map) - 1
            while(p_min < p_max):
                p = (p_max - p_min)//2 + p_min
                if c >= d_fontx2_map[p][0]:
                    p_min = p
                if c <= d_fontx2_map[p][1]:
                    p_max = p
            if(p_min == p_max):
                address = d_fontx2_map[p_min][2] + 8 * (c - d_fontx2_map[p_min][0])
                i2c.write_i2c_block_data(sd1306, d_mode_w, list(d_fontx2[address:address+8]))
                # print(disp_port[y][x],hex(c),hex(address),hex(address//8),d_fontx2[address:address+8])
            else:
                i = ord(disp_port[y][x]) - 32
                if i > 0 and i*8+8 <= len(d_font):
                    i2c.write_i2c_block_data(sd1306, d_mode_w, list(d_font[i*8:i*8+8]))
                else:
                    i2c.write_i2c_block_data(sd1306, d_mode_w, list(d_font[0:8]) )
    sleep(3)
    for y in range(8)[::-1]:
        for x in range(16)[::-1]:
            b = disp_land[y][x].encode('CP932') # シフトJISコードに変換
            c = int.from_bytes(b, 'big')        # 整数に変換
            p_min = 0
            p_max = len(d_fontx2_map) - 1
            while(p_min < p_max):
                p = (p_max - p_min)//2 + p_min
                if c >= d_fontx2_map[p][0]:
                    p_min = p
                if c <= d_fontx2_map[p][1]:
                    p_max = p
            if(p_min == p_max):
                address = d_fontx2_map[p_min][2] + 8 * (c - d_fontx2_map[p_min][0])
                font = b''
                for j in range(8):
                    c = 0x00
                    for k in range(8):
                        c += ((d_fontx2[address+7-k] >> j) & 0x01) << k
                    font += c.to_bytes(1,'little')
                i2c.write_i2c_block_data(sd1306, d_mode_w, list(font))
            else: # ASCII処理
                i = ord(disp_land[y][x]) - 32
                if i > 0 and i*8+8 <= len(d_font):
                    font = b''
                    for j in range(8):
                        c = 0x00
                        for k in range(8):
                            c += ((d_font[i*8+7-k] >> j) & 0x01) << k
                        font += c.to_bytes(1,'little')
                    i2c.write_i2c_block_data(sd1306, d_mode_w, list(font))
                else:
                    i2c.write_i2c_block_data(sd1306, d_mode_w, list(d_font[0:8]))
    sleep(3)
    i2c.close()

def load_font():
    return b'\
\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\x10\x10\x00\x10\x00\
\xD8\x48\x90\x00\x00\x00\x00\x00\x14\x7E\x28\x28\x28\xFC\x50\x00\
\x08\x3E\x48\x3C\x12\x7C\x10\x00\x42\xA4\x48\x10\x24\x4A\x84\x00\
\x30\x48\x50\x24\x54\x88\x76\x00\x40\x40\x80\x00\x00\x00\x00\x00\
\x02\x04\x08\x08\x08\x04\x02\x00\x80\x40\x20\x20\x20\x40\x80\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\xFE\x10\x10\x10\x00\
\x00\x00\x00\x00\xC0\x40\x80\x00\x00\x00\x00\xFE\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\xC0\xC0\x00\x02\x04\x08\x10\x20\x40\x80\x00\
\x3C\x42\x42\x42\x42\x42\x3C\x00\x10\x30\x10\x10\x10\x10\x38\x00\
\x3C\x42\x02\x0C\x30\x40\x7E\x00\x3C\x42\x02\x1C\x02\x42\x3C\x00\
\x04\x0C\x14\x24\x44\x7E\x04\x00\x7E\x40\x7C\x42\x02\x42\x3C\x00\
\x3C\x42\x40\x7C\x42\x42\x3C\x00\x7E\x02\x04\x08\x08\x10\x10\x00\
\x3C\x42\x42\x3C\x42\x42\x3C\x00\x3C\x42\x42\x3E\x02\x42\x3C\x00\
\x00\x30\x30\x00\x30\x30\x00\x00\x00\x30\x30\x00\x30\x10\x20\x00\
\x00\x06\x38\xC0\x38\x06\x00\x00\x00\x00\xFE\x00\xFE\x00\x00\x00\
\x00\xC0\x38\x06\x38\xC0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x38\x44\x9A\xAA\xB4\x40\x38\x00\x10\x28\x28\x44\x7C\x82\x82\x00\
\x7C\x42\x42\x7C\x42\x42\x7C\x00\x1C\x22\x40\x40\x40\x22\x1C\x00\
\x78\x44\x42\x42\x42\x44\x78\x00\x7E\x40\x40\x7C\x40\x40\x7E\x00\
\x7E\x40\x40\x7C\x40\x40\x40\x00\x1C\x22\x40\x4E\x42\x22\x1C\x00\
\x42\x42\x42\x7E\x42\x42\x42\x00\x38\x10\x10\x10\x10\x10\x38\x00\
\x02\x02\x02\x02\x02\x42\x3C\x00\x42\x44\x48\x50\x68\x44\x42\x00\
\x40\x40\x40\x40\x40\x40\x7E\x00\x82\xC6\xAA\xAA\x92\x92\x82\x00\
\x42\x62\x52\x4A\x46\x42\x42\x00\x18\x24\x42\x42\x42\x24\x18\x00\
\x7C\x42\x42\x7C\x40\x40\x40\x00\x18\x24\x42\x42\x4A\x24\x1A\x00\
\x7C\x42\x42\x7C\x48\x44\x42\x00\x3C\x42\x40\x3C\x02\x42\x3C\x00\
\xFE\x10\x10\x10\x10\x10\x10\x00\x42\x42\x42\x42\x42\x42\x3C\x00\
\x82\x82\x44\x44\x28\x28\x10\x00\x82\x92\x92\xAA\xAA\x44\x44\x00\
\x82\x44\x28\x10\x28\x44\x82\x00\x82\x44\x28\x10\x10\x10\x10\x00\
\x7E\x02\x04\x08\x10\x20\x7E\x00\x0E\x08\x08\x08\x08\x08\x0E\x00\
\x44\x44\x28\x7C\x10\x7C\x10\x00\xE0\x20\x20\x20\x20\x20\xE0\x00\
\x10\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFE\x00\
\x02\x04\x06\x00\x00\x00\x00\x00\x00\x00\x38\x04\x3C\x44\x3C\x00\
\x40\x40\x58\x64\x44\x44\x78\x00\x00\x00\x38\x44\x40\x44\x38\x00\
\x04\x04\x34\x4C\x44\x44\x3C\x00\x00\x00\x38\x44\x7C\x40\x38\x00\
\x0C\x10\x38\x10\x10\x10\x10\x00\x00\x00\x3C\x44\x3C\x04\x38\x00\
\x40\x40\x58\x64\x44\x44\x44\x00\x10\x00\x10\x10\x10\x10\x10\x00\
\x08\x00\x08\x08\x08\x48\x30\x00\x20\x20\x24\x28\x30\x28\x24\x00\
\x30\x10\x10\x10\x10\x10\x10\x00\x00\x00\x68\x54\x54\x54\x54\x00\
\x00\x00\x58\x64\x44\x44\x44\x00\x00\x00\x38\x44\x44\x44\x38\x00\
\x00\x00\x78\x44\x78\x40\x40\x00\x00\x00\x3C\x44\x3C\x04\x04\x00\
\x00\x00\x58\x64\x40\x40\x40\x00\x00\x00\x3C\x40\x38\x04\x78\x00\
\x00\x20\x78\x20\x20\x24\x18\x00\x00\x00\x44\x44\x44\x4C\x34\x00\
\x00\x00\x44\x44\x28\x28\x10\x00\x00\x00\x44\x54\x54\x28\x28\x00\
\x00\x00\x44\x28\x10\x28\x44\x00\x00\x00\x44\x28\x28\x10\x60\x00\
\x00\x00\x7C\x08\x10\x20\x7C\x00\x06\x08\x08\x10\x08\x08\x06\x00\
\x10\x10\x10\x10\x10\x10\x10\x00\xC0\x20\x20\x10\x20\x20\xC0\x00\
\xC0\x40\x80\x00\x00\x00\x00\x00'

def load_fontx2():
    global d_fontx2_map
    fp = open('misaki.fnt','rb')        # 美咲フォントのファイルを開く
    buf = fp.read()                     # ファイルを読み込み
    fp.close()                          # ファイルを閉じる
    print('Identifer =',buf[0:6].decode())
    print('Font Name =',buf[6:14].decode())
    print('Font Size =',int(buf[14]),'x',int(buf[15]))
    print('Font Type =',int(buf[16]))
    map_size = int(buf[17])
    print('Table Size =', map_size)
    address = 0
    for i in range(map_size):
        code_start = int.from_bytes(buf[18+i*4+0:18+i*4+2], 'little')
        code_end   = int.from_bytes(buf[18+i*4+2:18+i*4+4], 'little')
        d_fontx2_map.append((code_start,code_end,address))
        # print('            ', format(i,'#04x'), hex(code_start),hex(code_end),hex(address))
        address += (code_end - code_start + 1) * 8
    return buf[18 + 4 * map_size:]

d_font = load_font()
print("loaded ASCII fonts, len =",len(d_font))
d_fontx2 = load_fontx2()
print('loaded KANJI fontx2 len =',len(d_fontx2))
while True:
    main()

################################################################################
# 参考文献 8×8 ドット日本語フォント「美咲フォント」
# https://littlelimit.net/misaki.htm
'''
美咲フォントの一部(アルファベット、数字、記号)の全角版(8x8)を使用しました。
下記は権利者によるライセンス表示です。

　These fonts are free softwares.
　Unlimited permission is granted to use, copy, and distribute it, with or without modification, either commercially and noncommercially.
　THESE FONTS ARE PROVIDED "AS IS" WITHOUT WARRANTY.

　これらのフォントはフリー（自由な）ソフトウエアです。
　あらゆる改変の有無に関わらず、また商業的な利用であっても、自由にご利用、複製、再配布することができますが、全て無保証とさせていただきます。

　Copyright(C) 2002-2012 Num Kadoma
'''
################################################################################
# 参考文献
# https://bokunimo.net/ichigojam/oled.html
'''
             8AA  8AC               8B2
800 'INIT    mode 描画位置指定        INIT 
810 let[85],#4000,#2100,#227F,#0700,#D5AE,#8D80,#2014,#DA00,#8112,#D9CF,#DBF1,#A440,#AFA6
820 ifi2cw(60,#8AA,1,#8B2,18)?"E


900 'OUT
910 ifi2cw(60,#8AA,1,#8AC,6)?"E
920 for[98]=0to7:for[99]=0to15:copy#8A2,vpeek(7-[98],[99])*8,8:ifi2cw(60,#8AB,1,#8A2,8)?"E
930 next:next:rtn

' #800 [0]～#87F 128 bytes ロゴ画像64×16px
' #880[64]～#8A1  34 bytes （空き）
' #8A2[81]～#8A9   8 bytes OLED データ8×8px
' #8AA[85]～#8AB   2 bytes OLED モード切替
' #8AC[86]～#8B1   6 bytes OLED 描画位置指定
' #8B2[89]～#8C3  18 bytes OLED 初期化用
' #8C4[98]～#8C7   4 bytes for ループ用変数
' #8C8[100]～8CB   4 bytes 予備

LED モード切替 2 bytes
    ADR, VAL, Description
    #00, #00, Command mode
    #01, #40, Data mode

OLED 初期化用 18 bytes
    ADR, VAL, Description
    #00, #AE, DISPLAY OFF
    #01, #D5, SET DISPLAY CLOCK DIV
    #02, #80,     0x80
    #03, #8D, CHARGE PUMP
    #04, #14,     0x10(enable)/0x14(disable)
    #05, #20, MEMORY MODE
    #06, #00,     0x00
    #07, #DA, SET COMPINS
    #08, #12,     0x12
    #09, #81, SET CONTRAST
    #0A, #CF,     0x7F(defalt)
    #0B, #D9, SET PRECHARGE PERIOD
    #0C, #F1,     0x02(defalt) -> 0xF1
    #0D, #DB, SET VCOM DETECT
    #0E, #40,     0x40
    #0F, #A4, DISPLAY ALLON_RESUME
    #10, #A6, NORMAL DISPLAY
    #11, #AF, DISPLAY ON

OLED 描画位置指定 6 bytes
    ADR, VAL, Description
    #00, #21, COLUMN ADDR
    #01, #00,     Column start
    #02, #7F,     Column end
    #03, #22, PAGE ADDR
    #04, #00,     Page start
    #05, #07,     Page end
'''