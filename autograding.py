import sys
import tkinter
from io import StringIO
from tkinter import filedialog

import pytest

"""
generates the 'autograding.json' based on the pytests.
used for the automatic grading in GitHub Classroom.
"""

class Capturing(list):
    """
    captures the output to stdout and stderr
    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


def main():
    """
    generate the file
    :return:
    """
    root = tkinter.Tk()
    root.withdraw()

    project_folder = filedialog.askdirectory()
    args = f'{project_folder} --collect-only'.split(' ')
    with Capturing() as output:
        pytest.main(args)
    json = '{\n"tests": [\n'
    for line in output:
        if '<Function' in line:
            line = line.lstrip()
            name = line[10:-1]
            json += make_testcase(name) + ',\n'

    json = json[0:-2]
    json += '\n]\n}'
    file = open(project_folder + '/.github/classroom/autograding2.json', 'w')
    file.write(json)
    file.close()


def make_testcase(name):
    """
    make the json for one testcase
    :param name:
    :return:
    """
    testcase = '{' \
               f'"name": "{name}",\n' \
               f'"setup": "sudo -H pip3 install -r requirements.txt",\n' \
               f'"run": "pytest -v  -k \\"{name}\\"",\n' \
               f'"input": "",\n' \
               f'"output": "",\n' \
               f'"comparison": "included",\n' \
               f'"timeout": 10,\n' \
               f'"points": 1\n' \
               f'}}'
    return testcase


if __name__ == '__main__':
    main()
