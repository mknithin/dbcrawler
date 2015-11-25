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
	def __init__(self,starting_url,depth,start_record):
		self.starting_url=starting_url
		self.depth=depth
		self.companies=[]
		self.company_link=[]
		self.email_out=[]
		self.start_record=start_record

	def crawl(self):
	
		cmpn=self.get_company_from_link(self.starting_url)
		self.companies.extend(cmpn.company_name)

		print "*Finished Extracting the company names"
		#print(self.companies)
		
		self.get_company_from_google(self.companies)
		'''
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
		'''
	
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
		cmpn_no=1
		#loc_list=['"MCFIVA (THAILAND) CO.,LTD."','"MIR" INTERGOVERNMENTAL TV AND RADIO.']
		for cmpn in company_list:
			print "--------------------------------------------------------"
			print "Google Search for : %d.%s(track:%d)" %(cmpn_no,cmpn,(self.start_record+(cmpn_no-1)))
			query = urllib.urlencode({'q': cmpn.encode("utf-8")})
  			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  			search_response = urllib.urlopen(url)
  			search_results = search_response.read()
  			results = json.loads(search_results)
  			if 	results is not None:
	  			data = results['responseData']
	  			hits = data['results']
	  			for h in hits:
	  				#link.append((hits[0]['url']).encode("utf-8"))
	  				#link.append((hits[1]['url']).encode("utf-8"))
	  				link=(h['url']).encode("utf-8")
	  				if  "imdb"  in link or "facebook" in link or "youtube" in link or "linkedin" in link or "wikipedia" in link or "my-mip" in link:
							continue
	  				print link
	  				email=self.get_email_from_link(link,self.depth)
	  				if email is not None:
						self.put_email_to_file(email)
			else:
				continue
			cmpn_no+=1
	def get_email_from_link(self,link,depth):
		email_link=[]
		print "Extracting emails from %s" %link
		try:
			emails = defaultdict(int)
			for url in e.crawl_site('%s' %link, depth):
				for email in e.grab_email(e.urltext(url)):
					if not emails.has_key(email):
						if('reedmidem.com' in email or '.png' in email or '.jpg' in email):
								continue
						else:
							email_link.append(email)
		except:
			print "Socket connection error"
			email_link=''
			return email_link
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
	base_url='http://my.midem.com/en/online-database/companies/?rpp=64&startRecord='
	batch=0
	start_record=1
	while start_record < 2203:
		print "Batch:%d Start_record:%d"%((batch+1),start_record)
		crawler=MipCrawler('%s' %base_url+str(start_record),10,start_record)
		crawler.crawl()
		batch+=1
		start_record+=64