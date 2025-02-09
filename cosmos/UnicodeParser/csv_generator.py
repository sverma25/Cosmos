import sys

#set up psycopg2 environment
import psycopg2

#driving_distance module
#note the lack of trailing semi-colon in the query string, as per the Postgres documentation


def generate_csv(db,outputfile):
    """
    Export the db as a csv file.
    :param db: db connection string.
    :param outputfile: Name of the output csv.
    """

    variable_lj_document = """
        SELECT document.name AS document_name,
        variable.*
        FROM variable
        LEFT JOIN document ON document.id=variable.document_id 
    """

    sent_attr = [
        'xpath',
        'words',
        'top',
        'table_id',
        'section_id',
        'row_start',
        'row_end',
        'right',
        'position',
        'pos_tags',
        'paragraph_id',
        'page',
        'ner_tags',
        'name',
        'lemmas',
        'left',
        'html_tag',
        'html_attrs',
        'document_id',
        'dep_parents',
        'dep_labels',
        'col_start',
        'col_end',
        'char_offsets',
        'cell_id',
        'bottom',
        'abs_char_offsets']

    variable_lj_document_lj_sentence = """
    SELECT t.*, %s
    FROM (%s) AS t
    LEFT JOIN sentence ON sentence.id=t.sentence_id
    """%(','.join(list(map(lambda x: 'sentence.%s AS sent_%s ' % (x, x), sent_attr))), variable_lj_document)


    variable_lj_document_lj_sentence_lj_equation = """
    SELECT t.*, equation.top AS equation_top, equation.bottom AS equation_bottom, equation.left AS equation_left, equation.right AS equation_right, equation.page AS equation_page
    FROM (%s) as t
    LEFT JOIN equation ON equation.id=t.equation_id
    """%(variable_lj_document_lj_sentence)

    variable_lj_document_lj_sentence_lj_equation_lj_corenlp = """
    SELECT t.*, table_x.symbols, table_x.phrases, table_x.phrases_top, table_x.phrases_bottom, table_x.phrases_left, table_x.phrases_right, table_x.phrases_page 
    FROM (%s) as t
    LEFT JOIN table_x ON table_x.equation_id=t.equation_id
    """%(variable_lj_document_lj_sentence_lj_equation)

    
    variable_lj_document_lj_sentence_lj_equation_lj_corenlp_lj_image = """
    SELECT t.*, image.img_path as sentence_img
    FROM (%s) as t
    LEFT JOIN image ON image.id=t.sentence_id
    """%(variable_lj_document_lj_sentence_lj_equation_lj_corenlp)

    variable_lj_document_lj_sentence_lj_equation_lj_corenlp_lj_image_lj_image = """
    SELECT t.*, image.img_path as equation_img
    FROM (%s) as t
    LEFT JOIN image ON image.id=t.equation_id
    """%(variable_lj_document_lj_sentence_lj_equation_lj_corenlp_lj_image)

    query = variable_lj_document_lj_sentence_lj_equation_lj_corenlp_lj_image_lj_image

    #make connection between python and postgresql
    conn = psycopg2.connect(db)
    conn.set_client_encoding('UTF8')
    cur = conn.cursor()

    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

    with open(outputfile, 'wb') as f:
        cur.copy_expert(outputquery, f)

    conn.close()


