"""
Create python script for directory and/or file search. Script takes one argument - directory or file name or its part. Script should show results:
if it is a file:
file name
file path
other file attributes like owner, permissions, create or access date ( show 2 attributes only )
 if it is a directory:
show content of directory ( one level )
show directory path
other file attributes like owner, permissions, create or access date ( show 2 attributes only )
 All searches should be saved in a log file:
call date
script parameter ( what file or dir name was provided )
result that was show to user
all these results should be separated by delimiter ( like ------ or #### )

"""


import os
import sys
from datetime import datetime

log_name = "search_log.txt"


# https://stackoverflow.com/questions/1094841/get-a-human-readable-version-of-a-file-size
def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
# End of borrowed code :D



def setup_log_file():
    if os.path.exists(log_name):
        # all is good
        pass
    else:
        # no such file, create it
        with open(log_name, "w") as file:
            pass
    

def input_to_log_file(result:str)->None:
    call_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    parameter = sys.argv[1]
    with open(log_name, "a") as file:
        file.write(f'\n{call_date}\nGiven parameter: {parameter}\n\n{result}\n#####################################') 


maybe_dir_maybe_file = sys.argv[1]
# print(f'Path given is: {maybe_dir_maybe_file}')

# does path even exist?
if not os.path.exists(maybe_dir_maybe_file):
    print(f'Path {maybe_dir_maybe_file} does not exist')
    input_to_log_file(f'Given path does not exist')
    sys.exit()


setup_log_file()

# zinom kad duotas path egzistuoja
# toliau du skirtingi keliai
# 1-jei tai failas 2-jei tai direktorija

if os.path.isfile(maybe_dir_maybe_file):
    # file
    file = maybe_dir_maybe_file
    print(f'{file} is a file')
    res = f'{os.path.basename(file).split('/')[-1]}\n{os.path.abspath(file)}\nFile size: {sizeof_fmt(os.path.getsize(file))}\nLast modified: {datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d %H:%M:%S")}'
    print(res)
    input_to_log_file(res)


elif os.path.isdir(maybe_dir_maybe_file):
    # directory
    directory = maybe_dir_maybe_file
    contains = os.listdir(directory)
    print(f'{maybe_dir_maybe_file} is a directory')
    res = f'{os.path.basename(directory).split('/')[-1]}\nDirectory contains: {sizeof_fmt(os.path.getsize(directory))}:\n\t{" | ".join(contains)}\nLast modified: {datetime.fromtimestamp(os.path.getmtime(directory)).strftime("%Y-%m-%d %H:%M:%S")}'
    print(res)
    input_to_log_file(res)

else:
    print(f'No idea what given path is...')
    print(f'but it does exist... spooky')
    input_to_log_file(f'Given path exists, but couldn\'t be indentified')
    sys.exit()

