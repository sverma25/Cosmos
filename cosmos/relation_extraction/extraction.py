"""
extraction.py
After database has been created, perform relation extraction
"""

from fonduer.parser.models import Document, Sentence
from fonduer.candidates.models import mention_subclass
from fonduer import Meta
import os
import sys
import logging
from config import extraction_thread_count, input_pdf_dir


def text_variable_matcher_do_nothing(span):
    return True
    
    
def extract():
    logging.basicConfig(stream=sys.stdout, format='[%(levelname)s] %(name)s - %(message)s')
    log = logging.getLogger('cosmos')
    log.setLevel(logging.INFO)
    
    PARALLEL = extraction_thread_count # assuming a quad-core machine
    ATTRIBUTE = "cosmos"
    conn_string = 'postgresql://postgres@localhost:54321/' + ATTRIBUTE
    
    session = Meta.init(conn_string).Session()

    print(f"Documents: {session.query(Document).count()}")
    print(f"Sentences: {session.query(Sentence).count()}")

    Variable = mention_subclass("Variable")


if __name__ == '__main__':
    extract()



