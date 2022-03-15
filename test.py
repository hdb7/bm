#!/usr/bin/env python3

import os 

#cmds for testing
jpg_compresed = 'python3 bm.py -jpg -f IU.jpg -q 40 '
jpg_to_png = 'python3 bm.py -cpng -f IU.jpg'
pdf_to_jpg = 'python3 bm.py -pjpg -f mementopython3-english.pdf'
pdf_compresed = 'python3 bm.py -pdf -f mementopython3-english.pdf -q 3 -of out.pdf'
img_to_pdf = 'python3 bm.py -cpdf -f IU.jpg'
png_to_jpg = 'python3 bm.py -cjpg -f BM.png'

print("Testing...")

cmds = [jpg_compresed,jpg_to_png,pdf_to_jpg,pdf_compresed,img_to_pdf,png_to_jpg]

counter = 1
try: 
  for x in cmds:
    print(f'Testing{counter}: {x}')
    os.system(x)
    counter += 1
except:
  print('Test failed !')

print('All Test passed !')