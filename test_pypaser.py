import configparser

config = configparser.ConfigParser()
config.read('ini/example.ini')
#print(config.sections())
print(config['bitbucket.org'])
#for key in config['bitbucket.org']:  
#    print(key)
#    print(" = ")
#    print(print(config['bitbucket.org'][key]))

'''
def list_section(config):
    #print(config.sections())
    return config.sections()

def read_INI_to_dict(path):
    config = configparser.ConfigParser()
    config.read(path)
    dic_con = {}
    for section in list_section(config):
        dic_con[section]={}
        for key,value in config.items(section):
            dic_con[section][key]=value
    return dic_con 



test_result2 = read_INI_to_dict('ini/example.ini')
print(test_result2)
'''
'''
#convert to mac(HEX) to string
def mac_address_convertTOstring(mac):
    return str(mac[0]+mac[1]+mac[2])

#convert status to string
def status_convert(stu):
    if(stu == 0x00000):
        return "normal status"
    elif(stu == 0x0099):
        return "abnormal status"

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

mac_test = ["AB","C0","12"]
Device_ID= "BCD20MC"
IP_read = "127.0.0.1"
mac_read = mac_address_convertTOstring(mac_test)
port_read = 12345
status = status_convert(0x0000)
firmVersion_read = "0x0123"

FTP_data={"ip address":IP_read,"mac address":mac_read,"port":port_read}

ini_print("EMU-B20MC",status,FTP_data,firmVersion_read,Device_ID)

'''
'''

config = configparser.ConfigParser()

config['DEFAULT'] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                      'CompressionLevel': '9'}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('ini/example.ini', 'w') as configfile:
    config.write(configfile)
    print("ini done")
'''
'''
from ConfigParser import ConfigParser
from collections import defaultdict

config = ConfigParser()
config.readfp(open('/path/to/file.ini'))

def convert_to_dict(config):
    config_dict = defaultdict(dict)
    for section in config.sections():
        for key, value in config.items(section):
            config_dict[section][key] = value

    return config_dict

print convert_to_dict(config)
'''

