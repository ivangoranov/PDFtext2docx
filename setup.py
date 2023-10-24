from setuptools import setup, find_packages

setup(
    name="PDFtext2docx",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "extract-and-create-docx = PDFtext2docx.main:extract_and_create_docx",
        ]
    },
    install_requires=[
        "python-docx",
        "PyMuPDF",
    ],
)
