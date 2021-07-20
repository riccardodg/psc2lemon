#! /usr/bin/env python
import sys
import collections
import shutil
import os
import os.path
import hashlib

# file used to list all entries as lemon entries in different files according to the hashing of their lemmas
# Please BE CAREFUL with the namespaces. Before launching the script, have a look to the header file.
# Each file is then saved in a specific folder under the name space:
# <!ENTITY singlepsc "http://www.languagelibrary.eu/owl/simple/psc" >
# If  BASE_ROOT=http://www.languagelibrary.eu"
# and LOC_ROOT=owl/simple/
# Then we have that the final namespace psc is "http://www.languagelibrary.eu/owl/simple/psc" >
# while the single namespace is singlepsc
# So, use psc as namespace and singlepsc as namespace_4_singlepsc


if len(sys.argv) >3:
	# Usage: python convert.py [file.csv] [namespace] 

	#the domain is used in the GlobalInformation and to give the name to the file
	text = sys.argv[1]
	namespace = sys.argv[2]
	namespace_mf = sys.argv[3]
	#namespace=""
else:
	print "Usage: python simple2rdf_manyfolders.py [file.csv] [namespace] [namespace_4_singlepsc]"
	sys.exit()

lexicon = collections.defaultdict(list)



#The input file as the following structure:
#abate,USem67408abate
#where
# 0 -> lemma
# 1 -> usem
file = open(text)
if file :
	for line in file :
#		print line
		line_stripped = line.strip()
		line_array = line_stripped.split(",")
		lexical_entry = line_array[0]
		sense = line_array[1]

		lexicon[lexical_entry].append( sense )

	file.close()
else :
	print "errore"


if not os.path.exists(namespace):
	os.makedirs(namespace)
#result_filename = namespace + "individuals.owl"

header_file="header_lemon"
header_file_manyfile="header_lemon_manyfile"
file_h = open(header_file,'r')
text = file_h.read()
file_h.close()
file_h_mf = open(header_file_manyfile,'r')
text_s = file_h_mf.read()
file_h_mf.close()
# description files
desc_filename = namespace + "/lemonentriespointingtobigfile"
desc_filename_mf = namespace + "/lemonentriespointingtosinglefile"




# desription file lemonentriespointingtobigfile
file_d = open(desc_filename,'w')
file_d.write(text)

# description file lemonentriespointingtosinglefile
file_d_mf = open(desc_filename_mf,'w')
file_d_mf.write(text_s)

for lemma, sense_list in lexicon.iteritems():
	s=1
	
	#transoforms the lemma in a hash string (same lemma has >=1 senses taht in this way are grouped under the same folder)
	m = hashlib.md5()
	m.update(lemma)
	hash_string = m.hexdigest()
	
	#create first order folder if non existant
	first_order_folder = str(hash_string[:1])
	if not os.path.exists(namespace+"/" + first_order_folder):
		os.makedirs(namespace+"/" + first_order_folder)

	#create second order folder if non existant
	second_order_folder = str(hash_string[0:3])
	if not os.path.exists(namespace+"/" + first_order_folder + "/" + second_order_folder):
		os.makedirs(namespace+"/" + first_order_folder + "/" + second_order_folder)

	
	#writes the result file in the right folder with the hash_string attached (u may remove this, just for check)
	
	result_filename = namespace+"/" + first_order_folder + "/" + second_order_folder + "/" +lemma # source file name
			
	#writes the hash: lemma, hash,first_folder, sec_folder, sense 
	
	file = open(result_filename,'w')
	
	# starting writing files each single file points to SINGLE FILE NOT TO the BIG ONE
	file.write(text_s) # put the header
	
	# desription file lemonentriespointingtobigfile
	file_d.write("\t<rdf:Description rdf:about=\"&" + namespace + ";#" + lemma + "\">")
	file_d.write("</rdf:Description>" + "\n")
	
	# description file lemonentriespointingtosinglefile	
	file_d_mf.write("\t<rdf:Description rdf:about=\"&" + namespace_mf + ";" + first_order_folder + "/" + second_order_folder + "/" + lemma + "\">")
	file_d_mf.write("</rdf:Description>" + "\n")
	file.write( "\t\t<lemon:entry>\n" )
	file.write ( "\t\t\t<lemon:LexicalEntry rdf:about=\"&"+ namespace_mf + ";" + first_order_folder + "/" + second_order_folder + "/" + lemma + "\">\n" )
	file.write ( "\t\t\t\t<lemon:canonicalForm>\n" )
	file.write ("\t\t\t\t\t<lemon:Form>\n")
	file.write ("\t\t\t\t\t\t<lemon:writtenRep xml:lang=\"it\">" + lemma + "</lemon:writtenRep>\n")
	file.write ("\t\t\t\t\t</lemon:Form>\n")
	file.write ( "\t\t\t\t</lemon:canonicalForm>\n" )
	file.write ( "\t\t\t\t<lexinfo:partOfSpeech rdf:resource=\"&lexinfo;noun\"/>\n")
	
	for sense in sense_list: 
		file.write("\t\t\t\t<lemon:sense>\n")
		file.write("\t\t\t\t\t<lemon:LexicalSense rdf:about=\"&"+ namespace_mf+";"+ first_order_folder + "/" + second_order_folder + "/" +lemma+"_sense"+str(s)+"\">\n" )
		file.write("\t\t\t\t\t\t<lemon:reference rdf:resource=\"&singleind;"+ first_order_folder + "/" + second_order_folder + "/"+sense +"\"/>\n" )
		file.write("\t\t\t\t\t</lemon:LexicalSense>\n")
		file.write("\t\t\t\t</lemon:sense>\n")
		s=s+1
	file.write( "\t\t\t</lemon:LexicalEntry>\n" )
	file.write( "\t\t</lemon:entry>\n" )
	
	file.write("</rdf:RDF>\n")
	file.close()
file_d.write("</rdf:RDF>")
file_d_mf.write("</rdf:RDF>")
file_d.close()
file_h.close()
