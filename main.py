from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PyPDF2 import PdfFileReader
import textract
import csv
import io

app = FastAPI()

class Msg(BaseModel):
    msg: str

@app.post("/upload")
async def upload_file(file: UploadFile = UploadFile(...)):
    file_extension = file.filename.split(".")[-1]

    if file_extension == 'pdf':
        text = extract_text_from_pdf(file.file)
    elif file_extension == 'csv':
        text = extract_text_from_csv(file.file)
    elif file_extension == 'doc':
        text = extract_text_from_doc(file.file)
    else:
        return {"error": "Invalid file format. Please upload a PDF, CSV, or DOC file."}

    return {"text": text.decode("utf-8")}

def extract_text_from_pdf(file):
    pdf = PdfFileReader(file)
    text = ""

    for page_num in range(pdf.getNumPages()):
        page = pdf.getPage(page_num)
        text += page.extractText()

    return text


def extract_text_from_csv(file):
    text = ""

    # Assuming CSV file has a single column with text
    reader = csv.reader(io.TextIOWrapper(file))
    for row in reader:
        text += ",".join(row)

    return text


def extract_text_from_doc(file):
    text = textract.process(file)
    return text.decode("utf-8")

@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}
