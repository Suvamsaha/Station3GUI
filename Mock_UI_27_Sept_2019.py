#!/usr/bin/env python3
from tkinter import messagebox, Tk, NO, mainloop, HORIZONTAL
from tkinter.ttk import Button, Treeview, Progressbar
from requests import request, exceptions
from multiprocessing import Process

# global variable declarations
progress = []


# Update the given parameters of device continuously.
def update_item():
    print("updating...")
    mac, status, statusp, start, end = request_api()
    if len(mac) < 1:
        return
    else:
        i = 0
        for item in tree.get_children():
            tree.item(item, values=(statusp[i], status[i], start[i], end[i]))
            bar(i, statusp[i])
            i = i + 1
        root.after(1000, update_item)


# Callback function to Discovery button.
def show_discovered():
    print("Discovering Device")
    global progress
    if (len(progress)) > 0:
        for i in range(len(progress)):
            progress[i].destroy()
    progress = []
    mac, status, statusp, start, end = request_api()
    tree.delete(*tree.get_children())
    if len(mac) < 1:
        choice = messagebox.askyesno(
            "station3", "No Device Found Do You want to scan again ?")
        if choice:
            show_discovered()
        else:
            return
    else:
        yy = 73
        for i in range(len(mac)):
            progress.append(Progressbar(root, orient=HORIZONTAL, length=250, mode='determinate'))
            progress[i].place(x=400, y=yy)
            tree.insert('', 'end', mac[i], text=mac[i], values=(statusp[i], status[i], start[i], end[i]))
            yy = yy + 20
        update_item()


# Request api to get the information of all device.
def request_api():
    mac = []
    status = []
    statusp = []
    start = []
    end = []
    url = "http://localhost/st3server/v1/devices"
    try:
        response = request("GET", url)
    except exceptions.HTTPError as err:
        messagebox.showerror("Error HTTPError :", err)
        return mac, status, statusp, start, end
    except exceptions.Timeout:
        messagebox.showerror("Error", "Request TimeOut")
        return mac, status, statusp, start, end
    except exceptions.TooManyRedirects:
        messagebox.showerror("Error", "Bad URL too many redirects")
        return mac, status, statusp, start, end
    except exceptions.RequestException:
        messagebox.showerror("Error", "Bad Request")
        return mac, status, statusp, start, end
    except:
        return mac, status, statusp, start, end
    json_obj = response.json()
    if json_obj["total"] == 0:
        return mac, status, statusp, start, end
    else:
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
        return mac, status, statusp, start, end


# destory the UI
def close_window():
    root.destroy()


# delete the device from database
def delete_device():
    dev_name = tree.focus()
    # check if device is selected from ui tree view
    if dev_name:
        # confirm from user
        result = messagebox.askyesno(
            "station3", "Are you sure you want to delete device : " + str(dev_name) + "?")
        if str(result) == "True":
            url = "http://localhost/st3server/v1/devices/" + str(dev_name)
        else:
            return
    else:
        messagebox.showwarning("Station3", "No item selected from tree")
        return
    try:
        response = request("DELETE", url)
        http_ret = response.status_code
        if http_ret == 204:
            show_discovered()
            messagebox.showinfo(
                "Station3", "Device with mac address: " + str(dev_name) + " deleted successfully")
        else:
            messagebox.showerror(
                "Station3", "Failed to delete device with macaddr: " + str(dev_name))
    except exceptions.HTTPError as err:
        messagebox.showerror("Error HTTPError :", err)
    except exceptions.Timeout:
        messagebox.showerror("Error", "Request TimeOut")
    except exceptions.TooManyRedirects:
        messagebox.showerror("Error", "Bad URL too many redirects")
    except exceptions.RequestException:
        messagebox.showerror("Error", "Bad Request")
        return


# start the provisioning of device
def device_provisioning():
    dev_name = tree.focus()
    if dev_name:
        # confirm from user
        result = messagebox.askyesno(
            "station3", "Are you sure you want to provision device: " + str(dev_name) + "?")
        if str(result) == "True":
            url = "http://localhost/st3server/v1/devices/" + \
                  str(dev_name) + "/provision"
        else:
            return
    else:
        messagebox.showwarning("Station3", "No item selected from tree")
        return
    try:
        response = request("PUT", url)
        http_ret = response.status_code
        if http_ret == 200:
            messagebox.showinfo(
                "Station3", "Signaled device with macaddress: " + str(dev_name) + " for provisioning")
        else:
            messagebox.showerror("Station3",
                                 "Failed to signal device with macaddr: " + str(dev_name) + " for provisioning")
    except exceptions.HTTPError as err:
        messagebox.showerror("Error HTTPError :", err)
    except exceptions.Timeout:
        messagebox.showerror("Error", "Request TimeOut")
    except exceptions.TooManyRedirects:
        messagebox.showerror("Error", "Bad URL too many redirects")
    except exceptions.RequestException:
        messagebox.showerror("Error", "Bad Request")
        return


# start lockdown of device
def start_locking():
    dev_name = tree.focus()
    if dev_name:
        # confirm from user
        result = messagebox.askyesno(
            "station3", "Are you sure you want to lockdown device: " + str(dev_name) + "?")
        if str(result) == "True":
            url = "http://localhost/st3server/v1/devices/" + \
                  str(dev_name) + "/startLock"
        else:
            return
    else:
        messagebox.showwarning("Station3", "No item selected from tree")
        return
    try:
        response = request("PUT", url)
        http_ret = response.status_code
        if http_ret == 200:
            messagebox.showinfo(
                "Station3", "Initiated lockdown for device with macaddress: " + str(dev_name))
        else:
            messagebox.showerror("Station3",
                                 "Failed to initiate the device with macaddress: " + str(dev_name) + " for lockdown")
    except exceptions.HTTPError as err:
        messagebox.showerror("Error", "Error HTTPError :", err)
    except exceptions.Timeout:
        messagebox.showerror("Error", "Request TimeOut")
    except exceptions.TooManyRedirects:
        messagebox.showerror("Error", "Bad URL too many redirects")
    except exceptions.RequestException:
        messagebox.showerror("Error", "Bad Request")
        return


# increase progress of progress-bar
def bar(prog, val):
    progress[prog]['value'] = val
    root.update_idletasks()


# MAIN UI PLACEMENTS
if __name__ == '__main__':
    root = Tk()
    root.geometry("1220x350")
    root.resizable(0, 0)
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

    tree.place(x=150, y=50)
    Button(root, text='Discover Device', command=show_discovered, width=14).place(x=19, y=50)
    Button(root, text='Start Provision', command=device_provisioning, width=14).place(x=19, y=111)
    Button(root, text='Start Locking', command=start_locking, width=14).place(x=19, y=178)
    Button(root, text='Delete Device', command=delete_device, width=14).place(x=19, y=242)
    Button(root, text='Exit', command=close_window).place(x=600, y=300)

    mainloop()
