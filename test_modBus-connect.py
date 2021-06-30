
from os import path
from pymodbus import client
from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient
import configparser

#write single&multi register values
#bit_address = device bit-address 
#bit_value = payload 
#num_regist = in case multi-writ **default =1**
#unit =0 #number init-device **default is 0 --upon device***

async def write_bit_register(bit_value=1,bit_address=0,num_regist=1,unit=0):
    await client.write_registers(bit_address,[bit_value]*num_regist,unit)

#read holding-regist values

def print_outputFrom_register(round_count,result):
    for i in range(round_count) :
        print("round"+str(i)+": "+result[i])

async def read_holding_register(count=1,address_HR=0):
    result_HR = await client.read_holding_registers(address_HR,count)
    print_outputFrom_register(count,result_HR)
    return result_HR

#read input-regist values
async def read_input_register(count=1,address_IR=0):
    result_IR = await client.read_input_registers(address_IR,count)
    print_outputFrom_register(count,result_IR)
    return result_IR

#connect Modbus TCP client
def connect_client(ip_add):
    return ModbusTcpClient(ip_add)

#convert to mac(HEX) to string
def mac_address_convertTOstring(mac):
    return str(mac[0]+mac[1]+mac[2])

#convert status to string
def status_convert(stu):
    if(stu == 0x00000):
        return "normal status"
    elif(stu == 0x0099):
        return "abnormal status"

#convert version to String
#def version_convert(ver):
 #   if(ver )

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
    #FTP_data ={"ip":"127.0.0.1","mac":"","psw":"123456","port":"0000"}
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
    value = 10
    round_count =2
    client = connect_client(ip)
    print(client) #test status connect

    write_bit_register(value)
    test_result_holdding = read_holding_register(round_count)
    
    #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #holding
    #ip_ModAdd = 0x1100
    mac_Modadd = 0x0000
    port_Modadd = 0x0042
    status_add = 0x038A
    #input
    deID = 0x0000
    version_add =0x0001

    Device_ID= str(read_input_register())
    IP_read = ip
    mac_read = mac_address_convertTOstring(read_holding_register(3,mac_Modadd))
    port_read = str(read_holding_register(1,port_Modadd))
    status = status_convert(read_input_register(1,status_add))
    firmVersion_read = str(read_input_register(1,version_add))

    FTP_data={"ip address":IP_read,"mac address":mac_read,"port":port_read}

    ini_print("EMU-B20MC",status,FTP_data,firmVersion_read,Device_ID)
    test_dic_convert = read_INI_to_dict(path)