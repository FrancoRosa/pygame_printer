import cups
conn = cups.Connection()
printers = conn.getPrinters()
print("___________ All ___________________")
for printer in printers:
    print(printer)
print("__________ Default ____________________")
prin = 'Canon_SELPHY_CP1300_USB_'
prin = 'ML-1670-Series'
print(prin)
print("______________________________")
myfile = "/home/senseable/Desktop/irtest/output.pdf"
myfile = "/home/fx/px/pygame_printer/output.pdf"
conn.printFile(prin, myfile, "Project Report", {})
