/*
javac jessica_relation_extraction_main.java
java jessica_relation_extraction_main
*/

import java.util.*;
import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ie.util.*;
import edu.stanford.nlp.pipeline.*;

public class jessica_relation_extraction_main {

	public static void main(String[] args) {
		jessica_relation_extraction m = new jessica_relation_extraction();
		String text = "Smith's wife is Jessica. Jessica is working for Apple. Jessica is 23 years old.";
		List<String> outputs = m.relation_extraction(text);
		for(int i=0; i<outputs.size();i++){
			System.out.println(outputs.get(i));		
		}
	}

}
