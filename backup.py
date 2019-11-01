
import os
import sys
import traceback
import logging
import time
import shutil

condition = "201907"

src_dir = "/home/data/record/src"
dest_dir = "/home/data/record/dest" + (condition)
command_dir = "/home/data/record"


def log_config():
	global log_normal, log_error
	curtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
	
	log_normal = logging.getLogger("backup_normal")
	log_normal.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
	file_handler = logging.FileHandler(command_dir + "/backup_" + curtime + ".log")
	file_handler.setFormatter(formatter)
	log_normal.addHandler(file_handler)
	#stream_handler = logging.StreamHandler(sys.stdout)
	#log_normal.addHandler(stream_handler)
	log_normal.info("log_normal config OK")

	log_error = logging.getLogger("backup_error")
	log_error.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(message)s")
	file_handler = logging.FileHandler(command_dir + "/backup_error_" + curtime + ".log")
	file_handler.setFormatter(formatter)
	log_error.addHandler(file_handler)
	log_normal.info("log_error config OK")
	
def print_params():
	log_normal.info("###################################################################")
	log_normal.info("COMMOND: %s" % sys.argv[0])
	for i in range(1, len(sys.argv)):
		log_normal.info("PARAM %d %s" %(i, sys.argv[i]))
	
	log_normal.info("###################################################################")

def copy_to_dest(dir_first, dir_second, dir_third):
	src_dir_third_all = src_dir + "/" + dir_first + "/" + dir_second + "/" + dir_third
	dest_dir_third_all = dest_dir + "/" + dir_first + "/" + dir_second + "/" + dir_third
	if os.path.exists(dest_dir_third_all):
		log_normal.info("dest_dir_third_all is already exists: %s" % dest_dir_third_all)
		return

	try:
		shutil.copytree(src_dir_third_all, dest_dir_third_all)
	except Exception, e:
		log_normal.error("something wrong(%s)" % str(e))
		log_error.info(src_dir_third_all)
	else:
		log_normal.info("backup success")

def backup_record_third(src_dir_first, src_dir_second):
	src_dir_second_all = src_dir + "/" + src_dir_first + "/" + src_dir_second
	if not os.path.isdir(src_dir_second_all):
		return

	log_normal.info("start scan dir: %s" % src_dir_second_all)
	try:
		for src_dir_third in os.listdir(src_dir_second_all):
			src_dir_third_all = src_dir_second_all + "/" + src_dir_third
			if not os.path.isdir(src_dir_third_all):
				continue

			if condition in src_dir_third:
				log_normal.info("find a dir need backup: %s" % src_dir_third_all)
				copy_to_dest(src_dir_first, src_dir_second, src_dir_third)

	except Exception, e:
		log_normal.error("something wrong(%s)" % str(e))
		log_error.info(src_dir_second_all)

	log_normal.info("end scan dir: %s" % src_dir_second_all)

def backup_record_second(src_dir_first):
	if "as_backup" == src_dir_first or "as_backup_compress" == src_dir_first or "as_error" == src_dir_first or "e9_ai" == src_dir_first or "error" == src_dir_first:
		return

	src_dir_first_all = src_dir + "/" + src_dir_first
	if not os.path.isdir(src_dir_first_all):
		return

	log_normal.info("start scan dir: %s" % src_dir_first_all)
	try:
		for src_dir_second in os.listdir(src_dir_first_all):
			backup_record_third(src_dir_first, src_dir_second)
	except Exception, e:
		log_normal.error("something wrong(%s)" % str(e))
		log_error.info(src_dir_first_all)

	log_normal.info("end scan dir: %s" % src_dir_first_all)

def backup_record():
	log_normal.info("###################################################################")
	log_normal.info("backup_record(%s) start" % condition)
	
	log_normal.info("start scan dir: %s" % src_dir)
	for src_dir_first in os.listdir(src_dir):
		backup_record_second(src_dir_first)

	log_normal.info("end scan dir: %s" % src_dir)
	log_normal.info("backup_record(%s) end" % condition)
	log_normal.info("###################################################################")

def parse_dirname(dirname):
	log_normal.info("parse_dirname(%s) start" % dirname)
	if os.path.exists(dirname):
		if dirname.startswith(src_dir):
			child_name = dirname.replace(src_dir + '/', '')
			log_normal.info("child_name: %s" % child_name)

			dir_childs = child_name.split('/')
			if 1 == int(len(dir_childs)):
				log_normal.info("dir_childs[0]=%s" % (dir_childs[0]))
				backup_record_second(dir_childs[0])
			if 2 == int(len(dir_childs)):
				log_normal.info("dir_childs[0]=%s, dir_childs[1]=%s" % (dir_childs[0], dir_childs[1]))
				backup_record_third(dir_childs[0], dir_childs[1])
			elif 3 == int(len(dir_childs)):
				log_normal.info("dir_childs[0]=%s, dir_childs[1]=%s, dir_childs[2]=%s" % (dir_childs[0], dir_childs[1], dir_childs[2]))
				copy_to_dest(dir_childs[0], dir_childs[1], dir_childs[2])
			else:
				log_normal.error("dir_childs len is not match")
		else:
			log_normal.error("dirname(%s) is not start with %s" % (dirname, src_dir))
	else:
		log_normal.error("dirname(%s) is not exists" % dirname)

def parse_param1(errorfile):
	log_normal.info("###################################################################")
	log_normal.info("parse_param1(%s) start" % condition)

	if os.path.exists(errorfile):
		filehandler = open(errorfile)
		for dirname in filehandler.readlines():
			parse_dirname(dirname.strip("\n"))

		filehandler.close()
	else:
		log_normal.error("errorfile(%s) is not exists" % errorfile)

	log_normal.info("parse_param1(%s) end" % condition)
	log_normal.info("###################################################################")

def parse_params():
	if 1 == int(len(sys.argv)):
		log_normal.info("param1 is NULL")
		backup_record()
	else:
		param1 = sys.argv[1] 
		log_normal.info("param1 is not NULL")
		parse_param1(param1)

if __name__ == "__main__":
	log_config()

	print_params()

	parse_params()
	
	log_normal.info("backup.py end###################################")



