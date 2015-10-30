#!/usr/bin/env python
import requests
from lxml import html
import json #for the google search
import urllib # for the google search 
import time
import email_extractor as e #for the email extract
from collections import defaultdict #for the email extract 
import os.path #for output file deletion

class MipCrawler:
	def __init__(self,starting_url,depth):
		self.starting_url=starting_url
		self.depth=depth
		self.companies=[]
		self.company_link=[]
		self.email_out=[]

	def crawl(self):
	
		cmpn=self.get_company_from_link(self.starting_url)
		self.companies.extend(cmpn.company_name)

		print "*Finished Extracting the company names"
		#print(self.companies)
		
		link=self.get_company_from_google(self.companies)
		#link=['http://www.mediafrance.eu/']
		self.company_link.extend(link)
		print "*Finished google search for company names"
		#print(self.company_link)
		

		#to get the email from the company website 
		#print(self.company_link)
		
		email=self.get_email_from_link(self.company_link,self.depth)
		self.email_out.extend(email)
		print "*Finished extracting emails"
		#print(self.email_out)
		self.put_email_to_file(self.email_out)
		print "*Fininshed writing emails to file <output.txt>"
	
	def get_company_from_link(self,link):
		start_page=requests.get(link)
		tree=html.fromstring(start_page.text)
		name=tree.xpath('//h3[@class="name"]//a/text()')
		#for item in name:
		#	print(item)
		cmpn=Company(name)
		return cmpn

	def get_company_from_google(self,company_list):
		link=[]
		#loc_list=['"MCFIVA (THAILAND) CO.,LTD."','"MIR" INTERGOVERNMENTAL TV AND RADIO.']
		for cmpn in company_list:
			query = urllib.urlencode({'q': cmpn.encode("utf-8")})
  			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  			search_response = urllib.urlopen(url)
  			search_results = search_response.read()
  			results = json.loads(search_results)
  			data = results['responseData']
  			hits = data['results']
  			link.append((hits[0]['url']).encode("utf-8"))
  			link.append((hits[1]['url']).encode("utf-8"))
			time.sleep(35)
		return link 

	def get_email_from_link(self,link,depth):
		email_link=[]
		print "Starting email extraction >>>>>>"
		emails = defaultdict(int)
		for site in link:
			for url in e.crawl_site('%s' %site, depth):
				for email in e.grab_email(e.urltext(url)):
					if not emails.has_key(email):
						if('reedmidem.com' in email):
							continue
						else:
							email_link.append(email)
		return email_link

	def put_email_to_file(self,email):
		data=open("output.txt",'a')
		for e in email:
			data.write(e)
			data.write("\n")
		data.close()

	

class Company:

	def __init__(self,company_name):
		self.company_name=company_name

	#def __str__(self):
	#	return str(self.company_name)

if __name__ == '__main__':
	if os.path.isfile("output.txt"):
		os.remove("output.txt")
	base_url='http://www.my-mip.com/en/online-database/mipcom/companies/?rpp=64&startRecord='
	batch=0
	start_record=1
	while start_record < 65:
		print "Batch:%d"%(batch+1)
		crawler=MipCrawler('%s' %base_url+str(start_record),10)
		crawler.crawl()
		batch+=1
		start_record+=64

