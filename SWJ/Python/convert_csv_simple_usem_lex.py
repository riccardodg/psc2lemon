#! /usr/bin/env python
import sys
import collections


if len(sys.argv) >1:
	# Usage: python convert.py [file.csv]

	#the domain is used in the GlobalInformation and to give the name to the file
	text = sys.argv[1]
else:
	print "Usage: python convert.py [file.csv]"
	sys.exit()

lexicon = collections.defaultdict(list)




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


result_filename = "SimpleLexicon.owl"


file = open(result_filename,'w')
file.write("<rdf:RDF>\n")
file.write( "\t<lemon:Lexicon rdf:about=\"SimpleLexicon\" lemon:language=\"it\">\n")



for lemma, sense_list in lexicon.iteritems():
	
	file.write( "\t\t<lemon:entry>\n" )
	file.write ( "\t\t\t<lemon:LexicalEntry rdf:about=\"" + lemma + "\">\n" )
	file.write ("\t\t\t\t<lemon:form rdf:parseType=\"Resource\">\n")
	file.write ("\t\t\t\t\t<lemon:writtenRep xml:lang=\"it\">" + lemma + "</lemon:writtenRep>\n")
	file.write ("\t\t\t\t</lemon:form>\n")

	for sense in sense_list: 
		file.write("\t\t\t\t<lemon:sense rdf:parseType=\"Resource\">\n")
		file.write("\t\t\t\t\t<lemon:reference rdf:resource=\"&simple_ind;" + sense + "\"/>\n" )
		file.write("\t\t\t\t</lemon:sense>\n")
	file.write( "\t\t\t</lemon:LexicalEntry>\n" )
	file.write( "\t\t</lemon:entry>\n" )
file.write("\t</lemon:Lexicon>\n")
file.write("</rdf:RDF>\n")
file.close()

