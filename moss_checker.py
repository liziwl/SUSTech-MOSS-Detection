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
    # Submission Files
    # file_list = get_res_by_ext('input/Assignment 1_20190525200309')
    # file_list = get_res_by_ext('input/Assignment 2_20190525200347')
    # file_list = get_res_by_ext('input/Assignment 3_20190525200421')
    # file_list = get_res_by_ext('input/Assignment 4_20190525200439')
    file_list = get_res_by_ext('input/Assignment 5_20190525200455')
    # file_list = get_res_by_ext('input/Assignment 6_20190525200517')
    for i in get_res_by_ext('C:\\Users\liziq\\Desktop\\ass5'):
        m.addBaseFile(i)

    for i in file_list:
        try:
            m.addFile(i)
        except Exception as e:
            pass

    url = m.send()  # Submission Report URL

    print("Report Url: " + url)

    # Save report file
    num = 5
    m.saveWebPage(url, "submission/report{}.html".format(num))
    result_html2csv.csv_report("submission/report{}.html".format(num),num)
