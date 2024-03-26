import argparse
import fitz  # PyMuPDF
import pytesseract
import sys

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print("Error extracting text from PDF:", e)
        sys.exit(1)

def ocr_from_image(image_path):
    try:
        return pytesseract.image_to_string(image_path)
    except Exception as e:
        print("Error performing OCR on image:", e)
        sys.exit(1)

def extract_and_ocr_from_pdf(pdf_path, output_file):
    try:
        doc = fitz.open(pdf_path)
        ocr_text = ""
        for i in range(len(doc)):
            for img in doc.get_page_images(i):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                with open("temp_image.png", "wb") as f:
                    f.write(image_bytes)
                ocr_result = ocr_from_image("temp_image.png")
                ocr_text += ocr_result + "\n"
        doc.close()
        with open(output_file, "w") as f:
            f.write(ocr_text)
    except Exception as e:
        print("Error extracting and OCRing images from PDF:", e)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert scanned PDF to OCR text")
    parser.add_argument("-i", "--input", help="Input PDF file path", required=True)
    parser.add_argument("-o", "--output", help="Output file path for OCR text", required=True)
    args = parser.parse_args()
    
    input_pdf = args.input
    output_file = args.output

    extract_and_ocr_from_pdf(input_pdf, output_file)
