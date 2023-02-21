#Dev UNAH-VS
from Tkinter import *
import ttk
import os
import tkFont
import tkMessageBox

#crear ventana
v0=Tk()
v0.title("Control Gpio")
v0.geometry("600x300+0+0")
text1= tkFont.Font(family="Arial",size=20)
label_titulo= Label(v0,text="")

#funciones 
def encender():
    # tkMessageBox.showinfo(message="Encendido")
    os.system("sudo ./turnOn.sh")

def apagar():
    os.system("sudo ./turnOff.sh")

def actualizar ():
    pf= open("./estado.txt", "r")
    for linea in pf:
        campo = linea.split("\n")
        campo_f= campo[0]
        if campo_f=="1":
            label_s= Label(v0,text="1",font=text1).place(x=100,y=200)
            v0.after(1000,actualizar)
        if campo_f=="0":
            label_s= Label(v0,text="0",font=text1).place(x=100,y=200)
            v0.after(1000,actualizar)
        print(campo_f)


#Cargar en el load la funcion actualizar
actualizar();

#Etiquetas
label_t=Label(v0, text="CONTROL GPIO", font=text1).place(x=100, y=10)
btn_on=Button(v0,text="On", command=encender).place(x=100, y=50)
btn_off=Button(v0,text="Off", command=apagar).place(x=250, y=50)
v0.mainloop()