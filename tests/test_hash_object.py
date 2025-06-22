import os
from src.core.hash_object import hash_object_git

def test_hash_without_write(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")
    result = hash_object_git(str(test_file), write=False)
    assert isinstance(result, str) and len(result) == 40
