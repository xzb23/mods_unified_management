WORK_DIR: str = "./"
MODS_DIR: str
VERSIONS_MODS_LIST_PATH: str

g_mods_dir: str = ""

wait_c: int = 100

# nf: Not found
# te: Type err
EXIT_CODE = {"ok": 0, "nf": -1, "te": -2}