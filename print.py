import cups
conn = cups.Connection()
printers = conn.getPrinters()
print("___________ All ___________________")
for printer in printers:
    print(printer)
print("__________ Default ____________________")
prin = 'Canon_SELPHY_CP1300_USB_'
print(prin)
print("______________________________")
myfile = "/home/senseable/Desktop/irtest/hi.txt"
conn.printFile (prin, myfile, "Project Report", {})