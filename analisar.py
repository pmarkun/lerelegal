import codecs, sys
from readability_score.calculators.fleschkincaid import *

with codecs.open(sys.argv[1], 'r', encoding='utf-8') as tmp:
	fk = FleschKincaid(tmp.read(), locale='pt_BR')
	print fk.min_age