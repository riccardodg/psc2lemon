#! /usr/bin/env python
import sys
import collections
import shutil


if len(sys.argv) >2:
	# Usage: python convert.py [file.csv] [namespace]

	#the domain is used in the GlobalInformation and to give the name to the file
	text = sys.argv[1]
	namespace = sys.argv[2]
	#namespace=""
else:
	print "Usage: python convert.py [file.csv] [namespace]"
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
# 5 -> target_lemma NOT USED
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
		relation = line_array[3] + "#" + line_array[6]

		individuals[individual].append( relation )

	file.close()
else :
	print "errore"


#result_filename = namespace + "individuals.owl"
header_file="header"
file_h = open(header_file,'r')
text = file_h.read()
file_h.close()
# description files
desc_filename = namespace + "individuals.owl"

#
file_d = open(desc_filename,'w')
file_d.write(text)
for ind, value in individuals.iteritems():
	#file.write( ind.split("#")[0] + " is a " + ind.split("#")[1] + "\n")
	result_filename = "inds/"+ind.split("#")[1]	
	file = open(result_filename,'w')
	
	file.write(text)
	
	file_d.write("\t<rdf:Description rdf:about=\"&" + namespace + ";" + ind.split("#")[1] + "\">")
	file_d.write("</rdf:Description>" + "\n")
	file.write( "\t<owl:NamedIndividual rdf:about=\"&" + namespace + ";" + ind.split("#")[1] + "\">" + "\n")
	file.write( "\t\t<rdfs:label> "+ind.split("#")[0] +"_as_"+ind.split("#")[2] +"</rdfs:label>" + "\n")
	file.write( "\t\t<rdfs:comment> The lemma of "+ind.split("#")[1] +" is "+ind.split("#")[0] +"</rdfs:comment>" + "\n")
	file.write( "\t\t<rdf:type rdf:resource=\"&prop;" + ind.split("#")[2] + "\"/>\n" )
	for rel in value: 
		file.write("\t\t\t" + "<prop:has" + rel.split("#")[0] + " rdf:resource=\"&" + namespace + ";" + rel.split("#")[1] + "\"/>" + "\n" )
	file.write( "\t</owl:NamedIndividual>\n" )
	file.write( "</rdf:RDF>\n" )
	file.close()
file_d.write("</rdf:RDF>")
file_d.close()
