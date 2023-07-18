	
from hashlib import md5
def calculate_rpc_index(name, salt):
		m = md5()
		m.update(name + salt)
		b = m.digest()
		return ((ord(b[-4]) & 0x7F) << 24) + (ord(b[-3]) << 16) + (ord(b[-2]) << 8) + ord(b[-1])
		# return ((ord(b[-2]) & 0x7F) << 8) + ord(b[-1])
x = calculate_rpc_index("set_send_rpc_salt","0")
print x 