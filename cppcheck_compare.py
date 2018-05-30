from subprocess import call, PIPE, Popen, check_output
import os, sys
import re
import shutil

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


def branch_cppcheck(branch_name):
    print('Start branch: ' + branch_name)
    checkout_path = r'/tmp/cppcheck/' + branch_name
    output_file_name = 'cppcheck_' + branch_name + '.txt'
    output_file_path = os.path.join(temp_path, output_file_name)
    if not os.path.exists(checkout_path):
        os.makedirs(checkout_path)
    ps = Popen(('git', 'archive', branch_name), stdout=PIPE)
    check_output(('tar', '-x', '-C', checkout_path), stdin=ps.stdout)

    current_dir = os.getcwd()
    os.chdir(checkout_path)
    with open(output_file_path, 'wb') as f:
        call(['cppcheck', '--enable=all', 'src'], stderr=f, stdout=DEVNULL)
    os.chdir(current_dir)

    # Make backup of original
    shutil.copy(output_file_path, output_file_path + '.orig')

    # Re-write the output without line numbers
    lines = open(output_file_path, 'r').readlines()
    for i in range(len(lines)):
        lines[i] = re.sub(r'\:[0-9]+\]\:*', ']', lines[i])
    open(output_file_path, 'w').writelines(lines)

    print('End branch: ' + branch_name)
    return output_file_path


def cppcheck_diff(branch1, branch2, temp_path, save_path):
    branch1_output_path = branch_cppcheck(branch1)
    branch2_output_path = branch_cppcheck(branch2)

    with open(save_path, 'wb') as f:
        call(['diff', branch1_output_path, branch2_output_path], stdout=f)


    # get line numbers
    diff_lines = open(save_path, 'r').read().splitlines()
    branch1_lines = open(branch1_output_path + '.orig', 'r').read().splitlines()
    branch2_lines = open(branch2_output_path + '.orig', 'r').read().splitlines()

    # rewrite diff.txt
    diff_lines_output = []
    for i, diff_line in enumerate(diff_lines):
        if diff_line[0].isdigit():
            if 'a' in diff_line:
                diff_lines_output.append(diff_line)

                a, b = diff_line.split('a')
                line_numbers = map(int, b.split(','))
                line_slice = slice(line_numbers[0] - 1, line_numbers[-1])
                for line in branch2_lines[line_slice]:
                    diff_lines_output.append('+ ' + line)
            elif 'd' in diff_line:
                diff_lines_output.append(diff_line)

                a, b = diff_line.split('d')
                line_numbers = map(int, a.split(','))
                line_slice = slice(line_numbers[0] - 1, line_numbers[-1])
                for line in branch1_lines[line_slice]:
                    diff_lines_output.append('- ' + line)
            else:
                diff_lines_output.append(diff_line)

                a, b = diff_line.split('c')

                line_numbers = map(int, a.split(','))
                line_slice = slice(line_numbers[0] - 1, line_numbers[-1])
                for line in branch1_lines[line_slice]:
                    diff_lines_output.append('- ' + line)

                line_numbers = map(int, b.split(','))
                line_slice = slice(line_numbers[0] - 1, line_numbers[-1])
                for line in branch2_lines[line_slice]:
                    diff_lines_output.append('+ ' + line)
        else:
            pass

    print('***RESULT***')
    with open(save_path, 'w') as f:
        for line in diff_lines_output:
            f.write(line + '\n')
            print(line)

    print('***END RESULT***')

    # Clean all temporary files
    shutil.rmtree(temp_path)

if __name__ == "__main__":
    # sys.argv[0] is this script
    branch1 = sys.argv[1]
    branch2 = sys.argv[2]
    save_path = sys.argv[3]
    temp_path = '/tmp/cppcheck'
    cppcheck_diff(branch1, branch2, temp_path, save_path)
