# yan_relation_extraction_docker 

## start the service

```bash

docker build -t yanliang12/yan_relation_extraction:1.0.2 .

docker run -it yanliang12/yan_relation_extraction:1.0.2
```

## usage 

```python
>>> from jessica_relation_extraction import relation_extraction
>>>
>>> text = u"""
... Yan Liang is a student at Liverpool John Moores University. She lives in Abu Dhabi.
... """
>>>
>>> for r in relation_extraction(text):
...     if r['relation'] != 'mention':
...             print(r)
...
{'subject_name': 'Liverpool John Moores University', 'subject_type': 'ORGANIZATION', 'subject': '-3390477974305657385', 'object_name': 'Yan Liang', 'object_type': 'PERSON', 'object': '8353631198248842826', 'relation': 'top_members_employees'}
{'subject_name': 'Yan Liang', 'subject_type': 'PERSON', 'subject': '8353631198248842826', 'object_name': 'student', 'object_type': 'TITLE', 'object': '4652583983336114654', 'relation': 'title'}
{'subject_name': 'Yan Liang', 'subject_type': 'PERSON', 'subject': '8353631198248842826', 'object_name': 'Liverpool John Moores University', 'object_type': 'ORGANIZATION', 'object': '-3390477974305657385', 'relation': 'schools_attended'}
{'subject_name': 'Yan Liang', 'subject_type': 'PERSON', 'subject': '8353631198248842826', 'object_name': 'Abu Dhabi', 'object_type': 'CITY', 'object': '754441771943617307', 'relation': 'cities_of_residence'}
>>> 
>>> for r in relation_extraction(text):
...     if r['relation'] == 'mention':
...             print(r)
...
{'subject_name': 'Yan Liang is a student at Liverpool John Moores University.', 'subject_type': 'SENTENCE', 'subject': '2207712906784586127', 'relation': 'mention', 'object_name': 'Liverpool John Moores University', 'object_type': 'ORGANIZATION', 'object': '-3390477974305657385'}
{'subject_name': 'Yan Liang is a student at Liverpool John Moores University.', 'subject_type': 'SENTENCE', 'subject': '2207712906784586127', 'relation': 'mention', 'object_name': 'Yan Liang', 'object_type': 'PERSON', 'object': '8353631198248842826'}
{'subject_name': 'Yan Liang is a student at Liverpool John Moores University.', 'subject_type': 'SENTENCE', 'subject': '2207712906784586127', 'relation': 'mention', 'object_name': 'student', 'object_type': 'TITLE', 'object': '4652583983336114654'}
{'subject_name': 'She lives in Abu Dhabi.', 'subject_type': 'SENTENCE', 'subject': '5469523196361189012', 'relation': 'mention', 'object_name': 'Yan Liang', 'object_type': 'PERSON', 'object': '8353631198248842826'}
{'subject_name': 'She lives in Abu Dhabi.', 'subject_type': 'SENTENCE', 'subject': '5469523196361189012', 'relation': 'mention', 'object_name': 'Abu Dhabi', 'object_type': 'CITY', 'object': '754441771943617307'}
```

## entity linking

```bash
java -Xmx16g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,entitylink -file example.txt
```

output:

```bash
Document: ID=example.txt (1 sentences, 7 tokens)

Sentence #1 (7 tokens):
Joe Smith was born in Oregon.

Tokens:
[Text=Joe CharacterOffsetBegin=0 CharacterOffsetEnd=3 PartOfSpeech=NNP Lemma=Joe NamedEntityTag=PERSON WikipediaEntity=Joe_Smith_(basketball)]
[Text=Smith CharacterOffsetBegin=4 CharacterOffsetEnd=9 PartOfSpeech=NNP Lemma=Smith NamedEntityTag=PERSON WikipediaEntity=Joe_Smith_(basketball)]
[Text=was CharacterOffsetBegin=10 CharacterOffsetEnd=13 PartOfSpeech=VBD Lemma=be NamedEntityTag=O WikipediaEntity=O]
[Text=born CharacterOffsetBegin=14 CharacterOffsetEnd=18 PartOfSpeech=VBN Lemma=bear NamedEntityTag=O WikipediaEntity=O]
[Text=in CharacterOffsetBegin=19 CharacterOffsetEnd=21 PartOfSpeech=IN Lemma=in NamedEntityTag=O WikipediaEntity=O]
[Text=Oregon CharacterOffsetBegin=22 CharacterOffsetEnd=28 PartOfSpeech=NNP Lemma=Oregon NamedEntityTag=STATE_OR_PROVINCE WikipediaEntity=Oregon]
[Text=. CharacterOffsetBegin=28 CharacterOffsetEnd=29 PartOfSpeech=. Lemma=. NamedEntityTag=O WikipediaEntity=O]

Extracted the following NER entity mentions:
Joe Smith	PERSON	PERSON:0.9994280560852734
Oregon	STATE_OR_PROVINCE	LOCATION:0.9982464307494803
```
