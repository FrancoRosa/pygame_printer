from PIL import Image
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas

# Load the image
image_path = "demo.png"  # Replace with your image path
image = Image.open(image_path)

# Create a PDF file with size 4x6 inches
pdf_path = "output.pdf"
pdf_canvas = canvas.Canvas(pdf_path, pagesize=(6 * inch, 4 * inch))

# Get the image dimensions
image_width, image_height = image.size

# Set the image size relative to the 4x6 inches PDF (convert to points, 1 inch = 72 points)
pdf_width = 6 * inch
pdf_height = 4 * inch

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
