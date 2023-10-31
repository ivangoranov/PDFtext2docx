
# PDFtext2docx

The **PDFtext2docx Converter** is a Python package that allows you to extract text from PDF documents, scanned PDFs, and images. It provides options for text translation and can output the extracted text in DOCX format with customizable font settings.

## Features

- Extract text from PDF documents.
- Recognize and extract text from scanned PDF pages and images.
- Translate extracted text to other languages.
- Create DOCX documents with customizable font settings.

## Installation

You can install the package using pip:

```bash
pip install PDFtext2docx
```

## Usage

### Extract Text from PDF and Create DOCX

To extract text from a PDF document and create a DOCX file, you can use the following command:

```bash
pdf-text-converter extract_and_create_docx /path/to/input_pdf /path/to/output_dir --font-name Arial --font-size 12 --translate --source-lang en --target-lang es
```

- `/path/to/input_pdf`: Path to the input PDF file or directory containing PDFs.
- `/path/to/output_dir`: Path to the directory where the DOCX files will be saved.
- `--font-name`: (Optional) Font name for the generated DOCX document (default is Arial).
- `--font-size`: (Optional) Font size for the generated DOCX document (default is 12).
- `--translate`: (Optional) Enable translation of extracted text to another language.
- `--source-lang`: (Optional) Source language for translation (default is English - "en").
- `--target-lang`: (Optional) Target language for translation (default is Spanish - "es").

### Extract Text from Scanned PDFs and Images

The package can also automatically detect scanned pages in PDF documents and images, and then extract text from them. Simply use the `extract_and_create_docx` command as shown above.

## Examples

1. Extract text from a single PDF and create a DOCX:

```bash
pdf-text-converter extract_and_create_docx /path/to/input.pdf /path/to/output --translate
```

2. Extract text from a directory of PDFs and create DOCX files:

```bash
pdf-text-converter extract_and_create_docx /path/to/pdf_directory /path/to/output_directory --font-name Times --font-size 14
```

3. Extract text from a directory of images (scanned pages) and create a DOCX:

```bash
pdf-text-converter extract_and_create_docx /path/to/image_directory /path/to/output --translate --source-lang en --target-lang fr
```

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- Your Name

For more information and updates, visit the [GitHub repository](https://github.com/your/repo).

We hope you find this package helpful for your PDF text extraction needs. If you have any questions or encounter issues, please don't hesitate to [submit an issue](https://github.com/your/repo/issues) on GitHub.

Enjoy using **PDF Text Converter**!
```

Replace `/path/to/input.pdf`, `/path/to/output`, and other placeholders with the actual file paths and options you want to use. Make sure to include relevant author and repository information.

This README provides a basic overview of how to install and use your package. Feel free to expand it with more details, usage examples, and documentation specific to your package's functionality.