from _in_package import *


class FileHashResult(typing.NamedTuple):
    filepath: str
    hash_value: str
    algorithm: str


file_path_list: list[str] = []
file_hash_results: list[FileHashResult] = []

# hash_to_files: { (hash_value, algorithm): [filepath, ...] }
hash_to_paths: dict[tuple[str, str], str] = {}
