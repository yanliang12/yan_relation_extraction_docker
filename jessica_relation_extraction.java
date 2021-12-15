/////////////jessica_relation_extraction.java////////
/*
https://stackoverflow.com/questions/20754129/how-to-call-java-from-python-using-py4j

https://stanfordnlp.github.io/CoreNLP/coref.html

https://stanfordnlp.github.io/CoreNLP/kbp.html#list-of-relations

https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/pipeline/CoreDocument.html

http://manmustbecool.github.io/MyWiki/Wiki/Python/python_java.html

for file in `find . -name "*.jar"`; do export CLASSPATH="$CLASSPATH:`realpath $file`"; done
javac jessica_relation_extraction.java
jar -cvf jessica_relation_extraction.jar jessica_relation_extraction.class

javac jessica_relation_extraction.java
java jessica_relation_extraction &

*/

import java.util.*;
import py4j.GatewayServer;
import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.ie.util.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.coref.data.*;

public class jessica_relation_extraction {

	public static StanfordCoreNLP pipeline;

	public class jessica_relation_result {
		public List<List<String>> setence_words;
		public List<List<String>> setence_tags;
		public List<String> setences;
		public List<List<String>> coref;
		public List<String> relation;
	}

	public jessica_relation_extraction(){
	}

	public jessica_relation_extraction(String relation_model){
		long startTime;
		long elapsedTime;

		startTime = System.nanoTime();
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,depparse"+relation_model);
		pipeline = new StanfordCoreNLP(props);
		elapsedTime = System.nanoTime() - startTime;
		System.out.println("model laoding time: "+ elapsedTime/1000000000 +" seconds.");	
	}

	public static List<List<String>> doc2setence_words(CoreDocument document){
		List<List<String>> sentence_word = new ArrayList<>();

		for(CoreSentence s: document.sentences()){
			sentence_word.add(s.tokensAsStrings());
		}
		return sentence_word;
	}

	public static List<List<String>> doc2setence_tags(CoreDocument document){
		List<List<String>> sentence_word = new ArrayList<>();

		for(CoreSentence s: document.sentences()){
			sentence_word.add(s.nerTags());
		}
		return sentence_word;
	}

	public static List<String> doc2setences(CoreDocument document){
		List<String> sentences = new ArrayList<>();

		for(CoreSentence s: document.sentences()){
			sentences.add(s.text());
		}
		return sentences;
	}

	public static List<List<String>> doc2coref(CoreDocument document){

		Map<Integer,CorefChain>	 corefc = document.corefChains();
		List<List<String>> corefs = new ArrayList<>();

		for(Map.Entry<Integer, CorefChain> e: corefc.entrySet()) {
			List<String> corefs1 = new ArrayList<>();
			CorefChain corefv = e.getValue();
			CorefChain.CorefMention	corefvPre = corefv.getRepresentativeMention();
			for(CorefChain.CorefMention m: corefv.getMentionsInTextualOrder()){
				String coref_text = String.format("{\"sentence_index\":%d,\"start_index\":%d,\"end_index\":%s,\"presentation\":\"%s\"}",
					m.sentNum, 
					m.startIndex, 
					m.endIndex,
					corefvPre.mentionSpan);
				corefs1.add(coref_text);
			}
			corefs.add(corefs1);
		}
		return corefs;
	}

	public static List<String> doc2relation(CoreDocument document){
		List<String> relation_triplets = new ArrayList<>();

		for(CoreSentence s1: document.sentences()){
			for(RelationTriple t: s1.relations()){

				int subject_start_index = 2147483647;
				int subject_end_index = 0;
				int subject_sentence_index = 0;
				for(CoreLabel c: t.subject){
					subject_sentence_index = c.sentIndex();
					if(c.index() < subject_start_index) subject_start_index = c.index();
					if(c.index() > subject_end_index) subject_end_index = c.index();
				}
				subject_end_index++;
				subject_sentence_index++;

				int object_start_index = 2147483647;
				int object_end_index = 0;
				int object_sentence_index = 0;
				for(CoreLabel c: t.object){
					object_sentence_index = c.sentIndex();
					if(c.index() < object_start_index) object_start_index = c.index();
					if(c.index() > object_end_index) object_end_index = c.index();
				}
				object_end_index++;
				object_sentence_index++;

				String relation_text = String.format("{\"subject_start_index\":%d, \"subject_end_index\":%d,\"subject_sentence\":%d,\"subject_type\": \"%s\",\"object_start_index\":%d,\"object_end_index\":%d,\"object_sentence\":%d,\"object_type\":\"%s\",\"relation\":\"%s\"}", 
					subject_start_index, 
					subject_end_index,
					subject_sentence_index, 
					t.subjectHead().ner(),
					object_start_index, 
					object_end_index,
					object_sentence_index, 
					t.objectHead().ner(),
					t.relationGloss());
				relation_triplets.add(relation_text);
			}
		}
		return relation_triplets;
	}

	public static CoreDocument text2doc(String text){
		return  pipeline.processToCoreDocument(text);
	}

	public static void main(String[] args) {
		jessica_relation_extraction app = new jessica_relation_extraction();
		GatewayServer server = new GatewayServer(app);
		server.start();
		System.out.println("jessica relation extraction service started");
	}

	/*
	public static void main(String[] args) {
		jessica_relation_extraction app = new jessica_relation_extraction(",coref,kbp");
	}
	*/

}
/////////////jessica_relation_extraction.java////////
