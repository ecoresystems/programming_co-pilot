import configparser

import mysql.connector


class DBUtils:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_ip = config['DEFAULT']['DBAddress']
        self.db_port = config['DEFAULT']['DBPort']
        self.db_name = config['DEFAULT']['DBName']
        self.db_password = config['DEFAULT']['DBPassword']
        self.db_username = config['DEFAULT']['DBUsername']
        self.cnx = mysql.connector.connect(user=self.db_username, password=self.db_password,
                                           host=self.db_ip, database=self.db_name)
        self.cursor = self.cnx.cursor()
        pass

    def commit_operation(self):
        self.cnx.commit()

    def close(self):
        self.commit_operation()
        self.cnx.close()

    def append_column(self, table_name):
        query = ("ALTER TABLE {table_name} ADD COLUMN FeatureVector MEDIUMBLOB,"
                 "ADD COLUMN VectorSum FLOAT,"
                 "ADD COLUMN CodeVector MEDIUMBLOB,"
                 "ADD COLUMN CodeVectorSum FLOAT,"
                 "ADD COLUMN ErrMsgVector MEDIUMBLOB,"
                 "ADD COLUMN ErrMsgVectorSum FLOAT".format(table_name=table_name))
        self.cursor.execute(query)

    def duplicate_table(self, table_name, appendix='Test'):
        create_query = ("CREATE TABLE {old_table_name} LIKE {new_table_name}"
                        .format(old_table_name=table_name, new_table_name=(table_name + appendix)))
        copy_data_query = ("INSERT INTO {new_table_name} SELECT * FROM {old_table_name};"
                           .format(new_table_name=(table_name + appendix), old_table_name=table_name))
        self.cursor.execute(create_query)
        self.commit_operation()
        self.cursor.execute(copy_data_query)
        self.commit_operation()

    def select_question(self, err_type, is_random=True, limits=10):
        query = ("SELECT * FROM {err_type} LIMIT %s".format(err_type=err_type))
        query_random = ("SELECT * FROM {err_type} ORDER BY RAND() LIMIT %s".format(err_type=err_type))
        if is_random:
            query = query_random
        self.cursor.execute(query, (limits,))
        return self.cursor.fetchall()

    def iterate_rows(self, err_type, start_point=0, step=1000):
        query = ("SELECT * FROM {err_type} ORDER BY Id LIMIT %s,%s".format(err_type=err_type))
        self.cursor.execute(query, (start_point, step))
        return self.cursor.fetchall()

    def insert_vector(self, row_id, table_name, vector, vector_sum, code_vector, code_vector_sum, err_msg_vector,
                      err_msg_vector_sum):
        query = (
            "UPDATE {table_name} SET FeatureVector = %s, VectorSum = %s, CodeVector = %s, CodeVectorSum = %s,"
            " ErrMsgVector = %s,ErrMsgVectorSum = %s WHERE Id = %s;".format(table_name=table_name))
        self.cursor.execute(query, (
            vector, vector_sum, code_vector, code_vector_sum, err_msg_vector, err_msg_vector_sum, row_id))
        self.commit_operation()
        return None

    def get_row_count(self, table_name):
        query = ("SELECT COUNT(*) FROM {table_name}".format(table_name=table_name))
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]


if __name__ == "__main__":
    db_utils = DBUtils()
    print(db_utils.get_row_count(table_name='PythonImportError'))
