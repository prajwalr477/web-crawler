from urllib.parse import urlparse

def get_domain_name(url):
    try:
        domain = urlparse(url).netloc
        parts = domain.split('.')
        if len(parts) > 2:  # Handles subdomains properly
            return ".".join(parts[-2:])
        return domain  # Fallback
    except:
        return ''

def get_sub_domain_name(url):
	try:
		return urlparse(url).netloc
	except:
		return ''


#print(get_domain_name('https://www.youtube.com/watch?v=PPonGS2RZNc&index=14&list=PL6gx4Cwl9DGA8Vys-f48mAH9OKSUyav0q'))