#!/usr/bin/env python3
from tkinter import *
from tkinter.ttk import *

from tkinter import messagebox

import time
import requests

root = Tk()
root.geometry("1200x600")
root.resizable(0,0)
root.title("Station3.v1.web-server")

tree = Treeview(root)
tree["columns"] = ('Percent', 'Status', 'Start', 'End')

tree.column("#0", width=200, minwidth=150, stretch=NO)
tree.column("Status", width=100, minwidth=80, stretch=NO)
tree.column("Percent", width=300, minwidth=80, stretch=NO)
tree.column("Start", width=220, minwidth=80, stretch=NO)
tree.column("End", width=220, minwidth=80, stretch=NO)

tree.heading('#0', text='MAC')
tree.heading('Status', text='Status')
tree.heading('Percent', text='Percent')
tree.heading('Start', text='Start Time')
tree.heading('End', text='End Time')


#tree view variables
mac = [] 
status = []  
statusp = [] 
start = []
end = []
progress = []


def update_item():
    global mac
    global status
    global statusp
    global start
    global end
    request_api()
    i = 0
    for item in tree.get_children():
        tree.item(item, values=(statusp[i], status[i],start[i], end[i]))
        bar(i, statusp[i])

        i = i + 1
    root.after(1000, update_item)


def show_discovered():
    global mac
    global status
    global statusp
    global progress
    global start
    global end

    if (len(progress)) > 0:
        for i in range(len(progress)):
            progress[i].destroy()
    progress = []
    ret=request_api()
    if (ret==1):
      return 
      
    tree.delete(*tree.get_children())
    print("Discovering Device")
    yy = 70
    for i in range(len(mac)):  # 'item%i' % i
        progress.append(Progressbar(root, orient=HORIZONTAL, length=250, mode='determinate'))
        progress[i].place(x=400, y=yy)
        tree.insert('', 'end', mac[i], text=mac[i], values=(statusp[i], status[i], start [i], end[i]))
        yy = yy + 20

    update_item()


def request_api():
    global mac
    global status
    global statusp
    global start
    global end

    mac = []
    status = []
    statusp = []
    start = []
    end = []

    url = "http://localhost/st3server/v1/devices"

    try:  
       response = requests.request("GET", url)
    except:
        messagebox.showinfo("station3", "Connection refused:Exceeds maximum attempt")
        return 1

    json_obj = response.json()
    if json_obj["total"] == 0:
        messagebox.showinfo("station3", "No device found! Please retry")
        return 1
    for item in json_obj["items"]:
        mac.append(item["mac"])
        status.append(item["status"])
        statusp.append(item["statusPercentage"])
        if "startTime" in item:
            start.append(item["startTime"])
        else:
            start.append(" ")
        if "endTime" in item:
            end.append(item["endTime"])
        else:
            end.append(" ")


#destory the UI
def close_window():
    root.destroy()


#delete the device from database
def delete_device():
    dev_name = tree.focus()
    # check if device is selected from ui tree view
    if dev_name:
      #confirm from user
      result = messagebox.askyesno("station3","Are you sure you want to delete device : "+ str(dev_name)+"?")
      if str(result)=="True":
        url = "http://localhost/st3server/v1/devices/" + str(dev_name)
      else:
        return
    else:
      messagebox.showwarning("Station3","No item selected from tree")
      return
    try:
        response = requests.request("DELETE", url)
    except:
         messagebox.showerror("Error","Connection")
         return
    http_ret = response.status_code

    if http_ret == 204:
      show_discovered()
      messagebox.showinfo("Station3","Device with mac address: "+str(dev_name)+" deleted successfully")
    else:
      messagebox.showerror("Station3","Failed to delete device with macaddr: "+str(dev_name))
 
        

#start the provisioning of deivce
def device_provisioning():
    dev_name = tree.focus()
    # check if device is selected from ui tree view
    if dev_name:
      #confirm from user
      result = messagebox.askyesno("station3","Are you sure you want to provision device: "+str(dev_name)+"?")
      if str(result)=="True":
         url = "http://localhost/st3server/v1/devices/" + str(dev_name) + "/provision"
      else:
         return
    else:
      messagebox.showwarning("Station3","No item selected from tree")
      return

    try:
       response=requests.request("PUT", url)
    except:
       messagebox.showerror("Error","Connection Error")
       return 

    http_ret = response.status_code
    if http_ret == 200:
      messagebox.showinfo("Station3","Signaled device with macaddress: "+str(dev_name)+" for provisioning")
    else:
      messagebox.showerror("Station3","Failed to signal device with macaddr: "+str(dev_name)+" for provisioning")




#start lockdown of device
def start_locking():
    dev_name = tree.focus()
    # check if device is selected from ui tree view
    if dev_name:
       #confirm from user
       result = messagebox.askyesno("station3","Are you sure you want to lockdown device: "+ str(dev_name)+"?")
       if str(result)=="True":
          url = "http://localhost/st3server/v1/devices/" + str(dev_name) + "/startLock"
       else:
          return 
    else:
       messagebox.showwarning("Station3","No item selected from tree")
       return
    try:
       response=requests.request("PUT", url)
    except:
        messagebox.showerror("Error","Connection Error") 
        return 
    http_ret = response.status_code

    if http_ret == 200:
      messagebox.showinfo("Station3","Initiated lockdown for device with macaddress: "+str(dev_name))
    else:
      messagebox.showerror("Station3","Failed to initiate the device with macaddress: "+str(dev_name)+" for lockdown")


#increase progress of progress-bar
def bar(prog, val):
    for i in range(0, 100, 2):
        progress[prog]['value'] = val
        root.update_idletasks()


# MAIN UI PLACEMENTS
tree.place(x=150, y=50)
# progress.place(x=10, y=300)
Button(root, text='Discover Device', command=show_discovered, width = 14).place(x=19, y=50)
Button(root, text='Start Provision', command=device_provisioning, width = 14).place(x=19, y=111)
Button(root, text='Start Locking', command=start_locking, width = 14).place(x=19, y=178)
Button(root, text='Delete Device', command=delete_device, width = 14).place(x=19, y=242)
Button(root, text='Exit', command=close_window).place(x=600, y=300)

mainloop()
