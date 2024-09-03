from operator import truediv

from flask import Flask,session
def checkSession()->bool:
    if 'username' in session:
        return True
    else:
        return False