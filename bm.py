
"""
bm : a simple cli file compressor and conversion tools 

Compression levels for the jpg/JPEG file : 10 to 95

Compression levels for the pdf file :
    0: default
    1: prepress
    2: printer
    3: ebook
    4: screen

For compressing the pdf files Ghostscript is required
"""

import os
import sys
import subprocess
import os.path
import argparse
import shutil
import img2pdf
from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path

# compressed jpg file
def compressed_jpg(file, quality):
    img = Image.open(file)
    req_quality = int(quality)
    img.save('compressed_'+file,'JPEG',optimze=True,quality=req_quality)
    return
    
# convert png to jpg file
def to_jpg(file):
    img = Image.open(file)
    # Get rid of A(Alpha) from RGBA 
    # since jpg does not support transparency
    rbg_img = img.convert('RGB')
    filename = img.filename.split('.png')
    rbg_img.save(filename[0]+'.jpg')

# Convert JPEG image file to PNG
def to_png(file):
    img = Image.open(file)
    filename = img.filename.split('.jpg')
    img.save(filename[0]+'.png')

# convert jpg/png to pdf
def img_to_pdf(file):
    img = Image.open(file)
    # split the filename for making the pdf file name as same as image file
    img_file_name = img.filename.split('.')
    # print(img_file_name[0])
    pdf_bytes = img2pdf.convert(img.filename)
    pdf_file = open(img_file_name[0]+'.pdf','wb')
    pdf_file.write(pdf_bytes)

# convert jpg to pdf
#TODO: File name as pdf name and to png file format
def pdf_to_img(file):
    images = convert_from_path(file)
    #print(images)
    for i in range(len(images)):
        images[i].save('New_image.jpg', 'JPEG')

# compressed pdf files
def pdf_compressor(input_file, out_file, nq=0):
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }

    if input_file.split('.')[-1].lower() != 'pdf':
        print('Error: input file is not a PDF ')
        sys.exit(1)

    gs = get_ghostscript_path()
    original_size = os.path.getsize(input_file)
    #show in MB
    size_in_mb = original_size/1000000
    print(f'File size: {round(size_in_mb,2)} MB ')
    #ghostscript -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer-dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
    subprocess.call([gs, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS={}'.format(quality[nq]),
        '-dNOPAUSE', '-dQUIET', '-dBATCH',
        '-sOutputFile={}'.format(out_file),
         input_file]
    )
    new_file_size = os.path.getsize(out_file)
    new_file_in_mb = new_file_size/1000000
    print(f'Compressed file size: {round(new_file_in_mb,2)} MB ')

def get_ghostscript_path():
    gs_names = ['gs','gswin32','gswin64']
    for gs in gs_names:
        if shutil.which(gs):
            return shutil.which(gs)
    raise FileNotFoundError('No Ghostscript was found !')

def main():
    parser = argparse.ArgumentParser(
        description= __doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    #parser.add_argument('-i',action='store_true',help='for image manipulation')
    # takes the value for the compression
    parser.add_argument('-q',action='store',help='value for the compression')
    # takes the file as input
    parser.add_argument('-f',action='store',help='input file')
    # images manipulation parser.add_argument('-q',action='store',help='value for the compression')
    parser.add_argument('-jpg',action='store_true',help='compress jpg file')
    parser.add_argument('-cjpg',action='store_true',help='convert to jpg file')
    parser.add_argument('-cpng',action='store_true',help='convert to png file')
    parser.add_argument('-cpdf',action='store_true',help='convert to pdf from image file')
    parser.add_argument('-pjpg',action='store_true',help='convert from pdf to jpg file')
    # for the pdf file compression
    #parser.add_argument('-if',action='store', help='input file for the pdf compressor')
    parser.add_argument('-of',action='store', help='output file for the pdf compressor')
    parser.add_argument('-pdf',action='store_true',help='compress pdf file')
    # show the version
    parser.add_argument('-v','--version',action='version',version='%(prog)s 1.0')

    args = parser.parse_args()
    input_file = args.f
    nquality = args.q
    # for pdf compression 
    outfile = args.of
    #print(type(args.q))

    if args.jpg:
        compressed_jpg(input_file, nquality)
    elif args.cjpg:
        to_jpg(input_file)
    elif args.cpng:
        to_png(input_file)
    elif args.cpdf:
        img_to_pdf(input_file)
    elif args.pjpg:
        pdf_to_img(input_file)
    elif args.pdf:
        pdf_compressor(input_file, outfile, int(nquality))
    else:
        print('Error: invalid options')
        sys.exit(1)

if __name__ == '__main__':
    main()
