from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LTTextBox, LTText, LTTextLine, LTChar
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pandas as pd




def parse_pdf(fp):
    with open(fp, "rb") as fh:
        parser = PDFParser(fh)
        doc = PDFDocument(parser)
        laparams = LAParams()
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr=rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        texts = []
        positions = []
        pages = []
        for idx, page in enumerate(PDFPage.create_pages(doc)):
            interpreter.process_page(page)
            layout = device.get_result()
            for child in layout:
                if isinstance(child, LTTextBox):
                    for line in child:
                        for char in line:
                            if isinstance(char, LTChar):
                                text = char.get_text()
                                pos = char.bbox
                                page = idx
                                texts.append(text)
                                positions.append(pos)
                                pages.append(page)
    x1, y1, x2, y2 = list(zip(*positions))
    df = pd.DataFrame({
        "text": texts,
        "x1": x1,
        "y1":y1,
        "x2": x2,
        "y2":y2,
        "page": pages
                       })
    return df


"""
PDF Extraction over a single PDF file
"""


class PDFExtractor:
    def __init__(self, fp):
        self.df = parse_pdf(fp)

    def query(self, bbox, page):
        pass

    def get_page(self, page):
        return self.df[self.df["page"] == page]
