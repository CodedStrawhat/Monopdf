from os.path import join
import os
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdfview
from pdf2image import convert_from_path

root = Tk()
var = DoubleVar()
thresh = 125
loc =''
root.geometry("600x600")

def click():
    global submit
    global loc
    global savebut
    global dir
    global images
    submit.pack_forget()
    root.filename = filedialog.askopenfilename(initialdir="C:/",title="Select_pdf",filetypes=(("pdf files","*.pdf"),))
    loc = root.filename
    dir = ''
    l = len(loc)
    p_path = os.getcwd()+'\poppler-21.03.0\Library\\bin'
    images = convert_from_path(loc,poppler_path=p_path,grayscale=True,fmt="jpeg",thread_count=4)
    for i in range(l):
        if loc[i] == '/':
            pos = i
    dir = loc[:pos+1]
    slider.pack()
    savebut.pack()
    lab = Label(root,text="Preview of the first page").pack()
    show()

def save():
    files = [('pdf files','*.pdf'),]
    file = filedialog.asksaveasfilename(initialdir=dir,filetypes=files,defaultextension=files)
    fn = lambda x : 255 if x > thresh else 0
    i = images[0]
    i = i.convert('L').point(fn, mode='1')
    i = i.convert('1')
    i.save(file)
    for i in images[1:]:
        conv(i).save(file,append=True)

def conv(image):
    fn = lambda x : 255 if x > thresh else 0
    image = image.convert('L').point(fn, mode='1')
    image = image.convert('1')
    return image
def show():
    global img
    global thresh
    global label
    img= images[0]
    img = conv(img).resize((500,500),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    label = Label(root,image = img)
    label.pack()

def sho(val):
    global thresh
    thresh = var.get()
    label.pack_forget()
    show()
    
submit = Button(root,text = "Choose a pdf",command = click)
savebut = Button(root,text = "Save pdf",command = save)
slider = Scale(root,from_=0,to=255,orient=HORIZONTAL,variable=var,command=sho)
submit.pack(pady=250)
root.mainloop()