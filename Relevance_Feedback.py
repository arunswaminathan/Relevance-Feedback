from __future__ import division
import urllib2
import base64
from xml.dom import minidom
import re
import nltk
import math
import sys
import operator as itertiems
import operator as itemgetter
import operator
from collections import OrderedDict


final_query=''
countAllOnes=0
#Words to be ignored
stop=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
punctuation = re.compile(r'[.?!,":;]') 
query=''

#Get BING Key
accountKey = str(sys.argv[1])

# Get target value from command line
target=float(sys.argv[2])

#Get query from command line
i=3
for arg in sys.argv[3:]:
	query=query + '+' + str(sys.argv[i])
	i+=1
query=query[1:]
query=query.replace("'","")
query=query.replace(" ","+")


OD={}
weight={}

#Queries the bing api and fetches the results
def query_ask(query):
	bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'+query+'%27&$top=10&$format=Atom'
	# accountKey = 'pZyOYhNovB61fTsh3yf6QW6sVCbldiH2QLctVAk2zyw'
	accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
	headers = {'Authorization': 'Basic ' + accountKeyEnc}
	req = urllib2.Request(bingUrl, headers = headers)
	response = urllib2.urlopen(req)
	content1 = response.read()

	#Write output from BingAPI to xml file
	with open('file.xml', 'w') as the_file:
		the_file.write(content1)
	parse()
	
#Parse the XML file to obtain title, URL and description
def parse():
	result=[]
	xmldoc = minidom.parse('file.xml')
	itemlist = xmldoc.getElementsByTagName('content') 
	for s in itemlist :
		properties = s.getElementsByTagName('m:properties')[0]
		each = []
		each.append(properties.getElementsByTagName('d:Title')[0].firstChild.nodeValue)
		each.append(properties.getElementsByTagName('d:Url')[0].firstChild.nodeValue)
		each.append(properties.getElementsByTagName('d:Description')[0].firstChild.nodeValue)
		result.append(each)
	feedback(result)
	index(result)

#Function to calculate tf-idf of the terms
def index(result):
	corpus=[] #Holds the 
	tfdic={}
	tfidf={}
	df={}
	new_toklist=[]
	new_tokdoc=[]
	for value in result:
		corpus.append(value[0]+" "+value[2])
	for text in corpus:
		toklist=nltk.word_tokenize(text)
		for word in toklist:
			word=word.lower()
			if word not in stop and word not in new_toklist:
				word=punctuation.sub("",word)
				if word!='':
					new_toklist.append(word)
	
	for text in corpus:
		temp=[]
		tokdoc=nltk.word_tokenize(text)
		for word in tokdoc:
			word=word.lower()
			if word not in stop:
				word=punctuation.sub("",word)
				if word!='':
					temp.append(word)
		new_tokdoc.append(temp)

	for word in new_toklist:
		i=1
		lis=[]
		for word1 in new_tokdoc:
			freq=0
			for word2 in word1:
				if word==word2:
					freq=freq+1
			lis.append([i,freq])
			i=i+1
		tfdic[word]=lis
	

	k=[]

	#TF-IDF is calculated here 
	for word in new_toklist:
		k=[]
		for i in range(0,10):
			tf=0
			df=0
			x=tfdic[word]
			tf=int(x[i][1])/len(new_tokdoc[i]);
			for l in new_tokdoc:
				if word in l:
					df=df+1	
			idf=math.log(10/df)	
			k.append(tf*idf)
		tfidf[word]=k
	rocchio(new_toklist,tfidf)	

#Rocchio algorithm is implemented here
def rocchio(new_toklist,tfidf):
	relevantwt={}
	nonrelevantwt={}

	for word in new_toklist:  #this calculates the relevant and non relevant weights of each of the words and stores in the dictionary relevantwt and nonrelevantwt
		
		relwt=0
		nonrelwt=0
		relcount=0
		nonrelcount=0
		templist=[]
		templist=tfidf[word]
		b=0.17
		c=0.25
		for i in range(0,10):
			if response[i]==1:
				relwt+=float(templist[i])
				relcount = relcount+1
			else:
				nonrelwt+=float(templist[i])
				nonrelcount=nonrelcount+1
		
		if relcount==0:
			relevantwt[word]=0
		else:
			relevantwt[word]=float(relwt / relcount)
		
		if nonrelcount==0:
			nonrelevantwt[word]=0
		else:
			nonrelevantwt[word]=float(nonrelwt/nonrelcount)
		
		weight[word]=float(b *relevantwt[word]) - float(b * nonrelevantwt[word])
		
	sort_a = sorted(weight.iteritems(), key=operator.itemgetter(1), reverse=True)
	#print sort_a[0][0], sort_a[1][0], target*10, len(relevant)
	global final_query
	#Repeat process if target precision has not been reached
	if target*10 > len(relevant):
		
		print "Target percision not reached. Next iteration with added words " + sort_a[0][0] + " and " + sort_a[1][0] 
		print "--------------------------------------"



		new_query = query + "+" + sort_a[0][0] + "+" + sort_a[1][0]
		final_query = query.replace("+"," ") + " " + sort_a[0][0] + " " + sort_a[1][0]
		query_ask(new_query)
	else:
		if countAllOnes==10:
			print "Precision value reached with query: '" + query.replace("+"," ") +"'"
		else:
			print "Precision value reached with query: '" + final_query +"'"
		print "--------------------------------------"
		print "END"

#Gets user feedback thru the command line on the relevancy of each query result
def feedback(result):
	global response
	response=[]
	global relevant
	relevant=[]
	irrelevant=[]
	rfreq={}
	ifreq={}
	count = 0
	global countAllOnes
	for value in result:
		print("Title: "+value[0])
		print("")
		print("URL: "+value[1])
		print("")
		print("Description: "+value[2])
		print("")


		k=raw_input("Enter 1 for Relevant 0 for Non-relevant : ")
		while(1):
			if(k=='0' or k=='1'):
				break;
			else:
				print("Invalid Input Enter again")
				k=raw_input("Enter 1 for Relevant 0 for Non-relevant : ")
		if(k=='1'):
			relevant.append(value)
			response.append(int(k))
			countAllOnes+=1
			# print response
		if(k=='0'):
			irrelevant.append(value)
			response.append(int(k))
			count+=1
			# print response
		if count==10:
			print "--------------------------------------"
			print "Expected target: " + str(target)
			print "Achieved target: " + str(len(relevant)/10)
			print "No relevant queries. Exiting program."
			exit()
	print "--------------------------------------"
	print "Expected target: " + str(target)
	print "Achieved target: " + str(len(relevant)/10)
    
query_ask(query)


