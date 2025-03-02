from urllib.request import urlopen
from link_finder import LinkFinder
from urllib.parse import urlparse, parse_qs
from general import *

class Spider:

	project_name = ''
	base_url = ''
	domain_name = ''
	queue_file = ''
	crawled_file = '' 
	queue = set()
	crawled = set()

	def __init__(self, project_name, base_url, domain_name):
		Spider.project_name = project_name
		Spider.base_url = base_url
		Spider.domain_name = domain_name
		Spider.queue_file = Spider.project_name+"/queue.txt"
		Spider.crawled_file = Spider.project_name+"/crawled.txt"
		self.boot()
		self.crawl_page('First spider', Spider.base_url)

	''''''
	@staticmethod
	def extract_parameters(url):
		parsed_url = urlparse(url)
		params = parse_qs(parsed_url.query)  # Dictionary of parameters
		path = parsed_url.path if parsed_url.path else "/"  # Default to "/"
		if params:
			return path, params  # Return endpoint and params
		return None, None
	''''''

	@staticmethod
	def boot():
		create_project_dir(Spider.project_name)
		create_data_files(Spider.project_name, Spider.base_url)
		Spider.queue = file_to_set(Spider.queue_file)
		Spider.crawled = file_to_set(Spider.crawled_file)

	''' '''

	unique_params = set()  # Store unique parameter entries

	@staticmethod
	def crawl_page(spiderName, pageUrl):
		if pageUrl not in Spider.crawled:
			print(spiderName+ ' now crawling: ' +pageUrl)
			print('Queue: '+str(len(Spider.queue)) + ' | Crawled: '+str(len(Spider.crawled)))
			Spider.add_links_to_queue(Spider.gather_links(pageUrl))
			Spider.queue.remove(pageUrl)
			Spider.crawled.add(pageUrl)
			Spider.update_files()

			''''''
			endpoint, params = Spider.extract_parameters(pageUrl)
			if params:
				entry = f"{endpoint} -> {params}"
				if entry not in Spider.unique_params:
					Spider.unique_params.add(entry)  # Avoid duplicates
				Spider.save_parameters()  # Save after each crawl

	
	@staticmethod
	def save_parameters():
		set_to_file(Spider.project_name + "/parameters.txt", Spider.unique_params)  # Use general.py's function

	#Sorted structure (if set_to_file() was used, which sorts the entries).
	''''''


	@staticmethod
	def gather_links(pageUrl):
		html_string = ''
		try:
			response = urlopen(pageUrl)
			if 'text/html' in response.getheader('Content-Type'):
				html_bytes = response.read()
				print('html bytes')
				print(html_bytes)
				html_string = html_bytes.decode('utf-8')
			finder = LinkFinder(Spider.base_url, pageUrl)
			finder.feed(html_string)
		except:
			print('Error: can not crawl page')
			return set()

		return finder.page_links()


	@staticmethod
	def add_links_to_queue(links):
		for url in links:
			if url in Spider.queue:
				continue 
			if url in Spider.crawled:
				continue
			if Spider.domain_name not in url:
				continue
			Spider.queue.add(url)

	@staticmethod
	def update_files():
		set_to_file(Spider.queue_file, Spider.queue)
		set_to_file(Spider.crawled_file, Spider.crawled)









