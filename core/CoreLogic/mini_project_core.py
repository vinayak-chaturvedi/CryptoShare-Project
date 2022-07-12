import sys
import os
from Crypto.Cipher import AES  # for Crypto module use "pip3 install pycryptodome"
from Crypto import Random
import hashlib
from Crypto.Cipher import DES3
from hashlib import md5
from zipfile import ZipFile
import pyAesCrypt
from unipath import Path
import threading

CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def splitFile(inputFile, chunkSize):

    f = open(inputFile, 'rb')
    data = f.read()
    f.close()

    bytes = len(data)


    if sys.version_info.major == 3:
        noOfChunks = int(bytes / chunkSize)
    elif sys.version_info.major == 2:
        noOfChunks = bytes / chunkSize
    if(bytes % chunkSize):
        noOfChunks += 1

    chunkNames = []
    j = 0
    for i in range(0, bytes + 1, chunkSize):
        j += 1
        fn1 = "%s-chunk-%s" % (inputFile,j)
        chunkNames.append(fn1)
        f = open(fn1, 'wb')
        f.write(data[i:i + chunkSize])
        f.close()

def split(filename):
  stats = os.stat(filename)
  if(stats.st_size>1000):
    chunkSize = stats.st_size // 10
  else:
    chunkSize = 1
  splitFile(filename, chunkSize)


def AESencrypt(key, aes_files):
    for filename in aes_files:
        pyAesCrypt.encryptFile(filename, filename + ".enc", key)

def AESdecrypt(key, filename):
    pyAesCrypt.decryptFile(filename, filename.replace(".enc", ""), key)

def DESEncryption(key, des_files):

    for filename in des_files:

        key_hash = md5(key.encode('ascii')).digest()


        tdes_key = DES3.adjust_key_parity(key_hash)

        cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')


        with open(filename, 'rb') as input_file:
            file_bytes = input_file.read()
            
            new_file_bytes = cipher.encrypt(file_bytes)
        filename = filename+".enc"
        with open(filename, 'wb') as output_file:
            output_file.write(new_file_bytes)
            
def DESDecryption(filename,key):


    key_hash = md5(key.encode('ascii')).digest()


    tdes_key = DES3.adjust_key_parity(key_hash)

    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')


    with open(filename, 'rb') as input_file:
        file_bytes = input_file.read()
        
        new_file_bytes = cipher.decrypt(file_bytes)
    with open(filename.replace(".enc", ""), 'wb') as output_file:
        output_file.write(new_file_bytes)

def joinFiles(origFileName, newFileName, noOfChunks):
    dataList = []
    
    j = 0
    for i in range(0, noOfChunks, 1):
        j += 1
        chunkName = "%s-chunk-%s" % (origFileName, j)
        f = open(chunkName, 'rb')
        dataList.append(f.read())
        f.close()

    j = 0
    for i in range(0, noOfChunks, 1):
        j += 1
        chunkName = "%s-chunk-%s" % (origFileName, j)
        os.remove(chunkName)

    f2 = open(newFileName, 'wb')
    for data in dataList:
        f2.write(data)
    f2.close()



def encryptor(fileDirectory, password):
  directory, OnlyFileName = fileDirectory.split('/')
  dir_name = os.path.join(CORE_DIR, 'uploadedfiles/{}'.format(directory))
  filename = os.path.join(CORE_DIR, 'uploadedfiles/{}'.format(fileDirectory))
  relativePath = "../uploadedfiles/"+directory+'/'
  split(filename)
  allfiles = os.listdir(dir_name)
  totalchunk=0
  aes_files = []
  des_files = []
  for item in allfiles:
    if OnlyFileName in item and "chunk" in item :
        
        if int(str(item)[-1])%2==1:
            aes_files.append(dir_name+"/"+item)
        else:
            des_files.append(dir_name+"/"+item)
        
        totalchunk+=1

  t1 = threading.Thread(target=AESencrypt, args=(password, aes_files,))
  t2 = threading.Thread(target=DESEncryption, args=(password, des_files,))
  t1.start()
  t2.start()
  t1.join()
  t2.join()


  for item in allfiles:
    if OnlyFileName in item and "chunk" in item:
        if(item.endswith(".enc")):
            continue
        else:
            os.remove(os.path.join(dir_name, item))

  os.remove(os.path.join(dir_name, filename))
  print("Encryption Done.")
  removeChunks(OnlyFileName, dir_name)
  
def removeChunks(filename, dir_name):
    allfiles = os.listdir(dir_name)
    totalchunk=0
    for item in allfiles:
        if filename in item and "chunk" in item and ".enc" not in item :
            os.remove(os.path.join(dir_name, item))
    
def Decryptor(fileDirectory, password):
  directory, OnlyFileName = fileDirectory.split('/')
  dir_name = os.path.join(CORE_DIR, 'uploadedfiles/{}'.format(directory))
  filenameWithDir = os.path.join(CORE_DIR, 'uploadedfiles/{}'.format(fileDirectory))
  filename = OnlyFileName
  allfiles = os.listdir(dir_name)
  totalchunk=0
  for item in allfiles:
    if filename in item and "chunk" in item :
        if int(str(item)[-5])%2==1:
            AESdecrypt(password,dir_name+"/"+item)
        else:
            DESDecryption(dir_name+"/"+item,password)
        totalchunk+=1
  joinFiles(filenameWithDir,filenameWithDir,totalchunk)
  print("Decryption Done.")
  
