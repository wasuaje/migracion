
import sys,re,subprocess,os

# Dado un directorio lo recorre, lee arhicvo por archivo
# buscando un patro dado y lo reemplaza por el nuevo
# patron deseado
# replace_pattern /home/user/files 111.1111.11 222-222-22
# replace_pattern /home/user/files 111.1111.11 222-222-22 [allthisextensions]
# replace_pattern /home/user/files/file.ext 111.1111.11 222-222-22
# puede ser directorio o archivo

def main(p1,p2,p3,p4):
	if os.path.isdir(p1):
		for root,dirs,files in os.walk(p1):
		    for file in [f for f in files ]:
		    	archivo=os.path.join(root, file)
    	        	#print(os.path.join(root, file))	
		    	if p4 != "" and archivo.endswith(p4):
		    		print archivo,
	    			procesar(archivo,p2,p3)
	    		elif p4 == "":
		    		print archivo,
	    			procesar(archivo,p2,p3)
	    		
	else:
	    	archivo=p1
	    	print archivo,
	    	procesar(archivo,p2,p3)

def procesar(archivo,p2,p3):
	try:
		fle = open(archivo, "r")
		buff=fle.read()
		inicia = buff.find(p2)		
		fle.close()
		if inicia > 0:
		    	fle = open(archivo, "w")
			finaliza = inicia+len(p2)
			buff = buff.replace(buff[inicia:finaliza], p3)
			fle.write(buff)
			print "                   *** Modificado *** \n",
			fle.close()
		else:
			print "\n",
	except IOError, (errno, strerror):  
		print "I/O error(%s): %s" % (errno, strerror)	
	except ValueError:
		print "Could not convert data to an integer."
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise

        	
if len(sys.argv) == 3:
	parametro=sys.argv[1]
	parametro2=""
	parametro3=""
	parametro4=""
elif len(sys.argv) == 4:
	parametro=sys.argv[1]		
	parametro2=sys.argv[2]		
	parametro3=sys.argv[3]
	parametro4=""
elif len(sys.argv) == 5:
	parametro=sys.argv[1]		
	parametro2=sys.argv[2]		
	parametro3=sys.argv[3]			
	parametro4=sys.argv[4]			
else:
	parametro=""
	parametro2=""
	parametro3=""
	parametro4=""

if parametro=="" or parametro2=="" or parametro3=="" :
	print "\n\n **** Solo la extension es un parametro opcional ***\n"
	print "Uso:  python replace_pattern /home/mydir/[files.ext] stringtofind replaceby  [.soloestaextension]\n\n"
else:
	main(parametro,parametro2,parametro3,parametro4)
	
	
	
	
	
