Waveshare Pico-LCD 1.3 Example Code
https://www.waveshare.com/wiki/Pico-LCD-1.3

- picolcd1inch3.py
waveshare'in lcd kutuphanesi

- hello_world.py
Basit text yazdirma ornegi Sadece 8x8 karakter yazabiliyor

- writer_demo.py
Font kullanarak yazdirma ornegi

- font_to_py.py ile font dosyalari olusturulabilir
onun icin font dosyalarini indirmek gerekiyor
ornek yok

kayitli ornek font dosyalari
font6.py
font10.py
freesans20.py
courier20.py

Yeni font olusturmak icin:
python font_to_py.py <font dosyasi.ttf>  <font boyutu> <font dosyasi.py> -x
Ornek :python font_to_py.py .\ARLRDBD.TTF 28 ArialRounded27.py -x
