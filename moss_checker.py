import mosspy
import os
import fnmatch
import socks
import socket

import moss_id
import result_html2csv


class SS:
    """
    For proxy
    Set if connection refused
    """

    def __init__(self):
        self.orig_socket = socket.socket
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
        socket.socket = socks.socksocket
        print("Set proxy to 127.0.0.1:1080")

    def restore(self):
        socket.socket = self.orig_socket
        print("Restore proxy")


def get_res_by_ext(loc_res_dir):
    files_list = list()
    exten = ['c', 'h', 'cpp', 'hpp']
    for r, d, files in os.walk(loc_res_dir):
        for ext in exten:
            code_files = fnmatch.filter(files, '*.' + ext)
            if len(code_files) > 0:
                tmp_paths = [os.path.join(os.path.abspath(r), f) for f in code_files]
                files_list.extend(tmp_paths)
    print("Found %d CODE files" % (len(files_list)))
    return files_list


if __name__ == '__main__':
    ss = SS()
    userid = moss_id.my_moss_id

    # "cc" for C++ / "c" for C
    m = mosspy.Moss(userid, "cc")

    # Submission Base Files
    # print("-" * 50)
    # print("Add base file")
    # sub_file_dir_path = 'C:\\Users\liziq\\Desktop\\ass5'
    # file_list = get_res_by_ext(sub_file_dir_path)
    # for i in file_list:
    #     m.addBaseFile(i)
    # print("-" * 50)

    # Submission Files
    print("Add file")
    sub_file_dir_path = 'input/Assignment 1_20190525200309'
    file_list = get_res_by_ext(sub_file_dir_path)

    for i in file_list:
        try:
            m.addFile(i)
        except Exception as e:
            print(i, e, end="")
            print(" or File size is zero")
    print("-" * 50)

    # Submission Report URL
    url = m.send()
    print("Report Url: " + url)

    # Save report file
    os.makedirs("report")
    html_path = os.path.join("report", os.path.basename(sub_file_dir_path) + '.html')
    m.saveWebPage(url, html_path)
    result_html2csv.csv_report(html_path)

    # Download whole report locally including code diff links
    mosspy.download_report(url, os.path.join("report", os.path.basename(sub_file_dir_path)), connections=8)
