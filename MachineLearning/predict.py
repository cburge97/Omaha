import sys, json

def read_in():
    input - sys.stdin.readlines()
    return json.loads(lines[0])

def main():
    lines = read_in()
    print lines

if __name__=='_main_':
    main()