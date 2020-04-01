import subprocess

def run(args):
    result = subprocess.run(args, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as args_file:
            args = args_file.readlines()
        print(args)
        line = args[0].strip()
        arg_arr = line.split(' ')
        print(arg_arr)
        print(run(['python3', 'solver.py'] + arg_arr))
        # for line in args:
        #     arg_arr = line.split(' ')
        #     print(run(['python3'] + arg_arr))