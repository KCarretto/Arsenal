"""
Quick script to generate markdown documentation based on API call docstrings.
"""
import sys
from os.path import abspath, dirname

sys.path.insert(0, abspath(dirname(abspath(dirname(__file__)))))
import teamserver.api as api # pylint: disable-all

def main():
    """
    Generate documentation.
    """
    methods = list(filter(lambda x: not x.startswith('_'), dir(api)))
    for call in methods:
        if call in ['webhook', 'log', 'action', 'target', 'group', 'group_action', 'auth', 'session', 'agent']:
            continue

        obj = getattr(api, call)
        call = ''.join([word.capitalize() for word in call.replace('_', ' ').split()])

        print('## {}'.format(call))
        print(obj.__doc__)
        print('\n\n')

if __name__ == '__main__':
    main()
