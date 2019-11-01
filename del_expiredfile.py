
import os
import sys
import traceback
import logging
import time
import shutil

condition = "365"
dircondition = "300"
src_dir = "/home/data/record/src"
#dest_dir = "/home/data/record/dest" + (condition)
command_dir = "/home/data/record"

expiredtime = time.time() - (int(condition) * 24 * 60 * 60)
dir_expiredtime = time.time() - (int(dircondition) * 24 * 60 * 60)

def log_config():
	global log_normal, log_error
	curtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
	
	log_normal = logging.getLogger("del_expiredfile_normal")
	log_normal.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
	file_handler = logging.FileHandler(command_dir + "/del_expiredfile_" + curtime + ".log")
	file_handler.setFormatter(formatter)
	log_normal.addHandler(file_handler)
	#stream_handler = logging.StreamHandler(sys.stdout)
	#log_normal.addHandler(stream_handler)
	log_normal.info("log_normal config OK")

	log_error = logging.getLogger("del_expiredfile_error")
	log_error.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(message)s")
	file_handler = logging.FileHandler(command_dir + "/del_expiredfile_error_" + curtime + ".log")
	file_handler.setFormatter(formatter)
	log_error.addHandler(file_handler)
	log_normal.info("log_error config OK")
	
def print_params():
	log_normal.info("###################################################################")
	log_normal.info("COMMOND: %s" % sys.argv[0])
	for i in range(1, len(sys.argv)):
		log_normal.info("PARAM %d %s" %(i, sys.argv[i]))
	
	log_normal.info("###################################################################")

def del_null_dir(dirname):
	log_normal.info("del_null_dir(%s)" % dirname)

	if not os.path.exists(dirname):
		return

	if not os.path.isdir(dirname):
		return
	
	try:
		statinfo = os.stat(dirname)
		if (dir_expiredtime > statinfo.st_mtime) and (not os.listdir(dirname)):
			os.rmdir(dirname)
			log_normal.info("delete dir success")

	except Exception, e:
		log_normal.error("something wrong(%s)" % str(e))
		log_error.info(dirname)		
	
	return 

def del_file(filename):
	log_normal.info("del_file(%s)" % filename)
	if not os.path.exists(filename):
		return

	if not os.path.isfile(filename):
		del_null_dir(filename)
		return

	if not filename.startswith(src_dir):
		return
	
	if not filename.endswith(".mp3"):
		return

	#get file modify time, match condition
	try:
		statinfo = os.stat(filename)
		if expiredtime > statinfo.st_mtime:
			os.remove(filename)
			log_normal.info("delete file success")

	except Exception, e:
		log_normal.error("something wrong(%s)" % str(e))
		log_error.info(filename)		


def del_expire_record():
	log_normal.info("###################################################################")
	log_normal.info("del_expire_record(%s) start" % condition)
	
	for root, dirs, files in os.walk(src_dir):
		for file in files:
			del_file(root + "/" + file)

		for dir in dirs:
			del_null_dir(root + "/" + dir)

	log_normal.info("del_expire_record(%s) end" % condition)
	log_normal.info("###################################################################")

def parse_param1(errorfile):
	log_normal.info("###################################################################")
	log_normal.info("parse_param1(%s) start" % condition)
	if os.path.exists(errorfile):
		filehandler = open(errorfile)
		for filename in filehandler.readlines():
			del_file(filename.strip("\n"))

		filehandler.close()
	else:
		log_normal.error("errorfile(%s) is not exists" % errorfile)

	log_normal.info("parse_param1(%s) end" % condition)
	log_normal.info("###################################################################")

def parse_params():
	if 1 == int(len(sys.argv)):
		log_normal.info("param1 is NULL")
		del_expire_record()
	else:
		param1 = sys.argv[1] 
		log_normal.info("param1 is not NULL")
		parse_param1(param1)

if __name__ == "__main__":
	log_config()

	print_params()

	parse_params()
	
	log_normal.info("del_expiredfile.py end###################################")


