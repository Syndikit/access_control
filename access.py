
# coding: utf-8

# In[6]:


"""
Purpose: implement a simplified access control platform. 
"""

import os
import sys

#cwd = os.getcwd()

#print(cwd)


# In[8]:


def get_file(filename):
    for root, dirs, files in os.walk('c:\\users\\michael'):
        for name in files:
            if name == filename:
                print(os.path.abspath(os.path.join(root, name)))
    
    #print(os.path.abspath(filename))
    
def main(arg):
    get_file(arg)
    
main(sys.argv[1])
    

