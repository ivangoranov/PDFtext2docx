import docx
import fitz
import argparse
import os
from pprint import pprint


def get_arguments():
    parser = argparse.ArgumentParser(
        description="A Python script to extract text from PDF documents."
    )
    parser.add_argument(
        "input_dir", help="Input directory for PDF files or path to single PDF"
    )
    parser.add_argument(
        "--output_dir",
        help="Optional: Output directory for docx files. "
        "If not specified, will be used the same directory as the input PDF",
    )
    # parse the arguments from the command-line
    args = parser.parse_args()
    # print the arguments, just for logging purposes
    pprint(vars(args))

    # collect only pdf files from directory
    input_files = []
    if not os.path.isdir(args.input_dir):
        # check if file extension is .pdf
        if not args.input_dir.split(".")[1] == "pdf":
            raise TypeError("Input file is not PDF")
        pdf_name = args.input_dir.split("/")[-1].split(".")[0]
        input_files.append({"path": args.input_dir, "name": pdf_name})
    else:
        input_files = [
            {"path": pdf.path, "name": pdf.name.replace(".pdf", "")}
            for pdf in list(
                filter(
                    lambda a: a.name[len(a.name) - 3 :] == "pdf",
                    [f for f in os.scandir(args.input_dir)],
                )
            )
        ]

    return {
        "input_dir": args.input_dir,
        "input_files": input_files,
        "output_dir": args.output_dir,
    }


def get_pages_dict(input_file):
    doc_in = fitz.open(input_file)
    pages_dict = {}
    for page in doc_in:
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
        pages_dict.update({page.number: page_blocks_text})
    return pages_dict


def create_docx(pdf_pages, doc_name, output_dir):
    # Create a document
    doc = docx.Document()
    for page in pdf_pages.values():
        for paragraph in page:
            # Add another paragraph (left blank for an empty line)
            doc.add_paragraph()

            # Add another paragraph
            p = doc.add_paragraph()
            run = p.add_run(paragraph)
            run.font.name = "Arial"
            run.font.size = docx.shared.Pt(12)

    # Save the document
    doc.save(f"{output_dir}/{doc_name}.docx")


def extract_text():
    # extract the arguments
    args = get_arguments()
    input_files = args.get("input_files")
    output_dir = args.get("output_dir")
    if not output_dir:
        output_dir = args.get("input_dir")
    # iterate over pages
    for pdf in input_files:
        pages = get_pages_dict(pdf.get("path"))
        create_docx(pages, pdf.get("name"), output_dir)
