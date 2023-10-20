from setuptools import setup, find_packages

setup(
    name="PDFtext2docx",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pdf_to_docx_extractor = PDFtext2docx.main:extract_text'
        ]
    },
    install_requires=[
        'python-docx',
        'PyMuPDF',
    ],
)
