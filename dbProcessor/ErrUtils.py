import csv

python_err = open("PythonErrors.csv", "r", encoding='utf-8')
csv_reader = csv.reader(python_err)
for index, row in enumerate(csv_reader):
    print(row[0])
    print(index + 1)
python_err.close()
