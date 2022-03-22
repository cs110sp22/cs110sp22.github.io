'''
This script reads each notebook in the current directory and
converts it to a python file (so that it can run outside of Jupyter)
'''
import json
import argparse
import os
import sys
from excluded import EXCLUDED

def write_line_to_file(fout, line):
    # print(line)
    fout.write(line)

def get_notebooks(path):
    import glob
    file_matcher = '{0}/*.ipynb'.format(path)
    return glob.glob(file_matcher)

def generate_python_path(notebook):
    import re
    tokens = notebook.split('/')
    notebook = tokens[len(tokens) - 1]
    tokens.pop()
    path = '/'.join(tokens)
    
    file_name = notebook.replace('.ipynb', '')
    # replace spaces with underscores:
    file_name = file_name.lower().replace(' ', '_')
    # remove special characters:
    chars = '():,;/!#'
    # characters that mean something vis a vis regex:
    escaped_chars = '\-\.\'\[\]\?\*'
    regex_exp = '[' + chars + escaped_chars + ']'
    file_name = re.sub(regex_exp,'', file_name)
    return path + '/notebook_' + file_name + '.py'


def add_comments_message(fout, notebook):
    # Instructor: Sarah Van Wart
    # License: CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/
    msg = '''
# # ----------------------------------------------------------------
# # Course: EECS 110, Northwestern University
# # Term: Winter 2019
# # Autogenerated from: "{0}"
# # 
# # Note: Each example is commented out. To uncomment, highlight
# # the area you want to uncomment and type "cmd /" (which both adds
# # and removes comments).
# # ----------------------------------------------------------------
'''.format(notebook)
    write_line_to_file(fout, msg)

def do_conversions(path):
    # Read existing iPython Notebook file:
    for notebook in get_notebooks(path):
        print(generate_python_path(notebook))
        with open(notebook) as json_file: 
            data = json.load(json_file)

            # Create new file:
            fout = open(generate_python_path(notebook), 'w')

            add_comments_message(fout, notebook)
            for cell in data['cells']:
                write_line_to_file(fout, '\n')
                if cell['cell_type'] == 'markdown':
                    write_line_to_file(fout, '\n\n\n# # ' + '-'*80 + '\n')
                    for line in cell['source']:
                        write_line_to_file(fout, '# # ' + line)
                    write_line_to_file(fout, '\n# # ' + '-'*80 + '\n')
                else:
                    for line in cell['source']:
                        # ignore HTML markup:
                        if line.startswith('%%html'):
                            break
                        write_line_to_file(fout, '# ' + line)

        fout.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    dir = args.directory + '/'

    filenames = [
        fname for fname in sorted(os.listdir(dir))
        if fname not in EXCLUDED and os.path.isfile(dir+fname)
    ]
    dirnames = [
        fname for fname in sorted(os.listdir(dir))
        if fname not in EXCLUDED
    ]
    dirnames = [
        dir + fname for fname in dirnames if fname not in filenames
    ]
    
    print(
        'About to convert notebooks to python scripts for the following directories:', 
        dirnames
    )

    go_ahead = input('Would you like to proceed? (y/N) ')
    if go_ahead.upper() == 'Y':
        for dirname in dirnames:
            do_conversions(dirname)
    else:
        print('Cancelled.')
    
    sys.exit()

if __name__ == '__main__':
    main()