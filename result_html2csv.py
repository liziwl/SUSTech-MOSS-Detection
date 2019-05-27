from bs4 import BeautifulSoup
import csv
import re
from os.path import join, basename, dirname, splitext


def is_similar_uid(row):
    file1, file2 = row[0:2]
    p = re.compile(r"\(11\d{6}\)")
    id1 = p.findall(file1)[0][1:-1]
    id2 = p.findall(file2)[0][1:-1]
    if int(id1) != int(id2):
        print(row)
        return False
    else:
        return True


def get_sim_list(table):
    out = []
    for r in table:
        if len(r) > 0 and not is_similar_uid(r):
            out.append(r)
    return out


def csv_report(html_report_path, remove_dup_uid_csv_path=None, all_csv_path=None):
    html = open(html_report_path, encoding='utf8').read()
    soup = BeautifulSoup(html, features='lxml')
    table = soup.find("table")

    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        if len(columns) > 0:
            output_row.append(columns[0].text.strip())
            output_row.append(columns[1].text.strip())
            output_row.append(int(columns[2].text.strip()))
            output_row.append(columns[0].find('a').get('href'))
            print(output_row)
            output_rows.append(output_row)

    if all_csv_path is None:
        org_name = splitext(basename(html_report_path))[0]
        all_csv_path = join(dirname(html_report_path), org_name + ".csv")
    with open(all_csv_path, "w", encoding='utf_8_sig', newline='')as csvfile:
        writer = csv.writer(csvfile)
        for i_row in output_rows:
            if len(i_row) > 0:
                writer.writerow(i_row)
                is_similar_uid(i_row)

    if remove_dup_uid_csv_path is None:
        org_name = splitext(basename(html_report_path))[0]
        remove_dup_uid_csv_path = join(dirname(html_report_path), org_name + "_unq.csv")
    with open(remove_dup_uid_csv_path, "w", encoding='utf_8_sig', newline='')as csvfile:
        writer = csv.writer(csvfile)
        tmp = get_sim_list(output_rows)
        tmp.sort(key=lambda k: k[2], reverse=True)
        writer.writerows(tmp)
