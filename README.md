# oled

OLED SSD1306 and SSD1309 Device Driver for Raspberry Pi and Raspberry Pi Pico  

![Schematic1](https://bokunimo.net/blog/wp-content/uploads/2023/05/DSC_2650wd.jpg)  

## Operation Cheked OLED Modules

- SUNHOKEY Electronics SSD1306  
- Seeed Studio Grove OLED Display 0.96" module  
- DIY MORE (深圳市四海芯舟科技) Transparent OLED Screen SSD1309  

## bokunimo.net Blog Site

- 解説ページ(bokunimo.netのブログ内)：  
	[https://bokunimo.net/blog/raspberry-pi/3619/](https://bokunimo.net/blog/raspberry-pi/3619/)  
- Google Transrate to English：  
	[https://bokunimo.net/blog/raspberry-pi/3619/](https://bokunimo-net.translate.goog/blog/raspberry-pi/3619/?_x_tr_sl=ja&_x_tr_tl=en)  

## Schematic for OLED SSD1306

Fig. 1; Schematic for OLED SSD1306:  
![Schematic1](https://bokunimo.net/blog/wp-content/uploads/2023/05/ssd1306schema.png)  

Fig. 2; Connect VCC, GND, SCL, and SDA to your Raspberry Pi:  

![Photo1](https://bokunimo.net/blog/wp-content/uploads/2023/05/DSC_2662w.jpg)  


## Schematic for OLED SSD1309

SSD1309 is need to change the chip resistor on the OLED module board. According to the silk-printed "I2C PORT: R8, R4" and "SPI PORT R9" on the board, please remove a chip resistor R9, and solder 0Ω jumpers on R8 and R4. The following schematic is an example of the reset circuit.

Fig. 3; schematic of reset circuit:

![Schematic2](https://bokunimo.net/blog/wp-content/uploads/2023/05/ssd1609schema_pi.png)  

Fig. 4; R9 is removed, and R8 and R4 are soldered:
![Photo2](https://bokunimo.net/blog/wp-content/uploads/2023/04/DSC_2612w.jpg)  

## Usage, Download and Display Contents

	pi@raspberrypi:~ $ git clone https://bokunimo.net/git/oled ⏎  
	pi@raspberrypi:~ $ cd oled/raspi ⏎  
	pi@raspberrypi:~/oled/raspi $ ls -1 ⏎  
	misaki.fnt  ............. Misaki Fonts on FONTX2 format
	misaki_README.txt  ...... LICENSE text for Misaki Fonts
	test_oled.py  ........... Program for ASCII Character 
	test_oled_kanji.py  ..... Program for Japanese Character
	  
	pi@raspberrypi:~ $ ./test_oled_kanji.py ⏎  

## How to change the text

"disp_port" and "disp_land" in this program are variables for the characters on the display.
The variable disp_port is for portrait, and the variable disp_port is for landscape view.

----------------------------------------------------------------

## GitHub Pages (This Document)
* [https://git.bokunimo.com/oled/](https://git.bokunimo.com/oled/)  

----------------------------------------------------------------

# git.bokunimo.com GitHub Pages site
[http://git.bokunimo.com/](http://git.bokunimo.com/)  

----------------------------------------------------------------
