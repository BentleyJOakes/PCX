#!/usr/bin/env python

#===- cindex-dump.py - cindex/Python Source Dump -------------*- python -*--===#
#
#                     The LLVM Compiler Infrastructure
#
# This file is distributed under the University of Illinois Open Source
# License. See LICENSE.TXT for details.
#
#===------------------------------------------------------------------------===#
from clang.cindex import *
from pprint import pprint
from to_xml import *

#make new token class to handle equality
from ASTToken import *

import re


"""
A simple command line tool for dumping a source file using the Clang Index
Library.
"""


def get_diag_info(diag):
    return { 'severity' : diag.severity,
             'location' : diag.location,
             'spelling' : diag.spelling,
             'ranges' : diag.ranges,
             'fixits' : diag.fixits }

def get_cursor_id(cursor, cursor_list = []):
    if not opts.showIDs:
        return None

    if cursor is None:
        return None

    # FIXME: This is really slow. It would be nice if the index API exposed
    # something that let us hash cursors.
    for i,c in enumerate(cursor_list):
        if cursor == c:
            return i
    cursor_list.append(cursor)
    return len(cursor_list) - 1   
    
def get_tokens(node):
    tokens = []
    for t in node.get_tokens():
        token = ASTToken(t)
        tokens.append(token)
    return tokens
    
def get_location(node):
    loc = str(node.location)
    loc = re.sub('["\'>,]', '', loc)
    loc_array = loc.split(' ')
    if loc_array[2] == 'None':
        return None
    return loc_array[2] + ":" + loc_array[4] + "," + loc_array[6] 

def get_info(node, depth=0):
    if opts.maxDepth is not None and depth >= opts.maxDepth:
        children = None
    else:
        children = [get_info(c, depth+1)
                    for c in node.get_children()]
                     
    return { #'id' : get_cursor_id(node),
             'kind' : node.kind,
             #'usr' : node.get_usr(),
             'spelling' : node.spelling,
             'location' : get_location(node),
             #'extent.start' : node.extent.start,
             #'extent.end' : node.extent.end,
             #'is_definition' : node.is_definition(),
             #'definition_id' : get_cursor_id(node.get_definition()),
             'children' : children,
             'tokens' : get_tokens(node) }

def main():
    from clang.cindex import Index
    from pprint import pprint

    from optparse import OptionParser, OptionGroup

    global opts

    parser = OptionParser("usage: %prog [options] {filename} [clang-args*]")
    parser.add_option("", "--show-ids", dest="showIDs",
                      help="Compute cursor IDs (very slow)",
                      action="store_true", default=False)
    parser.add_option("", "--max-depth", dest="maxDepth",
                      help="Limit cursor expansion to depth N",
                      metavar="N", type=int, default=None)
    parser.disable_interspersed_args()
    (opts, args) = parser.parse_args()

    if len(args) == 0:
        parser.error('invalid number arguments')

    #tu = TranslationUnit.from 
    index = Index.create()
    tu = index.parse(None, args)
    if not tu:
        parser.error("unable to load input")

    #print("Starting to get info")


    #pprint(('diags', map(get_diag_info, tu.diagnostics)))
    program = get_info(tu.cursor)
    write_xml(program, args[0])

if __name__ == '__main__':
    main()

