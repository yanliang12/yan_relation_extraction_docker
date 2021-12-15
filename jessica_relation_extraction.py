##########jessica_relation_extraction.py##########
import os
import re
from py4j.java_gateway import JavaGateway

#	for file in `find . -name "*.jar"`; do export CLASSPATH="$CLASSPATH:`realpath $file`"; done

os.system(u"""
export CLASSPATH="$CLASSPATH:ejml-core-0.38-sources.jar"
export CLASSPATH="$CLASSPATH:ejml-core-0.38.jar"
export CLASSPATH="$CLASSPATH:ejml-ddense-0.38-sources.jar"
export CLASSPATH="$CLASSPATH:ejml-ddense-0.38.jar"
export CLASSPATH="$CLASSPATH:ejml-simple-0.38-sources.jar"
export CLASSPATH="$CLASSPATH:ejml-simple-0.38.jar"
export CLASSPATH="$CLASSPATH:javax.activation-api-1.2.0-sources.jar"
export CLASSPATH="$CLASSPATH:javax.activation-api-1.2.0.jar"
export CLASSPATH="$CLASSPATH:javax.json-api-1.0-sources.jar"
export CLASSPATH="$CLASSPATH:javax.json.jar"
export CLASSPATH="$CLASSPATH:jaxb-api-2.4.0-b180830.0359-sources.jar"
export CLASSPATH="$CLASSPATH:jaxb-api-2.4.0-b180830.0359.jar"
export CLASSPATH="$CLASSPATH:jaxb-core-2.3.0.1-sources.jar"
export CLASSPATH="$CLASSPATH:jaxb-core-2.3.0.1.jar"
export CLASSPATH="$CLASSPATH:jaxb-impl-2.4.0-b180830.0438-sources.jar"
export CLASSPATH="$CLASSPATH:jaxb-impl-2.4.0-b180830.0438.jar"
export CLASSPATH="$CLASSPATH:jessica_relation_extraction.jar"
export CLASSPATH="$CLASSPATH:joda-time-2.10.5-sources.jar"
export CLASSPATH="$CLASSPATH:joda-time.jar"
export CLASSPATH="$CLASSPATH:jollyday-0.4.9-sources.jar"
export CLASSPATH="$CLASSPATH:jollyday.jar"
export CLASSPATH="$CLASSPATH:protobuf.jar"
export CLASSPATH="$CLASSPATH:py4j-0.10.7.jar"
export CLASSPATH="$CLASSPATH:slf4j-api.jar"
export CLASSPATH="$CLASSPATH:slf4j-simple.jar"
export CLASSPATH="$CLASSPATH:stanford-corenlp-4.1.0-javadoc.jar"
export CLASSPATH="$CLASSPATH:stanford-corenlp-4.1.0-models-english-kbp.jar"
export CLASSPATH="$CLASSPATH:stanford-corenlp-4.1.0-models.jar"
export CLASSPATH="$CLASSPATH:stanford-corenlp-4.1.0-sources.jar"
export CLASSPATH="$CLASSPATH:stanford-corenlp-4.1.0.jar"
export CLASSPATH="$CLASSPATH:xom-1.3.2-sources.jar"
export CLASSPATH="$CLASSPATH:xom.jar"
echo $CLASSPATH
java jessica_relation_extraction &
""")

while True:
	try:
		gateway = JavaGateway()
		random = gateway.jvm.java.util.Random()
		number1 = random.nextInt(10)
		break
	except:
		pass

jessica = gateway.jvm.jessica_relation_extraction(',coref,kbp')

def relation_processing(renaltion_name):
	output = re.sub(r'^.*\:', r'', renaltion_name)
	output = re.sub(r'[^A-z]+', r'_', output)
	output = re.sub(r'^[^A-z]+|[^A-z]+$', r'', output)
	return output

def relation_extraction(text):
	relations = []
	######
	doc = jessica.text2doc(text)
	#####
	sentence_words = jessica.doc2setence_words(doc)
	sentence_tags = jessica.doc2setence_tags(doc)
	setences = jessica.doc2setences(doc)
	coref = jessica.doc2coref(doc)
	relation = jessica.doc2relation(doc)
	######for each entity build the lookup table and its instance mapping to the entity
	entity_mapping_dic_name = {}
	entity_mapping_dic_type = {}
	instance_sentence_map = {}
	instance_entity_map = {}
	for c in coref:
		### for the same entity
		entity_type = None
		entity_key = str(hash(str(c)))
		for c1 in c:
			c2 = eval(c1)
			sent = sentence_words[c2["sentence_index"]-1]
			tags = sentence_tags[c2["sentence_index"]-1]
			#entity_text = sent[c2["start_index"]-1:c2["end_index"]-1]
			entity_tag = tags[c2["start_index"]-1]
			#####
			instance_key = 'sent %d start %d end %d'%(c2["sentence_index"], 
				c2["start_index"],
				c2["end_index"])
			instance_entity_map[instance_key] = entity_key
			instance_sentence_map[instance_key] = setences[c2["sentence_index"]-1]
			entity_mapping_dic_name[entity_key] = c2["presentation"]
			if entity_tag not in ["O"]:
				entity_mapping_dic_type[entity_key] = entity_tag
	#######for each instance , map its entity names, type and id to itself
	instance_name = {}
	instance_type = {}
	instance_entity_id = {}
	for i in instance_entity_map:
		instance_name[i] = entity_mapping_dic_name[instance_entity_map[i]]
		instance_type[i] = entity_mapping_dic_type[instance_entity_map[i]]
		instance_entity_id[i] = instance_entity_map[i]
	######for each relation, map the instance name, type and id to the subject and object
	for r in relation:
		r1 = eval(r)
		subject_sent = sentence_words[r1["subject_sentence"]-1]
		object_sent = sentence_words[r1["object_sentence"]-1]
		subject_key = 'sent %d start %d end %d'%(r1["subject_sentence"], 
				r1["subject_start_index"],
				r1["subject_end_index"])
		object_key = 'sent %d start %d end %d'%(r1["object_sentence"], 
				r1["object_start_index"],
				r1["object_end_index"])
		########
		t = {}
		if subject_key in instance_name:
			t['subject_name'] = instance_name[subject_key]
			t['subject_type'] = instance_type[subject_key]
			t['subject'] = instance_entity_id[subject_key]
		else:
			t['subject_name'] = ' '.join(subject_sent[r1["subject_start_index"]-1:r1["subject_end_index"]-1])
			t['subject_type'] = r1['subject_type']
			t['subject'] = str(hash(subject_key))
		#####
		if object_key in instance_name:
			t['object_name'] = instance_name[object_key]
			t['object_type'] = instance_type[object_key]
			t['object'] = instance_entity_id[object_key]
		else:
			t['object_name'] = ' '.join(object_sent[r1["object_start_index"]-1:r1["object_end_index"]-1])
			t['object_type'] = r1['object_type']
			t['object'] = str(hash(object_key))
		#####
		t['relation'] = relation_processing(r1["relation"])
		relations.append(t)
		######and add the subject object metnioned by the sentence
		t1 = {}
		t1['subject_name'] = setences[r1["subject_sentence"]-1]
		t1['subject_type'] = "SENTENCE"
		t1['subject'] = str(hash(setences[r1["subject_sentence"]-1]))
		t1['relation'] = "mention"
		t1['object_name'] = t['subject_name']
		t1['object_type'] = t['subject_type']
		t1['object'] = t['subject']
		relations.append(t1)
		####
		t2 = {}
		t2['subject_name'] = setences[r1["object_sentence"]-1]
		t2['subject_type'] = "SENTENCE"
		t2['subject'] = str(hash(setences[r1["object_sentence"]-1]))
		t2['relation'] = "mention"
		t2['object_name'] = t['object_name']
		t2['object_type'] = t['object_type']
		t2['object'] = t['object']
		relations.append(t2)
	output = []
	for r in relations:
		if r not in output:
			output.append(r)
	return output

##########jessica_relation_extraction.py##########
