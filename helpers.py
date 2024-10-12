import os
import cups
import shutil

from time import sleep
from datetime import datetime
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from fpdf import FPDF


printer_name = 'Canon_SELPHY_CP1300_USB_'
printer_dir = "/home/senseable/print_history"
logo_dir="/home/senseable/pygame_printer"

p_width, p_height = 6*inch,  4*inch

def composePdf(image_dir, out_dir, logo_dir):
    logo_width=50
    logo_hight=50
    paper_width=148.5
    paper_height=210
    pdf = FPDF(orientation="L", unit="mm", format="A5")
    pdf.add_page()
    pdf.image(name=image_dir, x=0,y = 0, w = paper_width, h = paper_height)
    pdf.image(name=logo_dir, x=10, y = paper_height/2-logo_hight/2, w = logo_width, h = logo_hight)
    pdf.output(out_dir)
    
def composePdfObj(image_obj, out_dir):
    new_img_path = "/tmp/img.jpg"
    image_obj.save(new_img_path)
    logo_width=50
    logo_hight=50
    paper_width=148.5
    paper_height=210
    pdf = FPDF(orientation="L", unit="mm", format="A5")
    pdf.add_page()
    pdf.image(name=new_img_path, x=0,y = 0, w = paper_width, h = paper_height)
    pdf.image(name=logo_dir, x=10, y = paper_height/2-logo_hight/2, w = logo_width, h = logo_hight)
    pdf.output(out_dir)
    
    history_record = get_pdf_name()
    shutil.copy("/tmp/out.pdf", history_record)

    print(f"...pdf saved at: {history_record}")
    return history_record
        
def verify_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"... '{dir_path}' created.")

def get_pdf_name():
    verify_dir(printer_dir)
    now = datetime.now()
    filename = printer_dir + "/" + now.strftime("%Y%m%d_%H%M%S") + ".pdf"
    return filename

def get_pdf(pdf_path, img_obj):
    
    new_img_path = "/tmp/img.jpg"

    img_obj.save(new_img_path)
    image_width, image_height = img_obj.size
    
    pdf_canvas = canvas.Canvas(pdf_path, pagesize=(p_width, p_height))
    pdf_width = p_width
    pdf_height = p_height    
    
    # Scale the image to fit the PDF size while maintaining aspect ratio
    aspect_ratio = min(pdf_width / image_width, pdf_height / image_height)
    scaled_width = image_width * aspect_ratio
    scaled_height = image_height * aspect_ratio

    # Calculate position to center the image
    x_position = round((pdf_width - scaled_width) / 2)
    y_position = round((pdf_height - scaled_height) / 2)

    # Draw the image on the PDF
    pdf_canvas.drawImage(new_img_path, x_position, y_position,
                        scaled_width, scaled_height)

    
    # Save the PDF
    pdf_canvas.save()
    history_record = get_pdf_name()
    shutil.copy("/tmp/out.pdf", history_record)

    print(f"...pdf saved at: {history_record}")
    return history_record

def print_file(file_name):
    conn = cups.Connection()
    printers = conn.getPrinters()
    print("...available printer:")
    for printer in printers:
        print(printer)
    print("... printing")
    sleep(1)
    conn.printFile(printer_name, file_name, "ir_image", {})
    
