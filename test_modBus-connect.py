from os import path
from pymodbus import client
from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient
import configparser

from pymodbus.file_message import WriteFileRecordRequest

class Modbus_connect():
    
    #test display list from module
    def print_outputFrom_register(result):
        for i in range(result) :
            print("round"+str(i)+": "+hex(result[i]))

    #connect Modbus TCP client
    def connect_client(self,ip_add):
        self.Client_Modbus = ModbusTcpClient(ip_add)

    #convert to mac(HEX) to string
    def mac_convertTOstring(self,mac):
        hex_mac = str(hex(mac[0])+hex(mac[1])+hex(mac[2]))
        hex_mac = "0x"+self.uppercase_string(hex_mac.replace("0x",""))
        # hex_mac = hex_mac.upper
        return hex_mac

    #convert status to string
    def status_convert(stu):
        if(stu == hex(0)):
            return "normal status"
        elif(stu == hex(99)):
            return "abnormal status"

    def uppercase_string(word):
        NWord =""
        for i in word:
            switcher = {
                "a": "A",
                "b": "B",
                "c": "C",
                "d": "D",
                "e": "E",
                "f": "F"   
            }
            NWord += switcher.get(i,i)
        return NWord
                
    #///////////////////////////////////////////////////////////////////////////////////////////////////////
    # core function py modbus to user 
    #///////////////////////////////////////////////////////////////////////////////////////////////////////

    #write single&multi register values
    #bit_address = device bit-address 
    #bit_value = payload 
    #num_regist = in case multi-writ **default =1**
    def write_bit_register(self,bit_value=1,bit_address=0,num_regist=1):
        self.Client_Modbus.write_registers(bit_address,[bit_value]*num_regist)

    def mac_read(self):
        mac_addr = 0x0000
        mac_read = self.mac_convertTOstring(self.Client_Modbus.read_holding_registers(mac_addr,3).registers)
        return mac_read

    def fireware_read(self):
        version_addr =0x0001
        firmVersion_read = self.Client_Modbus.read_input_registers(version_addr,1).registers
        return hex(firmVersion_read[0])

    def device_id_read(self):
        deID_addr = 0x0000
        deID = self.Client_Modbus.read_input_registers(deID_addr,1).registers
        return  hex(deID[0])

    def status_read(self):
        status_addr = 0x038A
        status = self.Client_Modbus.read_input_registers(status_addr,4).registers
        MES_sta = self.status_convert(hex(status[0]))
        SDC_sta = self.status_convert(hex(status[1]))
        NTP_sta = self.status_convert(hex(status[2]))
        TCP_sta = self.status_convert(hex(status[3]))
        return MES_sta,SDC_sta,NTP_sta,TCP_sta

    def update_firmware(self):
        OTA_update_addr = 0xFFFFFF63C0
        self.write_bit_register(0x1,OTA_update_addr,1)


    #///////////////////////////////////////////////////////////////////////////////////////////////////////
    # core function py configparser to user 
    #///////////////////////////////////////////////////////////////////////////////////////////////////////

    #print data to ini file
    #device_name = string
    #status = string
    #FTP = oject form
    #firmware = uint
    def ini_print(self,device_name,status,FTP_data,firmware_version,id):
        self.data = configparser.ConfigParser() #inherit parser object

        path ='ini/'
        file_name = path+'config_'+device_name+'.ini'
        Device_data ={"id":id,"status":status}
        up_version ={"available version":firmware_version}
        self.data[device_name] = Device_data
        self.data['FTP server'] = FTP_data
        self.data['update version'] = up_version
        with open(file_name, 'w') as configfile:
            self.data.write(configfile)
            print("ini file printed")

    #return all section in .ini file
    def list_section(self):
        return self.data.sections()

    #convert .ini file to dict
    def read_INI_to_dict(self,path):
        #config = configparser.ConfigParser()
        self.data.read(path)
        dic_con = {}
        for section in self.list_section(self.data):
            dic_con[section]={}
            for key,value in self.data.items(section):
                dic_con[section][key]=value
        return dic_con 

if __name__ == "__main__":
    
    path = '/ini/EMU-B20MC'
    #connect client
    ip = '******'
    Word = "ac2d"
    #Word = uppercase_string(Word)
    #print(Word)
    '''
    client = connect_client(ip)
    print(client) #test status connect
    #test read
    mac = mac_read()
    print("\nmac: "+ mac)
    device_ID = device_id_read()
    print("\ndevice ID: "+str(device_ID))
    firmVersion = fireware_read()
    print("\nver.device: "+str(firmVersion))
    MES,SDC,NTP,TCP = status_read()
    print("MES status: "+MES)
    print("\nSDC status: "+SDC)
    print("\nNTP status: "+NTP)
    print("\nTCP status: "+TCP)

    #test write

    #///////////////////////////////////////////////////////////////////////////////////////////////////////

    FTP_data={"ip address":ip,"mac address":mac}
    status = {"MES status":MES,"SDC status":SDC,"NTP status":NTP,"TCP status":TCP}
    ini_print("EMU-B20MC",status,FTP_data,firmVersion,device_ID)
    test_dic_convert = read_INI_to_dict(path)
    print(test_dic_convert)

    #close connection
    client.close()
    '''