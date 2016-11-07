
import argparse
import sys
import os
#import yaml
#import json

#from cStringIO import StringIO
#from parser import HashCommentParser

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
    print     
    print ".Roles:"
    print "----"
    for role in play.get_roles():
        print role.get_name()
    print "----"

    for role in play.get_roles():
        print 
        print "##",role
        PATH= role.get_loader().get_basedir()+"/roles/"+role.get_name()

        if (len(role.get_task_blocks())>0):
            if len(role.get_all_dependencies())>0:
                print ".Dependencies:"
                print "----"
                done=[]
                for dep in role.get_all_dependencies():
                    if not dep.get_name() in done:
                        print dep.get_name()
                        done.append(dep.get_name())
                print '----'

            print "\n.Actions"
            print "----"
            for bl in role.get_task_blocks():
                for b in bl.block:
                    print "      * ",b.name
            print "----"

        if role.get_task_blocks()==[]:
            for dep in role.get_all_dependencies():
                for blck in dep.get_task_blocks():
                    for task in blck.block:
                        print "     ",task.get_name()
sys.exit(0)
