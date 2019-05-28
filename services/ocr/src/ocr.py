"""
Run object level OCR
"""
import pymongo
from group_cls import group_cls
from object_ocr import run_object_ocr

def ocr(db_insert_fn: Callable[[Mapping[T, T], T], None]) -> None:
    """
    On event trigger, run the proposals script
    """
    logging.info('Starting ocr process')
    start_time = time.time()
    client = MongoClient(os.environ["DBCONNECT"])
    logging.info(f'Connected to client: {client}. Setting watch on raw_pdfs collection')
    db = client.pdfs
    # Open a cursor that will watch for inserts on detect_pdfs
    try:
        with db.detect_pdfs.watch([{'$match': {'operationType': 'insert'}}]) as stream:
            for doc in stream:
                logging.info('Document found and added to queue')

                full = doc['fullDocument']
                page_data = full['page_data']
                for page in page_data:
                    if 'detected_objs' not in page:
                        # No detected objects for this page
                        continue
                    objs = page['detected_objs']
                    new_objs = group_cls(objs, 'Table', do_table_merge=True, merge_over_classes=['Figure', 'Section Header', 'Page Footer', 'Page Header'])
                    new_objs = group_cls(new_objs, 'Figure')
                    page['new_objs'] = new_objs
                run_object_ocr(full)

                db_insert_fn(full, client)

    except pymongo.errors.PyMongoError as err:
        logging.error("Error in pymongo:")
        logging.error(err)

def mongo_insert_fn(obj: Mapping[T, T], client: T) -> None:
    db = client.pdfs
    detect_pdfs = db.detect_pdfs
    result = detect_pdfs.insert_one(obj)
    logging.info(f"Inserted result: {result}")

if __name__ == '__main__':
    ocr(mongo_insert_fn)
