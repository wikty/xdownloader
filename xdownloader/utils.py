import re, os
from urllib.parse import urlparse


def unique_filename(filename):
	count = 1
	name, ext = os.path.splitext(filename)
	while os.path.exists(filename):
		filename = '{}{}{}'.format(name, count, ext)
		count += 1
	return filename

def filter_filename(filename):
	filename = re.sub(r'\n', ' ', filename)
	return re.sub(r'[^\.)(_\w\d\s-]', ' ', filename)

def get_domain(url):
	return urlparse(url).netloc

def str2dict(s, item_separator=';', key_separator='=', quote='"'):
	'''
	inline; filename="test.png"; something;
	'''
	regex = re.compile(r'(?P<key>\w+)(\s*=\s*(?P<quote>[\'"]?)(?P<value>.+?)(?P=quote))?(;|$)')
	d = {}
	s = s.strip()
	while s:
		m = regex.match(s)
		if not m:
			return None
		d[m.groupdict()['key']] = m.groupdict()['value']
		s = s[m.end():].strip()
	return d