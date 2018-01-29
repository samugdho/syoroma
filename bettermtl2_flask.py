#better mtl maker
import time, random
from bs4 import BeautifulSoup
import requests
import threading
from pykakasi import kakasi,wakati
import tinysegmenter
import re 

doChapters = True
doChapOnly = False
chapnames = []
rlist = (('…', '...'))


REQ={}
repSyo = (('…','...'),('「','<qs1>'),('」','<qs2>'),('『','<qs3>',),('』','<qs4>',),('１','1'), ('２','2'), ('３','3'), ('４','4'), ('５','5'), ('６','6'), ('７','7'), ('８','8'), ('９','9'),)



gtest= [0]
def test(n):
	if n == gtest[0]:
		return 'Same' + str(n)
	else:
		gtest[0] = n
		return 'different' + str(n)

		
def getter(link):
	# get syosetu text
	#driver.get(input("Enter syosetu chapter link: "))
	ttt = time.time()
	r = requests.get(link)
	r.encoding = 'utf-8'
	data = r.text
	soup = BeautifulSoup(data,'html.parser')
	rtext = soup.find_all(class_='novel_subtitle')[0].text
	rtext = rtext+'\n'+soup.find(id='novel_honbun').text
		
	# get romaji
	
	
	
	
	romaji_link = 'http://nihongo.j-talk.com/'


	r = requests.get(romaji_link)
	soup = BeautifulSoup(r.content, 'html.parser')
	d = soup.select('#formwrap > form > input[type="hidden"]')
	timestamp = d[0]['value']
	uniqid = d[1]['value']
	kanji = rtext


	headers = {
		"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"


	}




	data = {
		'timestamp' : timestamp,
		'uniqid' : uniqid,
		'kanji' : kanji,
		'Submit' : 'Translate Now',
		'kana_output' : 'romaji',
		'converter' : 'spacedrollover',
		'kanji_parts' : 'unchanged'
	}

	p = requests.post(romaji_link, data = data, headers = headers)

	soup2 = BeautifulSoup(p.content, 'html.parser')
	out = soup2.select('.romaji')[0]
	out2 = []
	outtemp = []
	for c in out.children:
		print(c)
		if c.name == 'br':
			out2.append(' '.join(outtemp).replace('[?]', ''))
			outtemp = []
		elif c.name == None:
			outtemp.append(c)
		else:
			try:
				t = c.select('.trigger')[0].text
				outtemp.append(t)
			except Exception:
				print(c)
				pass
	ftext = out2
	
	
	
	
	
	
	
	
	
	
	num_chars = len(rtext)
	rtext = rtext.split('\n')
	#ftext = ftext.split('\n')
	
	mtext = ''
	ttt = time.time() - ttt
	print('Get time: {}s'.format(ttt))
	return mtext, rtext, ftext, num_chars
	
def filemake(m, r, f, num, url):
	etext = []
	a = '<head> \n\t\
	<meta name="viewport" content="width=device-width" />\n\t\
	<meta charset="utf-8"/>\n\t\
	<link rel="stylesheet" href="/static/bmtl_style.css">\n\t\
	<script src="/static/bmtl_script.js"></script>\n\
	</head>\n\
	<body>\n\t\
	<div class="bmtl">\n'
	etext.append(a)
	ii = num
	e = '\t\t<span class="f">'+f[0].strip()+'</span>\n\
		\t\t<span class="m">'+m.strip()+'</span>\n\
		\t\t<span class="r">'+r[0].strip()+'</span>\n'
	
	e = '\t<h1>\n'+e+'\t</h1>\n\t<hr>\n'
	etext.append(e)
	x = url.split('/')
	y = '/'.join(x[:4])
	prev = y+'/{}/'.format(int(x[4])-1)
	next = y+'/{}/'.format(int(x[4])+1)
	
	
	
	aa = '''<div class="nav"><a class="p" href="/do?url={pr}">Previous</a> <a class="n" href="/do?url={nx}">Next</a></div>\n'''.format(pr=prev, nx=next)
	etext.append(aa)
	
	for i in range(1,len(f)):
		if(f[i] == ''):
			e = '<div class="blank"></div>'
		else:
			e = '<p>\
		<span class="f">'+f[i].strip()+'</span>\
		<span class="m">'+m.strip()+'</span>\
		<span class="r">'+r[i].strip()+'</span></p><hr>\n'
		etext.append(e)
	etext.append(aa)
	etext.append("\t</div>\n</body>")
	
	return '\n'.join(etext)
	
	


def multiple_replace(dict, text):
	# Create a regular expression  from the dictionary keys
	regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

	# For each match, look-up corresponding value in dictionary
	return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 		
def deleteMe(id):
	if id in REQ:
		if REQ[id][1] != 0:
			REQ[id][1].cancel()
		del REQ[id]
		print(id,'was deleted')
	
Getting_part_one = False
def getPart(link, part, total,id):
	if(id in REQ):
		raw = REQ[id][0]
		REQ[id][1].cancel()
		t = threading.Timer(30.0,deleteMe,[id])
		print('reset timer for',id)
		t.start()
		REQ[id][1] = t
	else:
		raw = getSyo(link, title = part == 1)
		t = threading.Timer(30.0,deleteMe,[id])
		t.start()
		REQ[id] = [raw,t]
		
		
	if part == total:
		deleteMe(id)
	l = len(raw)
	rs = raw.split('\n')
	lines = len(rs)
	st = lines//total * (part-1)
	fn = lines if part == total else lines//total * (part)
	html = _process(link,st, fn, rs)
	return html
	
def _process(link, s, f, rraw):
	raw = rraw[s:f]
	raw = '\n'.join(raw)
	raw = multiple_replace({'。':'. ','、':', '}, raw)
	roma = getRoma(raw)
	raw = raw.split('\n')
	roma = processRoma(roma)
	#roma = fixRomaBlanks(raw,roma)
	#raw = rawPostProcess(raw)
	html = filemake_partial('', raw, roma, link)
	return html
	
	
def rawPostProcess(raw):
	rep = (('<qs1>','「',),('<qs2>','」',),('<qs3>','『',),('<qs4>','』',))
	for r in rep:
		for i in range(len(raw)):
			raw[i] = raw[i].replace(r[0],r[1])
			
	return raw
	
def fixRomaBlanks(raw, roma):
	i = 0
	while raw[i] == '':
		i+=1
	k = 0
	j = len(raw) - 1
	while raw[j] == '':
		j-=1
		k+=1
	return ['']*i + roma + ['']*k
	
	
def getSyo(link, title = False):
	print('GetSyo: ',link)
	r = requests.get(link)
	r.encoding = 'utf-8'
	data = r.text
	soup = BeautifulSoup(data,'html.parser')
	rtext = soup.find_all(class_='novel_subtitle')[0].text
	rtext += '\n'+soup.find(id='novel_honbun').text
	'''
	for r in repSyo:
		rtext = rtext.replace(r[0],r[1])
	'''
	return rtext
	
def puncfix(text):
	a = text.replace('。','. ')
	a = a.replace('、',', ')
	return a
def getRoma(raw):
	minlen = 5
	kakasi2 = kakasi()
	kakasi2.setMode("H","a") # default: Hiragana no conversion
	kakasi2.setMode("K","a") # default: Katakana no conversion
	kakasi2.setMode("J","a") # default: Japanese no conversion
	kakasi2.setMode("r","Hepburn") # default: use Hepburn Roman table
	#kakasi.setMode("C", True) # add space default: no Separator
	kakasi2.setMode("s", True) # add space default: no Separator
	kakasi2.setMode("c", False) # capitalize default: no Capitalize
	conv = kakasi2.getConverter()
	text = raw
	#ftext = conv.do(text)
	#ftext = puncfix(ftext)
	#convk = kakasi.getConverter()
	segmenter = tinysegmenter.TinySegmenter()
	wakati2 = wakati()
	convw = wakati2.getConverter()
	resultw = convw.do(text)
	#print(resultw)
	arr = []

	resultw = resultw.split(' ')
	for i in range(len(resultw)):
		part = resultw[i]
		if len(part) > minlen:
			part = ' '.join(segmenter.tokenize(part))
		arr.append(conv.do(part))
	result = ' '.join(arr)
	result = multiple_replace({
	'  ':' ',
	'o-':'ō',
	'a-':'ā',
	'ou':'ō',
	' ha ': 'wa',
	'tsu te':'tte',
	'tsu to':'tto',
	'e-' : 'ē',
	'i-' : 'ī', 
	' - ': '~'
	}, result)
	ftext = result
	
	
	
	
	''' doesnt work
	romaji_link = 'http://nihongo.j-talk.com/'


	r = requests.get(romaji_link)
	soup = BeautifulSoup(r.content, 'html.parser')
	d = soup.select('#formwrap > form > input[type="hidden"]')
	timestamp = d[0]['value']
	uniqid = d[1]['value']
	kanji = raw
	

	headers = {
		"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"


	}
	data = {
		'timestamp' : timestamp,
		'uniqid' : uniqid,
		'kanji' : kanji,
		'Submit' : 'Translate Now',
		'kana_output' : 'romaji',
		'converter' : 'spacedrollover',
		'kanji_parts' : 'unchanged'
	}
	return requests.post(romaji_link, data = data, headers = headers)
	'''
	return ftext

	
def processRoma(p):
	''' not required
	soup2 = BeautifulSoup(p.content, 'html.parser')
	out = soup2.select('.romaji')[0]
	out2 = []
	outtemp = []
	for c in out.children:
		print(c)
		if c.name == 'br':
			out2.append(''.join(outtemp))
			outtemp = []
		elif c.name == None:
			
			outtemp.append(c)
		else:
			try:
				t = c.select('.trigger')[0].text
				outtemp.append(t+' ')
			except Exception:
				# its's 'n'
				if len(outtemp) > 0:
					outtemp.append('n')
	ftext = out2
	'''
	ftext = p.split('\n')
	rep = (('[?]', ''),('< qs 1 >','「'),('< qs 2 >','」'),('< qs 3 >','『',),('< qs 4 >','』',))
	for r in rep:
		for f in range(len(ftext)):
			ftext[f] = ftext[f].replace(r[0],r[1])
	return ftext
	
	
	
def make(url):
	t = time.time()
	mtext, rtext, ftext, num_chars = getter(url)
	H = filemake(mtext, rtext, ftext, url.split('/')[4], url)
	t = time.time() - t
	print('Done in {} seconds | {} seconds per character'.format(t, round(t/num_chars, 7)))
	return H
	
def make2(url):
	x = url.split('/')
	if len(x) == 6:
		y = '/'.join(x[:4])
		prev = y+'/{}/'.format(int(x[4])-1)
		next = y+'/{}/'.format(int(x[4])+1)
		return getFileInit(url, prev, next)
	elif len(x) == 5:
		return getFileTOC(url)
		
	
def filemake_partial(m, r, f, url):
	etext = []
	
	
	for i in range(len(f)):
		if(f[i] == ''):
			e = '<div class="blank"></div>'
		else:
			e = '<p>\
		<span class="f">'+f[i].strip()+'</span>\
		<span class="m">'+m.strip()+'</span>\
		<span class="r">'+r[i].strip()+'</span></p><hr>\n'
		#print(e)
		etext.append(e)
	
	return ''.join(etext)
	
def getToc(url):
	print('GetSyoTOC: ',url)
	r = requests.get(url)
	r.encoding = 'utf-8'
	data = r.text
	soup = BeautifulSoup(data,'html.parser')
	chapters= str(soup.find_all(class_='index_box')[0])
	U = '/'.join(url.split('/')[:-2])
	chapters = re.sub(r'href="(.*)"',r'href="do?url=%s\1"'%(U),chapters)
	
		
	rtext = chapters
	

	return rtext
	
def getFileTOC(URL):
	return open('toc.html','r').read()%(getToc(URL))
	
	
def getFileInit(URL, prv, nxt):
	id = str(random.random())
	return open('chapter.html', 'r').read()%(prv,nxt,prv,nxt,id,URL)

	
	

		
	
	
	
	










