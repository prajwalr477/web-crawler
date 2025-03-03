from html.parser import HTMLParser
from urllib import parse 


class LinkFinder(HTMLParser):
	def __init__(self, base_url, page_url):
		super().__init__()
		self.base_url = base_url
		self.page_url = page_url
		self.links = set()

	def error(self, message):
		pass
	
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for (attribute, value) in attrs:
				if attribute == 'href' and value:
					url = parse.urljoin(self.base_url, value.strip())  # Remove extra spaces
					if url.startswith("http"):  # Ensure it's a valid absolute URL
						self.links.add(url)


	def page_links(self):
		return self.links
