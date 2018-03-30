#!/usr/bin/env python
# coding=utf-8

import xml.etree.ElementTree as ET
#help(ET)

tree = ET.parse('test.xml')
root = tree.getroot()
print root
print tree
print "root.tag:", root.tag
print "root.attr:", root.attrib

#遍历子节点

def tranv(node, backcount):
    a = ' ' * backcount
    for child in node:
        print a, child.tag, child.attrib, child.text
        tranv(child, backcount + 1)

print "遍历:"
tranv(root, 0)
