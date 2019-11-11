from hashlib import sha1
from random import getrandbits

s = sha1()
s.update(b"1234")
data = s.digest()
s = sha1()
s.update(data)
print(s.hexdigest())
