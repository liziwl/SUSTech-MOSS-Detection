import fnmatch
import os
import socket
from datetime import datetime
from os.path import splitext, basename, join

import pytz
import socks
from loguru import logger

import moss_id
import mosspy

LOCAL_TZ = 'Asia/Shanghai'


def init_logger(this_filename):
    file_name = splitext(basename(this_filename))[0]
    logger.add(file_name + "_{time}.log", encoding="utf8")


class Proxy:
    """
    For proxy
    Set if connection refused
    """

    def __init__(self, proxy_server_ip="127.0.0.1", port=7891):
        self.orig_socket = socket.socket
        socks.set_default_proxy(socks.SOCKS5, proxy_server_ip, port)
        socket.socket = socks.socksocket
        logger.info(f"Set socket proxy to {proxy_server_ip}:{port}")

    def restore(self):
        socket.socket = self.orig_socket
        logger.info("Restore proxy")


def get_res_by_ext(loc_res_dir, exten_list):
    """
    get files by extension list
    Args:
        loc_res_dir: directory to walk
        exten_list: list like ['c', 'h', 'cpp', 'hpp']

    Returns:
        file list
    """

    files_list = list()
    for r, d, files in os.walk(loc_res_dir):
        for ext in exten_list:
            code_files = fnmatch.filter(files, '*.' + ext)
            if len(code_files) > 0:
                tmp_paths = [os.path.join(os.path.abspath(r), f) for f in code_files]
                files_list.extend(tmp_paths)
    logger.info("Found %d CODE files" % (len(files_list)))
    return files_list


if __name__ == '__main__':
    ss = Proxy(port=7891)
    userid = moss_id.my_moss_id
    init_logger(__file__)

    # 支持 languages = ("c", "cc", "java", "ml", "pascal", "ada", "lisp",
    # "scheme", "haskell", "fortran", "ascii", "vhdl", "perl", "matlab",
    # "python", "mips", "prolog", "spice", "vb", "csharp", "modula2",
    # "a8086", "javascript", "plsql", "verilog");
    m = mosspy.Moss(userid, "cc")
    # "cc" for C++ / "c" for C

    # Submission Base Files
    # 加入基础文件，不计入查重范围
    # logger.info("-" * 50)
    # logger.info("Add base file")
    # sub_file_dir_path = 'C:\\Users\liziq\\Desktop\\ass5'
    # file_list = get_res_by_ext(sub_file_dir_path)
    # for i in file_list:
    #     m.addBaseFile(i)
    # logger.info("-" * 50)

    # Submission Files
    # 学生提交文件
    logger.info("Add file")
    sub_file_dir_path = './res'
    file_list = get_res_by_ext(sub_file_dir_path, ['c', 'h', 'cpp', 'hpp'])
    logger.info(file_list)

    for i in file_list:
        try:
            m.addFile(i)
        except Exception as e:
            print(i, e, end="")
            print(" or File size is zero")
    logger.info("-" * 50)

    # Submission Report URL
    # 下载报告
    url = m.send()
    logger.info("Report Url: " + url)

    # Save report file
    # 保存报告
    os.makedirs("report", exist_ok=True)
    REPORT_PATH = 'report'
    time_f = datetime.now(tz=pytz.timezone(LOCAL_TZ)).strftime('%Y-%m-%d_%H-%M-%S_%f')
    PATH_PREFIX = f"{basename(sub_file_dir_path)}_{time_f}"
    html_path = join(REPORT_PATH, PATH_PREFIX + '.html')
    m.saveWebPage(url, html_path)
    logger.info(f"Download report to {html_path}")

    # Download whole report locally including code diff links
    # 下载完全报告
    whole_report_path = join(REPORT_PATH, PATH_PREFIX)
    mosspy.download_report(url, whole_report_path, connections=8)
    logger.info(f"Download whole report to {whole_report_path}")

    # Convert html report to csv file, may need to modify the logic
    # html报告转化为csv，根据需要自己修改函数逻辑
    # result_html2csv.csv_report(html_path)
