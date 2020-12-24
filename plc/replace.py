import os
import shutil
 
filePath = 'D:\\mouse\\laser\\tongjian.jpg'
# aimPath = '\\\\192.168.0.100\\plt\\test.jpg'
aimPath = '\\\\SKY-20200924VIS\\plt\\tongjian.jpg'
 
def comp_del(com_filename,orgpath):   
    n = 0
    for fpath,fdir,ffile in os.walk(aimPath):
        while n < len(ffile):
            if com_filename == ffile[n]:
                (aimPath + '\\' + ffile[n])
                print('update_file--------' + orgpath + '\\' + ffile[n] + '\n')
            n = n + 1
     
def mov_file(ndfile,edfile,fpos):
    shutil.move(ndfile + '\\' + fpos,edfile)

 
# for i,j,k in os.walk(filePath):
#     if "appcom" in i:
#         filedir = eval(repr(i).replace('\\', '\\\\'))
#         pos = 0
#         while pos < len(k):
#             comp_del(k[pos],filedir)
#             mov_file(filedir,aimPath,k[pos])
#             pos = pos + 1

if __name__ == "__main__":
    shutil.copyfile( filePath, aimPath)            