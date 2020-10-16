import csv
import logging

from dbProcessor.DBEncoder import DBEncoder
from dbProcessor.DBUtils import DBUtils

if __name__ == "__main__":
    logging.basicConfig(filename='error_encoder.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    python_errors = []
    db_encoder = DBEncoder()
    bert_servers = ['192.168.17.250', '192.168.17.252']
    db_utils = DBUtils()
    encoded_tables = ["ImportError"]
    with open("PythonErrors.csv", "r", encoding='utf-8') as python_err:
        csv_reader = csv.reader(python_err)
        for index, row in enumerate(csv_reader):
            python_errors.append(row[0])

    for err in python_errors:
        if err in encoded_tables:
            pass
        else:
            try:
                table_name = 'Python' + err + 'Test'
                # db_utils.duplicate_table(table_name=table_name)
                # db_utils.append_column(table_name=table_name)
                db_encoder.encode_table(table_name=table_name, server_addresses=bert_servers)
            except Exception as e:
                logging.critical(err + " Encoding Failed")
                logging.critical("Error Massage: " + str(e))

        # db_encoder.encode_table(table_name=table_name, server_addresses=bert_servers)
