# -*- coding: utf-8 -*-


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import serial as sr

#------global variables
data = np.array([])
data2 = np.array([])
data3 = np.array([])
cond = False

#-----plot data-----
def plot_data():
    global cond, data ,data2 , data3
    msg = []
    if (cond == True):
        
        a = s.readline()
        temp = a.decode()
        if len(temp)>0:
            if "#" in temp:
                msg = temp.split("#")
                del msg[0]
                del msg[len(msg) - 1]
                print(msg)
                a = msg[0]
                b = msg[1]
                speed = float(a)
                speed = int(speed)

                speed_cube = ((speed*speed*speed)/(3600**3))*100

                print(a,b,speed_cube)


        
        if(len(data) < 100):
            data = np.append(data,float(a[0:4]))
            data2 = np.append(data2,float(b[0:6]))
            data3 = np.append(data3,speed_cube)
        else:
            
            data2[0:99] = data2[1:100]
            data2[99] = float(b[0:6])

            data3[0:99] = data3[1:100]
            data3[99] = speed_cube

            data[0:99] = data[1:100]
            data[99] = float(a[0:4])
		
        lines.set_xdata(np.arange(0,len(data)))
        lines.set_ydata(data)
        
        lines2.set_xdata(np.arange(0,len(data2)))
        lines2.set_ydata(data2)

        lines3.set_xdata(np.arange(0,len(data3)))
        lines3.set_ydata(data3)

        canvas.draw()
        canvas2.draw()
        canvas3.draw()
    root.after(1,plot_data)

def plot_start():
    global cond
    cond = True
    s.reset_input_buffer()

def plot_stop():
    global cond
    cond = False




#-----Main GUI code-----
root = tk.Tk()
root.title('Real Time Plot')
root.configure(background = 'purple')
#root.configure(background = '#00B050')
root.geometry("1230x830") # set the window size

#------create Plot object on GUI----------
# add figure canvas
fig = Figure()
fig2 = Figure()
fig3 = Figure()
    
ax = fig.add_subplot(111)

ax2 = fig2.add_subplot(111)
ax3 = fig3.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax.set_title('Speed Data')
ax.set_xlabel('Sample')
ax.set_ylabel('Speed RPM')
ax.set_xlim(0,100)
ax.set_ylim(1000,3800)


ax2.set_title('Frequency Data')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Frequency Hz')
ax2.set_xlim(0, 100)
ax2.set_ylim(49.52, 50.2)

ax3.set_title('Estimated Fan Power')
ax3.set_xlabel('Sample')
ax3.set_ylabel('% of power')
ax3.set_xlim(0, 100)
ax3.set_ylim(0, 100)

lines = ax.plot([],[])[0]
lines2 = ax2.plot([],[])[0]
lines3 = ax3.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().place(x = 620,y=10, width = 600,height = 400)
canvas.draw()
canvas2 = FigureCanvasTkAgg(fig2,master=root)
canvas2.get_tk_widget().place(x= 10,y=10,width=600,height=400)
canvas2.draw()
canvas3 = FigureCanvasTkAgg(fig3,master=root)
canvas3.get_tk_widget().place(x= 10,y=420,width=600,height=400)
canvas2.draw()
#----------create button---------
root.update()
start = tk.Button(root, text = "Start", font = ('calbiri',12),command = lambda: plot_start())
start.place(x = 700, y = 700 )

root.update()
stop = tk.Button(root, text = "Stop", font = ('calbiri',12), command = lambda:plot_stop())
stop.place(x = start.winfo_x()+start.winfo_reqwidth() + 20, y = 700)
root.update()
image = Image.open("UoM.jpg")
resize_image = image.resize((150, 75))
img = ImageTk.PhotoImage(resize_image)
panel = Label(root, image = img)
panel.place(x = 900, y = 420)

root.update()
nidec_image = Image.open("Nidec.jpg")
resize_image_n = nidec_image.resize((150,75))
img_n = ImageTk.PhotoImage(resize_image_n)
panel_nidec = Label(root,image=img_n)
panel_nidec.place(x = 725,y = 420)
#----start serial port----
s = sr.Serial('COM3',115200)
s.reset_input_buffer()



root.after(1,plot_data)
root.mainloop()





