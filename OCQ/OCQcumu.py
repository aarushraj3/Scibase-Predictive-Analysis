import json
import os.path
import csv

path = []
directory = '/home/sourav/Documents/Temp_codes/Finalized_structure'
for filename in os.listdir(directory):
	if filename.endswith(".json"):
		x = os.path.join(directory, filename)
		path.append(x)
#print(path)
count_list=[0]
year=[]
quarter_1=[0,1,2,3,4,5,6,"January","February","March","April","May","June","Jan","Feb","Mar","Apr","Jun","Jan.","Feb.","Mar.","Apr.","Jun.","january","february","march","april","may","june","jan","feb","mar","apr","jun","jan.","feb.","mar.","apr.","jun.",None]
quarter_2=[7,8,9,10,11,12,"July","August","September","October","November","December","Jul.","Aug.","Sept.","Oct.","Nov.","Dec.","Jul","Aug","Sept","Oct","Nov","Dec","july","august","september","october","november","december","jul.","aug.","sept.","oct.","nov.","dec.","jul","aug","sept","oct","nov","dec"]

def pass_one(journal):
	ret=''
	with open(journal) as data_file:
		json1 = json.load(data_file)
	for key_1,value_1 in json1.items():
		ret=key_1
		for key_2,value_2 in value_1['Volumes'].items():					#volume level
			for key_3,value_3 in value_2.items():							#issue level
				for key_4,value_4 in value_3['date'].items():
					if key_4 == 'year' and value_4 not in year:
						year.append(value_4)
	year.sort()
	return ret





def pass_journal(journal,yr,qtr):
	count=0

	with open(journal) as data_file:
		json1 = json.load(data_file)
	for key_1,value_1 in json1.items():
		for key_2,value_2 in value_1['Volumes'].items():				#volume level
			value_1['Country']='united states'
			for key_3,value_3 in value_2.items():
				if value_3['date']['year'] == yr and value_3['date']['month'] in qtr :
					for key_4,value_4 in value_3['articles'].items():			#article level
						author=[]
						citation=[]
						for authors in value_4['authors']:
							author.append(authors['name'].lower())
						for citations in value_4['citations']:
							citation.append(citations['Name'].lower())
						for a in author:
							for cite in citation:
								if a in cite:
									#print "Author:",a
									citation.remove(cite)
									count+=1
	return count









for journal in path:
	name=pass_one(journal)
	name=name+'.csv'
	print name
	with open(name, 'a+') as filec:
		fieldnames = ['Year','Half1','Half2']
		writer = csv.DictWriter(filec, fieldnames=fieldnames)
		writer.writeheader()

		for yr in year:
			
			val1=pass_journal(journal,yr,quarter_1)
			count_list.append(count_list[-1]+val1)
			val2=pass_journal(journal,yr,quarter_2)
			count_list.append(count_list[-1]+val2)
			print(yr,val1,val2)
			writer.writerow({'Year':yr,'Half1':count_list[-2],'Half2':count_list[-1]})
	print count_list
	year=[]
	count_list=[0]

