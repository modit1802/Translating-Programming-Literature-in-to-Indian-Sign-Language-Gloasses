import pdfplumber

# Open the PDF file
with pdfplumber.open('ch4.pdf') as pdf:
    extracted_text = ''

    # Define the vertical range to exclude (header and footer)
    top_margin = 100  # Adjust this value to match your document
    bottom_margin = 100  # Adjust this value to match your document

    # Iterate through each page in the PDF
    for page in pdf.pages:
        # Get the full height and width of the page
        page_height = page.height
        page_width = page.width

        # Define the cropping box to exclude the header and footer
        cropping_box = (0, top_margin, page_width, page_height - bottom_margin)

        # Crop the page to exclude the header and footer
        cropped_page = page.crop(cropping_box)

        # Extract text from the cropped page and append it to the result
        extracted_text += cropped_page.extract_text()

# Save the extracted text to a text file
with open('extracted_text_no_header_footer.txt', 'w', encoding='utf-8') as text_file:
    text_file.write(extracted_text)

print("Text extracted (without header and footer) and saved to 'extracted_text_no_header_footer.txt'")
