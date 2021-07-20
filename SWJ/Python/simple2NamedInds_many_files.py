#! /usr/bin/env python
import sys
import collections
import shutil
import os
import os.path
import hashlib

# file used to list entries as namedindividuals in different files according to the hashing of their lemmas (many Usems in the same folder) 
# Please BE CAREFUL with the namespaces. Before launching the script, have a look to the header file.
# For example <!ENTITY inds "BASE_ROOT/LOC_ROOT/inds/SimpleEntries#" > is the namespace for the individuals to be saved into.
# Each file is then saved in a specific folder under the name space:
# <!ENTITY singleind "http://www.languagelibrary.eu/owl/simple/inds" >
# If  BASE_ROOT=http://www.languagelibrary.eu"
# and LOC_ROOT=owl/simple/
# Then we have that the final namespace inds is "http://www.languagelibrary.eu/owl/simple/inds/SimpleEntries#" >
# while the single namespace is singleind
# So, use inds as namespace and singleind as namespace_4_singleind
if len(sys.argv) >2:
	# Usage: python convert.py [file.csv] [namespace]

	#the domain is used in the GlobalInformation and to give the name to the file
	text = sys.argv[1]
	namespace = sys.argv[2]
	namespace_mf = sys.argv[3]
	#namespace=""
else:
	print "Usage: python simple2rdf_manyfolders.py [file.csv] [namespace] [namespace_4_singleind]"
	sys.exit()

individuals = collections.defaultdict(list)



#The input file as the following structure:
#abate,USem67408abate,Social_status,Isa,Formal,uomo,USem3591uomo,Human
#where
# 0 -> source_lemma
# 1 -> source_usem
# 2 -> type of the source
# 3 -> relation
# 4 -> relation type NOT USED
# 5 -> target_lemma 
# 6 -> target_usem
# 7 -> type of the target NOT USED

# the individual is the concatenation of 0, 1 and 2 fields. This fields are used to create the label and the lemma
# the relation is the concatenation of 3 and 6 and 5 fields 


file = open(text)
if file :
	for line in file :
#		print line
		line_stripped = line.strip()
		line_array = line_stripped.split(",")
		individual = line_array[0] + "#" + line_array[1]+"#"+line_array[2]
		relation = line_array[3] + "#" + line_array[6]+"#" + line_array[5]

		individuals[individual].append( relation )

	file.close()
else :
	print "errore"

if not os.path.exists("inds"):
	os.makedirs("inds")
#result_filename = namespace + "individuals.owl"

header_file="header"
header_file_manyfile="header_manyfile"
file_h = open(header_file,'r')
text = file_h.read()
file_h.close()
file_h_mf = open(header_file_manyfile,'r')
text_s = file_h_mf.read()
file_h_mf.close()
# description files
desc_filename = namespace + "/individualspointingtobigfile.owl"
desc_filename_mf = namespace_mf + "/individualspointingtosinglefile.owl"
hash_filename = namespace + "/hashes.owl"



# desription file individualspointingtobigfile
file_d = open(desc_filename,'w')
file_d.write(text)

# description file individualspointingtosinglefile
file_d_mf = open(desc_filename_mf,'w')
file_d_mf.write(text_s)

# hash file
file_h = open(hash_filename,'w')
for ind, value in individuals.iteritems():
	#file.write( ind.split("#")[0] + " is a " + ind.split("#")[1] + "\n")
	
	#create "inds" folder if non existant
	
	
	#transoforms the lemma in a hash string (same lemma has >=1 senses taht in this way are grouped under the same folder)
	s = hashlib.md5()
	s.update(ind.split("#")[0]) # position 0 is the source lemma
	hash_string = s.hexdigest()
	
	#create first order folder if non existant
	first_order_folder = str(hash_string[:1])
	if not os.path.exists(namespace+"/" + first_order_folder):
		os.makedirs(namespace+"/" + first_order_folder)

	#create second order folder if non existant
	second_order_folder = str(hash_string[0:3])
	if not os.path.exists(namespace+"/" + first_order_folder + "/" + second_order_folder):
		os.makedirs(namespace+"/" + first_order_folder + "/" + second_order_folder)
	
	#writes the result file in the right folder with the hash_string attached (u may remove this, just for check)
	
	result_filename = namespace_mf+"/" + first_order_folder + "/" + second_order_folder + "/" +ind.split("#")[1] # source file name

			
	
	#writes the hash: lemma, hash,first_folder, sec_folder, sense 
	out="lemma="+ind.split("#")[0]+", hash="+ hash_string+ ", first_folder="+first_order_folder+ ", second_folder=" + second_order_folder+ ", usem="+ind.split("#")[1]
	file_h.write(out+"\n")
	file = open(result_filename,'w')
	
	# starting writing files each single file points to SINGLE FILE NOT TO the BIG ONE
	file.write(text_s) # put the header
	
	# desription file individualspointingtobigfile
	file_d.write("\t<rdf:Description rdf:about=\"&" + namespace + ";" + first_order_folder + "/" + second_order_folder + "/" + ind.split("#")[1] + "\">")
	file_d.write("</rdf:Description>" + "\n")
	
	# description file individualspointingtosinglefile	
	file_d_mf.write("\t<rdf:Description rdf:about=\"&" + namespace_mf + ";" + first_order_folder + "/" + second_order_folder + "/" + ind.split("#")[1] + "\">")
	file_d_mf.write("</rdf:Description>" + "\n")
	file.write( "\t<owl:NamedIndividual rdf:about=\"&" +  namespace_mf + ";" + first_order_folder + "/" + second_order_folder + "/" + ind.split("#")[1] + "\">\n")
	file.write( "\t\t<rdfs:label> "+ind.split("#")[0] +"_as_"+ind.split("#")[2] +"</rdfs:label>" + "\n")
	file.write( "\t\t<rdfs:comment> The lemma of "+ind.split("#")[1] +" is "+ind.split("#")[0] +"</rdfs:comment>" + "\n")
	file.write( "\t\t<rdf:type rdf:resource=\"&simple;" + ind.split("#")[2] + "\"/>\n" )
	
	
	for rel in value: 
		#also target filelame must be managed
		#transoforms the target lemma in a hash string (same lemma has >=1 senses taht in this way are grouped under the same folder)
		t = hashlib.md5()
		t.update(rel.split("#")[2]) # position 2 in rel is the target lemma
		hash_t_string = t.hexdigest()
	
		#create first order folder if non existant
		t_first_order_folder = str(hash_t_string[:1])
		if not os.path.exists(namespace+"/" + t_first_order_folder):
			os.makedirs(namespace+"/" + t_first_order_folder)

		#create second order folder if non existant
		t_second_order_folder = str(hash_t_string[0:3])
		if not os.path.exists(namespace+"/" + t_first_order_folder + "/" + t_second_order_folder):
			os.makedirs(namespace+"/" + t_first_order_folder + "/" + t_second_order_folder)

		file.write("\t\t\t" + "<simple:has" + rel.split("#")[0] + " rdf:resource=\"&" + namespace_mf + ";"  + t_first_order_folder + "/" + t_second_order_folder + "/"+ rel.split("#")[1] + "\"/>" + "\n" )
	file.write( "\t</owl:NamedIndividual>\n" )
	file.write( "</rdf:RDF>\n" )
	file.close()
file_d.write("</rdf:RDF>")
file_d.close()
file_h.close()
