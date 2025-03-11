# Open the new image file to extract the script
img_path_3 = "/mnt/data/image.png"
img_3 = Image.open(img_path_3)

# Extract text from the image using pytesseract
text_3 = pytesseract.image_to_string(img_3)
text_3
