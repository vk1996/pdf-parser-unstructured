import pdfplumber
from pdf2image import convert_from_path
from unstructured.partition.pdf import partition_pdf

class PDFParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.tables = []
        self.images = []
        self.text_elements = []

    def extract_tables(self):
        """Extract tables from PDF using pdfplumber"""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    self.tables.append(table)

    def extract_images(self):
        """Extract images from PDF using pdf2image"""
        images = convert_from_path(self.pdf_path)
        for i, img in enumerate(images):
            img_path = f"image_{i + 1}.png"
            img.save(img_path, "PNG")
            self.images.append(img_path)

    def extract_text_with_unstructured(self):
        """Extract structured text elements using unstructured"""
        elements = partition_pdf(filename=self.pdf_path)
        for element in elements:
            self.text_elements.append(str(element))

    def parse_pdf(self):
        """Runs all extraction methods"""
        self.extract_tables()
        self.extract_images()
        self.extract_text_with_unstructured()
        return {
            "tables": self.tables,
            "images": self.images,
            "text": self.text_elements,
        }

if __name__ == "__main__":
    pdf_path = "your-pdf.pdf"
    parser = PDFParser(pdf_path)
    data = parser.parse_pdf()

    print("Extracted Tables:")
    for table in data["tables"]:
        for row in table:
            print(row)

    print("\nExtracted Images:", data["images"])
    print("\nExtracted Text:")
    print("\n".join(data["text"]))