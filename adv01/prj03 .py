###############################匯入模組###############################
from tkinter import *

a = 0
###############################建立視窗###############################
windows = Tk()
windows.title("My First GUI")

A = True


##############################定義函式###############################
def hi_fun():
    if A == True:

        display.Label(windows, text="功德+1", fg="red", bg="black")
        A = False
    else:

        display.Label(windows, text="功德+1", fg="black", bg="red")
        A = True


##############################建立按鈕###############################
btn1 = Button(windows, text="功德+1", command=hi_fun, bg="red")
a = 0
btn1.pack()
# btn2 = Button(windows, text="成績+1", command=clear_fun)
# btn2.pack()
##############################建立標籤###############################
display = Label(windows, text="功德+1")
display.pack()

##############################運行應用程式##############################
windows.mainloop()
