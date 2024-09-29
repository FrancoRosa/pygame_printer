import cups
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from PIL import Image

printer_name = 'Canon_SELPHY_CP1300_USB_'
p_width, p_height = 6*inch,  4*inch


def get_pdf(pdf_path, image_path):
    image = Image.open(image_path)
    image_width, image_height = image.size
    
    pdf_canvas = canvas.Canvas(pdf_path, pagesize=(p_width, p_height))
    pdf_width = p_width
    pdf_height = p_height    
    
    # Scale the image to fit the PDF size while maintaining aspect ratio
    aspect_ratio = min(pdf_width / image_width, pdf_height / image_height)
    scaled_width = image_width * aspect_ratio
    scaled_height = image_height * aspect_ratio

    # Calculate position to center the image
    x_position = (pdf_width - scaled_width) / 2
    y_position = (pdf_height - scaled_height) / 2

    # Draw the image on the PDF
    pdf_canvas.drawImage(image_path, x_position, y_position,
                        scaled_width, scaled_height)

    # Save the PDF
    pdf_canvas.save()

    print(f"PDF created successfully at: {pdf_path}")

def print_file(file_name):
    conn = cups.Connection()
    printers = conn.getPrinters()
    print("___________ Printer found___________________")
    for printer in printers:
        print(printer)
    print("____________________________________________")
    conn.printFile(printer_name, file_name, "ir_image", {})
    
    
get_pdf("out.pdf","tests/demo.png" ) 
print_file("out.pdf")