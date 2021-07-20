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
	#namespace="simple_lemon"
else:
	print "Usage: python simple2lemon_rdf.py [file.csv] [namespace]"
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

#create "inds" folder if non existant
if not os.path.exists("psc"):
	os.makedirs("psc")
header_file="header_lemon"
file_h = open(header_file,'r')
text = file_h.read()
file_h.close()
# description files

desc_filename = "psc/"+namespace + "listindividuals.owl" # contains the list of the 


file_d = open(desc_filename,'w')
file_d.write(text)


file_d.write( "\t<lemon:Lexicon rdf:about=\"SimpleLexicon\" lemon:language=\"it\">\n")
#file_d.write( "\t\t<lemon:entry>\n" )



# one file for each resource
for lemma, sense_list in lexicon.iteritems():
	s=1
	#transoforms the lemma in a hash string (same lemma has >=1 senses taht in this way are grouped under the same folder)
	m = hashlib.md5()
	m.update(lemma)
	hash_string = m.hexdigest()
	
	#define first and second order folder if non existant. This is a link to
	first_order_folder = str(hash_string[:1])
	second_order_folder = str(hash_string[0:3])
	
	

	#create first order folder if non existant
	first_order_folder = str(hash_string[:1])
	if not os.path.exists("psc/" + first_order_folder):
		os.makedirs("psc/" + first_order_folder)

	#create second order folder if non existant
	second_order_folder = str(hash_string[0:3])
	if not os.path.exists("psc/" + first_order_folder + "/" + second_order_folder):
		os.makedirs("psc/" + first_order_folder + "/" + second_order_folder)
	
	#writes the result file in the right folder with the hash_string attached (u may remove this, just for check)
	file_d.write( "\t\t<lemon:entry>\n" )
	file_d.write ( "\t\t\t<lemon:LexicalEntry rdf:about=\"&"+ namespace+";/" + first_order_folder + "/" + second_order_folder+ "/"+lemma + "\" />\n" )
	file_d.write( "\t\t</lemon:entry>\n" )
#	file_d.write ("</lemon:LexicalEntry>" + "\n")
	result_filename = "psc/" + first_order_folder + "/" + second_order_folder + "/" +lemma
	file = open(result_filename,'w')
	file.write(text)
	file.write ( "\t<lemon:LexicalEntry rdf:about=\"&"+ namespace+";/" + first_order_folder + "/" + second_order_folder+ "/"+lemma + "\">\n" )
	

	for sense in sense_list: 
		file.write("\t\t<lemon:sense>\n")
		file.write("\t\t\t<lemon:LexicalSense rdf:about=\"&"+ namespace+";/" + first_order_folder + "/" + second_order_folder+ "/"+lemma + "#sense"+str(s)+"\">\n" )
		file.write("\t\t\t\t<lemon:reference rdf:resource=\"&simple_ind;" +"/"+first_order_folder+"/"+second_order_folder+"/"+sense +"\"/>\n" )
		file.write("\t\t\t</lemon:LexicalSense>\n")
		file.write("\t\t</lemon:sense>\n")
		s=s+1
	file.write ( "\t\t<lemon:canonicalForm>\n" )
	file.write ("\t\t\t<lemon:Form rdf:about=\"&"+ namespace+";/" + first_order_folder + "/" + second_order_folder+ "/"+lemma + "\">\n" )
	file.write ("\t\t\t\t<lemon:writtenRep xml:lang=\"it\">" + lemma + "</lemon:writtenRep>\n")
	file.write ("\t\t\t</lemon:Form>\n")
	file.write ( "\t\t</lemon:canonicalForm>\n" )
	file.write ("\t\t<lexinfo:partOfSpeech rdf:resource=\"http://www.lexinfo.net/ontology/2.0/lexinfo#noun\"/>\n")
	file.write( "\t</lemon:LexicalEntry>\n" )
	file.write( "</rdf:RDF>\n" )
	file.close()
#file_d.write( "\t\t</lemon:entry>\n" )
file_d.write("\t</lemon:Lexicon>\n")
file_d.write("</rdf:RDF>\n")
file_d.close()



