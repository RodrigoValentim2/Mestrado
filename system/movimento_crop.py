# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:25:19 2019

@author: leandro
"""

import serial
import time
import cv2
import os
vc = cv2.VideoCapture(0)
crop_left = 159
crop_up = 460     
class Movimento:
    def run(palheta, amostra):

        new_folder = palheta+"_"+amostra
        os.mkdir("res/"+new_folder)
        


        k=1
        
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
        delay=0.7
        f=open(gcode)
        var=f.readlines()
        comm=serial.Serial(port=port,baudrate=9600,dsrdtr=True,xonxoff=True)
        time.sleep(3)
        comm.write('G28;\n'.encode())
        time.sleep(15)
        comm.write('G0 X32 Y99;\n'.encode())
        time.sleep(3.3)
        for i in range(0,end_1):
            time.sleep(delay)
            var[i]=var[i]
            comm.write(var[i].encode())
            time.sleep(delay)
            rval, frame = vc.read()
            if k <= 5:
               cv2.imwrite("res/"+new_folder+"/"+new_folder+"_foto"+str(k)+".png", frame)
               print(frame.shape)
            if k > 5 and k <=25:
               roi = frame[:, crop_left:640]
               print("ROI: ", roi.shape)
               cv2.imwrite("res/"+new_folder+"/"+new_folder+"_foto"+str(k)+".png", roi)
            
            k=k+1
        comm.close()
        time.sleep(delay)
        time.sleep(delay)
        aux = 0
        for j in range(0, (lines-1)):
            comm=serial.Serial(port=port,baudrate=9600,dsrdtr=True,xonxoff=True)
            time.sleep(2)
            comm.write('G28 X Z;\n'.encode())
            time.sleep(11)
            comm.write('G0 X32 Y6;\n'.encode())
            time.sleep(3)
            aux = 0
            for i in range(end_1,end_2):
                time.sleep(delay)
                var[i]=var[i]
                comm.write(var[i].encode())
                time.sleep(delay)
                rval, frame = vc.read()
                if aux == 0:
                   roi = frame[:, :640]
                   cv2.imwrite("res/"+new_folder+"/"+new_folder+"_foto"+str(k)+".png", roi)
                   aux = aux+1
                else:
                    roi = frame[:, crop_left:640]
                    cv2.imwrite("res/"+new_folder+"/"+new_folder+"_foto"+str(k)+".png", roi)

                
                
                
                time.sleep(delay)
                k=k+1
            comm.close()
            time.sleep(delay)
        roi = frame[:, crop_left:640]
        rval, frame = vc.read()
        k=201
        cv2.imwrite("res/"+new_folder+"/"+new_folder+"_foto"+str(k)+".png", roi)
        rval, frame = vc.read()
        roi = frame[:, crop_left:640]
        k=202
        cv2.imwrite("res/"+new_folder+"/"+new_folder+"_foto"+str(k)+".png", roi)
        rval, frame = vc.read()
        k=203
        roi = frame[:, crop_left:640]
        cv2.imwrite("res/"+new_folder+"/"+new_folder+"_foto"+str(k)+".png", roi)
        rval, frame = vc.read()
        k=204
        roi = frame[:, crop_left:640]
        cv2.imwrite("res/"+new_folder+"/"+new_folder+"_foto"+str(k)+".png", roi)
        comm=serial.Serial(port=port,baudrate=9600,dsrdtr=True,xonxoff=True)
        time.sleep(delay)
        comm.write('G28 X Z;\n'.encode())
        comm.close()
        f.close()
        
                

