# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

import os

def init():
    fp = (r"/Volumes/Seagate Backup Plus Drive/20220616_liposomes")
    print_dirs(2, fp)

def print_dirs(step, fp):
    print('\n\n')
    count = 0
    done = []
    for root, dirs, files in os.walk(fp):
        for name in files:
           # if count<135:  
            if step == 1:
                # if 'SR' in name:
                    if 'FitResults' in name:
                        for_ij = r'path[{0}]="{1}\";'.format(count, root)
                        if root not in done:
                            done.append(root)
                            print(for_ij.replace('\\', '/'))
                            count += 1
            elif step == 2:
                # if '.dl' in name:
                    if 'R1W2' in name:
                        # if count<500:
                            for_py = 'pathList.append(r"{0}")'.format(root)
                            print(for_py)
                            # print(count)
                        # count+=1
            elif step == 3:

                if 'GDSCSMLM_SR_width_python.tif' in name:
                    for_igor = r'filelist[{0}]="{1}\"'.format(count, root)
                    for_igor = for_igor.replace('/',':')
                    for_igor = for_igor.replace(':Users','Macintosh HD:Users')
                    print(for_igor.replace('\\', ':'))
                    
                    count += 1
            elif step == 4:
                if 'ThT_02' in name:
                    for_py = 'pathlist.append(r"{0}/")'.format(root)
                    print(for_py)
                    #print name
init()