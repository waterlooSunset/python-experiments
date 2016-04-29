# Import subprocess, json, os, pipes
import subprocess, json, os, shlex

def buildPDF(jobsInfoID):
	""" builds our PDF """
	# define command that we will execute
	command = "xvfb-run --server-args='-screen 0, 1024x768x16' scribus-trunk -g -py scribus_templates/template.py --python-arg {}".format(jobsInfoID)

	# run scribus command
	process = subprocess.Popen(command,
	 shell=True,
	 stdout=subprocess.PIPE
	)
	process.wait()

	pass
