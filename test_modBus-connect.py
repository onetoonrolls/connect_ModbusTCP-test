from os import path
from pymodbus import client
from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient
import configparser

from pymodbus.file_message import WriteFileRecordRequest


#test display list from module
def print_outputFrom_register(result):
    for i in range(result) :
        print("round"+str(i)+": "+hex(result[i]))

#connect Modbus TCP client
def connect_client(ip_add):
    return ModbusTcpClient(ip_add)

#convert to mac(HEX) to string
def mac_convertTOstring(mac):
    hex_mac = str(hex(mac[0])+hex(mac[1])+hex(mac[2]))
    hex_mac = "0x"+uppercase_string(hex_mac.replace("0x",""))
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
def write_bit_register(bit_value=1,bit_address=0,num_regist=1):
    client.write_registers(bit_address,[bit_value]*num_regist)

def mac_read():
    mac_addr = 0x0000
    mac_read = mac_convertTOstring(client.read_holding_registers(mac_addr,3).registers)
    return mac_read

def fireware_read():
     version_addr =0x0001
     firmVersion_read = client.read_input_registers(version_addr,1).registers
     return hex(firmVersion_read[0])

def device_id_read():
    deID_addr = 0x0000
    deID = client.read_input_registers(deID_addr,1).registers
    return  hex(deID[0])

def status_read():
    status_addr = 0x038A
    status = client.read_input_registers(status_addr,4).registers
    MES_sta = status_convert(hex(status[0]))
    SDC_sta = status_convert(hex(status[1]))
    NTP_sta = status_convert(hex(status[2]))
    TCP_sta = status_convert(hex(status[3]))
    return MES_sta,SDC_sta,NTP_sta,TCP_sta

def update_firmware():
    OTA_update_addr = 0xFFFFFF63C0
    write_bit_register(0x1,OTA_update_addr,1)


#///////////////////////////////////////////////////////////////////////////////////////////////////////
# core function py configparser to user 
#///////////////////////////////////////////////////////////////////////////////////////////////////////

#print data to ini file
#device_name = string
#status = string
#FTP = oject form
#firmware = uint
def ini_print(device_name,status,FTP_data,firmware_version,id):
    data = configparser.ConfigParser() #inherit parser object

    path ='ini/'
    file_name = path+'config_'+device_name+'.ini'
    Device_data ={"id":id,"status":status}
    up_version ={"available version":firmware_version}
    data[device_name] = Device_data
    data['FTP server'] = FTP_data
    data['update version'] = up_version
    with open(file_name, 'w') as configfile:
        data.write(configfile)
        print("ini file printed")

#return all section in .ini file
def list_section(config):
    return config.sections()

#convert .ini file to dict
def read_INI_to_dict(path):
    config = configparser.ConfigParser()
    config.read(path)
    dic_con = {}
    for section in list_section(config):
        dic_con[section]={}
        for key,value in config.items(section):
            dic_con[section][key]=value
    return dic_con 

if __name__ == "__main__":
    
    path = '/ini/EMU-B20MC'
    #connect client
    ip = '172.16.5.129'
    Word = "ac2d"
    Word = uppercase_string(Word)
    print(Word)
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