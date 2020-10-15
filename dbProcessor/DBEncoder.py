import time
from multiprocessing import Process

import bs4
from bert_serving.client import BertClient

from .DBUtils import DBUtils


class DBEncoder:
    def __init__(self):
        self.table_name = None
        self.row_count = None
        self.step = 1000
        self.process_num = 4
        self.bert_servers = ['vsse.cc.kyushu-u.ac.jp']
        pass

    def run_parallel_encoding(self):
        print("Running Parallel Task With Parallel Process: " + str(self.process_num))
        # with open("endpoint", "r", encoding='utf-8') as file:
        #     print(file.read())
        #     if file.read() != '':
        #         sp = int(file.read())
        #     else:
        #         sp = 0
        for batch_index in range(self.row_count // (self.step * self.process_num)):
            batch_size = self.step * self.process_num
            batch_string_time = time.time()
            batch_start_point = batch_index * batch_size
            with open("endpoint", 'w', encoding='utf-8') as file:
                file.write(str(batch_start_point))
            print("Processed %d rows of data" % batch_start_point)
            print("Completed Percentage: %0.2f%%" % (batch_start_point * 100 / self.row_count))
            print("String to process batch: " + str(batch_index))
            process_list = []
            for process_index in range(self.process_num):
                p = Process(target=self.encoding_database,
                            args=(batch_start_point + process_index * self.step, process_index,))
                process_list.append(p)
                p.start()

            print("All batch process load complete")
            print("Waiting process sync")
            for p in process_list:
                p.join()
                p.close()
            print("Process synced")
            time_cost = time.time() - batch_string_time
            print("Batch %d with %d rows cost %0.2f seconds, ETA: " % (batch_index, batch_size, time_cost), end='')
            print(time.strftime("%H:%M:%S",
                                time.gmtime(time_cost * (self.row_count - batch_size * batch_index) / batch_size)))

    def encoding_database(self, starting_point, process_index):
        bc = BertClient(ip=self.bert_servers[process_index])
        db_utils = DBUtils()
        table_name = self.table_name
        result = db_utils.iterate_rows(err_type=table_name, start_point=starting_point, step=self.step)
        for row in result:
            Id = row[0]
            print("Processing ID: %d" % Id)
            accepted_answer_id = row[2]
            question_body = row[8]
            soup = bs4.BeautifulSoup(question_body, "html.parser")
            code_list = []
            code_content = ''
            err_msg_content = ''
            for code in soup.find_all('code'):
                code_list.append(code.text)
                if "Traceback (most recent call last)" in code.text:
                    err_msg_content += code.text
                else:
                    code_content += code.text
            if code_list and '' not in code_list:
                encoded_code = bc.encode(code_list)
                code_dump = encoded_code.dumps()
                vector_sum = encoded_code.sum().item()
                if code_content:
                    encoded_code_content = bc.encode([code_content])
                    code_content_dump = encoded_code_content.dumps()
                    code_vector_sum = encoded_code_content.sum().item()
                else:
                    code_content_dump = None
                    code_vector_sum = None

                if err_msg_content:
                    encoded_err_msg_content = bc.encode([err_msg_content])
                    err_msg_content_dump = encoded_err_msg_content.dumps()
                    err_msg_vector_sum = encoded_err_msg_content.sum().item()
                else:
                    err_msg_content_dump = None
                    err_msg_vector_sum = None
                db_utils.insert_vector(row_id=Id, table_name=table_name, vector=code_dump, vector_sum=vector_sum,
                                       code_vector=code_content_dump, code_vector_sum=code_vector_sum,
                                       err_msg_vector=err_msg_content_dump, err_msg_vector_sum=err_msg_vector_sum)
        bc.close()
        db_utils.close()
        return None

    def encode_table(self, table_name, server_addresses, step=20):
        self.table_name = table_name
        self.bert_servers = server_addresses
        self.step = step
        self.process_num = len(server_addresses)
        database_tools = DBUtils()
        db_encoder.row_count = database_tools.get_row_count(table_name)
        self.run_parallel_encoding()
        pass


if __name__ == "__main__":
    db_encoder = DBEncoder()
    table = 'PythonImportErrorTest'
    bert_servers = ['192.168.17.250', '192.168.17.252']
    db_encoder.encode_table(table_name=table, server_addresses=bert_servers)
    pass
