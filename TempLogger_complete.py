import os, glob, time, gspread, sys, datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('file name.json', scope)

gc = gspread.authorize(credentials)

worksheet = gc.open("sheet name").sheet1

#part read Temp and append to sheet
#initiate the temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
#set up the location of the sensor in the system
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
print ('Code is running')
  
def read_temp_raw(): #a function that grabs the raw temperature data from the sensor
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines 
 
def read_temp(): #a function that checks that the connection was good and strips out the temperature
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos !=-1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string)/1000.0
      temp_f = temp_c * 9.0/5.0 + 32.0
      return temp_c
i =  1
while True: #infinite loop
    print('loop is running at round ' + str(i))
    tempin = read_temp() #get the temp
    values = [datetime.datetime.now(), tempin]
    worksheet.append_row(values)
    time.sleep(15)
    i = i + 1	 
