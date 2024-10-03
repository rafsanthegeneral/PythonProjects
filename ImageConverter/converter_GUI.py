from tkinter import *
from  PIL import Image
from tkinter import filedialog
from tkinter import messagebox
import random
rand = random.randint(1,100)
root = Tk()
root.title('Image Converter ')

def open_file():
    global a
    a = filedialog.askopenfilename()
    b = Image.open('{0}'.format(a))
    heght,width = b.size
    

    text2 = 'Selected File is ==>{0}\n This Image Hight is ==>{1} Width is ==>{2}'.format(a,heght,width)
    lev = Label(root,text=text2,fg='green',bg='black').grid(column=0,row=1)

def convert_file():
    global  file_extention
    global  file_hight
    global  file_width
    global a
    File_extention =  file_extention.get()
    File_hight = file_hight.get()
    File_width = file_width.get()
    try:
     b = Image.open('{0}'.format(a)).convert('RGB').resize((int(File_hight),int(File_width)), Image.ANTIALIAS)
     out= b.save('converted{0}.{1}'.format(rand,File_extention))
     f =  'converted{0}.{1}'.format(rand,File_extention)
     save = '[+]Save image in Same Directory name is ===>{0}'.format(f)
     lev = Label(root,text=save,fg='green',bg='black').grid(column=1,row=7)
     mass = '[+]Success==>{0}'.format(save)
     messagebox.showinfo('Status',mass)
    except:
     lev = Label(root,text='[!!]Yout Do Something Wrong',fg='white',bg='red').grid(column=1,row=7)
     tkMessageBox.showerror('status','Image Convertion faild')

def about():
    root2 = Tk()
    root2.title('About')
##    canvas = Canvas(root3,bg='black')
##    canvas.pack()
##    pilImage = Image.open('w.jpg')
##    img = ImageTk.PhotoImage(pilImage)
##    canvas.create_image(image=img)


    level = Label(root2,text='''

   ===[++]Free Image Converter tool[++]==
    ---------------------------------
    [+]Code By -> Md Rafsan jani Shazid <-
        [+]Gmail: shazidno123@gmail.com
    ---------------------------------

     ''',bg='khaki',fg='gray1',font=('Ubuntu',25)).pack()


def main():
    global  file_extention
    global  file_hight
    global  file_width
    a = '-'*20
    b = '-'*20
    c = '{0}Image Converter{1}'.format(a,b)
    lev = Label(root,text=c,bg='CadetBlue1',font=('Ubuntu',20)).grid(column=0,row=0)
    lev= Label(root,text='Browse File==>',font=('Ubuntu',15)).grid(column=0,row=1)

    but = Button(root,text='Browse',command=open_file,fg='black',bg='sky blue',font=('Ubuntu',10)).grid(column=1,row=1)
    lev = Label(root,text='What Types to You want Convert (EX:jpg png )===>',font=('Ubuntu',15)).grid(column=0,row=3)
    file_extention= StringVar()
    text = Entry(root,textvariable=file_extention,justify='center',bg='slategray',font=('Ubuntu',15)).grid(column=1,row=3)
    lev = Label(root,text='Enter Width ====>',font=('Ubuntu',15)).grid(column=0,row=4)
    file_hight = StringVar()
    text = Entry(root,textvariable=file_hight,justify='center',bg='slategray',font=('Ubuntu',15)).grid(column=1,row=4)
    lev = Label(root,text='Enter Hight ====>',font=('Ubuntu',15)).grid(column=0,row=5)
    file_width = StringVar()
    text = Entry(root,textvariable=file_width,justify='center',bg='slategray',font=('Ubuntu',15)).grid(column=1,row=5)
    button = Button(root,text='Convert',command=convert_file,fg='black',bg='light sea green',font=('Ubuntu',10)).grid(column=1,row=6,padx=60,pady=20)
    abou =  Button(root,text='About This Software ',command=about,bg='plum1').grid(column=1,row=8,padx=60,pady=20)



if __name__ == '__main__':
    main()
    root.mainloop()




##     a = Image.open('{0}'.format(args.f)).convert('RGB').resize((int(args.h),int(args.w)), Image.ANTIALIAS)
##     f = a.save('converted{0}.{1}'.format(rand,args.e))
##     print '[+]converting Image Succes'
##     print '[+]File Save name is ===>Convert{0}.{1}'.format(rand,args.e)
