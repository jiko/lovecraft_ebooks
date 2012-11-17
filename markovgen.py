import random

class Markov(object):
	
	def __init__(self, open_file):
		self.cache = {}
		self.open_file = open_file
		self.words = self.file_to_words()
		self.word_size = len(self.words)
		self.database()
		
	
	def file_to_words(self):
		self.open_file.seek(0)
		data = self.open_file.read()
		words = data.split()
		return words
		
	
	def quadruples(self):
		""" 
Generates quadruples from the given data string. So if our string were "What a very lovely day", we'd generate (What, a, very, lovely) and then (a, very, lovely, day).
		"""
		
		if len(self.words) < 4:
			return
		
		for i in range(len(self.words) - 3):
			yield (self.words[i], self.words[i+1], self.words[i+2], self.words[i+3])
			
	def database(self):
		for w1, w2, w3, w4 in self.quadruples():
			key = (w1, w2, w3)
			if key in self.cache:
				self.cache[key].append(w4)
			else:
				self.cache[key] = [w4]
				
	def generate_markov_text(self, size=25):
		seed = random.randint(0, self.word_size-4)
		seed_word, next_word, last_word = self.words[seed], self.words[seed+1], self.words[seed+2]
		w1, w2, w3 = seed_word, next_word, last_word
		gen_words = []
		for i in xrange(size):
			gen_words.append(w1)
			w1, w2, w3 = w2, w3, random.choice(self.cache[(w1, w2, w3)])
		gen_words.append(w3)
		return ' '.join(gen_words)
