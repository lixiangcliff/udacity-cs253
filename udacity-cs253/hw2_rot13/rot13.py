'''
Created on Jul 24, 2015

@author: clli
'''
import string

def rot13(str):
    res = ""
    for x in str:
        if not x.isalpha():
            res += x
        else:
            if x.isupper() and x <= 'M' or x.islower() and x <= 'm':
                res += (chr(ord(x) + 13))
            else:
                res += (chr(ord(x) - 13))
    return res


#print rot13("AHMN     ahmn?")