from jessica_relation_extraction import relation_extraction

text = u"""
Jessica Liang works for Group 42 Inc. She was born in China. She studies at Heriot-Watt University. Jessica is married to Smith.
"""

for r in relation_extraction(text):
	if r['relation'] != 'mention':
		print(r)

for r in relation_extraction(text):
	if r['relation'] == 'mention':
		print(r)
