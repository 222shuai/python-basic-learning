'''#加密
import binascii
import random

chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@#$%^&*()_+-*/<>,.[]'

def en(data):
  hex_data = binascii.b2a_hex(data.encode()).decode()
  data_index = 0
  ascii_data = ''
  while data_index < len(hex_data):
    for i in hex_data[data_index]:
      ascii_data += str(ord(i)) + random.choice(chars[10:])
      data_index += 1
  return ascii_data[::-1]

data = input('请输入明文:')
print('密文如下:{}'.format(en(data)))
'''

'''#解密
import binascii
from re import sub

def de(data):
  data_split = sub(r'\D', ' ', data[::-1])
  ascii_list = data_split.split()
  asciis = [int(i) for i in ascii_list]
  data = ''
  for x in asciis:
    data += chr(x)
  print(data)
  data = binascii.a2b_hex(data).decode()
  return data

data = input('请输入密文:')
print('明文如下:{}'.format(de(data)))
'''