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
		soup = parse(urllib2.urlopen(url)).getroot()
		link = soup.cssselect('font font a')
		if not link:
			return ''
		with open(nomearquivo, 'wb') as pdf:
			print url
			print link[0].get('href')
			pdf.write(urllib2.urlopen(link[0].get('href')).read())
			print "Wrote " + p['nome']
	
	try:
		print "Analyzing " + nomearquivo
		full_text = subprocess.check_output("pdftotext -q "+nomearquivo+" -", shell=True)
	except:
		print nomearquivo + " erro!"
		full_text = ""
	return full_text.strip()

def limpa(nome):
	return "".join([c for c in nome if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(' ','_')

vereadores = json.load(open('vereadores.json', 'r'))

for iv, v in enumerate(vereadores):
	if v.has_key('total_score'):
		continue
	print "Getting " + v['nome']
	count = 0.0
	score = 0
	for ip, p in enumerate(v['projetos']):
		if p.has_key('score'):
			continue

		try:
			texto = getPDF(p['url'], p['nome'], v['nome'])
		except:
			texto = ''
			print "Erro no download/conversao."
		if texto:
			fk = FleschKincaid(texto.decode('utf-8'), locale='pt_BR')
			vereadores[iv]['projetos'][ip]['full_text'] = texto
			vereadores[iv]['projetos'][ip]['score'] = fk.min_age
			count += 1
			score += fk.min_age
	if count > 0:
		vereadores[iv]['total_score'] = score/count
	with open('vereadores.json', 'w') as tmp:
		tmp.write(json.dumps(vereadores, indent=4))