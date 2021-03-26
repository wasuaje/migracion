# -*- coding: utf-8 -*-
import sys,tarfile,subprocess,os

#constantes
#SRCPATH="/instaladores/"
SRCPATH="/root/"
INSTALLPATH="/usr/local/"
INSTALLSRCPATH="/usr/local/src/"
INSTALADORES="."
INSTALLNFS="10.3.0.130 desarrollo"
INSTALLFSTAB="desarrollo:/home/manduca/src                   /instaladores            nfs     rw,bg,hard,intr,defaults,acl  0 0"
CVSSERVER="190.153.52.50   cvsserver"
#diccionario con los nombres de los comandos=carpeta final en user local, tipo de accion y otros
#*********PROBADO FUNCIONA OK *******************
serv_common={}
serv_common["0-common"]=["yum install -y nano cvs wget lynx htop iftop gcc gcc-devel autconf automake which nfs* make unzip tar dos2unix sudo vixie-cron crontabs unzip"]
serv_common["1-common"]=["service iptables stop; chkconfig iptables off", "service portmap start; chkconfig portmap on", "service nfs start; chkconfig nfs on" ]
serv_common["2-common"]=["echo "+INSTALLNFS+" >> /etc/hosts"]
serv_common["3-common"]=["echo "+CVSSERVER+" >> /etc/hosts"]
serv_common["4-common"]=["echo "+INSTALLFSTAB+" >> /etc/fstab"]
serv_common["5-common"]=["mount -a"]
serv_common["6-common"]=["groupadd manduca; useradd manduca -m -g manduca -d /home/manduca "]

serv_app_clasi={}
serv_app_clasi["0-ImageMagick"]=["yum install -y ImageMagick"]
serv_app_clasi["1-apache-ant"]=["tar -zxvf "+SRCPATH+"apache-ant-1.7.1-bin.tar.gz -C "+INSTALLPATH]
serv_app_clasi["2-jboss-5.1.0"]=["tar -zxvf "+SRCPATH+"jboss-5.1.0.GA-src.tar.gz -C "+INSTALLSRCPATH]
serv_app_clasi["3-java-jdk"]=["rpm -ivh jdk-6u7-linux-i586.rpm"]
serv_app_clasi["6-config"]=["echo \"PATH=$PATH:/usr/local/apache-ant/bin\" >> /etc/profile",
"echo \"JAVA_HOME=/usr/java/default/\" >> /etc/profile",
"echo \"export JAVA_HOME\" >> /etc/profile",
"echo \"export PATH\" >> /etc/profile" ,
"echo \"ANT_HOME=/usr/local/apache-ant/\" >> /etc/profile" ,
"echo \"export ANT_HOME\"  >> /etc/profile", 
"source /etc/profile" ]
serv_app_clasi["7-resin"]=["tar -zxvf "+SRCPATH+"resin-3.0.26.tar.gz -C "+INSTALLPATH,"export CFLAGS=\"\"", 
"cd "+INSTALLPATH+"resin-3.0.26; make clean; ./configure ;  make -j 4 && make install -j 4",
"echo \"RESIN_HOME=\"/usr/local/resin-3.0.26\"\" >> /etc/profile",
"echo \"export RESIN_HOME\" >> /etc/profile" ,"source /etc/profile"] 
serv_app_clasi["7-user"]=["groupadd manduca; useradd manduca -m -g manduca -d /home/manduca "]


serv_app_eu={}
serv_app_eu["1-pure-ftpd"]=["yum install pure-ftpd -y"]
serv_app_eu["2-apache-ant"]=["tar -zxvf "+SRCPATH+"apache-ant-1.7.1-bin.tar.gz -C "+INSTALLPATH,"mv "+INSTALLPATH+"apache-ant-1.7.1  "+INSTALLPATH+"apache-ant",
	"echo \"PATH=$PATH:/usr/local/apache-ant/bin\" >> /etc/profile",
	"echo \"ANT_HOME=/usr/local/apache-ant/\" >> /etc/profile" ,
	"echo \"export ANT_HOME\"  >> /etc/profile",
	"source /etc/profile" ]
	
serv_app_eu["3-resin"]=["tar -zxvf "+SRCPATH+"resin-3.0.26.tar.gz -C "+INSTALLPATH,"export CFLAGS=\"\"", 
"cd "+INSTALLPATH+"resin-3.0.26; make clean; ./configure ;  make -j 4 && make install -j 4",
"echo \"RESIN_HOME=\"/usr/local/resin-3.0.26\"\" >> /etc/profile",
"echo \"export RESIN_HOME\" >> /etc/profile" ,"source /etc/profile"] 

serv_app_eu["4-java"]=["cd /usr/local; echo \"yes\" > install.script;"+SRCPATH+"jdk-1_5_0_22-linux-i586.bin < install.script",
		"echo \"JAVA_HOME=\"/usr/local/jdk1.5.0_22\"\" >> /etc/profile","echo \"PATH=\$PATH:/usr/local/jdk1.5.0_22/bin\" >> /etc/profile",
		"echo \"export PATH\" >> /etc/profile", "echo \"export JAVA_HOME\" >> /etc/profile" ,"source /etc/profile" ]


#paquetes a isntallar via yum para web servers estaticos
#RAMDISK INCLUIR CREACION DE DIRECTORIOS Y RAMDISK COMO TAL
serv_static={}
serv_static["0-pre"]=["yum -y install libtool Zlib libxml2-devel libjpeg-devel libpng-devel libgif-devel"]
serv_static["1-apache-statics"]=["tar -zxvf "+SRCPATH+"httpd-2.2.15.tar.gz -C "+INSTALLSRCPATH]
serv_static["2-confstatic"]=[
      "cd "+INSTALLSRCPATH+"httpd-2.2.15; make clean; ./buildconf ; export CFLAGS=\"-D DYNAMIC_MODULE_LIMIT=0\" ; \
      ./configure --prefix=/usr/local/eu-static --enable-nonportable-atomics=yes --enable-cache --enable-disk_cache  --enable-deflate  --enable-expires --enable-alias \
     --enable-headers --enable-log-config --enable-rewrite --enable-suexec --disable-autoindex --disable-asis  --disable-cgid  --disable-cgi --disable-filter \
     --disable-negotiation --disable-userdir --enable-status  --disable-authn_file --disable-auth_basic --disable-authn_file --disable-authz_user --disable-authz_default \
     --disable-authz_groupfile --enable-authz_host --disable-autoindex --enable-include --disable-actions --disable-userdir --disable-authn_default \
     --disable-version --with-mpm=worker --with-suexec-caller=500   --disable-so ; make -j 4 && make install -j 4include",
      "cd "+INSTALLPATH+"eu-static/conf; scp  manduca@204.228.236.6:/usr/local/apacheTest-statics/conf/* ."
      ]
#serv_static["apache-widgets"]=["tar","httpd-2.2.15.tar.gz"]
#serv_static["php"]=["php","php-5.2.8.tar.gz"]
#serv_static["mysql"]=["mysql","mysql-5.1.41-linux-i686-icc-glibc23.tar.gz"]
#serv_static["mod_fcgi"]=["apachemod","mod_fcgid-2.3.4.tar.gz"]

serv_dyneu={}
serv_dyneu["0-pre"]=["yum -y install libtool Zlib libxml2-devel libjpeg-devel libpng-devel libgif-devel"]
serv_dyneu["1-apache-eu"]=["tar -zxvf "+SRCPATH+"httpd-2.2.15.tar.gz -C "+INSTALLSRCPATH]
serv_dyneu["2-eu-conf"]=["cd "+INSTALLSRCPATH+"httpd-2.2.15; make clean; ./buildconf ; export CFLAGS=\"-D DYNAMIC_MODULE_LIMIT=10\" ; \
      ./configure --prefix=/usr/local/eu-dynamic --enable-nonportable-atomics=yes --enable-cache --enable-mem-cache --enable-disk-cache --enable-deflate  --enable-expires \
     --enable-headers --enable-log-config --enable-rewrite --enable-suexec --disable-autoindex --disable-asis  --disable-cgid  --disable-cgi \
     --disable-filter --disable-negotiation --disable-userdir --enable-status  --disable-authn_file --disable-auth_basic --disable-authn_file \
     --disable-authz_user --disable-authz_default -disable-authz_groupfile --disable-authz_host --disable-autoindex --disable-actions          \
     --disable-userdir --disable-authn_default --disable-version --disable-alias --with-mpm=worker --with-suexec-caller=500 ; make -j 4 && make install -j 4", 
     "cd "+INSTALLPATH+"eu-dynamic/conf; scp -r manduca@204.228.236.7:/usr/local/apacheTest-eu/conf/* ."
     ]
serv_dyneu["3-java"]=["cd /usr/local; echo \"yes\" > install.script ; "+SRCPATH+"jdk-1_5_0_22-linux-i586.bin < install.script",
"echo \"JAVA_HOME=\"/usr/local/jdk1.5.0_22\"\" >> /etc/profile",
"echo \"PATH=$PATH:/usr/local/jdk1.5.0_22/bin\" >> /etc/profile", "echo \"export PATH\" >> /etc/profile", "echo \"export JAVA_HOME\" >> /etc/profile" ,"source /etc/profile"]

serv_dyneu["4-eu-resin"]=["tar -zxvf "+SRCPATH+"resin-3.0.26.tar.gz -C "+INSTALLSRCPATH,
"export CFLAGS=\"\"", "cd "+INSTALLSRCPATH+"resin-3.0.26; make clean; ./configure --with-apache=/usr/local/eu-dynamic;  make -j 4 && make install -j 4"]

serv_dyneu["5-estampas"]=["tar -zxvf "+SRCPATH+"httpd-2.2.15.tar.gz -C "+INSTALLSRCPATH]
serv_dyneu["6-estampas-conf"]=["cd "+INSTALLSRCPATH+"httpd-2.2.15; make clean; ./buildconf ; export CFLAGS=\"-D DYNAMIC_MODULE_LIMIT=10\" ; \
      ./configure --prefix=/usr/local/estampas-dynamic --enable-nonportable-atomics=yes --enable-cache --enable-mem-cache --enable-disk-cache --enable-deflate  --enable-expires \
     --enable-headers --enable-log-config --enable-rewrite --enable-suexec --disable-autoindex --disable-asis  --disable-cgid  --disable-cgi \
     --disable-filter --disable-negotiation --disable-userdir --enable-status  --disable-authn_file --disable-auth_basic --disable-authn_file \
     --disable-authz_user --disable-authz_default -disable-authz_groupfile --disable-authz_host --disable-autoindex --disable-actions          \
     --disable-userdir --disable-authn_default --disable-version --disable-alias --with-mpm=worker --with-suexec-caller=500 ; make -j 4 && make install -j 4", 
     "cd "+INSTALLPATH+"estampas-dynamic/conf; scp -r manduca@204.228.236.7:/usr/local/apacheD2-es/conf/* ."
     ]

serv_dyneu["7-estampas-resin"]=["tar -zxvf "+SRCPATH+"resin-3.0.26.tar.gz -C "+INSTALLSRCPATH,
"export CFLAGS=\"\"", "cd "+INSTALLSRCPATH+"resin-3.0.26; make clean; ./configure --with-apache=/usr/local/estampas-dynamic;  make -j 4 && make install -j 4"]

serv_dynclasi={}
serv_dynclasi["0-pre"]=["yum -y install libtool Zlib libxml2-devel libjpeg-devel libpng-devel libgif-devel"]
serv_dynclasi["1-apache-clasi"]=["tar -zxvf "+SRCPATH+"httpd-2.2.15.tar.gz -C "+INSTALLSRCPATH]
serv_dynclasi["2-apache-clasi-conf"]=["cd "+INSTALLSRCPATH+"httpd-2.2.15; make clean; export CFLAGS=\"\" ; \
  ./configure --prefix=/usr/local/apache-ceu --enable-proxy --enable-proxy-ajp --enable-rewrite --enable-deflate --enable-headers --enable-expires --with-mpm=prefork ;\
   make -j 4 && make install -j 4", "cd "+INSTALLPATH+"apache-ceu/conf; echo scp -r manduca@204.228.236.7:/usr/local/apache-ceu-2.2.11/conf/* ."]
	  
	  
serv_bbdd={}
serv_bbdd["0-pre0"]=["yum update -y"]
serv_bbdd["1-pre1"]=["yum install -y binutils compat-gcc compat-gcc-c++ compat-libstdc++ compat-libstdc++-devel cpp gcc gcc-c++ glibc glibc-common glibc-devel glibc-headers glibc-kernheaders libstdc++ libstdc++-devel libaio libai-devel pdksh setarch sysstat libXp compat-libstdc*"]
serv_bbdd["2-conf"]=["mkdir -p /clasificados", "mkdir -p /content", "mkdir -p /cvf3"]
serv_bbdd["3-conf1"]=["chmod -R 770 /clasificados", "chown -R oracle:oinstall /clasificados", "chmod -R 770 /content", "chown -R oracle:oinstall /content/" , "chmod -R 770 /cvf3",  "chown -R oracle:oinstall /cvf3"]
serv_bbdd["4-conf2"]=["source /etc/profile", "/usr/sbin/groupadd oinstall", "/usr/sbin/groupadd dba", "/usr/sbin/useradd -g oinstall -G dba oracle" ]
serv_bbdd["5-sysctl"]=["echo \"kernel.shmall = 2097152\" >> /etc/sysctl.conf",
"echo \"kernel.shmmax = 2147483648\" >> /etc/sysctl.conf",
"echo \"kernel.shmmni = 4096\" >> /etc/sysctl.conf",
"echo \"kernel.sem = 250 32000 100 128\" >> /etc/sysctl.conf",
"echo \"fs.file-max = 65536\" >> /etc/sysctl.conf",
"echo \"net.ipv4.ip_local_port_range = 1024 65000\" >> /etc/sysctl.conf",
"echo \"net.core.rmem_default = 262144\" >> /etc/sysctl.conf",
"echo \"net.core.rmem_max = 262144\" >> /etc/sysctl.conf",
"echo \"net.core.wmem_default = 262144\" >> /etc/sysctl.conf",
"echo \"net.core.wmem_max = 262144\" >> /etc/sysctl.conf"]

serv_bbdd["6-pamd"]=["echo \"session required pam_limits.so\" >> /etc/pam.d/login"]
serv_bbdd["7-limits"]=["echo \"oracle  soft  nproc   2047\" >> /etc/security/limits.conf",
		"echo \"oracle  hard  nproc   16384\" >> /etc/security/limits.conf",
		"echo \"oracle  soft  nofile  1024\" >> /etc/security/limits.conf",
		"echo \"oracle  hard  nofile  65536\" >> /etc/security/limits.conf"]
serv_bbdd["8-dirs"]=["mkdir /opt/oracle", "mkdir /opt/oracle/102", "chown -R oracle:dba /opt/oracle"]
serv_bbdd["9-profile"]=["echo \"ORACLE_BASE=/opt/oracle\" >> /home/oracle/.bash_profile",		
			"echo \"ORACLE_HOME=$ORACLE_BASE/102\" >> /home/oracle/.bash_profile",		
			"echo \"ORACLE_SID=ORCL\" >> /home/oracle/.bash_profile",		
			"echo \"LD_LIBRARY_PATH=$ORACLE_HOME/lib\" >> /home/oracle/.bash_profile",		
			"echo \"PATH=$PATH:$ORACLE_HOME/bin\" >> /home/oracle/.bash_profile",
			"cd /home/oracle; . .bash_profile"]
serv_prueba={}
serv_prueba["0-test"]=["echo \"probando\""]

#######
# Comandos utiles
#if filename.endswith(".txt"): ########### usefull para manejo de tipos de archivo
#os.chdir("/home/theoden/Desktop")   #aqui # para movernos de directorio
#f = open("hi.txt",'r')    #aqui abrimos el fichero con permisos de lectura
#chain = f.read() 
#chain = chain.replace("juan","ostia")    #sustituimos la cadena por la cadena que especificamos, en este caso sustituimos  la palabra juan por la palabra ostia y donde quiera que encuentre juan pondra ostiaestablecemos el directorio donde esta el fichero
#######

#sorbre este texto
#Thinking about that high school dance Worrying about the finals 
#inicia = result.find('Thinking') #buscamos el numero de caracer donde empieza la palabra
#finaliza = result.find('finals') #buscamos el numero de caracter donde empieza la palabra finals
#result = result.replace(result[inicia:finaliza+6], 'reemplazado') #remplazar todo lo que hay entre esas 2 palabras con reemplazado
#use un finaliza+6 por que al hacer el find 'finals' devuelve el valor donde comienza la letra "f" entonces borraria asta la "f" y no toda la palabra finals son 6 letras...

#para ordenar alfabeticamente las listas
def sortedDictValues2(adict):
    keys = adict.keys()
    keys.sort()
    return keys

#recibo archivo y ruta a descreargar si ruta=vacio en "."    
def untarfile(filep,path1="."):
	tar = tarfile.open(filep, "r:gz") # para crear uno 'w:gz'
	tar.extractall(path=path1)
	tar.close()

def tarfile():
	tar = tarfile.open("sample.tar.gz", "w:gz")
	for name in namelist:
	    tarinfo = tar.gettarinfo(name, "fakeproj-1.0/" + name)
	    tarinfo.uid = 123
	    tarinfo.gid = 456
	    tarinfo.uname = "johndoe"
	    tarinfo.gname = "fake"
	    tar.addfile(tarinfo, file(name))
	tar.close()

def write_file(newLine):
	file = open("paquetesyums.txt", "r")
	file.write(newLine)
	file.close()

def read_yumfile(newLine):
	file = open("paquetesyum.txt", "r")
	a=file.read()
	file.close()
	return a

def run_cmd(comando):				#ejecuta comandos en consola
	p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE)
	out = p.stdout.read().strip()
	return out  #This is the stdout from the shell command

def justrun(p1,dicts):
	comandos="comandos=sortedDictValues2(serv_"+dicts+")"
	try:
		exec(comandos)
	except (RuntimeError, TypeError, NameError):
		print "Unicos tipos admitidos son:  aplicaciones, static , widget, bbdd, dyneu, common"
		sys.exit(0)
	
	for key in comandos:
		if p1 != '':	
			#for cmd in serv_common[key]:
			exec("a=serv_"+dicts+"[key]")
			for cmd in a :
				if p1 in key:	
					print "Ejecutando "+cmd
				        result=run_cmd(cmd)
					print result						
		else:
			exec("a=serv_"+dicts+"[key]")			
			for cmd in a :
				print "Ejecutando "+cmd
				result=run_cmd(cmd)
				print result

if len(sys.argv) == 2:
	parametro=sys.argv[1]
	parametro2=""
elif len(sys.argv) == 3:
	parametro=sys.argv[1]		
	parametro2=sys.argv[2]		
else:
	parametro=""
	parametro2=""

#recibe tipo de servidor como parametro
justrun(parametro2,parametro)

