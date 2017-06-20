from urllib import parse

url1 = 'http://www.google.com/212.html/thfghfg'
url2 = '../../1.html'

print(parse.urljoin(url1, url2))
