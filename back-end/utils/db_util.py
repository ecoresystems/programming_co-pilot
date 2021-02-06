import mysql.connector
import pandas as pd
import time


def err_msg_match(err_msg: str):
    cnx = mysql.connector.connect(user='sotorrent', password='sotorrent',
                                  host='192.168.17.253',
                                  database='sotorrent20_03')
    err_type = err_msg.split('\n')[-1]
    err_type = err_type.replace("'", "''")
    print(err_type)
    sql = "SELECT AcceptedAnswerId,Title,Body FROM PythonModuleNotFoundError WHERE Body LIKE \'%%%s%%\' AND AnswerCount>2 AND AcceptedAnswerId IS NOT NULL" % err_type
    print(sql)
    start_time = time.time()
    question_df = pd.read_sql(sql, cnx, params={"err_type": err_type})
    question_query_end_time = time.time()
    accepted_answer_id_list = list(question_df['AcceptedAnswerId'])
    if len(accepted_answer_id_list) > 1:
        answer_sql = "SELECT Id,Body AS AnswerBody FROM Posts WHERE Id IN %s" % str(tuple(list(question_df['AcceptedAnswerId'])))
    elif len(accepted_answer_id_list) == 1:
        answer_sql = "SELECT Id,Body AS AnswerBody FROM Posts WHERE Id = %s" % str(list(question_df['AcceptedAnswerId'])[0])
    answer_df = pd.read_sql(answer_sql, cnx)
    answer_query_end_time = time.time()
    cnx.close()
    result = pd.merge(question_df,answer_df.rename(columns={'Id':'AcceptedAnswerId'}),on=['AcceptedAnswerId'])
    return result, question_query_end_time - start_time, answer_query_end_time - question_query_end_time
