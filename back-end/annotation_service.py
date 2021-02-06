import os,json
import sqlite3


class AnnotationService:
    def __init__(self):
        self.hello_msg = 'Test message from AnnotationService'
        self.db_dir_path = 'database'
        self.db_file = 'database.db'
        self.db_path = os.path.join(self.db_dir_path, self.db_file)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def test_func(self):
        print(self.hello_msg)

    def load_historical_code(self, error_type):
        sql = 'select id, code from student_code where (annotated is null or annotated = 0)' \
              ' and error_type = ? order by random() limit 1 '
        self.cursor.execute(sql, (error_type,))
        result = self.cursor.fetchone()
        return result[0], result[1]

    @staticmethod
    def response_builder(questions_list: list, answers: list):
        response_list = []
        for index, question_info in enumerate(questions_list):
            question_id = question_info[0]
            accepted_answer_id = question_info[1]
            question_title = question_info[2]
            question_body = question_info[3]
            answer_body = ''
            for answer in answers:
                if answer[0] == accepted_answer_id:
                    answer_body = answer[1]
                    break
            response_list.append(
                {'question_id': question_id, 'question_title': question_title, 'question_body': question_body,
                 'answer_body': answer_body})
        return json.dumps(response_list)


if __name__ == "__main__":
    # annotation_service = AnnotationService()
    # code_id, code_snippet = annotation_service.load_historical_code('ValueError')
    pass
