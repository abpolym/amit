import hashlib, ssdeep, sqlite3, os

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

def hash_all(inbytes):
	a = []
	a.append(hash_ssdeep(inbytes))
	a.append(hash_md5(inbytes))
	a.append(hash_sha1(inbytes))
	a.append(hash_sha256(inbytes))
	return a

def compare_ssdeep(hash1, hash2):
	return ssdeep.compare(hash1, hash2)

def compare_md5(hash1, hash2):
	return hash1 == hash2

def compare_sha1(hash2, hash1):
	return hash1 == hash2

def compare_sha256(hash1, hash2):
	return hash1 == hash2

def compare_all(hasharray1, hasharray2):
	if len(hasharray1)!=len(hasharray2): return None
	a = []
	a.append(compare_ssdeep(hasharray1[0], hasharray2[0]))
	a.append(compare_md5(hasharray1[1], hasharray2[1]))
	a.append(compare_sha1(hasharray1[2], hasharray2[2]))
	a.append(compare_sha256(hasharray1[3], hasharray2[3]))
	return a

def hashes_test():
	testdata = '\x90'*512*2
	testdata2 = 'mod'+'\x90'*512*2
	a1 = hash_all(testdata)
	a2 = hash_all(testdata2)
	for i in a1: print i
	for i in a2: print i
	print compare_all(a1, a2)

def db_execute(dbconn, dbquery):
	print '[db_execute] Executing query: [',dbquery,']'
	dbcursor = dbconn.cursor()
	dbcursor.execute(dbquery)
	result = dbcursor.fetchone()
	dbcursor.close()
	return result

def db_init(dbconn, dbconfig):
	if db_table_exists(dbconn, 'samples'): return
	print '[db_init] Creating database from config', dbconfig
	dbcursor = dbconn.cursor()
	dbqry = open(dbconfig, 'r').read()
	dbcursor.executescript(dbqry)
	dbcursor.close()
	print '[db_init] Created database'

def db_table_exists(dbconn, tablename):
	dbqry='SELECT name FROM sqlite_master WHERE type="table" AND name="{}";'.format(tablename)
	if db_execute(dbconn, dbqry) is None: return False
	return True

databasedir = 'database/'
database=databasedir+'/amit.db'
databaseconfig = databasedir+'/amit-db.sql'

if not os.path.exists(databasedir):
	os.makedirs(databasedir)

dbconn = sqlite3.connect(database)
db_init(dbconn, databaseconfig)
dbconn.close()
