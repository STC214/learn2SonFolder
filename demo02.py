import re

def floder_name_check(root):
    # patn = re.compile(r'(\d+)(__)(\d+)')
    patn = r'\d+\_\_\d+'
    ml = re.findall(patn,root)
    print(ml)
    if ml != None and len(ml) ==1:
        cl = True
    else:
        cl = False
    
    return cl



root = r'H:\learn_video\2019年8月6日\Python全系列教程全栈工程师\002__002'

dl = floder_name_check(root)

print(dl)