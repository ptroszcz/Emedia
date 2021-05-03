from MetaData import MetaData
from ICCprofile import ICCProfile



class BMPDecoder():
    def __init__(self):
        self.data = []
        self.pixel_offset=0
        self.meta = MetaData()
        self.profile = ICCProfile()


    def readFile(self,fname:str):
        try:
            with open("emedia/image/"+fname,"rb") as file:
                while True:
                    byte=file.read(1)
                    if not byte:
                        break
                    self.data.append(byte.hex())
                file.close()
        except FileNotFoundError:
            print("File not found.")
            raise FileNotFoundError
        

    def check_header(self):
        possible_header={"BM","BA","CI","CP","IC","PT"}
        header=(bytes.fromhex(self.data[0])).decode("ASCII")+(bytes.fromhex(self.data[1])).decode("ASCII")
        #print(header)
        for i in possible_header:
            if (i==header):
                return True
        return False

    def BMP_size(self):
        hex_size=self.data[5]+self.data[4]+self.data[3]+self.data[2]
        dec_size=int(hex_size,16)
        #print(dec_size)
        return dec_size

    def pixel_array_offset(self):
        hex_offset=self.data[13]+self.data[12]+self.data[11]+self.data[10]
        dec_offset=int(hex_offset,16)
        #print(dec_offset)
        self.pixel_offset=dec_offset
        return dec_offset

    def read_header_info(self):
        if (not self.check_header()):
            raise ValueError("Plik BMP ma niepoprawny naglowek")
        self.meta.bmp_size=self.BMP_size()
        self.pixel_array_offset()
        hex_offset=self.data[17]+self.data[16]+self.data[15]+self.data[14]
        dec_offset=int(hex_offset,16)
        self.meta.header_size=dec_offset
        if (self.meta.header_size==12):
            self.meta.width=int(self.data[19]+self.data[18],16)
            self.meta.height=int(self.data[21]+self.data[20],16)
            self.meta.color_depth=int(self.data[25]+self.data[24],16)
        else:
            self.meta.width=int(self.data[21]+self.data[20]+self.data[19]+self.data[18],16)
            self.meta.height=int(self.data[25]+self.data[24]+self.data[23]+self.data[22],16)
            self.meta.color_depth=int(self.data[29]+self.data[28],16)
            if self.meta.header_size>=40:
                self.meta.compression_method=int(self.data[33]+self.data[32]+self.data[31]+self.data[30],16)
                self.meta.image_size=int(self.data[37]+self.data[36]+self.data[35]+self.data[34],16)
                self.meta.horizontal_resolution=int(self.data[41]+self.data[40]+self.data[39]+self.data[38],16)
                self.meta.vertical_resolution=int(self.data[45]+self.data[44]+self.data[43]+self.data[42],16)
                self.meta.colors_palette=int(self.data[49]+self.data[48]+self.data[47]+self.data[46],16)
                self.meta.important_colors=int(self.data[53]+self.data[52]+self.data[51]+self.data[50],16)
                if self.meta.header_size==64:
                    self.meta.pixels_per_metre=int(self.data[55]+self.data[54],16)
                    self.meta.direction_bits_fill=int(self.data[59]+self.data[58],16)
                    self.meta.halftoning=int(self.data[61]+self.data[60],16)
                    self.meta.halftoning1=int(self.data[65]+self.data[64]+self.data[63]+self.data[62],16)
                    self.meta.halftoning2=int(self.data[69]+self.data[68]+self.data[67]+self.data[66],16)
                    self.meta.color_encoding=int(self.data[73]+self.data[72]+self.data[71]+self.data[70],16)
                
                if self.meta.header_size>40:
                    self.meta.red_color_mask=int(self.data[57]+self.data[56]+self.data[55]+self.data[54],16)
                    self.meta.green_color_mask=int(self.data[61]+self.data[60]+self.data[59]+self.data[58],16)
                    self.meta.blue_color_mask=int(self.data[65]+self.data[64]+self.data[63]+self.data[62],16)
                    if self.meta.header_size>52:
                        self.meta.alpha_color_mask=int(self.data[69]+self.data[68]+self.data[67]+self.data[66],16)
                        if self.meta.header_size>56:
                            self.meta.color_space=int(self.data[73]+self.data[72]+self.data[71]+self.data[70],16)
                            self.meta.end_points=[]
                            for i in range(74,110):
                                self.meta.end_points.append(self.data[i])
                            temp_int=int(self.data[111]+self.data[110],16)
                            temp_fractional=int(self.data[113]+self.data[112],16)
                            temp=str(temp_int)+"."+str(temp_fractional)
                            self.meta.gamma_red=float(temp)
                            temp_int=int(self.data[115]+self.data[114],16)
                            temp_fractional=int(self.data[117]+self.data[116],16)
                            temp=str(temp_int)+"."+str(temp_fractional)
                            self.meta.gamma_green=float(temp)
                            temp_int=int(self.data[119]+self.data[118],16)
                            temp_fractional=int(self.data[121]+self.data[120],16)
                            temp=str(temp_int)+"."+str(temp_fractional)
                            self.meta.gamma_blue=float(temp)
                            if self.meta.header_size>108:
                                self.meta.intent=int(self.data[125]+self.data[124]+self.data[123]+self.data[122],16)
                                self.meta.profile_data_offset=int(self.data[129]+self.data[128]+self.data[127]+self.data[126],16)
                                self.meta.profile_size=int(self.data[133]+self.data[132]+self.data[131]+self.data[130],16)


    def load_color_table(self):
        if self.meta.color_depth>8:
            print("Głębia kolorów większa niż 8. Tabela kolorów nie występuje.")
            pass
        else:
            begin=14+self.meta.header_size
            if self.meta.compression_method==3 and self.meta.header_size==40: 
                begin+=12
            elif self.meta.compression_method==4 and self.meta.header_size==40:
                begin+=16
            length=0
            if self.meta.colors_palette==0 or self.meta.colors_palette==None:
                length=(2**self.meta.color_depth)*4
            else:
                length=4*self.meta.colors_palette
            color_table=[]
            color=[]
            color.append(int(self.data[begin],16))
            color.append(int(self.data[begin+1],16))
            color.append(int(self.data[begin+2],16))
            color.append(int(self.data[begin+3],16))
            color_table.append(color.copy())
            i=4
            while(i<length):
                color[0]=int(self.data[begin+i],16)
                i+=1
                color[1]=int(self.data[begin+i],16)
                i+=1
                color[2]=int(self.data[begin+i],16)
                i+=1
                color[3]=int(self.data[begin+i],16)
                i+=1
                color_table.append(color.copy())
            print("Paleta kolorów:")
            for j in range(0,len(color_table)):
                print(str(j)+". R: "+str(color_table[j][2])+" G: "+str(color_table[j][1])+" B: "+str(color_table[j][0])+" Alpha: "+str(color_table[j][3]))



    def load_profile_data(self):
        if (self.meta.header_size==124 and self.meta.profile_size>0):
            begin=self.meta.profile_data_offset+14
            self.profile.size=int(self.data[begin]+self.data[begin+1]+self.data[begin+2]+self.data[begin+3],16)
            self.profile.cmmtype=int(self.data[begin+4]+self.data[begin+5]+self.data[begin+6]+self.data[begin+7],16)
            major_nr=int(self.data[begin+8],16)
            minor_nr=int(self.data[begin+9],16)
            self.profile.version=str(major_nr)+"."+str(minor_nr)
            self.profile.profile_class=int(self.data[begin+12]+self.data[begin+13]+self.data[begin+14]+self.data[begin+15],16)
            self.profile.color_space = int(self.data[begin+16]+self.data[begin+17]+self.data[begin+18]+self.data[begin+19],16)
            self.profile.connection_space = int(self.data[begin+20]+self.data[begin+21]+self.data[begin+22]+self.data[begin+23],16)
            self.profile.date=[(int(self.data[begin+24]+self.data[begin+25],16)),(int(self.data[begin+26]+self.data[begin+27],16)),(int(self.data[begin+28]+self.data[begin+29],16)),(int(self.data[begin+30]+self.data[begin+31],16)),(int(self.data[begin+32]+self.data[begin+33],16)),(int(self.data[begin+34]+self.data[begin+35],16))]
            self.profile.file_signature=int(self.data[begin+36]+self.data[begin+37]+self.data[begin+38]+self.data[begin+39],16)
            self.profile.platform_target=int(self.data[begin+40]+self.data[begin+41]+self.data[begin+42]+self.data[begin+43],16)
            self.profile.flags=int(self.data[begin+44]+self.data[begin+45]+self.data[begin+46]+self.data[begin+47],16)
            self.profile.device_man=int(self.data[begin+48]+self.data[begin+49]+self.data[begin+50]+self.data[begin+51],16)
            self.profile.device_model=int(self.data[begin+52]+self.data[begin+53]+self.data[begin+54]+self.data[begin+55],16)
            self.profile.device_attr=int(self.data[begin+56]+self.data[begin+57]+self.data[begin+58]+self.data[begin+59]+self.data[begin+60]+self.data[begin+61]+self.data[begin+62]+self.data[begin+63],16)
            self.profile.rendering=int(self.data[begin+64]+self.data[begin+65]+self.data[begin+66]+self.data[begin+67],16)
            self.profile.xyzvalues=[(int(self.data[begin+68]+self.data[begin+69],16)),(int(self.data[begin+70]+self.data[begin+71],16)),(int(self.data[begin+72]+self.data[begin+73],16)),(int(self.data[begin+74]+self.data[begin+75],16)),(int(self.data[begin+76]+self.data[begin+77],16)),(int(self.data[begin+78]+self.data[begin+79],16))]
            self.profile.creatorID=int(self.data[begin+80]+self.data[begin+81]+self.data[begin+82]+self.data[begin+83],16)
            begin=begin+128
            self.profile.tag_count=int(self.data[begin]+self.data[begin+1]+self.data[begin+2]+self.data[begin+3],16)
            begin=begin+4
            for i in range(0,self.profile.tag_count):
                self.profile.tags.append([int(self.data[begin+i*12]+self.data[begin+i*12+1]+self.data[begin+i*12+2]+self.data[begin+i*12+3],16),int(self.data[begin+i*12+4]+self.data[begin+i*12+5]+self.data[begin+i*12+6]+self.data[begin+i*12+7],16),int(self.data[begin+i*12+8]+self.data[begin+i*12+9]+self.data[begin+i*12+10]+self.data[begin+i*12+11],16)])
            begin=begin+12*self.profile.tag_count
            for i in range(0,(self.meta.profile_size-128-4-12*self.profile.tag_count)):
                self.profile.tagged_elemenet_data.append(self.data[begin+i])
            return True
        else:
            print("Paleta kolorów nie występuje.")
            return False




    def save_anoanonymization(self,file_name:str):
        with open("emedia/image/"+file_name,'wb') as file:
            offset=14+self.meta.header_size
            if self.meta.compression_method==3 and self.meta.header_size==40: 
                offset+=12
            elif self.meta.compression_method==4 and self.meta.header_size==40:
                offset+=16
            if self.meta.color_depth<=8:
                if self.meta.colors_palette==0 or self.meta.colors_palette==None:
                    offset+=(2**self.meta.color_depth)*4
                else:
                    offset+=4*self.meta.colors_palette
            byte_offset=offset.to_bytes(4,'big').hex()
            pixel_storage=int((self.meta.width*self.meta.color_depth+31)/32)
            pixel_storage=pixel_storage*4*self.meta.height
            if self.meta.compression_method==1:
                pixel_array=[]
                i=0
                j=0
                while(i<pixel_storage):
                    pixel_array.append(bytes.fromhex(self.data[self.pixel_offset+j]))
                    i=i+int(self.data[self.pixel_offset+j],16)
                    j=j+1
                    pixel_array.append(bytes.fromhex(self.data[self.pixel_offset+j]))
                    j=j+1
                pixel_storage=j
            profile_offset=0
            if (self.meta.header_size==124 and self.meta.profile_size>0):
                profile_offset=self.meta.profile_size
            BMP_new_size=offset+pixel_storage+profile_offset
            byte_BMP_new_size=BMP_new_size.to_bytes(4,'big').hex()
            for i in range(0,2):
                file.write(bytes.fromhex(self.data[i]))
            count=7
            while(count>0):
                file.write(bytes.fromhex(byte_BMP_new_size[count-1]+byte_BMP_new_size[count]))
                count-=2
            for i in range(6,10):
                file.write(bytes.fromhex("00"))
            count=7
            while(count>0):
                file.write(bytes.fromhex(byte_offset[count-1]+byte_offset[count]))
                count-=2
            #header
            if self.meta.header_size==12:
                for i in range(14,26):
                    file.write(bytes.fromhex(self.data[i]))
            else:
                for i in range(14,30):
                    file.write(bytes.fromhex(self.data[i]))
                if self.meta.header_size>16:
                    for i in range(30,34):
                        file.write(bytes.fromhex(self.data[i]))
                    for i in range(34,46):
                        file.write(bytes.fromhex("00"))
                    for i in range(46,54):
                        file.write(bytes.fromhex(self.data[i]))
                    if (self.meta.header_size>40):
                        if self.meta.compression_method==3:
                            for i in range(54,66):
                                file.write(bytes.fromhex(self.data[i]))
                        else:
                            for i in range(54,66):
                                file.write(bytes.fromhex("00"))
                        if self.meta.header_size==56:
                            for i in range(66,70):
                                file.write(bytes.fromhex(self.data[i]))
                        if self.meta.header_size>56:
                            for i in range(66,74):
                                file.write(bytes.fromhex(self.data[i]))
                            if self.meta.color_space==0:
                                for i in range(74,122):
                                    file.write(bytes.fromhex(self.data[i]))
                            else:
                                for i in range(74,122):
                                    file.write(bytes.fromhex("00"))
                            if self.meta.header_size==124:
                                if (profile_offset==0):
                                    for i in range(122,126):
                                        file.write(bytes.fromhex("00"))
                                    for i in range(126,138):
                                        file.write(bytes.fromhex(self.data[i]))
                                else:
                                    for i in range(122,126):
                                        file.write(bytes.fromhex("10"))
                                    byte_profile_offset=(BMP_new_size-profile_offset-14).to_bytes(4,'big').hex() 
                                    count=7
                                    while(count>0):
                                        file.write(bytes.fromhex(byte_profile_offset[count-1]+byte_profile_offset[count]))
                                        count-=2   
                                    for i in range(130,138):
                                        file.write(bytes.fromhex(self.data[i]))
            for i in range(14+self.meta.header_size,offset):
                file.write(bytes.fromhex(self.data[i]))
            #print(offset)
            #print(pixel_storage)
            if self.meta.compression_method==1:
                for i in range(0,len(pixel_array)):
                    file.write(pixel_array[i])
            else:
                for i in range(self.pixel_offset,self.pixel_offset+pixel_storage):
                    file.write(bytes.fromhex(self.data[i]))
            if self.meta.profile_size!=None and self.meta.profile_size!=0:
                for i in range(14+self.meta.profile_data_offset,14+self.meta.profile_data_offset+profile_offset):
                    file.write(bytes.fromhex(self.data[i]))

                




