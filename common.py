from _in_package import *
import runing_config


def formatting_path(path: str) -> str:
    path = path.strip()
    path = path.replace("\\", "/")
    if path[-1] != "/":
        path += "/"
    return path

def eula():
    print("请确认继续(Y/n): ")
    user_in = input()
    if user_in in ["", "y", "Y"]:
        w_config("eula", "true", True)
        return True
    else:
        exit(0)
        return False

def w_config(config_name: str, config_v: str, create_config_flag: bool = False):
    exe_dir = runing_config.EXE_DIR
    config_path = formatting_path(os.path.dirname(exe_dir))+"config.json"
    
    if create_config_flag:
        with open(config_path, "w") as f:
            f.write(json.dumps({config_name: config_v}))
        return True
    else:
        with open(config_path, "r") as f:
            config_ = json.loads(f.read().strip())
        config_[config_name] = config_v
        with open(config_path, "w") as f:
            f.write(json.dumps(config_))
        return True

def get_config(config_name):
    exe_dir = runing_config.EXE_DIR
    config_path = formatting_path(exe_dir)+"config.json"
    if not os.path.exists(config_path):
        return ""
    elif not os.path.isfile(config_path):
        print("err")
        time.sleep(3)
        exit(runing_config.EXIT_CODE["te"]) # config.json文件被占用
    with open(config_path, "r") as f:
        config_json = json.loads(f.read().strip())
        config_json: dict
        return config_json.get(config_name, "")
    return ""

def get_modlist():
    mod_list_path = runing_config.VERSIONS_MODS_LIST_PATH + "modlist"
    if not os.path.exists(mod_list_path):
        with open(mod_list_path, "w") as f: f.write("")
    elif not os.path.isfile(mod_list_path):
        print("err!")
        time.sleep(3)
        exit(-2) # mod_list文件被占用
    mod_hash_list = []
    mod_name_list = []
    with open(mod_list_path, "r") as f:
        mod_list = f.read().strip()
        mod_list = mod_list.split("\n")
        for mod in mod_list:
            mod_hash_list.append(mod.split(":")[0].strip())
            mod_name_list.append(mod.split(":")[1].strip())
    return mod_hash_list, mod_name_list


def add_game(c:int = 1):
    exe_dir = runing_config.EXE_DIR
    count = formatting_path(exe_dir)+"count"
    if not os.path.exists(count):
        with open(count, "w") as f:
            f.write("0")
    elif not os.path.isfile(count):
        print("err")
        time.sleep(3)
        exit(runing_config.EXIT_CODE["te"]) # count文件被占用/文件类型错误
    with open(count, "r+") as f:
        c = int(f.read().strip()) + 1
        f.seek(0)
        f.write(str(c))

def sub_game(c:int = 1):
    exe_dir = runing_config.EXE_DIR
    count = formatting_path(exe_dir)+"count"
    if not os.path.exists(count):
        with open(count, "w") as f:
            f.write("0")
        return 0
    elif not os.path.isfile(count):
        print("err")
        time.sleep(3)
        exit(runing_config.EXIT_CODE["te"]) # count文件被占用/文件类型错误
    with open(count, "r+") as f:
        c = int(f.read().strip()) - 1
        f.seek(0)
        f.write(str(c))
    return c

def get_exe_dir():
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    return formatting_path(exe_dir)

def check_file(file_path: str, def_):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(def_)
    elif not os.path.isfile(file_path):
        print("err")
        time.sleep(3)
        exit(runing_config.EXIT_CODE["te"]) # 文件被占用/文件类型错误