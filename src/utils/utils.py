import sys, os

# helper function to check if s is an int
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__