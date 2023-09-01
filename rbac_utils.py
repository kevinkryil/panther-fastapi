from utils import *

def has_access(user, permission):
    for group in user.groups:
        for permission in group.permissions:
            if permission == permission:
                return True
    return False
        