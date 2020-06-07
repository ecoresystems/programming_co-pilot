import mysql.connector
import pandas as pd
import time


def err_msg_match(err_msg: str):
    cnx = mysql.connector.connect(user='sotorrent', password='so-admin',
                                  host='192.168.17.253',
                                  database='sotorrent20_03')
    err_type = err_msg.split('\n')[-1]
    err_type = err_type.replace("'","''")
    sql =  "SELECT AcceptedAnswerId,Title,Body FROM PythonPosts WHERE Body LIKE \'%%%s%%\' AND AnswerCount>3 AND AcceptedAnswerId IS NOT NULL" % err_type
    print(sql)
    start_time = time.time()
    question_df = pd.read_sql(sql, cnx, params={"err_type": err_type})
    question_query_end_time = time.time()
    answer_sql = "SELECT * FROM Posts WHERE Id IN %s" % str(tuple(list(question_df['AcceptedAnswerId'])))
    answer_df = pd.read_sql(answer_sql, cnx)
    answer_query_end_time = time.time()
    cnx.close()
    return question_df, question_query_end_time - start_time, answer_df, answer_query_end_time - question_query_end_time
