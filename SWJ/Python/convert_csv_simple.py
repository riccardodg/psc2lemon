#! /usr/bin/env python
import sys
import collections


if len(sys.argv) >2:
	# Usage: python convert.py [file.csv] [namespace]

	#the domain is used in the GlobalInformation and to give the name to the file
	text = sys.argv[1]
	namespace = sys.argv[2]
else:
	print "Usage: python convert.py [file.csv] [namespace]"
	sys.exit()

individuals = collections.defaultdict(list)





#questa funzione converte l'scf in formato ristretto nelle sue funzioni e realizzazioni::: da riguardare/ modificare a seconda delle necessita!!!!



file = open(text)
count=0;
if file :
	for line in file :
		#count=count+1
#		print line
		line_stripped = line.strip()
		line_array = line_stripped.split(",")
		individual = line_array[0] + "_as_" + line_array[1] +"#"+line_array[1]
		relation = line_array[2] + "#" + line_array[4]+ "_as_"+line_array[5]

		individuals[individual].append( relation )
		#print count
	file.close()
	#print count
	print " -- "
else :
	print "errore"


result_filename = namespace + "individuals.owl"


file = open(result_filename,'w')

tot=0
for ind, value in individuals.iteritems():
	tot=tot+1
	#file.write( ind.split("#")[0] + " is a " + ind.split("#")[1] + "\n")	
	file.write( "<owl:NamedIndividual rdf:about=\"&" + namespace + ";" + ind.split("#")[0] + "\">" + "\n")
	file.write( "\t<rdf:type rdf:resource=\"&prop;" + ind.split("#")[1] + "\"/>\n" )
	for rel in value: 
		file.write("\t\t" + "<prop:has" + rel.split("#")[0] + " rdf:resource=\"&" + namespace + ";" + rel.split("#")[1] + "\"/>" + "\n" )
	file.write( "</owl:NamedIndividual>\n" )
file.close()
print tot

