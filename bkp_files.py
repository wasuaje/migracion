# -*- coding: utf-8 -*-
import sys,tarfile,subprocess,os,re

#TARGETDIR="/netapp/migracion/eu/"
#SRCDIR="/manduca10/local3/eluniversal/euroot/"

TARGETDIR="/home/wasuaje/Documentos/"
SRCDIR="/home/wasuaje/Documentos/desarrollo/"

dirs=[]
dirs=["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009"]
#dirs=["2003","2004"]

#tar -uf /netapp/migracion/eu/2000.tar /manduca10/local3/eluniversal/euroot/2000
#gzip /netapp/migracion/eu/2000.tar

def run_cmd(comando):				#ejecuta comandos en consola
	p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read().strip()
	return out  #This is the stdout from the shell command
	
def tarfile(vfile=SRCDIR, vpath=TARGETDIR):
	for dir in dirs:
		command="rm -rf /netapp/migracion/eu/*;"
		command=command+"tar -zchf "+TARGETDIR+dir+".tar.gz "+SRCDIR+dir
		run_cmd(command)
		print command
		
tarfile()
	

