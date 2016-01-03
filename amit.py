import hashlib, ssdeep

def hash_ssdeep(inbytes):
	return ssdeep.hash(inbytes)

def hash_md5(inbytes):
	m = hashlib.md5()
	m.update(inbytes)
	return m.hexdigest()

def hash_sha1(inbytes):
	m = hashlib.sha1()
	m.update(inbytes)
	return m.hexdigest()

def hash_sha256(inbytes):
	m = hashlib.sha256()
	m.update(inbytes)
	return m.hexdigest()

def hash_print_all(inbytes):
	print hash_ssdeep(inbytes)
	print hash_md5(inbytes)
	print hash_sha1(inbytes)
	print hash_sha256(inbytes)

testdata = '\x90'*512*2
testdata2 = 'mod\x90'*512*2
hash_print_all(testdata)
hash_print_all(testdata2)
