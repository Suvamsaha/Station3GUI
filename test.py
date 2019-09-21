from tkinter import *
from tkinter.ttk import *
import requests

root = Tk()
root.geometry("1000x400")
root.title("Application")

tree = Treeview(root)
tree["columns"] = ('Percent', 'Status', 'Start', 'End')

tree.column("#0", width=200, minwidth=150, stretch=NO)
tree.column("Percent", width=300, minwidth=80, stretch=NO)
tree.column("Status", width=100, minwidth=80, stretch=NO)
tree.column("Start", width=100, minwidth=80, stretch=NO)
tree.column("End", width=100, minwidth=80, stretch=NO)

tree.heading('#0', text='MAC')
tree.heading('Status', text='Status', anchor=W)
tree.heading('Percent', text='Percent')
tree.heading('Start', text='Start Time')
tree.heading('End', text='End Time')

mac = []  # ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
statusp = []  # ['1', '2', '3', '4', '5']
status = []  # ['a', 'b', 'c', 'd', 'e']
start = []
end = []
progress = []


def update_item():
    global mac
    global status
    global statusp
    global start
    request_api()
    i = 0
    for item in tree.get_children():
        tree.item(item, values=(statusp[i], status[i], start[i]))
        bar(i, statusp[i])

        i = i + 1
    root.after(1000, update_item)


def show_discovered():
    global mac
    global status
    global statusp
    global start
    request_api()
    tree.delete(*tree.get_children())
    yy = 70
    for i in range(len(mac)):  # 'item%i' % i
        progress.append(Progressbar(root, orient=HORIZONTAL, length=250, mode='determinate'))
        progress[i].place(x=400, y=yy)
        tree.insert('', 'end', mac[i], text=mac[i], values=(statusp[i], status[i], start[i]))
        yy = yy + 20

    update_item()


def request_api():
    global mac
    global status
    global statusp
    global start
    mac = []
    status = []
    statusp = []
    url = "http://localhost/st3server/v1/devices"
    response = requests.request("GET", url)
    json_obj = response.json()
    for item in json_obj["items"]:
        mac.append(item["mac"])
        status.append(item["status"])
        statusp.append(item["statusPercentage"])
        start.append(item["startTime"])


def close_window():
    root.destroy()  # destroying the main window


def delete_device():
    print("delete device", tree.focus())
    dev_name = tree.focus()
    url = "http://localhost/st3server/v1/devices/" + str(dev_name)
    print(url)
    requests.request("DELETE", url)
    show_discovered()


def device_provisioning():
    print("delete provisioning", tree.focus())
    dev_name = tree.focus()
    url = "http://localhost/st3server/v1/devices/" + str(dev_name) + "/provision"
    requests.request("PUT", url)
    print(url)


def start_locking():
    dev_name = tree.focus()
    url = "http://localhost/st3server/v1/devices/" + str(dev_name) + "/startLock"
    requests.request("PUT", url)


def bar(prog, val):
    for i in range(0, 100, 2):
        progress[prog]['value'] = val
        root.update_idletasks()


# MAIN UI PLACEMENTS
tree.place(x=150, y=50)
Button(root, text='Device Discover', command=show_discovered).place(x=50, y=100)
Button(root, text='Start Provisioning', command=device_provisioning).place(x=200, y=300)
Button(root, text='Start Locking', command=start_locking).place(x=500, y=300)
Button(root, text='Delete Device', command=delete_device).place(x=800, y=300)
Button(root, text='Exit', command=close_window).place(x=800, y=350)

mainloop()
