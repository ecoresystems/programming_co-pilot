import os
import sqlite3


class AnnotationService:
    def __init__(self):
        self.hello_msg = 'Test message from AnnotationService'
        self.db_dir_path = 'database'
        self.db_file = 'database.db'
        self.db_path = os.path.join(self.db_dir_path, self.db_file)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def test_func(self):
        print(self.hello_msg)

    def load_historical_code(self,error_type):
        sql = 'select id, code, error_type from student_code where (annotated is null or annotated = 0)' \
              ' and error_type = ? order by random() limit 1 '

