import codecs
import json, os, subprocess
import urllib2
from lxml.html import parse
from readability_score.calculators.fleschkincaid import *


def getPDF(url, projeto, vereador):
	directory = limpa(vereador)
	
	if not os.path.exists(directory):
		os.makedirs(directory)
    
	nomearquivo = directory+'/'+limpa(projeto)+'.pdf'
	if not os.path.isfile(nomearquivo):
		with open(nomearquivo, 'wb') as pdf:
			print url
			pdf.write(urllib2.urlopen(url).read())
			print "Wrote " + p['nome']
	
	full_text = subprocess.check_output("pdftotext -q "+nomearquivo+" -", shell=True)
	
	return full_text.strip()

def limpa(nome):
	return "".join([c for c in nome if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(' ','_')

vereadores = json.load(open('vereadores.json', 'r'))

for iv, v in enumerate(vereadores[0:2]):
	print "Getting " + v['nome']
	count = 0.0
	score = 0
	for ip, p in enumerate(v['projetos']):
		soup = parse(urllib2.urlopen(p['url'])).getroot()
		
		link = soup.cssselect('font font a')
		if link:
			texto = getPDF(link[0].get('href'), p['nome'], v['nome'])
			if texto:
				fk = FleschKincaid(texto.decode('utf-8'), locale='pt_BR')
				vereadores[iv]['projetos'][ip]['full_text'] = texto
				vereadores[iv]['projetos'][ip]['score'] = fk.min_age
				count += 1
				score += fk.min_age
	vereadores[iv]['total_score'] = score/count
	with open('vereadores.json', 'w') as tmp:
		tmp.write(json.dumps(vereadores, indent=4))