from _in_package import typing

WORK_DIR: str = "./"
MODS_DIR: str
VERSIONS_MODS_LIST_PATH: str

g_mods_dir: str = ""

wait_c: int = 100

# nf: Not found
# te: Type err
EXIT_CODE = {"ok": 0, "nf": -1, "te": -2}

menu = """
检测到mods文件改动
请选择：
1. 添加到mum模组清单，并按照清单拉取模组
2. 清除当前mods变更并按照清单拉取模组
3. 按照当前mods目录重建模组清单（请确认你知道这会发生什么）
4. 按照清单拉取模组并取消管理
"""

class MenuCode(typing.NamedTuple):
    add_: str = "1"
    del_: str = "2"
    re_: str = "3"
    uninstall: str = "4"
MENU_CODE = MenuCode()

EXE_DIR: str