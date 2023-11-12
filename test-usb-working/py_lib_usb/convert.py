from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import barcode 
from barcode.writer import ImageWriter


def write_barcode(bar_text,my_width=416,my_height=135) :
#EAN13(str(), writer=ImageWriter()).write(rv)
    ean13 = barcode.get("ean13",bar_text,writer=ImageWriter())
    fp = BytesIO()
    ean13.write(fp)
    bt = fp.getvalue()
    fp.seek(0)
    img = Image.open(fp)

    width,height = img.size
    left = 45
    top = 0
    right = width -45
    bottom = height -30

    img_crop = img.crop((left,top,right,bottom))

    newsize = (my_width,my_height)
    img_final = img_crop.resize(newsize)

    bit_im = img_final.convert("1")
    list_of_pixels = list(bit_im.getdata())
    
    return list_of_pixels

def show_image (list_of_pixels,width,height) :
    img2 = Image.new("1",size=[width,height])
    img2.putdata(list_of_pixels)
    img2.show()

def my_write_text (txt_string, width, height, fontsize=20, save=0):
    
    img = Image.new ("RGB",size=[width,height],color = (255,255,255))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("mitr.ttf",fontsize)
    # text = "ABCDEFGกขคงจฉ"

    draw.text((0,0),txt_string,font=font,align="left",fill=(0,0,0,255) )
    bit_im = img.convert("1")
    list_of_pixels = list(bit_im.getdata())

    for i in list_of_pixels :
        if (i != 0x00) and (i!= 0xFF):
            print ("FOUND SOMETHING %d"%(i))


    pixel_array = bytearray(list_of_pixels)
    if (save == 1) :
        to_save = ""
        for i in range (0,27):
            pixel_str = ''.join(format(x, '02x') for x in pixel_array[i:416*(i-1)])
            to_save = to_save + pixel_str + "\n"

        pixel_file = open ("pixel.txt","w")
        pixel_file.write(to_save)
        pixel_file.close()
        

    return list_of_pixels

# Convert back Bits to Bytes to save
def bits_to_byte (filename ,save = 0) :
    read_filename = filename +".bits"
    write_filename = filename + ".bytes"
    
    printer_bits_file = open(read_filename,"r")
    list_printer_bits = []
    for pixel_line in printer_bits_file:
        lines = pixel_line.split(",")
        for x in lines :
            list_printer_bits.append (int(str(x),16))
    printer_bits_file.close()
    printer_bits = len (list_printer_bits)
    printer_bits_string = ""
    for i in range(0,printer_bits) : # PRINTER_BYTES :
        tmp = ''
        if (list_printer_bits[i] == 255) :
             tmp = '1'
        else:
            tmp = '0'
        printer_bits_string = printer_bits_string + tmp

    list_printer_bytes = []
    for i in range (0,printer_bits,8) :
        bits_binary = printer_bits_string[i:i+8]
        decimal_representation = int(bits_binary, 2)
        list_printer_bytes.append (decimal_representation)

    if (save == 1 ) :
        pixel_str = ','.join(format(x, '02x') for x in list_printer_bytes)
        pixel_file = open (write_filename,"w")
        pixel_file.write(pixel_str)
        pixel_file.close()

    return list_printer_bytes


    return list_of_pixels

# Convert back Bits to Bytes to save
def list_bits_to_byte (list_printer_bits ,save = 0) :
    write_filename = "LIST_from_bits.bytes"

    printer_bits = len (list_printer_bits)
    printer_bits_string = ""
    for i in range(0,printer_bits) : # PRINTER_BYTES :
        tmp = ''
        if (list_printer_bits[i] == 255) :
             tmp = '1'
        else:
            tmp = '0'
        printer_bits_string = printer_bits_string + tmp

    

    list_printer_bytes = []
    for i in range (0,printer_bits,8) :
        bits_binary = printer_bits_string[i:i+8]
        decimal_representation = int(bits_binary, 2)
        list_printer_bytes.append (decimal_representation)
    
    if (save == 1 ) :
        pixel_str = ','.join(format(x, '02x') for x in list_printer_bytes)
        pixel_file = open (write_filename,"w")
        pixel_file.write(pixel_str)
        pixel_file.close()

    return list_printer_bytes



# read bytes from Printer and Convert to Bits Then Put to Image to Show
def list_bytes_to_bit (list_printer_bytes,save = 0) :
    write_filename = "LIST_from_bytes.bits"
    printer_bytes = len(list_printer_bytes)

    printer_bits_string = ""
    for i in range(0,printer_bytes) : # PRINTER_BYTES :
        tmp = format(list_printer_bytes[i], '08b')
        printer_bits_string = printer_bits_string + tmp


    list_printer_bits = []

    
    for c in printer_bits_string :
        if (c == '1') :
            list_printer_bits.append(255)
        else :
            list_printer_bits.append(0)
    
    if (save == 1 ) :
        pixel_str = ""
        pixel_str = ','.join(format(x, '02x') for x in list_printer_bits)
        pixel_file = open (write_filename,"w")
        pixel_file.write(pixel_str)
        pixel_file.close()

    return list_printer_bits

def bytes_to_bit (filename,save = 0) :

    read_filename = filename + ".bytes"
    write_filename = filename +".bits"
    printer_pixel_file = open(read_filename,"r")
    list_printer_bytes = []

    for pixel_line in printer_pixel_file:
        lines = pixel_line.split(",")
        for x in lines :
            list_printer_bytes.append (int(str(x),16))
    printer_pixel_file.close()

    printer_bytes = len(list_printer_bytes)


    printer_bits_string = ""
    for i in range(0,printer_bytes) : # PRINTER_BYTES :
        tmp = format(list_printer_bytes[i], '08b')
        printer_bits_string = printer_bits_string + tmp


    list_printer_bits = []

    
    for c in printer_bits_string :
        if (c == '1') :
            list_printer_bits.append(255)
        else :
            list_printer_bits.append(0)
    
    if (save == 1 ) :
        pixel_str = ""
        pixel_str = ','.join(format(x, '02x') for x in list_printer_bits)
        pixel_file = open (write_filename,"w")
        pixel_file.write(pixel_str)
        pixel_file.close()

    return list_printer_bits

# end Bytes to Bits 
def test_1() :
    ## convert file from pcap and save
    A_list_printer_bits = bytes_to_bit ("TO_BITS_AAA" , 1 )

    img3 = Image.new("1",size=[416,27])
    img3.putdata(A_list_printer_bits)
    img3.show()

    # convert and save
    A_list_printer_bytes = bits_to_byte("TO_BYTES_AAA" , 1 )

    # convert and no save 
    B_list_printer_bits = bytes_to_bit ("TO_BYTES_AAA", 0)

    img4 = Image.new("1",size=[416,27])
    img4.putdata(B_list_printer_bits)
    img4.show()


#test_1()
#my_write_text ( "HELLOWORLD" ,416,27,fontsize=20,save=0)


## DRAW IMAGE IN CANVAS
## RETURN PIXEL IN BITS
list_canvas_bits = my_write_text("TESTING 1.2.3.4", 416,27, save=0)
#show_image (list_canvas_bits,416,27)
#list_bytes_to_bit (list_canvas_bits,1)
list_bits_to_byte (list_canvas_bits,1)

