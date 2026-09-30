import os
import docx
from pypdf import PdfReader
from pptx import Presentation

sub_dir = 'submission_files'
print('=== SUBMISSION FILES AUDIT ===')

# 1. Brief Description DOCX
p_b_docx = os.path.join(sub_dir, 'OmniCare_AI_Brief_Project_Description.docx')
doc1 = docx.Document(p_b_docx)
print(f'[DOCX] Brief Project Description: {len(doc1.paragraphs)} paragraphs, {len(doc1.tables)} tables, size: {os.path.getsize(p_b_docx)//1024} KB')

# 2. Brief Description PDF
p_b_pdf = os.path.join(sub_dir, 'OmniCare_AI_Brief_Project_Description.pdf')
pdf1 = PdfReader(p_b_pdf)
print(f'[PDF] Brief Project Description: {len(pdf1.pages)} pages (TARGET: 3), size: {os.path.getsize(p_b_pdf)//1024} KB')

# 3. Whitepaper DOCX
p_w_docx = os.path.join(sub_dir, 'OmniCare_AI_Technical_Whitepaper.docx')
doc2 = docx.Document(p_w_docx)
print(f'[DOCX] Technical Whitepaper: {len(doc2.paragraphs)} paragraphs, {len(doc2.tables)} tables, size: {os.path.getsize(p_w_docx)//1024} KB')

# 4. Whitepaper PDF
p_w_pdf = os.path.join(sub_dir, 'OmniCare_AI_Technical_Whitepaper.pdf')
pdf2 = PdfReader(p_w_pdf)
print(f'[PDF] Technical Whitepaper: {len(pdf2.pages)} pages (TARGET: 5), size: {os.path.getsize(p_w_pdf)//1024} KB')

# 5. Pitch Presentation PPTX
p_p_pptx = os.path.join(sub_dir, 'OmniCare_AI_Short_Pitch_Presentation.pptx')
prs = Presentation(p_p_pptx)
print(f'[PPTX] Short Pitch Presentation: {len(prs.slides)} slides (TARGET: 12), size: {os.path.getsize(p_p_pptx)//1024} KB')

# 6. Pitch Presentation PDF
p_p_pdf = os.path.join(sub_dir, 'OmniCare_AI_Short_Pitch_Presentation.pdf')
pdf3 = PdfReader(p_p_pdf)
print(f'[PDF] Short Pitch Presentation: {len(pdf3.pages)} pages (TARGET: 12), size: {os.path.getsize(p_p_pdf)//1024} KB')

# 7. Executive Summary PDF
p_e_pdf = os.path.join(sub_dir, 'OmniCare_AI_Executive_Summary.pdf')
pdf4 = PdfReader(p_e_pdf)
print(f'[PDF] Executive Summary PDF: {len(pdf4.pages)} pages (TARGET: 3), size: {os.path.getsize(p_e_pdf)//1024} KB')

print('\nChecking speaker notes in PPTX slides:')
for i, slide in enumerate(prs.slides, 1):
    notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else 'NO NOTES'
    print(f'  Slide {i:02d}: {slide.shapes.title.text if slide.shapes.title else "No Title"} | Notes: {len(notes)} chars')

print('\nChecking text for potential typos / artifacts across all PDFs:')
for name, r in [('Brief PDF', pdf1), ('Whitepaper PDF', pdf2), ('Pitch PDF', pdf3)]:
    full_text = ' '.join([p.extract_text() or '' for p in r.pages])
    errors = []
    if 'transcribed medical audio' in full_text:
        errors.append('found "transcribed medical audio"')
    if 'undefined' in full_text:
        errors.append('found "undefined"')
    if 'TODO' in full_text:
        errors.append('found "TODO"')
    if 'NaN' in full_text:
        errors.append('found "NaN"')
    if 'Error:' in full_text:
        errors.append('found "Error:"')
    print(f'  {name}: {len(full_text)} chars extracted, errors: {errors if errors else "None (CLEAN)"}')
