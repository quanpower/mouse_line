import os, sys
import wmi
import hashlib
import base64
import logging

logger = logging.getLogger(__name__)


def get_str_md5_without_salt_secret_str(res:str):
    # 创建一个md5散列对象
    m = hashlib.md5()
    # 传入二进制数据
    data = res.encode("utf-8")
    m.update(data)
    # 获取加密后的值，digest是二进制，hexdigest则是十六进制
    print(m.digest())  
    print(m.hexdigest())


def get_str_md5_with_salt_secret_str(res:str, salt):
    '''
    虽然哈希是很难破解的，但是现在可能会通过撞库。
    就是先准备大量的数据，然后生成哈希值。然后通过哈希值再反过来推测出原来的值，就是碰运气。
    但是也可能真的中了，因此我们可以进行一个加盐操作。
    '''
    m = hashlib.md5(salt.encode('utf-8'))
    # 就是按照我指定的参数进行加密，这样就基本不可能破解了
    m.update(res.encode("utf-8"))
    return m.hexdigest()  


def get_str_sha1_secret_str(res:str):
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(res.encode('utf-8'))
    encrypts = sha.hexdigest()
    # print(encrypts)
    return encrypts


def get_hardware_info():
     encrypt_str = ""
     c = wmi.WMI ()
     for cpu in c.Win32_Processor():
     #cpu 序列号
          encrypt_str = encrypt_str+cpu.ProcessorId.strip()
          # print("cpu id:", cpu.ProcessorId.strip())
     for physical_disk in c.Win32_DiskDrive():
          encrypt_str = encrypt_str+physical_disk.SerialNumber.strip()
     #硬盘序列号
          # print('disk id:', physical_disk.SerialNumber.strip())
     return encrypt_str 


def generate_license():
    encrypt_str = get_hardware_info()
    # cpu + disk
    print('Your hardware info is: ', encrypt_str)
    license = get_str_md5_with_salt_secret_str(encrypt_str, 'shshuhang_wiiliam_zhang')
    print(license)
    return license


def get_license_from_file():
    with open('license.lic', mode='r', encoding='utf-8') as f:
        # seek()移动光标至指定位置
        f.seek(0)
        # read()读取整个文件，将文件内容放到一个字符串变量中，文件大于可用内存时不适用
        res = f.read()
        print('Your license is: ', res)
        return res
     

if __name__ == "__main__":
    generate_license()