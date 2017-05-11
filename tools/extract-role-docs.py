from cStringIO import StringIO
from parser import HashCommentParser

import argparse
import json
import os
import sys
import yaml


def generate_docs(roles, playbook, output=sys.stdout):
    for dirpath, dirnames, filenames in os.walk(roles):
        for keydir in ['meta', 'tasks', 'defaults']:
            if keydir in dirnames:
                break
        else:
            continue

        README = os.path.join(dirpath, 'README.rst')
        DEFAULTS = os.path.join(dirpath, 'defaults', 'main.yml')
        TASKS = os.path.join(dirpath, 'tasks', 'main.yml')

        if os.path.isfile(README):
            with open(README, 'r') as fd:
                output.write('\n')
                output.write(fd.read())

        if os.path.isfile(TASKS):
            output.write('\n')
            output.write('Actions defined on the role')
            output.write('\n')
            output.write('+++++++++++++++++++++++++++')
            output.write('\n\n')

            with open(TASKS, 'r') as fd:
                data = yaml.load(fd)

            for task in data:
                if 'name' in task.keys():
                    output.write('- ')
                    output.write(task['name'])
                    output.write('\n')
                if 'include' in task.keys():
                    FILE = os.path.join(dirpath, 'tasks', task['include'])
                    with open(FILE, 'r') as fd:
                        included_data = yaml.load(fd)
                    output.write('\n> ')
                    output.write(task['include'])
                    output.write('\n\n')
                    for inc_task in included_data:
                        if 'name' in inc_task.keys():
                            output.write('- ')
                            output.write(inc_task['name'])
                            output.write('\n')

            output.write('\n')

        if os.path.isfile(DEFAULTS):
            output.write('\n')
            output.write('Configuration')
            output.write('\n')
            output.write('+++++++++++++')
            output.write('\n\n')

            with open(DEFAULTS) as fd:
                parser = HashCommentParser(fd)
                for codeblock, doc in parser:
                    codebuf = StringIO('\n'.join(codeblock))
                    code = yaml.load(codebuf)

                    if not isinstance(code, dict):
                        continue

                    varname, varval = code.items()[0]

                    output.write('- `{}` (default: `{}`)'.format(
                        varname, json.dumps(varval)))
                    output.write('\n\n')

                    # This prints out the lines of the doc chunk indented
                    # by four spaces.  This should allow us to format
                    # multi-paragraph documentation chunks correctly.
                    output.write('\n'.join('    %s' % line.rstrip()
                                           for line in doc))
                    output.write('\n\n')

        output.write('\n')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--roles', '-r', default='roles')
    p.add_argument('--output', '-o', default='-')
    p.add_argument('--playbook', '-p', default='playbook.yml')
    return p.parse_args()


def validate_args(args):
    if args.playbook and (not os.path.isfile(args.playbook)):
        print("The playbook can not be read")
        sys.exit(1)


def main():
    args = parse_args()

    validate_args(args)

    pb = []
    with sys.stdout if args.output == '-' else open(args.output, 'w') as fd:
        generate_docs(args.roles, pb, output=fd)


if __name__ == '__main__':
    sys.exit(main())
