"""
Name: Michael Austin
Login-ID: maa0075
ID number: 800-259-122
Assignment #: PA-2
Date: 04/18/2019
Purpose: Implement a simplified access control platform.
Status: Compiles and runs
"""

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
profile_owner = "root"
viewing_profile = ""
friends_list = [] # Each entry is a string
pic_names = [] # Each entry is a string
pic_owner_list = []  # Each pic has the default form: {'name':photo_name, 'owner':viewing_profile, 'list':'nil', 'permissions':['rw','--','--']}
list_names_members = [] # Each entry is a string

def get_file(filename):
    """
    File not found in cwd, start from the root and work down 
    until you find the file
    """   
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

def add_output_entry(file,text):
    # Lazy method so I don't have to keep using with open()
    with open(file, 'a') as f:
        f.write(text + "\n")

def pre_check(cmd_list):
    """
    #Iterates through commands from input file to ensure valid command words are used.
    """
    for i in cmd_list:
        if i[0] not in COMMANDS:
            add_output_entry(AUDIT,f'{i} is not one of the valid commands.')
            print(f'{i} is not one of the valid commands.')
            
def friend_add(friend_name):
    """
    Reads friends.txt to see if friend name is in there.
    If not, append to the text file, otherwise, throw and log error.
    Input: friend name as a string
    Output: None
    """
    with open(FRIEND, 'r') as file:
        names = file.readlines()
    
    if friend_name not in friends_list:
        if friend_name not in names:
            add_output_entry(FRIEND,friend_name+'\n')
            friends_list.append(friend_name)
            message = f'Added {friend_name} to friends.txt'
            add_output_entry(AUDIT, message)
            print(message)
    else:
        message = 'Error: Name/ friend already in friends list.'
        add_output_entry(AUDIT, message)
        print(message)

def viewby(name):
        """
        Allows only people in friends list to view the profile passed in, then 
        adds them to the viewing list (which can be no larger than 1 element)
        and appends a message to screen and audit.txt.
        Input: name (string) of person trying to view the profile (string) passed in 
        as second parameter
        Output: None. Modifies global viewing list for that profile. 
        """
        global viewing_profile
        # will need to swap out allowed list name below.
        if (name in friends_list or profile_owner) and not viewing_profile:
            message = f'{name} is viewing the profile.'
            add_output_entry(AUDIT, message)
            viewing_profile = name
            print(message)
        else:
            message = f'{name} cannot view the profile.'
            add_output_entry(AUDIT, message)
            print(message)
        
def post_photo(photo_name):
    """
    Posts photo if the owner is a friend viewing the profile and photo name not taken.
    Input: name of photo (string); name of owner (string)
    Output: None. Modifies pic_names, pic_owner_list lists; audit.txt
    """
    
    if viewing_profile == "":
        # if the owner isn't viewing the profile, they either aren't a friend or can't post
        message = f'Cannot post photo. No one currently viewing the profile.'
        add_output_entry(AUDIT, message)
        print(message)
    elif photo_name in pic_names or photo_name in CONTENT_FORB:
        # Checks whether the photo name has already been used. If so, produce and log error.
        message = f'Error: {photo_name} is invalid. No duplicate photo names or names of output files allowed.'
        add_output_entry(AUDIT, message)
        print(message)
    else:
        # Adds photo to the list of photo names 
        pic_names.append(photo_name)
        # Adds a dictionary containing the photo name, owner, list associated with it, permissions as a list, and comments as a list.
        pic_owner_list.append({'name':photo_name, 'owner':viewing_profile, 'list':'nil', 'permissions':['rw','--','--'], 'comments':[]})
        message = f'{photo_name} has been posted.'
        add_output_entry(AUDIT, message)
        print(message)
        
def list_add(list_name):
    """
    Checks whether proposed list exists. If not, one with the form 
    {'name':list_name, 'members':[]} is added. By default, the list 
    membership is empty.
    Input: name of proposed list (string)
    Output: None. Modifies the audit.txt and list of lists
    """
    current_lists = get_list_names()

    if list_name == 'nil':
        message = f'{list_name} is invalid. nil reserved for no-group association with pictures.'
        add_output_entry(AUDIT, message)
        print(message)
        
    elif viewing_profile != profile_owner:
        message = f'Error: This command can only be executed by the profile owner {profile_owner}.'
        add_output_entry(AUDIT, message)
        print(message)
        
    elif list_name in current_lists:
        message = f'{list_name} is invalid. No duplicate list names.'
        add_output_entry(AUDIT, message)
        print(message)
        
    else:
        list_names_members.append({'name':list_name, 'members':[]})
        message = f'List {list_name} created.'
        add_output_entry(AUDIT, message)
        print(message)
    
def get_list_names():
    # Helper method for getting current list names. Should have used this more.
    current_lists = []
    for item in list_names_members:
        current_lists.append(item['name'])
    return current_lists
    
def chmod(pic_name, new_perms):
    # Modifies permission of a file to the new list of permissions passed in. 
    current_pics = []
    # Gets all available/ posted pics.
    for pic in pic_owner_list:
        current_pics.append(pic['name'])
    # If pic name passed in doesn't exist, throw error.
    if pic_name not in current_pics:
        print((f'Error: {pic_name} doesn\'t exist.'))
        add_output_entry(AUDIT,(f'Error: {pic_name} doesn\'t exist.'))
    else:
        index = current_pics.index(pic_name)
        pic_owner_list[index]['permissions'] = new_perms
        print((f'Changed permissions for {pic_name} to {new_perms}.'))
        add_output_entry(AUDIT,(f'Changed permissions for {pic_name} to {new_perms}.'))

def chown(pic_name, friend_name):
    """
    Changes the owner of the file if the current viewer is the profile owner.
    Pic also needs to exist in pic list to be changed.
    """
    op = get_owner_perms(pic_name)
    # If op is a None type, that means there is no owner/ picture doesn't exist. 
    if op==None:
        
        add_output_entry(AUDIT,(f'Error: {pic_name} doesn\'t exist.'))
       
    else:
        curr_owner = op[1]
        current_pics = []
        for pic in pic_owner_list:
            current_pics.append(pic['name'])
        # Pic doesn't exist. Throw error.
        if pic_name not in current_pics:
            print((f'Error: {pic_name} doesn\'t exist.'))
            add_output_entry(AUDIT,(f'Error: {pic_name} doesn\'t exist.'))
        # Only profile owner has permission to change owner of file.
        elif viewing_profile != profile_owner:
            print((f'Error: {viewing_profile} doesn\'t have permission to change owners.'))
            add_output_entry(AUDIT,(f'Error: {viewing_profile} doesn\'t have permission to change owners.'))
        else:
            index = current_pics.index(pic_name)
            pic_owner_list[index]['owner'] = friend_name
            print((f'Changed ownership of {pic_name} to {friend_name}.'))
            add_output_entry(AUDIT,(f'Changed ownership of {pic_name} to {friend_name}.'))        

def logout():
    # Resets the viewing_profile global variable to empty string to indicate no one is viewing the profile.
    global viewing_profile
    print(f'{viewing_profile} logged out.')
    add_output_entry(AUDIT,(f'{viewing_profile} logged out.'))
    viewing_profile = ""

def get_owner_perms(pic_name):
    """
    Helper method for getting owner name and permissions for a particular profile.
    """
    current_pics = []
    owner_perms = None
    for pic in pic_owner_list:
        if pic['name'] == pic_name:
            current_pics.append(pic['name'])
    
    if pic_name not in current_pics:
        print((f'Error: {pic_name} doesn\'t exist.'))
        #add_output_entry(AUDIT,(f'Error: {pic_name} doesn\'t exist.'))
    else:
        index = current_pics.index(pic_name)
        perms = pic_owner_list[index]['permissions']
        curr_owner = pic_owner_list[index]['owner']
        owner_perms = [curr_owner]
        owner_perms.append(perms)
        return owner_perms
    
def friend_list(friend_name, list_name):
    """ 
    Adds a friend to an existing list as long as they are:
    1. A friend of the profile owner; 2. The list name exists; 3. Their name is not currently in the list.
    Input: The friend's name and the list name as strings
    Output: None
    """
    curr_lists = []
    for l in list_names_members:
        curr_lists.append(l['name'])
    if friend_name not in friends_list or list_name not in curr_lists:
        message = f'Error: {friend_name} is not a friend or {list_name} doesn\'t exist'
        add_output_entry(AUDIT, message)
        print(message)
    elif viewing_profile != profile_owner:
        message = f'Error: {friend_name} is not the profile owner.'
        add_output_entry(AUDIT, message)
        print(message)
    else:
        index = curr_lists.index(list_name)
        list_names_members[index]['members'].append(friend_name) 
        message = f'{friend_name} added to {list_name}.'
        add_output_entry(AUDIT, message)
        print(message)
        
def chlst(pic_name, list_name):
    """
    Changes the list association of the pic name passed in to the new list name, if the person trying to effect this change is
    the file owner, or the profile owner.
    """
    # Reference variables
    curr_lists = []
    l_index = 0
    p_index = 0
    owner_lists = []
    owner = ''
    for l in pic_owner_list:
        if l['name'] == pic_name:
            owner = l['owner']
            break
        else:
            p_index += 1
    # Checks whether list exists or not.    
    for l in list_names_members:
        curr_lists.append(l['name'])
        if list_name not in curr_lists:
            print(f'{list_name} not found')
            break
        else:l_index = curr_lists.index(list_name)
        if owner in l['members']:
            owner_lists.append(l['name'])
    # If no one is viewing the profile, command can't be executed. 
    if viewing_profile == "":
        message = f'Error: No one is viewing the profile.'
        add_output_entry(AUDIT, message)
        print(message)
    # New name can't be nil
    elif list_name == 'nil' or list_name in owner_lists:
        pic_owner_list[p_index]['list'] = list_name
        message = f'Changed list of {pic_name} to {list_name}.'
        add_output_entry(AUDIT, message)
        print(message)
    else:
        message = f'Cannot change list association of {pic_name} to {list_name}.'
        add_output_entry(AUDIT, message)
        print(message)
        
def read_comments(pic_name):
    """
    Definitely made this more complicated than it should be, but here we are.
    Takes in pic name as a string and checks whether that picture exists, who owns it, are they the person viewing the profile/ file owner,
    are they part of a list with access. 
    If no to the above questions, error is thrown; otherwise, comments can be read, provided permission for those cases available.
    """
    # used to store reference attributes and comments
    comments = None
    target_pic = None
    perms = None
    viewer_lists = []
    # Retrieves relevant pic permissions and comments
    for pic in pic_owner_list:
        if pic['name'] == pic_name:
            target_pic = pic
            perms = pic['permissions']
            comments= pic['comments']
            break
    # If current viewer is allowed/ part of list with permission, great!
    for l in list_names_members:
        if viewing_profile in l['members']:
            viewer_lists.append(l['name'])
    if viewer_lists == None:
        print(f'{viewing_profile} is not a member of the lists associated with {pic_name}.')
    else:
        # Different paths for either valid access to comments, or error if none of the top three cases are met.
        # In hindsight, I probably could have combined the middle two elifs into the top if statement. 
        if viewing_profile == target_pic['owner']:
            message = f'{comments} read from {pic_name}.'
            add_output_entry(AUDIT, message)
            print(message)
        elif (viewing_profile in viewer_lists) and perms[1][0] == 'r':
            message = f'{comments} read from {pic_name}.'
            add_output_entry(AUDIT, message)
            print(message)
        elif (viewing_profile not in viewer_lists) and perms[2][0] == 'r':
            message = f'{comments} read from {pic_name}.'
            add_output_entry(AUDIT, message)
            print(message)
        else:
            message = f'Error: comments could not be read from {pic_name}.'
            add_output_entry(AUDIT, message)
            print(f'No access to {viewing_profile}')
            
def write_comments(pic_name, text):
    """
    If the current user has write permission for the picture name passed in, 
    their comments will be appended to the comment list for that photo/ file.
    This method is extremely similar to the read_comments() method in functionality. 
    Get lists current viewer is a member of --> find the target picture and grab permissions --> if current viewer has write access
    their text will be added. Otherwise, display + log error and move on. 
    Input: Pic name (string); text of comment (string)
    Output: None
    """
    
    target_pic = None
    perms = None
    viewer_lists = []
    
    """
    Get lists current viewer is a member of by iterating through list of lists with membership
    """
    for l in list_names_members:
        if viewing_profile in l['members']:
            viewer_lists.append(l['name'])
    # Viewer list would only be None type if the current viewer isn't part of any list, therefore has no access rights to write  comments.
    if viewer_lists == None:
        print(f'{viewing_profile} is not a member of the lists associated with {pic_name}.')
    else:
        # Gets permissions for file, since person is member of list/ file owner with access
        for pic in pic_owner_list:
            if pic['name'] == pic_name:
                target_pic = pic
                perms = pic['permissions']
                break
    
        if viewing_profile == target_pic['owner']:
            pic['comments'].append(text)
            pic_comments(pic_name,text)
            message = f'{text} added to {pic_name}.'
            add_output_entry(AUDIT, message)
            print(message)
           
        elif (viewing_profile in viewer_lists) and perms[1][1] == 'w':   # This and next case handle different options for viewer write access.
            pic['comments'].append(text)
            pic_comments(pic_name,text)
            message = f'{text} added to {pic_name}.'
            add_output_entry(AUDIT, message)
            print(message)
            
        elif (viewing_profile not in viewer_lists) and perms[2][1] == 'w':
            pic['comments'].append(text)
            pic_comments(pic_name,text)
            message = f'{text} added to {pic_name}.'
            add_output_entry(AUDIT, message)
            print(message)
    
        else:
            message = f'Comments could not be added to {pic_name}.'
            add_output_entry(AUDIT, message)
            print(f'No access to {viewing_profile}')

def end():
    """
    Outputs the final lists.txt and pictures.txt in a formatted fashion.
    The audit.txt and friends.txt were enumerated at each execution of respective methods.
    Input: None
    Output: Final lists.txt and pictures.txt
    """
    for i in list_names_members:
        formatted = "List Name: "+ str(i['name']) + "\n" + "List Members: "+str(i['members']) + "\n"
        add_output_entry(LIST,formatted)
    
    
    for i in pic_owner_list:
        formatted = "Pic Name: "+ str(i['name']) + "\n" + "Owner: "+str(i['owner']) + "\n" + 'Permissions: '+ str(i['permissions']) +"\n" +'Comments: '+ str(i['comments'])+ "\n"
        add_output_entry(PIC,formatted)
    print('\nFinal Output Files Available') 
    
def pic_comments(file, text):
    
    with open(file, 'a') as f:
        f.write(text+"\n")


# In[166]:


def main(arg):

    """
    Gets the root of the current operating system for the absolute filepath
    Returns a file object
    """
    
    
    file = get_file(arg)
    
    """
    Each element in f is a list in which each word in the line of 
    text read in is an element. E.g. f = [[friendadd,root], [viewby, root], ...]
    """
    
    f = read_text(file)
    dirs = os.listdir(os.getcwd())
    for file in dirs:
        if file.endswith(".txt"):
            os.remove(file)
    make_files()
    
    
    print('Open Command File')
    pre_check(f)
    add_output_entry(AUDIT, 'Initialized output text files.')
    print('Initialized output text files.')

    for command in f:
        if command[0] == "friendadd":
            friend_add(command[1])
        elif command[0] == "viewby":
            viewby(command[1])
        
        elif command[0] == "listadd":
            list_add(command[1])
        
        elif command[0] == "friendlist":
            friend_list(command[1], command[2])
        
        elif command[0] == "postpicture":
            post_photo(command[1])
        
        elif command[0] == "chlst":
            chlst(command[1],command[2])
        
        elif command[0] == "chmod":
            perms = [command[2],command[3],command[4]]
            chmod(command[1], perms)
        
        elif command[0] == "chown":
            chown(command[1], command[2])
        
        elif command[0] == "readcomments":
            read_comments(command[1])
        
        elif command[0] == "writecomments":
            text = ""
            for i in range(2,len(command)):
                text += command[i]+" "
            write_comments(command[1], text)
        
        elif command[0] == "logout":
            logout()
        
        elif command[0] == "end":
            end()
        
        else:
            print('Invalid Command.')


if __name__=="__main__":
   
    main('TestCase1.txt')



    


# In[154]:


print(list_names_members)

