import sys
def get_os():
    if sys.platform.lower().startswith('win'):
        return 'win'
    else:
        return 'linux'
