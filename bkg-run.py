#!/bin/env python
import os
import sys
import subprocess



def print_help():
    print("Usage: bkg-run <cmd> [args...]")

def main(argv):
    if len(argv) <= 1:
        print_help()
        return 1

    cmd = argv[1]
    if cmd in "-h -? --help /? /h".split(' '):
        print_help()
        return 0

    pid = bkg_run(argv[1:])
    print(pid)
    return 0

def bkg_run(cmd_and_args):
    cmd_and_args[0] = resolve_executable(cmd_and_args[0])
    sub = subprocess.Popen(cmd_and_args,
             executable=cmd_and_args[0],
             shell=False,
             stdin=open(os.devnull, 'r'),
             stdout=open(os.devnull, 'w'),
             stderr=open(os.devnull, 'w'))
    return sub.pid

def resolve_executable(exe):
    if os.sep in exe:
        return exe

    if os.path.exists(exe):
        return exe

    paths = os.getenv('PATH').split(os.pathsep)

    exe_ext = get_extname(exe)
    if exe_ext:
        pathexts = ['']
    else:
        pathexts = os.getenv('PATHEXT').split(os.pathsep)

    for path in paths:
        for ext in pathexts:
            file = os.path.join(path, exe + ext)
            if os.path.exists(file):
                return file

    return exe

def get_extname(file):
    try:
        parts = file.split(os.extsep)
        if len(parts) > 1:
            return parts[-1]
        else:
            return ''
    except:
        return ''

if __name__ == '__main__':
    sys.exit(main(sys.argv))


