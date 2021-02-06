import pickle
import time

import mysql.connector
import numpy as np
from bert_serving.client import BertClient


class VectorMatcher:
    def __init__(self):
        # Initialize database connection
        self.db_name = 'sotorrent20_03'
        self.db_password = 'sotorrent'
        self.db_username = 'sotorrent'
        self.encoder_addresses = ['192.168.17.253']
        self.db_address = '192.168.17.253'
        self.cnx = mysql.connector.connect(user=self.db_username, password=self.db_password,
                                           host=self.db_address, database=self.db_name)
        print('Connecting to Database @ %s' % self.db_address)
        self.cursor = self.cnx.cursor()
        print('Connected!')
        # Initialize BC encoders
        self.bc_encoders = []
        self.num_bc_encoders = len(self.encoder_addresses)
        self.status_list = [0] * self.num_bc_encoders
        for bc_addr in self.encoder_addresses:
            print('Connecting to Encoding Server @ %s' % bc_addr)
            try:
                self.bc_encoders.append(BertClient(ip=bc_addr, timeout=1000))
                print('Connected!')
            except TimeoutError:
                print("Connection time out for encoding server @ %s" % bc_addr)
        # Python Error types
        self.python_error_list = []
        with open('PythonErrors.csv', 'r') as python_errors:
            for error in python_errors:
                self.python_error_list.append(error[:-1])

    def vector_loader(self, table_name: str, central_vector_sum: float, threshold: float, msg_type: str):
        upper_limit = central_vector_sum + threshold
        lower_limit = central_vector_sum - threshold
        counting_sql = '''select count(*) from {table_name} where CodeVectorSum between %s and %s'''.format(
                table_name=table_name)
        self.cursor.execute(counting_sql, (lower_limit, upper_limit))
        print("Getting results, counting: ",end='')
        print(self.cursor.fetchone()[0])
        if msg_type == 'code':
            sql = '''select Id,CodeVector from {table_name} where CodeVectorSum between %s and %s'''.format(
                table_name=table_name)
        else:
            sql = '''select Id,ErrMsgVector from {table_name} where ErrMsgVectorSum between %s and %s'''.format(
                table_name=table_name)
        self.cursor.execute(sql, (lower_limit, upper_limit))
        print('Fetching result from vector base')
        results = self.cursor.fetchall()
        vector_arrays = np.array([]).reshape(0, 1024)
        post_id_list = []
        # This is the row count for each code's array
        array_row_list = []
        for row in results:
            post_id_list.append(row[0])
            vector_array = pickle.loads(row[1])
            array_row_list.append(vector_array.shape[0])
            vector_arrays = np.concatenate((vector_arrays, vector_array), axis=0)
        return vector_arrays, post_id_list, array_row_list

    def id_locator(self, vector_index: int, post_id_list: list, array_row_list: list):
        row_count_sum = 0
        id_index = 0
        for index, row_count in enumerate(array_row_list):
            row_count_sum += row_count
            if row_count_sum >= vector_index:
                id_index = index
                break
        return post_id_list[id_index]

    def code_matcher(self, src_vector, vector_arrays, post_id_list, array_row_list, num_candidates: int):
        l2_distances = np.linalg.norm(vector_arrays - src_vector, axis=1)
        sorting_array = np.argsort(l2_distances)[:num_candidates]
        id_list = []
        for vector_index in sorting_array:
            id_list.append(self.id_locator(vector_index, post_id_list, array_row_list))
        return id_list
        pass

    def sequences_encoder(self, sequences: list):
        print('String Encoding Routine')
        while True:
            for index, server_status in enumerate(self.status_list):
                if server_status == 0:
                    print('Using encoding server #%d'%index)
                    self.status_list[index] = 1
                    encoder = self.bc_encoders[index]
                    encoded_vector = encoder.encode(sequences)
                    self.status_list[index] = 0
                    return encoded_vector
            time.sleep(0.1)
        pass

    def solution_finder(self, err_msg: str, code_snippet: str, threshold: float, num_candidates: int):
        matches = [x for x in self.python_error_list if x in err_msg]
        if len(matches) == 0:
            err_type = 'Unknown'
            #     Sent to database dummy matching routine
            return 999999999
        else:
            err_type = matches[0]
        table_name = 'Python' + err_type + 'Test'
        encoded_code = self.sequences_encoder([code_snippet])
        central_vector_sum = encoded_code.sum()
        print('Central Vector Sum = %f' % central_vector_sum)
        vectors, post_ids, code_block_count = self.vector_loader(table_name, central_vector_sum, threshold, 'code')
        result_ids = self.code_matcher(encoded_code, vectors, post_ids, code_block_count, num_candidates)
        return result_ids

    def solution_loader(self, id_list: list):
        sql = '''select Id,AcceptedAnswerId,Title,Body from Posts where Id in (%s)'''
        answer_sql = '''select Id, Body from Posts where Id in (%s)'''
        format_strings = ','.join(['%s'] * len(id_list))
        self.cursor.execute(sql% format_strings,tuple(id_list))
        questions_info = self.cursor.fetchall()
        answer_id_list = []
        for question_info in questions_info:
            answer_id_list.append(question_info[1])
        format_strings = ','.join(['%s'] * len(answer_id_list))
        self.cursor.execute(answer_sql% format_strings,tuple(answer_id_list))
        answers = self.cursor.fetchall()
        return questions_info, answers


if __name__ == "__main__":
    # vector_matcher = VectorMatcher()
    # ids = vector_matcher.solution_finder('ValueError', 'print(x)', 0.01, 5)
    # print(ids)
    pass