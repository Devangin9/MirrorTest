'''
Created on 25-Jun-2013

@author: Devangini
'''
def Constant(f):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)

