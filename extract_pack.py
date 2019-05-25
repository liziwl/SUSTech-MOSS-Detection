from shutil import unpack_archive, register_unpack_format
import os
import fnmatch
from py7zr import unpack_7zarchive
import rarfile


def unpack_rar(archive, path, extra=None):
    arc = rarfile.RarFile(archive)
    arc.extractall(path)


register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
register_unpack_format('RAR', ['.rar'], unpack_rar)


def extract(compressed_file, path_to_extract):
    base_name = os.path.splitext(os.path.basename(compressed_file))[0]
    exdir = os.path.join(path_to_extract, base_name)
    os.makedirs(exdir, exist_ok=True)
    unpack_archive(compressed_file, exdir)


def recursive_unpack(dir_path):
    exten = ['7z', 'zip', 'rar']
    one_more = False
    for r, d, files in os.walk(dir_path):
        packed = []
        for ext in exten:
            code_files = fnmatch.filter(files, '*.' + ext)
            if len(code_files) > 0:
                tmp_paths = [os.path.join(os.path.abspath(r), f) for f in code_files]
                packed.extend(tmp_paths)
        if not one_more and len(packed) > 0:
            one_more = True
        print(packed)
        for p in packed:
            extract(p, os.path.dirname(p))
            os.remove(p)
    if one_more:
        recursive_unpack(dir_path)


recursive_unpack('input')
