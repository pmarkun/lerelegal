import json, codecs

vereadores = json.load(open('vereadores.json', 'r'))

with codecs.open("tabela.csv", 'w', encoding="utf-8") as tabela:
	tabela.write('nome,partido,score\n')
	for v in vereadores:
		if v.has_key('total_score'):
			tabela.write(v['nome']+','+v['partido']['sigla']+','+str(round(v['total_score'],2))+'\n')
