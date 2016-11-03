
import argparse
import sys
import os
import yaml
import json

from cStringIO import StringIO
from parser import HashCommentParser

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.playbook import Playbook
from ansible.playbook.role import Role


parser = argparse.ArgumentParser(
    description='Creates the documentation of a playbook and its roles')

parser.add_argument('-f','--file',dest='playbook_path',
                    help='The playbook file path',required=True)

parser.add_argument('-t','--title',dest='title',
                    help='The title of the documentation',required=False,
                    default='Documentation')

options = parser.parse_args()

if options.playbook_path and (not os.path.isfile(options.playbook_path)):
    print "The playbook can not be read"
    sys.exit(1)

vmanager = VariableManager()
dloader = DataLoader()

pb=Playbook.load(options.playbook_path,variable_manager=vmanager,loader=dloader)

print options.title
print "="*len(options.title)
print 
for play in pb.get_plays():
    print "#",play
    #print "   Roles to be applied:"
    print "\nThis will be applied on",
    for host in play.hosts:
        print host.encode('utf-8'),
    print


    for role in play.get_roles():
        print 

        PATH= role.get_loader().get_basedir()+"/roles/"+role.get_name()
        README=PATH+"/README.md"
        DEFAULTS = os.path.join(PATH, 'defaults', 'main.yml')

        if os.path.isfile(README):
            with open(README, 'r') as fd:
                print(fd.read())

        if (len(role.get_task_blocks())>0):
            print "\n### Actions"
            for bl in role.get_task_blocks():
                for b in bl.block:
                    print "      * ",b.name
            print


        if os.path.isfile(DEFAULTS):
            print('\n')
            print('### Configuration')
            print('\n\n')

            with open(DEFAULTS) as fd:
                parser = HashCommentParser(fd)
                for codeblock, doc in parser:
                    codebuf = StringIO('\n'.join(codeblock))
                    code = yaml.load(codebuf)

                    if not isinstance(code, dict):
                        continue

                    varname, varval = code.items()[0]

                    print('- `{}` (default: `{}`)'.format(
                        varname, json.dumps(varval)))
                    print('\n\n')

                    # This prints out the lines of the doc chunk indented
                    # by four spaces.  This should allow us to format
                    # multi-paragraph documentation chunks correctly.
                    print('\n'.join('    %s' % line.rstrip()
                                           for line in doc))
                    print('\n\n')

        print('\n')


        if role.get_task_blocks()==[]:
            for dep in role.get_all_dependencies():
                for blck in dep.get_task_blocks():
                    for task in blck.block:
                        print "     ",task.get_name()
        '''
        else:
            print "      Dependencies:"
            for dep in rol.get_all_dependencies():
                print "           ",dep.get_name()
        '''

sys.exit(0)
