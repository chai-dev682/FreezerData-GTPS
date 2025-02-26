import re
from llama_index.core import Document
from llama_index.readers.file import PDFReader

reader = PDFReader()

def clean_up_text(content: str) -> str:
    """
    Remove unwanted characters and patterns in text input.

    :param content: Text input.
    
    :return: Cleaned version of original text input.
    """

    # Fix hyphenated words broken by newline
    content = re.sub(r'(\w+)-\n(\w+)', r'\1\2', content)

    # Remove specific unwanted patterns and characters
    unwanted_patterns = [
        "\\n", "  —", "——————————", "—————————", "—————",
        r'\\u[\dA-Fa-f]{4}', r'\uf075', r'\uf0b7'
    ]
    for pattern in unwanted_patterns:
        content = re.sub(pattern, "", content)

    # Fix improperly spaced hyphenated words and normalize whitespace
    content = re.sub(r'(\w)\s*-\s*(\w)', r'\1-\2', content)
    content = re.sub(r'\s+', ' ', content)

    return content

def process_pdf(pdf_path: str, metadata: dict):
    documents = reader.load_data(file=pdf_path)
    # Call function
    cleaned_docs = []
    for d in documents:
        cleaned_text = clean_up_text(d.text)
        new_doc = Document(text=cleaned_text, metadata=d.metadata)
        cleaned_docs.append(new_doc)

    for cd in cleaned_docs:
        cd.metadata.update(metadata)
    return cleaned_docs