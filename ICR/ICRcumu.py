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
inationality=[]
jnationality={}
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
#for journal in path:

def final_computation(jnationality,inationality):
	one=0
	zero=0
	cml=0.0
	c=0
	for key,value in jnationality.items():
		if value ==1:
			one+=1
		if value == 0:
			zero+=1
	
	for ele in inationality:
		cml+=ele
	if one == 0 and zero ==0:

		if len(inationality) == 0:
			print 'l2'
			return 0.5*0+.5*0												#clarification needed
		else:
			print 'l1'
			return 0.5*0+0.5*(cml/len(inationality))						#clarification needed
	else:
		return 0.5*(one/(one+zero))+0.5*(cml/len(inationality))

def pass_journal(journal,yr,qtr):
	with open(journal) as data_file:
		json1 = json.load(data_file)
	for key_1,value_1 in json1.items():
		for key_2,value_2 in value_1['Volumes'].items():				#volume level
			value_1['Country']='united states'
			for key_3,value_3 in value_2.items():
				if value_3['date']['year'] == yr and value_3['date']['month'] in qtr :
						for key_4,value_4 in value_3['articles'].items():			#article level
							cnty_list=[]
							a=0
							for ele_1 in value_4['affiliation_data']:				#author affiliation level
								a+=1
								#print ele_1['country']
								if ele_1['country'] is not None:
									if ele_1['country'].lower() == value_1['Country'] or ele_1['country']==None:	#journal internationality
										jnationality[ele_1['Name']]=0			#considering authors from country none are from journal country
									else:
										jnationality[ele_1['Name']]=1
									if ele_1['country'].lower() not in cnty_list:
										cnty_list.append(ele_1['country'].lower())
							if a>1 or len(cnty_list)>1:
								inationality.append(float(len(cnty_list))/a)
							else:
								inationality.append(0)
		return final_computation(jnationality,inationality)

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
			val2=pass_journal(journal,yr,quarter_2)
			print(yr,val1,val2)
			writer.writerow({'Year':yr,'Half1':val1,'Half2':val2})
	year=[]
	jnationality={}
	inationality=[]