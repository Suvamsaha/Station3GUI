from tkinter import *
from tkinter.ttk import *
import time
import requests

root = Tk()
root.geometry("1000x400")
root.title("Application")

tree = Treeview(root)
tree["columns"] = ('Percent', 'Status', 'Start', 'End')

tree.column("#0", width=200, minwidth=150, stretch=NO)
tree.column("Status", width=100, minwidth=80, stretch=NO)
tree.column("Percent", width=300, minwidth=80, stretch=NO)
tree.column("Start", width=110, minwidth=80, stretch=NO)
tree.column("End", width=110, minwidth=80, stretch=NO)

tree.heading('#0', text='MAC', anchor=W)
tree.heading('Status', text='Status', anchor=W)
tree.heading('Percent', text='Percent')
tree.heading('Start', text='Start Time')
tree.heading('End', text='End Time')

mac = []  # ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
status = []  # ['a', 'b', 'c', 'd', 'e']
statusp = []  # ['1', '2', '3', '4', '5']
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

    request_api()
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

    url = "http://10.109.178.6/st3server/v1/devices"
    response = requests.request("GET", url)

    json_obj = response.json()
    print(json_obj)
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


def close_window():
    root.destroy()


def delete_device():
    print("delete device", tree.focus())
    dev_name = tree.focus()
    url = "http://10.109.178.6/st3server/v1/devices/" + str(dev_name)
    print(url)
    requests.request("DELETE", url)
    show_discovered()


def device_provisioning():
    dev_name = tree.focus()
    if dev_name is not None:
        url = "http://10.109.178.6/st3server/v1/devices/" + str(dev_name) + "/provision"
        requests.request("PUT", url)
        print(url)


def start_locking():
    dev_name = tree.focus()
    url = "http://10.109.178.6/st3server/v1/devices/" + str(dev_name) + "/startLock"
    requests.request("PUT", url)


def bar(prog, val):
    for i in range(0, 100, 2):
        progress[prog]['value'] = val
        root.update_idletasks()
    # progress[prog]['value'] = 100


# MAIN UI PLACEMENTS
tree.place(x=150, y=50)
# progress.place(x=10, y=300)
Button(root, text='Device Discover', command=show_discovered).place(x=50, y=100)
Button(root, text='Start Provisioning', command=device_provisioning).place(x=200, y=300)
Button(root, text='Start Locking', command=start_locking).place(x=500, y=300)
Button(root, text='Delete Device', command=delete_device).place(x=830, y=300)
Button(root, text='Exit', command=close_window).place(x=831, y=350)

mainloop()
