import time
import mysql
from bert_serving.client import BertClient


class VectorMatcher:
    def __init__(self):
        self.db_address = '192.168.17.253'
        self.encoder_addresses = ['192.168.17.253']
        self.bc_encoders = []
        self.num_bc_encoders = len(self.encoder_addresses)
        self.status_list = [0] * self.num_bc_encoders
        for bc_addr in self.encoder_addresses:
            self.bc_encoders.append(BertClient(ip=bc_addr))
        pass

    def vector_loader(self,table_name):
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
