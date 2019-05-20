from background_task import background
import os

@background(schedule=20)
def test_read_file():

    # Look for your absolute directory path
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + '/chilli_query.txt'

    file1 = open(file_path, 'r')
    file2 = open('otherfile', 'w+')

    for line in file1:
        file2.write(line)

    file1.close()
    file2.close()