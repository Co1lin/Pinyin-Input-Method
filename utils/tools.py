'''
some useful functions
'''

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fa5'

def dir_path(path):
    if path[-1] == '/':
        path = path[:-1]
    return path