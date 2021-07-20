#! /usr/bin/env python
import sys
import collections
import shutil
import os
import os.path
import hashlib
from sets import Set

# file used to list all entries as lemon entries in different files according to the hashing of their lemmas
# Please BE CAREFUL with the namespaces. Before launching the script, have a look to the header file and
# change accordingly the namespaces in the namespaces section
# Each file is then saved in a specific folder under the name space:
# <!ENTITY singlepsc "http://www.languagelibrary.eu/owl/simple/psc" >
# where BASE_ROOT=http://www.languagelibrary.eu" and LOC_ROOT=owl/simple/
# Then we have that the final namespace psc is "http://www.languagelibrary.eu/owl/simple/psc" >
# while the single namespace is singlepsc
# So, use psc as namespace and singlepsc as namespace_4_singlepsc


if len(sys.argv) >3:
	# Usage: python simple2lemon.py [text.csv] [lexrel] [lemonrel] [mapping_senseusem]

	text = sys.argv[1]
	lexrel = sys.argv[2]
	lemonrel = sys.argv[3]
        mapping_senseusem = sys.argv[4]
	#namespace=""
else:
	print "Usage: python simple2lemon.py [text.csv] [lexrel] [lemonrel] [mapping_senseusem]"
	sys.exit()

#VARIABLES
BASE_ROOT="http://www.languagelibrary.eu"
LOC_ROOT="owl/simple/"
tab="\t"
d_tab="\t\t"
t_tab="\t\t\t"
q_tab="\t\t\t\t"
c_tab="\t\t\t\t\t"

#namespaces
#namespace of the collection of entries for bigfile pscLemon
namespace="psc"

#namespace of collection of entries splitted by hash of lemmas
namespace_mf="singlepsc"

#namespaces for the ontology
simple="simple"

#dictionaries
lexicon = collections.defaultdict(list)
mapping = collections.defaultdict(list)
relations = collections.defaultdict(list)
lemonrelations = collections.defaultdict(list)



#The input file as the following structure:
#abate,USem67408abate
#where
# 0 -> lemma
# 1 -> usem
file = open(text)
if file :
	for line in file :
		#print line
		line_stripped = line.strip()
		line_array = line_stripped.split(",")
		lexical_entry = line_array[0]
		sense = line_array[1]

		lexicon[lexical_entry].append( sense )

	file.close()
else :
	print "error in reading file "+ text


#The input file as the following structure:
#abate,USem67408abate
#where
# 0 -> lemma
# 1 -> usem
file_m = open(mapping_senseusem)
if file_m :
	for line in file_m :
		#print line
		line_stripped = line.strip()
		line_array = line_stripped.split(",")
		lexical_entry = line_array[0]
		sense = line_array[1]

		mapping[lexical_entry].append( sense )

	file_m.close()
else :
	print "error in reading file "+ mapping


#The input file as the following structure:
#amareggiare,USem6593amareggiare,V,Experience_Event,PolysemyExperienceEvent-CauseExperienceEvent,Polysemy,amareggiare,USem6530amareggiare,V,Cause_Experience_Event
#where
# 0 -> source_lemma
# 1 -> source_usem
# 2 -> source_pos
# 3 -> source_type
# 4 -> relation
# 5 -> relation type
# 6 -> target_lemma
# 7 -> target_usem
# 8 -> target_pos
# 9 -> targete_type

# the result is source_usem, rel, target_lemma, target_usem, so #1, #4, #6, #7
file_lr = open(lexrel)
if file_lr :
	for line in file_lr :
		#print line
		line_stripped = line.strip()
		line_array = line_stripped.split(",")
		s_usem = line_array[1]
		rel = line_array[4]+"#"+line_array[6]+"#"+line_array[7]

		relations[s_usem].append( rel )

	file_lr.close()
else :
	print "error in reading file "+ lexrel

#The input file as the following structure:
#amareggiare,USem6593amareggiare,V,Experience_Event,PolysemyExperienceEvent-CauseExperienceEvent,Polysemy,amareggiare,USem6530amareggiare,V,Cause_Experience_Event
#where
# 0 -> source_lemma
# 1 -> source_usem
# 2 -> source_pos
# 3 -> source_type
# 4 -> relation
# 5 -> relation type
# 6 -> target_lemma
# 7 -> target_usem
# 8 -> target_pos
# 9 -> targete_type

# the result is source_usem, rel, target_lemma, target_usem, so #1, #4, #6, #7
file_lemr = open(lemonrel)
if file_lemr :
	for line in file_lemr :
		#print line
		line_stripped = line.strip()
		line_array = line_stripped.split(",")
		s_usem = line_array[1]
		rel = line_array[4]+"#"+line_array[6]+"#"+line_array[7]

		lemonrelations[s_usem].append( rel )

	file_lemr.close()
else :
	print "error in reading file "+ lexrel


# create  dicts
usem2sensenum=collections.defaultdict(list)
sensenum2usem=collections.defaultdict(list)	
for lemma, sense_list in mapping.iteritems():
	s=1
	for sense in sense_list:
		sensenum=lemma+"_"+str(s)
		usem=sense;
		s=s+1	
		#print usem+","+sensenum
		usem2sensenum[usem].append(sensenum)
 		sensenum2usem[sensenum].append(usem)


if not os.path.exists(namespace):
	os.makedirs(namespace)
#result_filename = namespace + "individuals.owl"

header_file="header_lemon"
header_file_manyfile="header_lemon_manyfile"

#header files for description files
header_lemon_4_description_bigfile="header_lemon_4_description_bigfile"
header_lemon_4_description_singlefile="header_lemon_4_description_singlefile"



file_h = open(header_file,'r')
text = file_h.read()
file_h.close()
file_h_mf = open(header_file_manyfile,'r')
text_s = file_h_mf.read()
file_h_mf.close()

# file for description
file_h_4dsf = open(header_lemon_4_description_singlefile,'r')
text_4dsf = file_h_4dsf.read()
file_h_4dsf.close()
file_h_4dbf = open(header_lemon_4_description_bigfile,'r')
text_4dbf = file_h_4dbf.read()
file_h_4dbf.close()
# description files
desc_filename = namespace + "/lemonentriespointingtobigfile" # the list of entries which point to the pscLemon file (collecting all entries)
desc_filename_mf = namespace + "/lemonentriespointingtosinglefile" # the list of entries which point to the single lemon file (collecting one entry -lemma)




# desription file lemonentriespointingtobigfile
file_d = open(desc_filename,'w')
file_d.write(text_4dbf)

# description file lemonentriespointingtosinglefile
file_d_mf = open(desc_filename_mf,'w')
file_d_mf.write(text_4dsf)

if not os.path.exists(namespace):
	os.makedirs(namespace)
result_filename_uniq = namespace+"/pscLemon" # contains the list of the lemonentries
file_uniq = open(result_filename_uniq,'w')
file_uniq.write(text)


file_uniq.write( "<lemon:Lexicon rdf:about=\"&"+namespace+";\" lemon:language=\"it\">\n")
subproperties_uniq = Set();
for lemma, sense_list in lexicon.iteritems():
	subproperties = Set();
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
	#file.write( "\t\t<lemon:entry>\n" )
	file.write ( d_tab+"<lemon:LexicalEntry rdf:ID=\""+ lemma + "\">\n" )
	file.write ( t_tab+"<lemon:canonicalForm>\n" )
	file.write (q_tab+"<lemon:Form>\n")
	file.write (c_tab+"<lemon:writtenRep xml:lang=\"it\">" + lemma + "</lemon:writtenRep>\n")
	file.write (q_tab+"</lemon:Form>\n")
	file.write ( t_tab+"</lemon:canonicalForm>\n" )
	file.write ( t_tab+"<lexinfo:partOfSpeech rdf:resource=\"&lexinfo;noun\"/>\n")

	# uniq file
	file_uniq.write( tab+"<lemon:entry>\n" )
	file_uniq.write ( d_tab+"<lemon:LexicalEntry rdf:about=\""+ lemma + "\">\n" )
	file_uniq.write ( t_tab+"<lemon:canonicalForm>\n" )
	file_uniq.write (q_tab+"<lemon:Form>\n")
	file_uniq.write (c_tab+"<lemon:writtenRep xml:lang=\"it\">" + lemma + "</lemon:writtenRep>\n")
	file_uniq.write (q_tab+"</lemon:Form>\n")
	file_uniq.write ( t_tab+"</lemon:canonicalForm>\n" )
	file_uniq.write ( t_tab+"<lexinfo:partOfSpeech rdf:resource=\"&lexinfo;noun\"/>\n")
	
	for sense in sense_list: 
		sensenum=usem2sensenum.get(sense)
              	#print "getting "+sense+ " "+str(sensenum[0])
		file.write(t_tab+"<lemon:sense>\n")
		file.write(q_tab+"<lemon:LexicalSense rdf:about=\"&"+ namespace_mf+";"+ first_order_folder + "/" + second_order_folder + "/" +lemma+"#"+str(sensenum[0])+"\">\n" )
		file.write(c_tab+"<lemon:reference rdf:resource=\"&singleind;"+ first_order_folder + "/" + second_order_folder + "/"+sense +"\"/>\n" )
		
		file_uniq.write(t_tab+"<lemon:sense>\n")
		file_uniq.write(q_tab+"<lemon:LexicalSense rdf:about=\"&"+ namespace+";#"+str(sensenum[0])+"\">\n" )
		file_uniq.write(c_tab+"<lemon:reference rdf:resource=\"&sense;#"+sense +"\"/>\n" )

		# lemon rels
		myrels=lemonrelations.get( sense )
		if myrels is not None:
			for rels in myrels:
				rel = rels.split("#")[0]
				t_lemma = rels.split("#")[1]
				t_usem = rels.split("#")[2]
				t_sensenum=usem2sensenum.get(t_usem)
				t_m = hashlib.md5()
				t_m.update(t_lemma)
				t_hash_string = t_m.hexdigest()
				
				#create first order folder if non existant
				t_first_order_folder = str(t_hash_string[:1])
	
				#create second order folder if non existant
				t_second_order_folder = str(t_hash_string[0:3])
				#print "relations " + sensenum[0]+ " "+rel+ " "+t_sensenum[0]
				file.write(c_tab+"<lemon:"+rel + " rdf:resource=\"&"+ namespace_mf+";"+ t_first_order_folder + "/" + t_second_order_folder + "/" +t_lemma+"#"+str(t_sensenum[0])+"\"/>\n")	
				file_uniq.write(c_tab+"<lemon:"+rel + " rdf:resource=\"&"+ namespace+";#"+ str(t_sensenum[0])+"\"/>\n")	
		myrels=relations.get( sense )
		if myrels is not None:
			for rels in myrels:
				rel = rels.split("#")[0]
				t_lemma = rels.split("#")[1]
				t_usem = rels.split("#")[2]
				t_sensenum=usem2sensenum.get(t_usem)
				t_m = hashlib.md5()
				t_m.update(t_lemma)
				t_hash_string = t_m.hexdigest()
			
			#add the list of relations in the subproperties
				subproperties.add(rel)
				subproperties_uniq.add(rel)
			#create first order folder if non existant
				t_first_order_folder = str(t_hash_string[:1])

			#create second order folder if non existant
				t_second_order_folder = str(t_hash_string[0:3])
			#print "relations " + sensenum[0]+ " "+rel+ " "+t_sensenum[0]
				file.write(c_tab+"<simple:"+rel + " rdf:resource=\"&"+ namespace_mf+";"+ t_first_order_folder + "/" + t_second_order_folder + "/" +t_lemma+"#"+str(t_sensenum[0])+"\"/>\n"
 )
				file_uniq.write(c_tab+"<simple:"+rel + " rdf:resource=\"&"+ namespace+";#"+ str(t_sensenum[0])+"\"/>\n")		
		file.write(q_tab+"</lemon:LexicalSense>\n")
		file.write(t_tab+"</lemon:sense>\n")
		file_uniq.write(q_tab+"</lemon:LexicalSense>\n")
		file_uniq.write(t_tab+"</lemon:sense>\n")
		s=s+1
        file.write( d_tab+"</lemon:LexicalEntry>\n" )	
	file_uniq.write( d_tab+"</lemon:LexicalEntry>\n" )
	file_uniq.write( tab+"</lemon:entry>\n" )
	#file.write( "\t\t</lemon:entry>\n" )
	# subproperties 
	for x in subproperties:
		file.write (tab+"<rdf:Property rdf:about=\"&simple;"+ x+"\">\n" )
		file.write (d_tab+"<rdfs:SubPropertyOf rdf:resource=\"&lemon;senseRelation" +"\"/>\n" )
		file.write (tab+"</rdf:Property>\n")
		
	file.write("</rdf:RDF>\n")
	file.close()
file_uniq.write("</lemon:Lexicon>\n")
for x in subproperties_uniq:
	file_uniq.write ("<rdf:Property rdf:about=\"&simple;"+ x+"\">\n" )
	file_uniq.write (tab+"<rdfs:SubPropertyOf rdf:resource=\"&lemon;senseRelation" +"\"/>\n" )
	file_uniq.write ("</rdf:Property>\n")
file_uniq.write("</rdf:RDF>\n")

file_uniq.close();
file_d.write("</rdf:RDF>")
file_d_mf.write("</rdf:RDF>")
file_d.close()
file_h.close()


