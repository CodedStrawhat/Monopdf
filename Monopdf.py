from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import os
from pdf2image import convert_from_path

root = Tk()
var = DoubleVar()
thresh = 125
loc =''
root.geometry("500x500")
def click():
    global submit
    global loc
    global savebut
    global images
    submit.pack_forget()
    root.filename = filedialog.askopenfilename(initialdir="C:/",title="Select_pdf",filetypes=(("pdf files","*.pdf"),))
    loc = root.filename
    p_path = os.getcwd()+'\poppler-21.03.0\Library\\bin'
    images = convert_from_path(loc,poppler_path=p_path,grayscale=True,fmt="jpeg",thread_count=4)
    slider.pack()
    savebut.pack()
    l = Label(root,text = "Preview of the first page").pack()
    show()

def save():
    files = [('pdf files','*.pdf')]
    file = filedialog.asksaveasfilename(filetypes=files,defaultextension=files)
    conv(images[0]).save(file)
    for img in images[1:]:
        img = conv(img)
        img.save(file,append=True)


def show():
    global img
    global thresh
    global label
    img= images[0]
    img = conv(img)
    img = img.resize((400,400)) 
    img = ImageTk.PhotoImage(img)
    label = Label(root,image = img)
    label.pack()

def conv(image):
    fn = lambda x : 255 if x > thresh else 0
    image = image.convert('L').point(fn, mode='1')
    image = image.convert('1')
    return image

def sho(val):
    global thresh
    thresh = var.get()
    label.pack_forget()
    show()
    
submit = Button(root,text = "Choose a pdf",command = click)
savebut = Button(root,text = "Save pdf",command = save)
slider = Scale(root,from_=0,to=255,orient=HORIZONTAL,variable=var,command=sho)
submit.pack(pady=200)
root.mainloop()
