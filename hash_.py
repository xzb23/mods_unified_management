from _in_package import *

import common
import runing_config
import runing_tmp_data

def traverse_dir(root_dir):
    print("正在遍历mod文件ing...")
    for path, dirs, files in os.walk(root_dir):
        path = common.formatting_path(path)
        for filename in files:
            runing_tmp_data.file_path_list.append(path + filename)
    print(f"完成\t总计 {len(runing_tmp_data.file_path_list)} 个文件")


def hash_files_from_glist(algorithm: function):
    print("正在计算mod文件散列ing...")
    i = 0
    p_old_i = -1
    for f_path in runing_tmp_data.file_path_list:
        with open(f_path, "rb") as f:
            f_hash = hashlib.file_digest(f, algorithm)
            runing_tmp_data.file_hash_results.append(runing_tmp_data.FileHashResult(f_path, f_hash.hexdigest(), algorithm.__name__))
            runing_tmp_data.hash_to_paths[(f_hash.hexdigest(), algorithm.__name__)] = f_path
        i += 1
        if i % runing_config.wait_c == 0:
            p_old_i = i
            print(f"\r{i}/{len(runing_tmp_data.file_path_list)}", end="")
    if p_old_i != -1 and i != p_old_i:
        print(f"\r{i}/{len(runing_tmp_data.file_path_list)}", end="")
    print()