from _in_package import *

import common
import hash_
import runing_config
import runing_tmp_data


def r_mods():
    runing_config.g_mods_dir = common.get_config("g_mods_dir")
    while runing_config.g_mods_dir == "":
        print("g_mods_dir未设置, 请先设置g_mods_dir")
        common.w_config("g_mods_dir", input("g_mods_dir: "))
        runing_config.g_mods_dir = common.get_config("g_mods_dir")
    runing_config.g_mods_dir = common.formatting_path(runing_config.g_mods_dir)

    hash_.traverse_dir(runing_config.MODS_DIR)
    hash_.hash_files_from_glist(hashlib.sha256)

    archive_dir = common.formatting_path(runing_config.g_mods_dir+"archive/")
    mod_list = runing_config.VERSIONS_MODS_LIST_PATH + "modlist"
    if not os.path.exists(archive_dir):
        os.mkdir(archive_dir)
    elif not os.path.isdir(archive_dir):
        print("err!")
        time.sleep(3)
        exit(-2) # archive目录被占用

    if not os.path.exists(mod_list):
        with open(mod_list, "w") as f: f.write("")
    elif not os.path.isfile(mod_list):
        print("err!")
        time.sleep(3)
        exit(-2) # mod_list文件被占用

    with open(mod_list, "a") as f:
        for mod in runing_tmp_data.file_hash_results:
            f.write(mod.hash_value+" : "+os.path.basename(mod.filepath)+"\n")
            os.rename(mod.filepath, archive_dir+mod.hash_value)

def w_mods():
    pass

def menu():
    mod_list = runing_config.VERSIONS_MODS_LIST_PATH + "modlist"
    if not os.path.exists(mod_list):
        r_mods()
    elif not os.path.isfile(mod_list):
        print("err!")
        time.sleep(3)
        exit(-2) # modlist文件被占用

if common.get_config("eula") != "true":
    print("这是一个实验性质的程序，你需要具备mc mod加载、存档管理相关知识，出现问题概不负责\n本程序理论上不修改存档，但是如果mod转移出现问题仍然加载存档可能发生数据丢失，请积极备份")
    if not common.eula():
        exit(0)

runing_config.WORK_DIR = common.formatting_path(os.getcwd())
runing_config.MODS_DIR = common.formatting_path(runing_config.WORK_DIR + "mods/")

if not (os.path.exists(runing_config.MODS_DIR) and os.path.isdir(runing_config.MODS_DIR)):
    print("err!")
    time.sleep(3)
    exit(-1) # 未找到mods目录

runing_config.VERSIONS_MODS_LIST_PATH = common.formatting_path(runing_config.WORK_DIR + "mum_list/")
if not os.path.exists(runing_config.VERSIONS_MODS_LIST_PATH):
    os.mkdir(runing_config.VERSIONS_MODS_LIST_PATH)
elif not os.path.isdir(runing_config.VERSIONS_MODS_LIST_PATH):
    print("err!")
    time.sleep(3)
    exit(-2) # mum_list目录被占用

if len(os.listdir(runing_config.MODS_DIR)) == 0:
    w_mods()
else:
    menu()
