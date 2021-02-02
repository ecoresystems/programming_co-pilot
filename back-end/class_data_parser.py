import os, sys
from pathlib import Path
import subprocess
import sqlite3
import codecs


class ClassDataParser:
    def __init__(self):
        self.data_path = os.path.join('class_data', 'run_code.jsons')
        self.data_dir_path = 'data'
        self.db_dir_path = 'database'
        self.db_file = 'database.db'
        self.db_path = os.path.join(self.db_dir_path, self.db_file)
        Path(self.db_dir_path).mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        pass

    def db_file_execution(self):
        self.cursor.execute('select * from student_code where executed is null')
        # self.cursor.execute('select * from student_code')
        data = self.cursor.fetchall()
        counter = 0
        total = len(data)
        print(total)
        for row in data:
            counter += 1
            print('Processing %d lines of data, total: %d'%(counter,total))
            id = row[0]
            code = codecs.escape_decode(bytes(row[1][1:-2], "utf-8"))[0].decode("utf-8")
            print(code)
            if 'input()' in code:
                return_code=0
                stdout=''
                stderr=''
            else:
                return_code, stdout, stderr = self.code_executor(code)
            print(return_code)
            if return_code == 0:
                status = 'passed'
            else:
                status = 'failed'
            sql = '''update student_code set execution_status = ?,executed = ? where id = ?'''
            self.cursor.execute(sql, (status, 1, id))
            if counter % 50 == 0:
                self.conn.commit()

    def code_executor(self, code_snippet):
        with open("main.py", 'w', encoding='utf-8') as python_file:
            python_file.write(code_snippet)
        os.environ['PYTHONUNBUFFERED'] = "1"
        proc = subprocess.Popen([sys.executable, 'main.py'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                )

        try:
            stdout, stderr = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired as e:
            proc.kill()
            stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr

    def table_creator(self):
        sql = '''create table if not exists student_code (id integer primary key AUTOINCREMENT,
        code text,
        execution_status text,
        executed integer)'''
        self.cursor.execute(sql)
        self.conn.commit()
        pass

    def db_writer(self):
        counter = 0
        with open(self.data_path, 'r', encoding='utf-8') as jsons_file:
            for row in jsons_file:
                counter += 1
                print('Writing No.%d' % counter)
                self.cursor.execute("INSERT INTO student_code (code) VALUES (?)", (row,))
        self.conn.commit()


if __name__ == "__main__":
    cdp = ClassDataParser()
    cdp.db_file_execution()
