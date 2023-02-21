#!/usr/bin/env python2
#Dev UNAH-VS
import time
from Tkinter import *
import ttk
import os
import tkFont
import tkMessageBox
#variables globales
hora_inicial = ""
minuto_inicial= ""
hora_final = ""
minuto_final= ""
path1= "/etc/cron.d/tarea1"
path2= "/etc/cron.d/tarea2"
path_dir= os.getcwd()
path_estado= path_dir+"/estado.txt"
path_turnOn= path_dir +"/turnOn.sh"
path_turnOff= path_dir+"/turnOff.sh"
path_tarea1= "/etc/cron.d/tarea1"
path_tarea2= "/etc/cron.d/tarea2"


#crear ventana
v0=Tk()
v0.title("Control Gpio")
v0.geometry("600x600+0+0")
text1= tkFont.Font(family="Arial",size=20)
label_titulo= Label(v0,text="")
#Etiquetas
label_t=Label(v0, text="CONTROL GPIO", font=text1).place(x=100, y=10)
#imagenes
img_on= PhotoImage(file="./bulbOn.gif").subsample(2,2)
img_off= PhotoImage(file="./bulbOff.gif").subsample(2,2)
#textbox hora inicial / final
horaInicial = StringVar();
horaFinal = StringVar();
textBoxHoraInicial= Entry(v0, width=30, textvariable=horaInicial ).place(x=150, y=100)
textBoxHoraFinal = Entry(v0,width=30, textvariable=horaFinal).place(x=150, y=150)
label_hora_inicial = Label(v0, text="Hora Inicial", font=text1).place(x=0, y=95)
label_hora_inicial = Label(v0, text="Hora Final", font=text1).place(x=0, y=145)


#funciones 
def encender():
    # tkMessageBox.showinfo(message="Encendido")
    os.system("sudo sh {}".format(path_turnOn))

def apagar():
    os.system("sudo sh {}".format(path_turnOff))

def actualizar ():
    if os.path.exists(path_estado):
        pf= open(path_estado, "r")
        for linea in pf:
            campo = linea.split("\n")
            campo_f= campo[0]
            if campo_f=="1":
                label_s= Label(v0,text="1",font=text1).place(x=100,y=200)
                btn_img= Button(v0, image=img_on).place(x=150, y=255)
                v0.after(1000,actualizar)
            if campo_f=="0":
                label_s= Label(v0,text="0",font=text1).place(x=100,y=200)
                btn_img= Button(v0, image=img_off).place(x=150, y=255)
                v0.after(1000,actualizar)
            print(campo_f)

def limpiar():
    horaInicial.set("")
    horaFinal.set("")

def saveFile():
    try:
        
        hora_inicial, minuto_inicial= horaInicial.get().split(":")
        hora_final, minuto_final = horaFinal.get().split(":")
        if int(hora_inicial) > 25 or int(minuto_inicial)>59 or int(hora_final)>25 or int(minuto_final)>59:
            raise   ValueError("Error fuera de rango")
        cron_data_tarea1= "{} {} * * * {} {}{}".format(minuto_inicial, hora_inicial,"root" ,"/."+ path_turnOn,"\n")
        cron_data_tarea2= "{} {} * * * {} {}{}".format(minuto_final, hora_final, "root" ,"/."+path_turnOff,"\n")
        with open(path1, 'w') as f:
            f.write(cron_data_tarea1)
            os.system("sudo chown root:root "+path_tarea1)
            os.system("sudo chmod 644 " + path_tarea1)
        with open(path2, 'w') as f:
            f.write(cron_data_tarea2)
            os.system("sudo chown root:root "+ path_tarea2 )
            os.system("sudo chmod 644 "+ path_tarea2)
        os.system("sudo /etc/init.d/cron restart")
        limpiar()

        
    except Exception as e:
        print("Error: "+str(e))
        tkMessageBox.showinfo(message="Valores Invalidos")



btn_on=Button(v0,text="On", command=encender).place(x=100, y=50)
btn_off=Button(v0,text="Off", command=apagar).place(x=250, y=50)
btn_save=Button(v0,text="Guardar", command=saveFile).place(x=500, y=125)
#Cargar en el load la funcion actualizar
actualizar();

v0.mainloop()