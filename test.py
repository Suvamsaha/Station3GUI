from tkinter import *
from tkinter.ttk import *
import time
import requests

root = Tk()

root.geometry("850x350")
root.title("Application")

PanedWindow(orient=VERTICAL)


def show_discovered(mac, status, statusp):
    yy = 50
    global flag
    v = IntVar()
    for i in range(len(mac)):
        Radiobutton(root, text=mac[i], variable=v, value=i).place(x=200, y=yy)
        Label(root, text=status[i]).place(x=350, y=yy)
        Label(root, text=statusp[i]).place(x=400, y=yy)
        yy = yy + 20
        if statusp[i] != 100:
            flag = True
        else:
            flag = False

    if flag:
        time.sleep(10)
        request_api()




# Function responsible for the updation
# of the progress bar value
# Progress bar widget
progress = Progressbar(root, orient=HORIZONTAL, length=800, mode='determinate')


def bar():
    for i in range(0, 100, 2):
        progress['value'] = i
        root.update_idletasks()
        time.sleep(0.1)
    progress['value'] = 100


progress.place(x=10, y=250)


def close_window():
    root.destroy()  # destroying the main window


def request_api():
    mac = []
    status = []
    statusp = []

    url = "http://10.109.178.6/st3server/v1/devices"
    response = requests.request("GET", url)
    json_obj = response.json()
    for item in json_obj["items"]:
        mac.append(item["mac"])
        status.append(item["status"])
        statusp.append(item["statusPercentage"])
    show_discovered(mac, status, statusp)


Frame(root).place(x=200, y=200)
Button(root, text='Device Discover', command=request_api).place(x=80, y=50)
# Button(root, text='Stop Discover', command=stop_request_api).place(x=80, y=100)
Button(root, text='Start Provisioning', command=bar).place(x=80, y=200)
Button(root, text='Start Locking').place(x=400, y=200)
Button(root, text='Delete Device').place(x=700, y=200)
Button(root, text='Exit', command=close_window).place(x=700, y=300)

mainloop()
