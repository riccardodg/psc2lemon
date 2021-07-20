#! /usr/bin/env python
import sys
import collections
import shutil
import os
import os.path
import hashlib


if len(sys.argv) >2:
	# Usage: python convert.py [file.csv] [namespace]

	#the domain is used in the GlobalInformation and to give the name to the file
	text = sys.argv[1]
	namespace = sys.argv[2]
	#namespace=""
else:
	print "Usage: python simple2rdf_manyfolders.py [file.csv] [namespace]"
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
# the relation is the concatenation of 3 and 6 fields 


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
file_h = open(header_file,'r')
text = file_h.read()
file_h.close()
# description files
desc_filename = "inds/"+namespace + "listindividuals.owl"
hash_filename = namespace + "hashes.owl"



#
file_d = open(desc_filename,'w')
file_h = open(hash_filename,'w')
file_d.write(text)
for ind, value in individuals.iteritems():
	#file.write( ind.split("#")[0] + " is a " + ind.split("#")[1] + "\n")
	
	#create "inds" folder if non existant
	
	
	#transoforms the lemma in a hash string (same lemma has >=1 senses taht in this way are grouped under the same folder)
	s = hashlib.md5()
	s.update(ind.split("#")[0])
	hash_string = s.hexdigest()
	
	#create first order folder if non existant
	first_order_folder = str(hash_string[:1])
	if not os.path.exists("inds/" + first_order_folder):
		os.makedirs("inds/" + first_order_folder)

	#create second order folder if non existant
	second_order_folder = str(hash_string[0:3])
	if not os.path.exists("inds/" + first_order_folder + "/" + second_order_folder):
		os.makedirs("inds/" + first_order_folder + "/" + second_order_folder)
	
	#writes the result file in the right folder with the hash_string attached (u may remove this, just for check)
	
	result_filename = "inds/" + first_order_folder + "/" + second_order_folder + "/" +ind.split("#")[1] # source file name

			
	
	#writes the hash: lemma, hash,first_folder, sec_folder, sense 
	out="lemma="+ind.split("#")[0]+", hash="+ hash_string+ ", first_folder="+first_order_folder+ ", second_folder=" + second_order_folder+ ", usem="+ind.split("#")[1]
	file_h.write(out+"\n")
	file = open(result_filename,'w')
	
	
	file.write(text)
	
	file_d.write("\t<rdf:Description rdf:about=\"&" + namespace + ";" + first_order_folder + "/" + second_order_folder + "/" + ind.split("#")[1] + "\">")
	file_d.write("</rdf:Description>" + "\n")
	file.write( "\t<owl:NamedIndividual rdf:about=\"&" +  namespace + ";" + first_order_folder + "/" + second_order_folder + "/" + ind.split("#")[1] + "\">\n")
	file.write( "\t\t<rdfs:label> "+ind.split("#")[0] +"_as_"+ind.split("#")[2] +"</rdfs:label>" + "\n")
	file.write( "\t\t<rdfs:comment> The lemma of "+ind.split("#")[1] +" is "+ind.split("#")[0] +"</rdfs:comment>" + "\n")
	file.write( "\t\t<rdf:type rdf:resource=\"&prop;" + ind.split("#")[2] + "\"/>\n" )
	for rel in value: 
		#also target filelame must be managed
		#transoforms the target lemma in a hash string (same lemma has >=1 senses taht in this way are grouped under the same folder)
		t = hashlib.md5()
		t.update(rel.split("#")[2])
		hash_t_string = t.hexdigest()
	
		#create first order folder if non existant
		t_first_order_folder = str(hash_t_string[:1])
		if not os.path.exists("inds/" + t_first_order_folder):
			os.makedirs("inds/" + t_first_order_folder)

		#create second order folder if non existant
		t_second_order_folder = str(hash_t_string[0:3])
		if not os.path.exists("inds/" + t_first_order_folder + "/" + t_second_order_folder):
			os.makedirs("inds/" + t_first_order_folder + "/" + t_second_order_folder)

		file.write("\t\t\t" + "<prop:has" + rel.split("#")[0] + " rdf:resource=\"&" + namespace + ";"  + t_first_order_folder + "/" + t_second_order_folder + "/"+ rel.split("#")[1] + "\"/>" + "\n" )
	file.write( "\t</owl:NamedIndividual>\n" )
	file.write( "</rdf:RDF>\n" )
	file.close()
file_d.write("</rdf:RDF>")
file_d.close()
file_h.close()
