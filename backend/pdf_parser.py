import pdfplumber
from io import BytesIO
from fastapi import UploadFile

async def extract_text_from_pdf(file: UploadFile) -> str:
    """从PDF文件中提取文本，兼容多页"""
    contents = await file.read()
    text = ""
    
    with pdfplumber.open(BytesIO(contents)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    
    # 简单的文本清洗
    text = text.replace("\t", " ").replace("\r", "\n")
    # 去除多余的空行
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    cleaned_text = "\n".join(lines)
    
    return cleaned_text
