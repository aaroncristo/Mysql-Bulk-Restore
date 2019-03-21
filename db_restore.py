from os import listdir, mkdir, path, getcwd, system
import argparse
import re
import mysql.connector

def getArgs():
	parser = argparse.ArgumentParser(description='Bulk database restoration utility')
	parser.add_argument('-u','--user', required=True, help="MySQL user name")
	parser.add_argument('-p', '--password',  help="MySQL user password. Prompts if not provided via CLI")
	parser.add_argument('-P', '--port', default="3306", help="MySQL Port")
	parser.add_argument('-r', '--db_regex', help="REGEX to identify 'database name' from the 'file name'")
	parser.add_argument('-b', '--bk_loc', default='.//', help="Path to backup directory(Separate with '//' to avoid errors).")
	parser.add_argument('-d', '--delimiter' , help="Delimiter to cut the file name")
	parser.add_argument('-f', '--field', default="0", help="Field number")
	parser.add_argument('-m', '--binary', default="mysql", help="Path to mysql binary")
	return parser.parse_args()


def dbRestore(arg, db, file):
	try:

		file = '"%s"'% path.join(arg.bk_loc,file)
		passwd = ' ' + (' -p' + arg.password if arg.password else '')
		cmd =  ('"%s"'%arg.binary) + ' -u' + arg.user  + passwd +' -P' + arg.port + ' ' + db + ' < ' + file

		if not system('"%s"'%cmd):
			print('Success : Restored ', db,'from',file)
	except Exception as e:
		print('Error : Failed to restore ', db ,e )


if __name__ == "__main__":	
	try:	
		arg = getArgs()
		if not arg.delimiter and not arg.db_regex:
			raise Exception('No db name identification methods used')
		
		print('Performing Restore ...')

		for file in listdir(arg.bk_loc):
			if re.match('.*\.sql$',file):
				db_name = re.findall(arg.db_regex, file)[int(arg.field)-1] if arg.db_regex else file.split(arg.delimiter)[int(arg.field)-1]
				dbRestore(arg, db_name, file)
		
	except  Exception as e:
		print('Error',e)

	
		
	