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
		print "*Finished google serach for company names"
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
			query = urllib.urlencode({'q': cmpn})
  			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  			search_response = urllib.urlopen(url)
  			search_results = search_response.read()
  			results = json.loads(search_results)
  			data = results['responseData']
  			hits = data['results']
			link.append((hits[0]['url']).encode("utf-8"))
			time.sleep(35)
		return link 

	def get_email_from_link(self,link,depth):
		email_link=[]
		print "Starting email extraction >>>>>>"
		emails = defaultdict(int)
		for site in link:
			for url in e.crawl_site('%s' %site, depth):
				for email in e.grab_email(e.urltext(url)):
					if not emails.has_key(email):email_link.append(email)
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
	base_url='http://www.my-mip.com/online-database/mipcom/companies/#search='
	page_urls=['rpp%3D64','rpp%3D64%26startRecord%3D65', 'startRecord%3D129%26rpp%3D64',
				 'startRecord%3D193%26rpp%3D65',
				 'startRecord%3D257%26rpp%3D66',
				 'startRecord%3D321%26rpp%3D67',
				 'startRecord%3D385%26rpp%3D68',
				 'startRecord%3D449%26rpp%3D69',
				 'startRecord%3D513%26rpp%3D70',
				 'startRecord%3D577%26rpp%3D71',
				 'startRecord%3D641%26rpp%3D72',
				 'startRecord%3D705%26rpp%3D73',
				 'startRecord%3D769%26rpp%3D74',
				 'startRecord%3D833%26rpp%3D75',
				 'startRecord%3D897%26rpp%3D76',
				 'startRecord%3D961%26rpp%3D77',
				 'startRecord%3D1025%26rpp%3D78',
				 'startRecord%3D1089%26rpp%3D79',
				 'startRecord%3D1153%26rpp%3D80',
				 'startRecord%3D1217%26rpp%3D81',
				 'startRecord%3D1281%26rpp%3D82',
				 'startRecord%3D1345%26rpp%3D83',
				 'startRecord%3D1409%26rpp%3D84',
				 'startRecord%3D1473%26rpp%3D85',
				 'startRecord%3D1537%26rpp%3D86',
				 'startRecord%3D1601%26rpp%3D87',
				 'startRecord%3D1665%26rpp%3D88',
				 'startRecord%3D1729%26rpp%3D89',
				 'startRecord%3D1793%26rpp%3D90',
				 'startRecord%3D1857%26rpp%3D91',
				 'startRecord%3D1921%26rpp%3D92',
				 'startRecord%3D1985%26rpp%3D93',
				 'startRecord%3D2049%26rpp%3D94',
				 'startRecord%3D2113%26rpp%3D95',
				 'startRecord%3D2177%26rpp%3D96',
				 'startRecord%3D2241%26rpp%3D97',
				 'startRecord%3D2305%26rpp%3D98',
				 'startRecord%3D2369%26rpp%3D99',
				 'startRecord%3D2433%26rpp%3D100',
				 'startRecord%3D2497%26rpp%3D101',
				 'startRecord%3D2561%26rpp%3D102',
				 'startRecord%3D2625%26rpp%3D103',
				 'startRecord%3D2689%26rpp%3D104',
				 'startRecord%3D2753%26rpp%3D105',
				 'startRecord%3D2817%26rpp%3D106',
				 'startRecord%3D2881%26rpp%3D107',
				 'startRecord%3D2945%26rpp%3D108',
				 'startRecord%3D3009%26rpp%3D109',
				 'startRecord%3D3073%26rpp%3D110',
				 'startRecord%3D3137%26rpp%3D111',
				 'startRecord%3D3201%26rpp%3D112',
				 'startRecord%3D3265%26rpp%3D113',
				 'startRecord%3D3329%26rpp%3D114',
				 'startRecord%3D3393%26rpp%3D115',
				 'startRecord%3D3457%26rpp%3D116',
				 'startRecord%3D3521%26rpp%3D117',
				 'startRecord%3D3585%26rpp%3D118',
				 'startRecord%3D3649%26rpp%3D119',
				 'startRecord%3D3713%26rpp%3D120',
				 'startRecord%3D3777%26rpp%3D121',
				 'startRecord%3D3841%26rpp%3D122',
				 'startRecord%3D3905%26rpp%3D123',
				 'startRecord%3D3969%26rpp%3D124',
				 'startRecord%3D4033%26rpp%3D125',
				 'startRecord%3D4097%26rpp%3D126',
				 'startRecord%3D4161%26rpp%3D127',
				 'startRecord%3D4225%26rpp%3D128',
				 'startRecord%3D4289%26rpp%3D129',
				 'startRecord%3D4353%26rpp%3D130',
				 'startRecord%3D4417%26rpp%3D131',
				 'startRecord%3D4481%26rpp%3D132',
				 'startRecord%3D4545%26rpp%3D133',
				 'startRecord%3D4609%26rpp%3D134',
				 'startRecord%3D4673%26rpp%3D135',
				]
	batch=0
	for url in page_urls:
		print "Batch:%d"%(batch+1)
		crawler=MipCrawler('%s' %base_url+url,5)
		crawler.crawl()
		batch+=1

