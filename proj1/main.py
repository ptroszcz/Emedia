from BMPDecoder import BMPDecoder 
from operation import fft, show_image

def main():
    bmp=BMPDecoder()
    file_name="v5ICC2.bmp"
    bmp.readFile(file_name)
    bmp.read_header_info()
    print(bmp.pixel_offset)
    bmp.meta.display_meta_data()
    bmp.load_color_table()
    bmp.load_profile_data()
    bmp.profile.display_profile_info()
    bmp.save_anoanonymization("zapisany.bmp")
    fft("emedia/image/"+file_name)
    show_image("emedia/image/"+file_name)
    show_image("emedia/image/zapisany.bmp")
    

if __name__=='__main__':
    main()