import numpy as np 
import re 
import nltk 
from	nltk.book	import*
moby = text1
moby_nopuntc = [Word.lower() for Word in moby if re.search("\w",Word)]
len (moby)
len (moby_nopuntc)
len(set(moby_nopuntc))

WSJ = text2
WSJ_nopuntc = [word.lower() for word in WSJ if re.search("\w",word)]
len(WSJ_nopuntc)
len(set(WSJ_nopuntc))

moby_type_tokenRatio = len(set(moby_nopuntc)) / len(moby_nopuntc)
print (moby_type_tokenRatio)
print(len (moby_nopuntc))
print(len (WSJ_nopuntc))
WSJ_type_tokenRatio = len(set(WSJ_nopuntc)) / len(WSJ_nopuntc)


