from tkinter import *
import os
import subprocess
from tkinter import filedialog
import sys

root = Tk()

root.title('Md Rafsan Jani made Encrypter')


root.configure(background='black')

def openfile():
    global a
    a = filedialog.askopenfilename()
    b = '[+]select File is ===>{0}'.format(a)
    level = Label(root,text=b).pack()

def Encript():
    global a
    fo = open(str(a), 'rb')

    image = fo.read()

    fo.close()

    image = bytearray(image)

    key =   int(password1.get())

    if key > 256:
       labal = Label(root,text='[-]Password not allow upto 256',fg='black',bg='red').pack()
    else:

      for index , value in enumerate(image):
         image[index] = value^key


      fo = open(a , 'wb')

      fo.write(image)
      fo.close()
##      subprocess.call(['cacls',filename,'/E','/p','everyone:n'])

      labal = Label(root,text='the password is===>'+str(key)).pack()
      labal = Label(root,text='[+]Encrypt complite',fg='black').pack()



def  dycript():
    global a
##    subprocess.call(['cacls',filename,'/E','/p','everyone:r'])
    fo = open(str(a), 'rb')

    image = fo.read()

    fo.close()

    image = bytearray(image)

    key =  int(password2.get())
    if key > 256:
       labal = Label(root,text='[-]Password not allow upto 256',fg='black',bg='red').pack()

    else:
      for index , value in enumerate(image):
           image[index] = value^key

      fo = open(a , 'wb')
      print (fo)

      fo.write(image)
      fo.close()
##      subprocess.call(['cacls',filename,'/E','/p','everyone:r'])
      labal = Label(root,text='the password is===>'+str(key)).pack()
      labal = Label(root,text='[+]Dyrypt complite',fg='black').pack()

def readme():
    root = Tk()
    root.title('About Author')

    root.configure(background='black')
    labal = Label(root,text='''
   [+]Uses=======>    This  software must place that folder Which object wannto encrypted


                              ABOUT

   ''',bg='black',fg='green').pack()

    labal = Label(root,text='''

                  Md Rafsan Jani made File encrypter
                     gmail : rafsanthegeneral@gmail.com
      ''',bg='black',fg='green').pack()
    root.mainloop()




#encripter
labal = Label(root,text='''------------------MD Rafsan Jani  Made  file Encrypter-----------------
                                                 [+]Gmail: shazidno123@gmail.comK
                                          ''',fg='green',bg='black').pack()
labal =Label(root,text='----------------ENCRYPTER--------------------------',fg='red',bg='black').pack()
labal = Button(root,text='Browse File',command=openfile,bg='blue',fg='white').pack()
password1 = StringVar()
labal = Label(root,text='Password',bg='blue',fg='white').pack()
textbox = Entry(root,textvariable=password1,bg='dark green').pack()
button = Button(root,text='Encryption',command=Encript,bg='green',fg='black').pack()



#decripter
labal =Label(root,text='----------------DYCRYPTER--------------------------',fg='green',bg='black').pack()
labal = Button(root,text='Browse  File name',command=openfile,bg='blue',fg='white').pack()
password2 = StringVar()
labal = Label(root,text='Password',bg='blue',fg='white').pack()
textbox = Entry(root,textvariable=password2,bg='dark green').pack()
button = Button(root,text='Decryption',command=dycript,bg='green',fg='black').pack()
# readme

button = Button(root,text='About author',command=readme).pack()



root.mainloop()



