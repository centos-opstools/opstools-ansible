from cStringIO import StringIO
from parser import HashCommentParser
import argparse
import os
import sys
import textwrap
import yaml
import json

def generate_docs(roles, output=sys.stdout):
    for dirpath, dirnames, filenames in os.walk(roles):
        for keydir in ['meta', 'tasks', 'defaults']:
            if keydir in dirnames:
                break
        else:
            continue

        README = os.path.join(dirpath, 'README.md')
        DEFAULTS = os.path.join(dirpath, 'defaults', 'main.yml')

        if os.path.isfile(README):
            with open(README, 'r') as fd:
                output.write(fd.read())

        if os.path.isfile(DEFAULTS):
            output.write('\n')
            output.write('### Configuration')
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
    return p.parse_args()

def main():
    args = parse_args()

    with sys.stdout if args.output == '-' else open(args.output, 'w') as fd:
        generate_docs(args.roles, output=fd)

if __name__ == '__main__':
    sys.exit(main())
