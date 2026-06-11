from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


def extract_text_from_pdf(uploaded_file):
    """Extract plain text from an uploaded PDF file.

    Raises:
        ValueError: If the file is missing, unreadable, or contains no text.
    """
    if uploaded_file is None:
        raise ValueError("No PDF file was uploaded.")

    try:
        uploaded_file.seek(0)
        reader = PdfReader(uploaded_file)
    except PdfReadError as exc:
        raise ValueError("The uploaded file is not a readable PDF.") from exc
    except Exception as exc:
        raise ValueError("Could not open the PDF file. Please upload a valid PDF.") from exc

    pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            page_text = page.extract_text() or ""
        except Exception as exc:
            raise ValueError(f"Text could not be extracted from page {page_number}.") from exc

        pages_text.append(page_text)

    extracted_text = "\n".join(pages_text).strip()

    if not extracted_text:
        raise ValueError(
            "No readable text was found in the PDF. It may be scanned, image-based, or protected."
        )

    return extracted_text
