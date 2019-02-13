from exp.pdf_extractor.extract import PDFExtractor
import pandas as pd

pd.options.display.max_columns = 10

fp = "data/test.pdf"
engine = PDFExtractor(fp)
print(engine.get_page(0).head(3))
print(engine.get_page(1).head(3))