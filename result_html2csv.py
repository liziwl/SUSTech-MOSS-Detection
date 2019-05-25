from bs4 import BeautifulSoup
import csv
import re

html = open("submission/report.html", encoding='utf8').read()
soup = BeautifulSoup(html, features='lxml')
table = soup.find("table")

output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)


def is_similar(row):
    file1, file2, line = row
    p = re.compile(r"11\d{6}")
    id1 = p.findall(file1)[0]
    id2 = p.findall(file2)[0]
    if id1 != id2:
        print(row)
        return True
    else:
        return False


def get_sim_list(table):
    out = []
    for r in table:
        if len(r) > 0 and is_similar(r):
            out.append(r)
    return out


with open('output.csv', "w", encoding='utf_8_sig', newline='')as csvfile:
    writer = csv.writer(csvfile)
    for i_row in output_rows:
        if len(i_row) > 0:
            writer.writerow(i_row)
            is_similar(i_row)

with open('output_dup.csv', "w", encoding='utf_8_sig', newline='')as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(get_sim_list(output_rows))
