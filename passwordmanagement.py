from hashlib import pbkdf2_hmac

def hash(password,salt,iters=2048):
	return pbkdf2_hmac(hash_name='sha512',password=password,salt=salt,iterations=iters)

def save_hash(hash):
    with open("pw.bin","wb") as file:
        file.write(hash)
def load_hash():
    with open("pw.bin", "rb") as file:
        return file.read()
