import docx
from sqlalchemy.orm import class_mapper

def process_txt_file(uploaded_file):
    content = uploaded_file.read()
    return content.decode("utf-8")

def process_docx_file(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = [para.text for para in doc.paragraphs]
    return '\n'.join(text)

def serialise(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)

def serialise_data_model(model):
    return {k: v for k, v in model.__dict__.items() if not k.startswith("_")}
