import mysql.connector


def create_separate_err_table():
    cnx = mysql.connector.connect(user='sotorrent', password='so-admin',
                                  host='192.168.17.253',
                                  database='sotorrent20_03')
    cursor = cnx.cursor()
    err_file = open("errs.txt", 'r')
    err_length = 49
    counter = 0
    for row in err_file:
        counter += 1
        err = row.split('+-- ')[1].strip()
        print("Processing %d out of %d errors, error name: %s" % (counter, err_length + 1, err))
        drop_sql = "DROP TABLE IF EXISTS Python%s" % err
        cursor.execute(drop_sql)
        sql = "CREATE TABLE Python%s AS SELECT * FROM PythonPosts WHERE Body LIKE \"%%%s%%\"" % (err, err)
        print(sql)
        cursor.execute(sql)
        break
    err_file.close()


if __name__ == "__main__":
    create_separate_err_table()
