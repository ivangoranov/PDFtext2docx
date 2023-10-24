import re

import click
from PIL import Image
import pytesseract
from googletrans import Translator
import os
import fitz
import docx

# TODO add config file
pytesseract.pytesseract.tesseract_cmd = (
    r"/usr/bin/tesseract"  # Adjust to your Tesseract path
)

translator = Translator()


@click.group()
def main():
    pass


@main.command()
@click.argument("input_dir")
@click.argument("output_dir")
@click.option("--font-name", default="Arial", help="Font name for the DOCX document")
@click.option(
    "--font-size", default=12, type=click.INT, help="Font size for the DOCX document"
)
@click.option("--translate", is_flag=True, help="Translate text to Spanish")
@click.option("--source-lang", default="en", help="Source language for translation")
@click.option("--target-lang", default="es", help="Target language for translation")
def extract_and_create_docx(
    input_dir, output_dir, font_name, font_size, translate, source_lang, target_lang
):
    if os.path.isfile(input_dir):
        # Process a single file
        extracted_text = process_single_pdf(input_dir)

        if translate:
            extracted_text = translate_text(extracted_text, source_lang, target_lang)

        for text in extracted_text:
            print(text)

        create_document(extracted_text, input_dir, output_dir, font_name, font_size)

    elif os.path.isdir(input_dir):
        # Process all PDF files in the directory
        document_text = []
        pdf_files = [
            {"path": pdf.path, "name": pdf.name.split(".")[0]}
            for pdf in list(
                filter(
                    lambda a: a.name.lower().endswith(".pdf"),
                    [f for f in os.scandir(input_dir)],
                )
            )
        ]
        image_files = [
            {"path": pdf.path, "name": pdf.name.split(".")[0]}
            for pdf in list(
                filter(
                    lambda a: a.name.lower().endswith(
                        (".jpg", ".jpeg", ".png", ".bmp", ".gif")
                    ),
                    [f for f in os.scandir(input_dir)],
                )
            )
        ]
        if len(image_files) > 0:
            for image in image_files:
                document_text.extend(extract_from_image(image["path"]))
            if translate:
                print("Translating...")
                document_text = translate_text(document_text, source_lang, target_lang)
            create_document(document_text, input_dir, output_dir, font_name, font_size)
        if len(pdf_files) > 0:
            for file_name in os.listdir(input_dir):
                file_path = os.path.join(input_dir, file_name)
                if file_name.endswith(".pdf"):
                    document_text = process_single_pdf(file_path)
                if translate:
                    document_text = translate_text(
                        document_text, source_lang, target_lang
                    )
                create_document(
                    document_text, input_dir, output_dir, font_name, font_size
                )
    else:
        print(f"Invalid input: {input_dir} is neither a file nor a directory.")


def sanitize_xml(text):
    # Replace control characters and non-ASCII characters
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]", "", text)
    # Ensure only valid XML characters are present
    text = "".join(
        char
        for char in text
        if 0x20 <= ord(char) <= 0xD7FF or 0xE000 <= ord(char) <= 0xFFFD
    )
    return text


def is_scanned_pdf_page(page):
    # Define a threshold for considering a page as scanned (adjust as needed)
    scanned_text_threshold = 0.1

    # Extract text from the page
    page_text = page.get_text()

    # Calculate the ratio of non-whitespace characters to total characters
    non_whitespace_chars = sum(c.isalnum() for c in page_text)
    total_chars = len(page_text)
    ratio = non_whitespace_chars / total_chars

    # If the ratio is below the threshold, consider it as a scanned page
    return ratio < scanned_text_threshold


def extract_from_scanned_page(page):
    image = page.get_pixmap()
    text = pytesseract.image_to_string(image)
    return text.split("\n\n")


def extract_from_image(img_file):
    img = Image.open(img_file)
    text = pytesseract.image_to_string(img)
    return text.split("\n\n")


def translate_text(input_text, source_lang, target_lang):
    translated_text = []
    sentence_delimiters = ['.', '!', '?']

    for paragraph in input_text:
        current_sentence = ""
        for char in sanitize_xml(paragraph):
            current_sentence += char
            if char in sentence_delimiters:
                translated = translator.translate(current_sentence, src=source_lang, dest=target_lang)
                translated_text.append(translated.text)
                current_sentence = ""
        # Handle any remaining text as a separate sentence
        if current_sentence:
            translated = translator.translate(current_sentence, src=source_lang, dest=target_lang)
            translated_text.append(translated.text)

    return " ".join(translated_text)


def create_document(extracted_text, input_pdf, output_dir, font_name, font_size):
    # Create a DOCX document with specified font settings
    doc = docx.Document()
    if type(extracted_text) == str:
        extracted_text = extracted_text.split("\n\n")
    for paragraph in extracted_text:
        # clean the text
        paragraph = sanitize_xml(paragraph)
        p = doc.add_paragraph(paragraph)
        run = p.runs[0]
        run.font.name = font_name
        run.font.size = docx.shared.Pt(font_size)

    # Save the DOCX document
    output_file = os.path.splitext(os.path.basename(input_pdf))[0] + ".docx"
    output_path = os.path.join(output_dir, output_file)
    doc.save(output_path)
    print(f"Saved: {output_path}")


def process_single_pdf(input_pdf):
    extracted_text = []

    # Add PDF text extraction logic here using PyMuPDF (fitz)
    doc_in = fitz.open(input_pdf)
    for page in doc_in:
        if is_scanned_pdf_page(page):
            extracted_text.extend(extract_from_scanned_page(page))
            continue
        # get text blocks
        page_blocks = page.get_text("blocks")
        # sort page blocks according to appearance
        page_blocks.sort(key=lambda a: a[5])
        # remove images and figures, and get only text block
        page_blocks_text = []
        for block in page_blocks:
            if block[4].lower().startswith("figure "):
                break
            if block[4].startswith("<image:"):
                continue
            page_blocks_text.append(block[4].replace("\n", ""))
        extracted_text.extend(page_blocks_text)

    return extracted_text


if __name__ == "__main__":
    main()
