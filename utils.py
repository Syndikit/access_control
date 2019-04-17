
# coding: utf-8

# In[ ]:


import os
import sys
import platform
"""
Constants
"""
START = 'friendadd'
NAME_LEN = 30
NAME_FORB =['/',':', '\n','\t',' ']
CONTENT_FORB = ['friends.txt','lists.txt','pictures.txt','audit.txt']
COMMANDS = ['friendadd','viewby','logout','listadd','friendlist','postpicture',
            'chlst','chmod','chown','readcomments','writecomments','end']

# Output file names 
FRIEND = 'friends.txt'
LIST = 'lists.txt'
PIC = 'pictures.txt'
AUDIT = 'audit.txt'

"""
Variables that make it easy to validate commands and iterate through after end() is called 
and final output files for lists.txt, friends.txt, and pictures.txt.
"""
profile_owner = ""
viewing_profile = ""
friends_list = [] # Each entry is a string
pic_names = [] # Each entry is a string
pic_owner_list = []  # Each entry has the form: {'name':photo_name, 'owner':owner, 'lists':[]}
list_names_members = [] # Each entry is a string
list_names = []
friend_list_assoc = {}

def get_file(filename):
    # Detects the OS: (Windows, Linux, MacOS = Darwin)
    this_os = platform.system()
    start = ''
    # Decides which root to start with
    if this_os == 'Windows':
        start = 'c:\\users'
    elif this_os == 'Linux':
        start = '/'
    elif this_os == 'Darwin':
        start = '/Users/'
    
    cwd = os.getcwd()
    try:
    # Checks current directory for files, first.
        if filename in cwd:
            file = os.path.abspath(cwd+'\\'+filename)
            print(file)
     
        else:
            for root, dirs, files in os.walk(start):
                for name in files:
                    if name == filename:
                        return os.path.abspath(os.path.join(root, name))
    except FileNotFoundError as err:
        make_file(AUDIT, err+' File was not found.')
        print('File was not found')
    
    

def read_text(file):
    """
    Returns each line in the commands file as a list
    """
    line_list = []
    # Standard Python open(), specifying read mode and taking in filename from above
    try:
        with open(file,'r') as f:
            for line in f:
                line_list.append(line.split())
        return line_list
    except Exception as err:
        add_output_entry(AUDIT, f'{err}' +' Empty/ Incorrect Command File\n')
        print('Empty/ Incorrect Command File\n' + err)
        


def make_files():
    """  Creates the initial friends, audit, list, or pictures output files  """
    files = [AUDIT, PIC,FRIEND,LIST]
    f_heads = ['Audit Log\n\nOpen Command File.\n', 'Photos\n\n','Final Friends List\n\n','Final List Associations\n\n']
    for i in range(4):
        with open(files[i], 'w') as f:
            f.write(f_heads[i])

