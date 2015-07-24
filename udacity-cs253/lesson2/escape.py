'''
Created on Jul 24, 2015

@author: clli
'''

import string
def escape_html(s):
    #if string.find(s, '&') > -1:
    s = s.replace('&', '&amp;')
    #if string.find(s, '>') > -1:
    s = s.replace('>', '&gt;')
    #if string.find(s, '<') > -1:
    s = s.replace('<', '&lt;')
    #if string.find(s, '"') > -1:
    s = s.replace('"', '&quot;')
    return s