import glob 
import re
import os.path
import json
import csv



def SELF_CITE(journal_data):
	j_count=0
	count=0
	citations=[]
	
	for key_0, value in journal_data.items():
		total_count=0
		for key_1,value_1 in value.items():
				if key_1 == 'Volumes':
					for key_2,value_2 in value_1.items():
						#print key_2
						for key_3,value_3 in value_2.items():
							#print key_3
							for key_4,value_4 in value_3.items():
								if key_4 == 'articles':
									for key_5,value_5 in value_4.items():
										#print key_5
										for key_6,value_6 in value_5.items():
											author=[]
											if key_6 == 'authors':
												
												for ele in value_6:
													for key in ele:
														if(key == "name"):
															author.append(ele[key])
												
											if key_6 == 'citations':
												citations=[]
												for item in value_6:
													item1=item['Name'].lower()
													citations.append(item1)
												
												#print citations
																								
											for a in author:
													for cite in citations:
														if(a in cite):
															#print "Author:",a
															citations.remove(cite)
									
															total_count=total_count+1
															count=count+1												
										journal_data[key_0][key_1][key_2][key_3][key_4][key_5].update({"self citation":count})
																																				
										j_count = j_count + count
										count=0						
											
							journal_data[key_0][key_1][key_2][key_3].update({"Journal self citation":j_count})							
							j_count=0
		journal_data[key_0]['Self Citation']=total_count
		print key_0,":",total_count
	
	with open(path,'w') as data_file:
		json.dump(journal_data,data_file)



print "Selftest.py"
'''with open('./self citation list.csv') as journal_file:
	journal_name = csv.reader(journal_file)
for row in journal_name:
	j_name = row[0]
	journal=j_name + ".json"
	#Change the path according to your local system'''
path=os.path.join('/home/sourav/Documents/Temp_codes/Finalized_structure/JACM.json') 
with open(path) as data_file:
	journal_data=json.load(data_file)
	SELF_CITE(journal_data)

