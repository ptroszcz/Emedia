from BMPDecoder import BMPDecoder 
from operation import fft, show_image
from RSA import *

def main():
    bmp=BMPDecoder()
    file_name="linuxg.bmp"
    bmp.readFile(file_name)
    bmp.read_header_info()
    #d,e,n=create_keys()
    #print("n: "+str(n))
    #print("e: "+str(e))
    #print("d: "+str(d))
    #bmp.encrypt()
    bmp.encrypt_ready()
    #bmp.encryptCBC()
    bmp.save_ecrypted_file('encrypted.bmp')
    #bmp.savefile('encrypted.bmp')
    bmp.decrypt_ready()
    #bmp.decryptCBC()
    #bmp.decrypt()
    bmp.save_decrypted_file('decrypted.bmp')
    #print(bmp.pixel_offset)
    #bmp.meta.display_meta_data()
    #bmp.load_color_table()
    #if bmp.load_profile_data():
        #bmp.profile.display_profile_info()
    #bmp.save_anoanonymization("zapisany.bmp")
    #fft("emedia/image/"+file_name)
    #show_image("emedia/image/"+file_name)
    #show_image("emedia/image/zapisany.bmp")
    

if __name__=='__main__':
    main()