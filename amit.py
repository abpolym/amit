import hashlib, re, ssdeep, sqlite3, subprocess, sys, os, zipfile

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

def db_init(dbconn, dbconfig):
	if db_table_exists(dbconn, 'samples'): return
	print '[db_init] Creating database from config', dbconfig,
	dbcursor = dbconn.cursor()
	dbqry = open(dbconfig, 'r').read()
	dbcursor.executescript(dbqry)
	dbcursor.close()
	print '[db_init] Created database.'

def db_table_exists(dbconn, tablename):
	dbqry='SELECT name FROM sqlite_master WHERE type="table" AND name=?;'
	#if db_execute(dbconn, dbqry) is None: return False
	dbcursor = dbconn.cursor()
	dbcursor.execute(dbqry, (tablename,))
	result = True
	if dbcursor.fetchone() is None: result = False
	dbcursor.close()
	return result

def db_insert_sdk_dates(dbconn, sdkconfig):
	sdklines = []
	with open(sdkconfig, 'r') as f:
		sdklines = f.readlines()
	dbcursor = dbconn.cursor()
	dbcursor.execute('SELECT * FROM sdk_release_dates;')
	result = dbcursor.fetchall()
	dbcursor.close()
	if len(result)>=len(sdklines): return
	print '[db_insert_sdk_dates] Inserting sdk release dates into database'
	for idx in range(len(result),len(sdklines)):
		line = sdklines[idx].replace('\n','')
		sdkversion, sdkreleasedate = line.split(' ')
		dbqry='INSERT INTO sdk_release_dates VALUES (?, strftime("%s", ?));'
		dbcursor = dbconn.cursor()
		dbcursor.execute(dbqry, (int(sdkversion), sdkreleasedate))
		result = dbcursor.fetchall()
		dbcursor.close()
	dbconn.commit()
	print '[db_insert_sdk_dates] Inserted sdk release dates.'

def get_package_name(apkpath):
	# TODO Check for command injection - just in case :)
	global sdktoolspath
	#Extract the AndroidManifest.xml permissions:
	command = sdktoolspath+"aapt dump badging " + apkpath + " | grep -E 'package:(?:.*) name'"
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	output = process.communicate()[0].replace('\n','')
	result = re.findall(r"name='([^']*)'", output)
	if len(result)<1: return None
	return result[0]

def get_cert_fingerprint(apkpath):
	zf = zipfile.ZipFile(apkpath)
	certnames = []
	for f in zf.namelist():
		result = re.findall(r'META-INF/.*\.[DR]{1}SA', f)
		if len(result) < 1: continue
		certnames.append(result[0])
	print 'NAMES:',certnames
	if len(certnames)>1:
		print 'ERROR: Not implemented to store more than one fingerprint for list:',certnames
		return None
	try:
		data = zf.read(certnames[0])
	except KeyError:
		print 'ERROR: Did not find {} in zip file'.format(certnames[0])
		return None
	with open('/tmp/amirtmp', 'wb') as f:
		f.write(data)
	# MD5, SHA1, SHA256
	fingerprint = [None, None, None]
	command = "keytool -file /tmp/amirtmp -printcert"
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	output = process.communicate()[0]
	result = re.findall(r"\t MD5: (.*)", output)
	if len(result)<1: return None
	fingerprint[0]=result[0]
	result = re.findall(r"\t SHA1: (.*)", output)
	if len(result)<1: return None
	fingerprint[1]=result[0]
	result = re.findall(r"\t SHA256: (.*)", output)
	if len(result)<1: return None
	fingerprint[2]=result[0]
	for idx in range(len(fingerprint)):
		fingerprint[idx]=re.sub('[:\ ]','',fingerprint[idx])
	return fingerprint
	
# TODO: Include argparse
if len(sys.argv)!=2: sys.exit(1)

sdktoolspath = sys.argv[1]
databasedir = 'database/'
database=databasedir+'/amit.db'
databaseconfig = databasedir+'/amit-db.sql'
sdkconfig = databasedir+'/sdks.list'

if not os.path.exists(databasedir):
	os.makedirs(databasedir)

dbconn = sqlite3.connect(database)
db_init(dbconn, databaseconfig)
db_insert_sdk_dates(dbconn, sdkconfig)
dbconn.close()

#print get_package_name('data/898d0bc43c4a5b21797ac844dc05df4d80960b21a7ae5d72d9611043a47f7d61.apk')
print get_cert_fingerprint('data/898d0bc43c4a5b21797ac844dc05df4d80960b21a7ae5d72d9611043a47f7d61.apk')
