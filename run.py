import subprocess

def run(args):
    result = subprocess.run(args, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        index = 0
        if len(sys.argv) > 2:
            index = int(sys.argv[2].strip())
        with open(file_location, 'r') as args_file:
            args = args_file.readlines()
        # print(args)
        # line = args[0].strip()
        # arg_arr = line.split(' ')
        # print(arg_arr)
        # print(run(['python3', 'solver.py'] + arg_arr))
        for i in range(index, len(args)):
            line = args[i]
            arg_arr = line.strip().split(' ')
            res = run(['python3', 'solver.py'] + arg_arr)
            write_file = arg_arr[0].split('/')[2]
            write_file = './sols/' + write_file
            print(write_file)
            f = open(write_file, "w")
            f.write(res)
            f.close()