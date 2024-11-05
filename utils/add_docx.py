from docx import Document


async def add_docx_func(text, user_id):
    doc = Document()
    doc.add_paragraph(text)
    doc.save('user_id.docx')
