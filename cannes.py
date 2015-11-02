#!/usr/bin/env python
import requests
from lxml import html
import json #for the google search
import urllib # for the google search 
import time
import email_extractor as e #for the email extract
from collections import defaultdict #for the email extract 
import os.path #for output file deletion
import sys #for passing the command line arguments 
class MipCrawler:
	def __init__(self,file,depth):
		self.input_file=file
		self.depth=depth
		self.companies=[]
		self.company_link=[]
		self.email_out=[]

	def crawl(self):
	
		cmpn=self.get_company_from_file(self.input_file)
		self.companies.extend(cmpn)

		print "*Loaded the company names from file"
		#print(self.companies)

		self.get_company_from_google(self.companies)



		#link=['http://www.mediafrance.eu/']
		#self.company_link.extend(link)
		#print "*Finished google search for company names"
		#print(self.company_link)
		

		#to get the email from the company website 
		#print(self.company_link)
		
		#email=self.get_email_from_link(self.company_link,self.depth)
		#self.email_out.extend(email)
		#print "*Finished extracting emails"
		#print(self.email_out)
		#self.put_email_to_file(self.email_out)
		#print "*Fininshed writing emails to file <output.txt>"

	def get_company_from_file(self,file_name):
		compn=[]
		with open(file_name) as file:
			compn=file.read().splitlines()
		return compn

	def get_company_from_google(self,company_list):
		#link=[]
		#loc_list=['"MCFIVA (THAILAND) CO.,LTD."','"MIR" INTERGOVERNMENTAL TV AND RADIO.']
		for cmpn in company_list:
			print "Searching emails for : %s" %cmpn
			query = urllib.urlencode({'q': cmpn})
  			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  			search_response = urllib.urlopen(url)
  			search_results = search_response.read()
  			results = json.loads(search_results)
  			if 	results is not None:
  				data = results['responseData']
  				hits = data['results']
  				for h in hits:
  					#print h['url']	
					#link.append((h['url']).encode("utf-8"))
					link=(h['url']).encode("utf-8")
					if  not "imdb" or "facebook" or "youtube" or "linkedin" or "wikipedia" in link:
						print link
						email=self.get_email_from_link(link,self.depth)
						self.put_email_to_file(email)
			else:
				continue
	def get_email_from_link(self,link,depth):
		email_link=[]
		print "Extracting emails >>>>>>"
		emails = defaultdict(int)
		for url in e.crawl_site('%s' %link, depth):
			try:
				for email in e.grab_email(e.urltext(url)):
					if not emails.has_key(email):
						if('reedmidem.com' in email):
							continue
						else:
							email_link.append(email)
			except:
				continue
		return email_link

	def put_email_to_file(self,email):
		data=open("output.txt",'a')
		for e in email:
			data.write(e)
			data.write("\n")
		data.close()

	
if __name__ == '__main__':
	if not len(sys.argv) >1:
		print "please pass the input file !"
		sys.exit(0)
	else:
		if os.path.isfile("output.txt"):
			os.remove("output.txt")
		input_file=sys.argv[-1]
		crawler=MipCrawler(input_file,10)
		crawler.crawl()
