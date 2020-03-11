import serial
import time

#Arquivo com G-code.
gcode='code.txt'
#Porta serial de comunicação:
#Linux: /dev/ttyUSBx
#Windows: COMx
port='/dev/ttyUSB0'
#Numero de comandos da linha 1.
end_1=25
#Numero de comandos das linhas seguintes.
end_2=50
#Numero de linhas percorridas.
lines=8
#Delay entre fotos.
delay=0.5
f=open(gcode)
var=f.readlines()
comm=serial.Serial(port=port,baudrate=9600,xonxoff=True)
time.sleep(3)
comm.write('G28;\n'.encode())
time.sleep(15)
comm.write('G0 X32 Y99;\n'.encode())
time.sleep(3.3)
for i in range(0,end_1):
    time.sleep(delay)
    var[i]=var[i]+'\n'
    comm.write(var[i].encode())
    print(i)
    time.sleep(delay)
comm.close()
for j in range(0, (lines-1)):
    comm=serial.Serial(port=port,baudrate=9600,xonxoff=True)
    time.sleep(2)
    comm.write('G28 X Z;\n'.encode())
    time.sleep(10)
    comm.write('G0 X32 Y6;\n'.encode())
    time.sleep(delay)
    time.sleep(delay)
    for i in range(end_1,end_2):
        time.sleep(delay)
        var[i]=var[i]+'\n'
        comm.write(var[i].encode())
        print(i)
        time.sleep(delay)
    comm.close()
    time.sleep(delay)
comm=serial.Serial(port=port,baudrate=9600,xonxoff=True)
time.sleep(3)
comm.write('G28 X Z;\n'.encode())
comm.close()
f.close()
