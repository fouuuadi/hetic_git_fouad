import os
import zlib

def read_commit(sha):
    """Lit un objet commit et retourne son contenu décodé."""
    obj_path = os.path.join('.git', 'objects', sha[:2], sha[2:])
    with open(obj_path, 'rb') as f:
        decompressed = zlib.decompress(f.read())
    header_end = decompressed.index(b'\0')
    content = decompressed[header_end+1:].decode()
    return content

def git_log():
    # 1. Lire HEAD
    with open('.git/HEAD') as f:
        ref = f.read().strip().split()[-1] 
    # 2. Lire le SHA du commit courant
    with open(os.path.join('.git', ref)) as f:
        sha = f.read().strip()
    # 3. Parcourir les commits
    while sha:
        content = read_commit(sha)
        print(f"commit {sha}")
        lines = content.split('\n')
        for line in lines:
            if line.startswith('tree '):
                continue
            elif line.startswith('parent '):
                parent = line.split()[1]
            elif line.strip() == '':
                msg_index = lines.index(line) + 1
                print('\n    ' + '\n    '.join(lines[msg_index:]))
                break
        else:
            parent = None
        print()
        sha = parent if 'parent' in locals() else None