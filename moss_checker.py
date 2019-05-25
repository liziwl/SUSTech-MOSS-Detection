import mosspy
import os
import fnmatch
import socks
import socket

import moss_id

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


def get_res_xml(loc_res_dir):
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
    for i in get_res_xml('input/ass1'):
        m.addFile(i)

    url = m.send()  # Submission Report URL

    print("Report Url: " + url)

    # Save report file
    m.saveWebPage(url, "submission/report.html")
