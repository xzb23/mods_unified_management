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
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))
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
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = formatting_path(os.path.dirname(exe_dir))+"config.json"
    if not os.path.exists(config_path):
        return ""
    elif not os.path.isfile(config_path):
        print("err")
        time.sleep(3)
        exit(-1) # config.json文件被占用
    with open(config_path, "r") as f:
        config_json = json.loads(f.read().strip())
        config_json: dict
        return config_json.get(config_name, "")
    return ""