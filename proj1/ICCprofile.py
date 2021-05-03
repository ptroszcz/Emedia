

class ICCProfile():
    def __init__(self):
        self.size = None
        self.cmmtype = None
        self.version = None
        self.profile_class = None
        self.color_space = None
        self.connection_space = None
        self.date = []
        self.file_signature = None
        self.platform_target = None
        self.flags = None
        self.device_man = None
        self.device_model = None
        self.device_attr = None
        self.rendering = None
        self.xyzvalues = []
        self.creatorID = None
        self.tag_count = None
        self.tags = []
        self.tagged_elemenet_data = []



    def profile_device_class(self):
        if self.profile_class==0x73636E72:
            return "Profil urządzenia wejściowego"
        if self.profile_class==0x6D6E7472:
            return "Profil urządzenia wyświetlającego"
        if self.profile_class==0x70727472:
            return "Profil urządzenia wyjściowego"
        if self.profile_class==0x6C696E6B:
            return "Profil łącza do urządzenia"
        if self.profile_class==0x73706163:
            return "Profil konwersji przestrzeni kolorów"
        if self.profile_class==0x61627374:
            return "Profil abstrakcyjny"
        if self.profile_class==0x6E6D636C:
            return "Profil nazwanych kolorów"
        else:
            return ("ID: "+str(self.profile_class))

    def profile_color_space(self):
        if self.color_space==0x58595A20:
            return "XYZ"
        if self.color_space==0x4C616220:
            return "Lab"
        if self.color_space==0x4C757620:
            return "Luv"
        if self.color_space==0x59436272:
            return "YCbr"
        if self.color_space==0x59787920:
            return "Yxy"
        if self.color_space==0x52474220:
            return "RGB"
        if self.color_space==0x47524159:
            return "GRAY"
        if self.color_space==0x48535620:
            return "HSV"
        if self.color_space==0x484C5320:
            return "HLS"
        if self.color_space==0x434D594B:
            return "CMYK"
        if self.color_space==0x434D5920:
            return "CMY"
        if self.color_space==0x32434C52:
            return "2CLR"
        if self.color_space==0x33434C52:
            return "3CLR"
        if self.color_space==0x34434C52:
            return "4CLR"
        if self.color_space==0x35434C52:
            return "5CLR"
        if self.color_space==0x36434C52:
            return "6CLR"
        if self.color_space==0x37434C52:
            return "7CLR"
        if self.color_space==0x38434C52:
            return "8CLR"
        if self.color_space==0x39434C52:
            return "9CLR"
        if self.color_space==0x41434C52:
            return "ACLR"
        if self.color_space==0x42434C52:
            return "BCLR"
        if self.color_space==0x43434C52:
            return "CCLR"
        if self.color_space==0x44434C52:
            return "DCLR"
        if self.color_space==0x45434C52:
            return "ECLR"
        if self.color_space==0x46434C52:
            return "FCLR"
        else:
            return ("ID: " +str(self.color_space))

    def profile_connection_space(self):
        if self.profile_class==0x6C696E6B:
            temp=self.profile_class
            self.profile_class=self.connection_space
            result=self.profile_color_space()
            self.profile_class=temp
            return result
        if self.connection_space == 0x58595A20:
            return "XYZ"
        elif self.connection_space == 0x4C616220:
            return "Lab"
        else:
            return ("ID: "+str(self.connection_space))
        
    def profile_date(self):
        year=self.date[0]
        month=self.date[1]
        day=self.date[2]
        hour=self.date[3]
        minute=self.date[4]
        second=self.date[5]
        return (str(day)+"."+str(month)+"."+str(year)+"r., "+str(hour)+":"+str(minute)+":"+str(second))


    def primary_platform_target(self):
        if self.platform_target==0x4150504C:
            return "Apple Computer"
        if self.platform_target==0x4D534654:
            return "Microsoft Corporation"
        if self.platform_target==0x53474920:
            return "Silicon Graphics"
        if self.platform_target==0x53554E57:
            return "Sun Microsystems"
        if self.platform_target==0x54474E54:
            return "Taligent"
        else:
            return ("ID: "+str(self.platform_target))


    def rendering_intend(self):
        if self.rendering==0:
            return "Percepcyjne"
        if self.rendering==1:
            return "Względne kolorymetryczne"
        if self.rendering==2:
            return "Nasycenia"
        if self.rendering==3:
            return "Absolutne kolorymetryczne"
        else:
            return ("ID: "+str(self.rendering))



    def xyzvalues_display(self):
        X=self.xyzvalues[0]+self.xyzvalues[1]/65535
        Y=self.xyzvalues[2]+self.xyzvalues[3]/65535
        Z=self.xyzvalues[4]+self.xyzvalues[5]/65535
        return ("X: "+str(X)+" Y: "+str(Y)+" Z: "+str(Z))



    def tag_data_display(self,offset,size):
        offset=offset-128-4-12*self.tag_count
        for i in range(offset,offset+size):
            print(str(self.tagged_elemenet_data[i]),end=" ")
        print("")

    def display_profile_info(self):
        if self.size == None or self.size == 0:
            return "Profil ICC nie występuje"
        print("Informacje o profilu:")
        print("Wielkość profilu: "+str(self.size))
        print("Rodzaj CMM: "+str(self.cmmtype))
        print("Wersja profilu: "+self.version)
        print("Klasa profilu: "+self.profile_device_class())
        print("Rodzaj przestrzeni kolorów: "+self.profile_color_space())
        print("Rodzaj przestnieni przyłączeniowej: "+ self.profile_connection_space())
        print("Data stworzenia profilu: "+self.profile_date())
        if self.file_signature==0x61637370:
            print("Sygnatura pliku profilu: acsp")
        else:
            print("Sygnatura pliku profilu: ID: "+str(self.file_signature))
        print("Docelowa platforma profilu: " +self.primary_platform_target())
        print("ID flag profilu: "+str(bin(self.flags)))
        print("ID producenta urządzenia, dla którego stworzony jest profil: "+str(self.device_man))
        print("ID modelu urządzenia, dla którego stworzony jest profil: "+str(self.device_model))
        print("ID atrybutów urządzenia, dla którego stworzony jest profil: "+str(bin(self.device_attr)))
        print("Rodzaj renderowania: "+self.rendering_intend())
        print("Wartości XYZ źródła światła w przesrzeni połączeniowej profilów: "+self.xyzvalues_display())
        print("Id twórcy profilu: "+str(self.creatorID))
        print("Liczba tagów: "+str(self.tag_count))
        for i in range(0,self.tag_count):
            print("Tag ID: "+str(self.tags[i][0])+" Offset do danych: "+str(self.tags[i][1])+" Wielkość danych: "+str(self.tags[i][2]))
            print("Zawartość taga:")
            self.tag_data_display(self.tags[i][1],self.tags[i][2])

