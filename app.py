from _in_package import *

import common
import hash_
import runing_config
import runing_tmp_data


def r_mods(pass_hash: list[str] = []):
    runing_config.g_mods_dir = common.get_config("g_mods_dir")
    while runing_config.g_mods_dir == "":
        print("g_mods_dir未设置, 请先设置g_mods_dir")
        common.w_config("g_mods_dir", common.formatting_path(input("g_mods_dir: ")))
        runing_config.g_mods_dir = common.get_config("g_mods_dir")
    runing_config.g_mods_dir = common.formatting_path(runing_config.g_mods_dir)

    hash_.traverse_dir(runing_config.MODS_DIR)
    hash_.hash_files_from_glist(hashlib.sha256)

    g_mods_archive_dir = common.formatting_path(runing_config.g_mods_dir+"archive/")
    mod_list = runing_config.VERSIONS_MODS_LIST_PATH + "modlist"
    if not os.path.exists(g_mods_archive_dir):
        os.mkdir(g_mods_archive_dir)
    elif not os.path.isdir(g_mods_archive_dir):
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
            if mod.hash_value in pass_hash:
                continue
            f.write(mod.hash_value+" : "+mod.filepath.split(runing_config.MODS_DIR)[1]+"\n")
            if os.path.exists(g_mods_archive_dir+mod.hash_value):
                continue
            # os.rename(mod.filepath, g_mods_archive_dir+mod.hash_value)
            with open(mod.filepath, "rb") as src, open(g_mods_archive_dir+mod.hash_value, "wb") as out:
                data = src.read(1024**2)
                while data:
                    out.write(data)
                    data = src.read(1024**2)

def w_mods():
    runing_config.g_mods_dir = common.get_config("g_mods_dir")
    g_mods_archive_dir = common.formatting_path(runing_config.g_mods_dir)+"archive/"
    g_mods_temp_dir = common.formatting_path(runing_config.g_mods_dir)+"temp/"
    mod_list_path = runing_config.VERSIONS_MODS_LIST_PATH + "modlist"

    if not (os.path.exists(mod_list_path) and os.path.isfile(mod_list_path)):
        print("未找到mod list")
        time.sleep(3)
        exit(0)
    if not (os.path.exists(g_mods_archive_dir) and os.path.isdir(g_mods_archive_dir)):
        print("err!")
        time.sleep(3)
        exit(-3) # g_mods_archive_dir损坏/不正确

    if not os.path.exists(g_mods_temp_dir):
        os.mkdir(g_mods_temp_dir)
    elif not os.path.isdir(g_mods_temp_dir):
        print("err!")
        time.sleep(3)
        exit(-2) # temp目录被占用

    with open(mod_list_path, "r") as f:
        mod_list = f.read().strip()
    mod_list = mod_list.split("\n")
    for mod in mod_list:
        mod_hash = mod.split(":")[0].strip()
        mod_name = mod.split(":")[1].strip()
        # 可选流程，验证temp和archive内文件hash，待开发
        if os.path.exists(runing_config.MODS_DIR+mod_name):
            continue
        if not os.path.exists(os.path.dirname(runing_config.MODS_DIR+mod_name)):
            os.makedirs(os.path.dirname(runing_config.MODS_DIR+mod_name))
        if os.path.exists(g_mods_temp_dir+mod_hash) and os.path.isfile(g_mods_temp_dir+mod_hash):
            os.rename(g_mods_temp_dir+mod_hash, runing_config.MODS_DIR+mod_name)
        elif os.path.exists(g_mods_archive_dir+mod_hash) and os.path.isfile(g_mods_archive_dir+mod_hash):
            with open(g_mods_archive_dir+mod_hash, "rb") as src, open(runing_config.MODS_DIR+mod_name, "wb") as out:
                data = src.read(1024**2)
                while data:
                    out.write(data)
                    data = src.read(1024**2)


def menu():
    mod_list = runing_config.VERSIONS_MODS_LIST_PATH + "modlist"
    if not os.path.exists(mod_list):
        r_mods()
    elif not os.path.isfile(mod_list):
        print("err!")
        time.sleep(3)
        exit(-2) # modlist文件被占用
    print(runing_config.menu)
    match input("> "):
        case runing_config.MENU_CODE.add_:
            modhsah_l, _ = common.get_modlist()
            r_mods(modhsah_l)
            w_mods()
        case runing_config.MENU_CODE.del_:
            for path, dirs, files in os.walk(runing_config.MODS_DIR):
                path = common.formatting_path(path)
                for file in files:
                    os.remove(path+file)
            w_mods()
        case runing_config.MENU_CODE.re_:
            os.remove(mod_list)
            r_mods()
        case runing_config.MENU_CODE.uninstall:
            w_mods()
            with open(runing_config.WORK_DIR + "mum_list/lock", "w") as f: f.write("1")


runing_config.EXE_DIR = common.get_exe_dir()
if common.get_config("eula") != "true":
    print("这是一个实验性质的程序，你需要具备mc mod加载、存档管理相关知识，出现问题概不负责\n本程序理论上不修改存档，但是如果mod转移出现问题仍然加载存档可能发生数据丢失，请积极备份")
    if not common.eula():
        exit(0)

exit_tips_flag = False
def init_():
    runing_config.WORK_DIR = common.formatting_path(os.getcwd())
    runing_config.MODS_DIR = common.formatting_path(runing_config.WORK_DIR + "mods/")

    if os.path.exists(runing_config.WORK_DIR + "mum_list/lock"):
        exit(0)

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

init_()

common.check_file(runing_config.EXE_DIR+"work_l", "")

if len(sys.argv) >= 2 and sys.argv[1] == "gameexit":
    if common.sub_game() > 0:
        exit(0)
    with open(runing_config.EXE_DIR+"work_l", "r") as f:
        work_l = f.read().strip()
    work_l = work_l.split("\n")
    for work in work_l:
        os.chdir(work.strip())
        init_()
        runing_config.g_mods_dir = common.get_config("g_mods_dir")
        g_mods_archive_dir = common.formatting_path(runing_config.g_mods_dir)+"archive/"
        g_mods_temp_dir = common.formatting_path(runing_config.g_mods_dir)+"temp/"
        mod_list_path = runing_config.VERSIONS_MODS_LIST_PATH + "modlist"

        if not (os.path.exists(mod_list_path) and os.path.isfile(mod_list_path)):
            print("未找到mod list")
            time.sleep(3)
            exit(0)
        if not (os.path.exists(g_mods_archive_dir) and os.path.isdir(g_mods_archive_dir)):
            print("err!")
            time.sleep(3)
            exit(-3) # g_mods_archive_dir损坏/不正确

        if not os.path.exists(g_mods_temp_dir):
            os.mkdir(g_mods_temp_dir)
        elif not os.path.isdir(g_mods_temp_dir):
            print("err!")
            time.sleep(3)
            exit(-2) # temp目录被占用

        with open(mod_list_path, "r") as f:
            mod_list = f.read().strip()
            mod_list = mod_list.split("\n")
            for mod in mod_list:
                mod_hash = mod.split(":")[0].strip()
                mod_name = mod.split(":")[1].strip()
                if not os.path.exists(g_mods_archive_dir+mod_hash):
                    os.rename(runing_config.MODS_DIR+mod_name, g_mods_archive_dir+mod_hash)
                elif not os.path.isfile(g_mods_archive_dir+mod_hash):
                    print(f"E: {mod_name}在g_mods_archive_dir中被占用")
                    exit_tips_flag = True
                elif not os.path.exists(g_mods_temp_dir+mod_hash):
                    os.rename(runing_config.MODS_DIR+mod_name, g_mods_temp_dir+mod_hash)
                elif not os.path.isfile(g_mods_archive_dir+mod_hash):
                    print(f"W: {mod_name}在g_mods_temp_dir中被占用")
        with open(runing_config.EXE_DIR+"work_l", "w") as f: f.write()
        if exit_tips_flag:
            input()
        exit(0)

common.add_game()
with open(runing_config.EXE_DIR+"work_l", "a") as f:
    f.write(runing_config.WORK_DIR+"\n")

if len(os.listdir(runing_config.MODS_DIR)) == 0:
    w_mods()
else:
    flag_list = []
    for path, dirs, files in os.walk(runing_config.MODS_DIR):
        for filename in files:
            flag_list.append(filename)
    if len(flag_list) == 0:
        w_mods()
    else:
        menu()
