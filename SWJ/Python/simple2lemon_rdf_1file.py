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
	print "Usage: python simple2lemon_rdf_1file.py [file.csv] [namespace]"
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

header_file="header_lemon"
file_h = open(header_file,'r')
text = file_h.read()
file_h.close()
# description files

if not os.path.exists("psc"):
	os.makedirs("psc")
result_filename = "psc/SimpleLemon" # contains the list of the 
file = open(result_filename,'w')
file.write(text)


file.write( "\t<lemon:Lexicon rdf:about=\"&"+namespace+";\" lemon:language=\"it\">\n")




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
	
	#create "inds" folder if non existant
	



	file.write( "\t\t<lemon:entry>\n" )
	file.write ( "\t\t\t<lemon:LexicalEntry rdf:about=\"&"+ namespace+";#" +lemma + "\">\n" )
	file.write ( "\t\t\t\t<lemon:canonicalForm>\n" )
	file.write ("\t\t\t\t\t<lemon:Form>\n")
	file.write ("\t\t\t\t\t\t<lemon:writtenRep xml:lang=\"it\">" + lemma + "</lemon:writtenRep>\n")
	file.write ("\t\t\t\t\t</lemon:Form>\n")
	file.write ( "\t\t\t\t</lemon:canonicalForm>\n" )
	file.write ( "\t\t\t\t<lexinfo:partOfSpeech rdf:resource=\"&lexinfo;noun\"/>\n")

	for sense in sense_list: 
		file.write("\t\t\t\t<lemon:sense>\n")
		file.write("\t\t\t\t\t<lemon:LexicalSense rdf:about=\"&"+ namespace+";#"+lemma + "_sense"+str(s)+"\">\n" )
		file.write("\t\t\t\t\t<lemon:reference rdf:resource=\"&sense;#"+sense +"\"/>\n" )
		file.write("\t\t\t\t\t</lemon:LexicalSense>\n")
		file.write("\t\t\t\t</lemon:sense>\n")
		s=s+1
	file.write( "\t\t\t</lemon:LexicalEntry>\n" )
	file.write( "\t\t</lemon:entry>\n" )
file.write("\t</lemon:Lexicon>\n")
file.write("</rdf:RDF>\n")
file.close()



