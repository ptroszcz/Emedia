


class MetaData():
    def __init__(self):
        self.bmp_size = None
        self.header_size = None
        self.width=None
        self.height=None
        self.color_depth=None
        self.compression_method=None
        self.image_size=None
        self.horizontal_resolution=None
        self.vertical_resolution=None
        self.colors_palette=None
        self.important_colors=None
        self.pixels_per_metre = None
        self.direction_bits_fill = None
        self.halftoning= None
        self.halftoning1 = None
        self.halftoning2 = None
        self.color_encoding = None
        self.red_color_mask = None
        self.green_color_mask = None
        self.blue_color_mask = None
        self.alpha_color_mask = None
        self.color_space = None 
        self.end_points = []
        self.gamma_red = None
        self.gamma_green = None  
        self.gamma_blue= None
        self.intent = None
        self.profile_data_offset = None
        self.profile_size = None 


    def header_type(self):
        if self.header_size == None:
            return "Nie wczytano jeszcze naglowka pliku"
        if self.header_size == 12:
            return "BITMAPCOREHEADER"
        if self.header_size == 64:
            return "OS22XBITMAPHEADER"
        if self.header_size == 16:
            return "Shorter OS22XBITMAPHEADER"
        if self.header_size == 40:
            return "BITMAPINFOHEADER"
        if self.header_size == 52:
            return "BITMAPV2INFOHEADER"
        if self.header_size == 56:
            return "BITMAPV3INFOHEADER"
        if self.header_size == 108:
            return "BITMAPV4HEADER"
        if self.header_size == 124:
            return "BITMAPV5HEADER"
        else:
            return "Nie poprawny nagłówek"

    def compression_type(self):
        if (self.compression_method==0):
           return "BI_RGB"
        elif (self.compression_method==1):
            return "BI_RLE8"
        elif (self.compression_method==2):
            return "BI_RLE4"
        elif (self.compression_method==3):
            return "BI_BITFIELDS"
        elif (self.compression_method==4):
            return "BI_JPEG"
        elif (self.compression_method==5):
            return "BI_PNG"
        elif (self.compression_method==6):
            return "BI_ALPHABITFIELDS"
        elif (self.compression_method==11):
            return "BI_CMYK"
        elif (self.compression_method==12):
            return "BI_CMYKRLE8"
        elif (self.compression_method==13):
            return "BI_CMYKRLE4"
        else:
            return ("ID:"+str(self.compression_method))
    
    
    def halftoning_algorothm(self):
        if self.halftoning == 0:
            return "None"
        elif self.halftoning == 1:
            return "Error diffusion"
        elif self.halftoning == 2:
            return "PANDA"
        elif self.halftoning == 3:
            return "Super-circle"
    

    def color_space_DIB(self):
        if self.color_space==0:
            return "LCS_CALIBRATED_RGB"
        elif self.color_space==1:
            return "LCS_sRGB"
        elif self.color_space==2:
            return "LCS_WINDOWS_COLOR_SPACE"
        elif self.color_space==3:
            return "PROFILE_LINKED"
        elif self.color_space==4:
            return "PROFILE_EMBEDDED"
        else:
            return ("ID:" + str(self.color_space))
        

    def intent_type(self):
        if self.intent==0:
            return "LCS_GM_ABS_COLORIMETRIC"
        elif self.intent==1:
            return "LCS_GM_BUSINESS"
        elif self.intent==2:
            return "LCS_GM_GRAPHICS"
        elif self.intent==3:
            return "LCS_GM_IMAGES"
        else:
            return ("ID: "+ str(self.intent))




    def display_meta_data(self):
        print("Wielkosc pliku w bajtach: " + str(self.bmp_size))
        print("Rozmiar nagłówka: " + str(self.header_size)+", Typ: " + self.header_type())
        print("Szerokosc w pikselach: "+str(self.width)+", Wysokosc w pikselach: "+str(self.height))
        print("Głębia kolorów: "+str(self.color_depth))
        if (self.header_size>=40):
            print("Metoda kompresji: "+self.compression_type())
            print("Wielkość obrazu: "+str(self.image_size))
            print("Rozdzielczość pozioma w pixelach na metr: "+str(self.horizontal_resolution)+", Rozdzielczość pionowa w pixelach na metr: "+str(self.vertical_resolution))
            if (self.color_depth<=8 and self.colors_palette==0):
                print("Liczba kolorów w palecie kolorów: "+str(2**self.color_depth))
            else:
                print("Liczba kolorów w palecie kolorów: "+str(self.colors_palette))
            print("Liczba ważnych kolorów w palecie kolorów: " +str(self.important_colors))
            if self.header_size>40:
                print("Maska kolorów, która określa czerwony składnik każdego piksela: "+str(int(self.red_color_mask)) )
                print("Maska kolorów, która określa zielony składnik każdego piksela: "+str(int(self.green_color_mask)) )
                print("Maska kolorów, która określa niebieski składnik każdego piksela: "+str(int(self.blue_color_mask)) )
                if self.header_size>52:
                    print("Maska kolorów, która określa składnik alfa każdego piskela: "+str(int(self.alpha_color_mask)) )
                    if (self.header_size>56):
                        print("Rodzaj przestrzeni kolorów DIB:" +self.color_space_DIB())
                        print("Gamma dla czerwieni: "+str(self.gamma_red))
                        print("Gamma dla zieleni: "+str(self.gamma_green))
                        print("Gamma dla niebieskiego: "+str(self.gamma_blue))
                        if (self.header_size>108):
                            print("Zamiar renderowania: "+self.intent_type())
                            print("Offset palety kolorów od poczatku nagłowka: "+str(self.profile_data_offset))
                            print("Wielkośc palety kolorów: "+str(self.profile_size))

