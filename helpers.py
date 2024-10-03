import os
import cups
from datetime import datetime
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from PIL import Image

printer_name = 'Canon_SELPHY_CP1300_USB_'
printer_dir = "/home/senseable/print_history"
p_width, p_height = 6*inch,  4*inch


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

    pdf_canvas.drawImage(get_pdf_name(), x_position, y_position,
                        scaled_width, scaled_height)
    # Save the PDF
    pdf_canvas.save()

    print(f"PDF created successfully at: {pdf_path}")

def print_file(file_name):
    conn = cups.Connection()
    printers = conn.getPrinters()
    print("...available printer:")
    for printer in printers:
        print(printer)
    print("... printing")
    conn.printFile(printer_name, file_name, "ir_image", {})
    
