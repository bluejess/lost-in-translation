import csv
import six
from google.cloud import translate_v2 as translate

def translate_text(target, text):
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)
    result["translatedText"].replace("&#39;'", " i")
    return result["translatedText"]

def get_pronoun(translation):
	try:		
		female_markers = ["she", "she's", "her"]
		male_markers = ["he", "he's", "his"]
		neuter_markers = ["it","it's","its","they","they're","them","who","this","that"]
		
		has_any = lambda markers, translation: any( [ marker.lower() in translation.lower().split() for marker in markers ] )

		if( has_any(female_markers, translation)):
			return 'Feminine' # Suggestion: (1,0,0)
		elif( has_any(male_markers, translation)):
			return 'Masculine' # Suggestion: (0,1,0)
		elif( has_any(neuter_markers, translation) ):
			return 'Neutral' # Suggestion: (0,0,1)
	except:
		return 'Unknown'
     
do_adj = False
do_two_adj = False
do_occ = False
do_adj_occ = False
do_both = False
do_translation = False

if do_adj:
	adjectives = list(csv.reader(open('adjectives/adjectives.tsv','r'), delimiter='\t'))
	with open('Results/result-adj.tsv','w') as output:
		output.write("Adjective English")
		output.write("\tAdjective Swedish")
		output.write("\tAdjective Gender Category")
		output.write("\tAdjective Quality")
		output.write("\tAdjective Translated Sentence")
		output.write("\tAdjective Translated Pronoun")
		output.write('\n')

		for entry in adjectives[1:]:

			adj_english 		= entry[0]
			adj_swedish			= entry[1]
			adj_gender 			= entry[2]
			adj_quality 		= entry[4]
   
			output.write(adj_english)
			output.write('\t' + adj_swedish)
			output.write('\t' + adj_gender)
			output.write('\t' + adj_quality)	
   
			phrase = "hen är %s " % adj_swedish
 
			translated_sentence = translate_text('en', phrase).lower()
			print("Phrase: {} | Translation: {}".format(phrase, translated_sentence))

			output.write('\t' + translated_sentence)			
			translated_pronoun = get_pronoun(translated_sentence)
			output.write('\t' + translated_pronoun)
			output.write('\n')
			output.flush()

if do_two_adj:
	adjectives_result = list(csv.reader(open('Results/result-adj.tsv','r'), delimiter='\t'))
	with open('Results/result-two-adj.tsv','w') as output:
		output.write("First Adjective English")
		output.write("\tFirst Adjective Swedish")
		output.write("\tFirst Adjective Gender Category")
		output.write("\tFirst Adjective Quality")
		output.write("\tFirst Adjective Translated Pronoun")
		output.write("\tSecond Adjective English")
		output.write("\tSecond Adjective Swedish")
		output.write("\tSecond Adjective Gender Category")
		output.write("\tSecond Adjective Quality")
		output.write("\tSecond Adjective Translated Pronoun")
		output.write("\tCombination Category")
		output.write("\tBoth Adjectives Translated Sentence")
		output.write("\tBoth Adjectives Translated Pronoun")
		output.write('\n')

		for entry in adjectives_result[1:]:

			adj_english 		= entry[0]
			adj_swedish			= entry[1]
			adj_gender 			= entry[2]
			adj_quality 		= entry[3]
			adj_pronoun			= entry[5]
   
   
			for entry in adjectives_result[1:]:

				sec_adj_english			= entry[0]
				sec_adj_swedish			= entry[1]
				if (sec_adj_swedish != adj_swedish):
					sec_adj_gender 			= entry[2]
					sec_adj_quality 		= entry[3]
					sec_adj_pronoun			= entry[5]

					output.write(adj_english)
					output.write('\t' + adj_swedish)
					output.write('\t' + adj_gender)
					output.write('\t' + adj_quality)	
					output.write('\t' + adj_pronoun)
					output.write('\t' + sec_adj_english)
					output.write('\t' + sec_adj_swedish)
					output.write('\t' + sec_adj_gender)
					output.write('\t' + sec_adj_quality)
					output.write('\t' + sec_adj_pronoun)
   
					phrase = "hen är {} och {}".format(adj_swedish, sec_adj_swedish)
 
					translated_sentence = translate_text('en', phrase).lower()
					print("Phrase: {} | Translation: {}".format(phrase, translated_sentence))

					combination_category = adj_pronoun[0] + sec_adj_pronoun[0]
					output.write('\t' + combination_category)
					output.write('\t' + translated_sentence)			
					translated_pronoun = get_pronoun(translated_sentence)
					output.write('\t' + translated_pronoun)
					output.write('\n')
			output.flush()

if do_occ:
	occupations = list(csv.reader(open('occupations/occupations.tsv','r'), delimiter='\t'))
	with open('Results/result-occ.tsv','w') as output:
		output.write("Occupation English")
		output.write("\tOccupation Swedish")
		output.write("\tOccupation Gender Category")
		output.write("\tOccupation US Gender Category")
		output.write("\tOccupation Sweden Gender Category")
		output.write("\tOccupation Translated Sentence")
		output.write("\tOccupation Translated Pronoun")
		output.write('\n')

		for entry in occupations[1:]:

			occ_english				= entry[0]
			occ_swedish 			= entry[1]
			occ_gender 				= entry[2]
			occ_us_gender 			= entry[3]
			occ_sweden_gender		= entry[4]
   
			output.write(occ_english)
			output.write('\t' + occ_swedish)
			output.write('\t' + occ_gender)
			output.write('\t' + occ_us_gender)
			output.write('\t' + occ_sweden_gender)
   
			phrase = "hen är %s" % occ_swedish
 
			translated_sentence = translate_text('en', phrase).lower()
			print("Phrase: {} | Translation: {}".format(phrase, translated_sentence))
			output.write('\t' + translated_sentence)			
			translated_pronoun = get_pronoun(translated_sentence)
			output.write('\t' + translated_pronoun)		
   	
			output.write('\n')
			output.flush()

if do_adj_occ:
	adjectives_result = list(csv.reader(open('Results/result-adj.tsv','r'), delimiter='\t'))
	with open('Results/result-adj-occ.tsv','w') as output:
		output.write("Adjective English")
		output.write("\tAdjective Swedish")
		output.write("\tAdjective Gender Category")
		output.write("\tAdjective Quality")
		output.write("\tAdjective Translated Pronoun")
		output.write("\tOccupation English")
		output.write("\tOccupation Swedish")
		output.write("\tOccupation Gender Category")
		output.write("\tOccupation US Gender Category")
		output.write("\tOccupation Sweden Gender Category")
		output.write("\tOccupation Translated Pronoun")
		output.write("\tCombination Category")	
		output.write("\tTranslated Sentence")
		output.write("\tTranslated Pronoun")
		output.write('\n')

		for entry in adjectives_result[1:]:
			adj_english 		= entry[0]
			adj_swedish			= entry[1]
			adj_gender			= entry[2]
			adj_quality			= entry[3]
			adj_pronoun			= entry[5]
   
			occupation_result = list(csv.reader(open('Results/result-occ.tsv','r'), delimiter='\t'))
			for entry in occupation_result[1:]:
    
				occ_english			= entry[0]
				occ_swedish 		= entry[1]
				occ_gender			= entry[2]
				occ_us_gender 		= entry[3]
				occ_swe_gender		= entry[4]
				occ_pronoun			= entry[6]
            
				output.write(adj_english)
				output.write('\t' + adj_swedish)
				output.write('\t' + adj_gender)
				output.write('\t' + adj_quality)
				output.write('\t' + adj_pronoun)
	
				phrase = "hen är en {} {}".format(adj_swedish, occ_swedish)
	
				translated_sentence = translate_text('en', phrase).lower()
				print("Phrase: {} | Translation: {}".format(phrase, translated_sentence))
				translated_pronoun = get_pronoun(translated_sentence)
    
				output.write('\t' + occ_english)
				output.write('\t' + occ_swedish)
				output.write('\t' + occ_gender)
				output.write('\t' + occ_us_gender)
				output.write('\t' + occ_swe_gender)
				output.write('\t' + occ_pronoun)
    
				combination_category = adj_pronoun[0] + occ_pronoun[0]
				output.write('\t' + combination_category)
				output.write('\t' + translated_sentence)	
				output.write('\t' + translated_pronoun)		
				output.write('\n')
				output.flush()

