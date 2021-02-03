import pickle
import time

import mysql.connector
import numpy as np
from bert_serving.client import BertClient


class VectorMatcher:
    def __init__(self):
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
        self.bc_encoders = []
        self.num_bc_encoders = len(self.encoder_addresses)
        self.status_list = [0] * self.num_bc_encoders
        for bc_addr in self.encoder_addresses:
            print('Connecting to Encoding Server @ %s' % bc_addr)
            try:
                self.bc_encoders.append(BertClient(ip=bc_addr, timeout=1))
                print('Connected!')
            except TimeoutError:
                print("Connection time out for encoding server @ %s" % bc_addr)
        pass

    def vector_loader(self, table_name: str, central_vector_sum: float, threshold: float,type:str):
        upper_limit = central_vector_sum + threshold
        lower_limit = central_vector_sum - threshold
        if type == 'code':
            sql = '''select Id,CodeVector from {table_name} where CodeVectorSum between %s and %s'''.format(
                table_name=table_name)
        else:
            sql = '''select Id,ErrMsgVector from {table_name} where ErrMsgVectorSum between %s and %s'''.format(
                table_name=table_name)
        self.cursor.execute(sql, (lower_limit, upper_limit))
        results = self.cursor.fetchall()
        vector_arrays = np.array([])
        post_id_list = []
        # This is the row count for each code's array
        array_row_list = []
        for row in results:
            post_id_list.append(row[0])
            vector_array = pickle.loads(row[1])
            array_row_list.append(vector_array.shape[0])
            vector_arrays = np.concatenate((vector_arrays, vector_array), axis=0)
        return vector_arrays, post_id_list, array_row_list
        pass

    def err_msg_matcher(self):
        pass

    def code_matcher(self):
        pass

    def sequences_encoder(self, sequences: list):
        while True:
            for index, server_status in enumerate(self.status_list):
                if server_status == 0:
                    self.status_list[index] = 1
                    encoder = self.bc_encoders[index]
                    encoded_vector = encoder.encode(sequences)
                    self.status_list[index] = 0
                    return encoded_vector
            time.sleep(0.1)
        pass

    def solution_finder(self, err_type: str, err_msg: str, code_snippet: str):
        encoding_list = [err_msg, code_snippet]
        table_name = 'Python' + err_type
        encoded_vector = self.sequences_encoder(encoding_list)
        pass


if __name__ == "__main__":
    vector_matcher = VectorMatcher()
    vectors, post_ids, code_block_count = vector_matcher.vector_loader('PythonValueErrorTest', 1, 0.05,'code')
