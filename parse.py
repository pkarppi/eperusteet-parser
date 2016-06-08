# encoding=utf8
import json
import re
from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class OpsParser:

	debug = False
	grades = {}
	subjects = []
	parent_map = []
	meta = {}

	def debug(self, level, str):
		print ' ' * (level * 3) + str


	def parse_grades(self, items):
		"""Parse grades"""
		self.debug(0, "Vuosiluokat")
		for item in items:
			name = item['nimi']['fi']	
			item['name'] = name  					# Default name for faster access 
			self.debug(1, name)
			self.grades[int(item['id'])] = item     


	def parse_subjects(self, items):
		"""Parse subjects"""
		self.debug(0, "Oppiaineet")

		for item in items:
			name = item['nimi']['fi']
			item['name'] = name
			self.subjects.append(item) 

			self.debug(1, name)

			# Loop target areas 
			if "kohdealueet" in item:
				self.debug(2, "Kohdealueet:")
				for area in item['kohdealueet']:
					self.debug(3, area['nimi']['fi'])

			# Loop target areas 
			if "oppimaarat" in item:
				self.debug(2, "Oppimäärät:")
				for tmp in item['oppimaarat']:
					self.debug(3, tmp['nimi']['fi'])

			# Get grades material 
			if 'vuosiluokkakokonaisuudet' in item:
				for info in item['vuosiluokkakokonaisuudet']:

					# Print target grades
					self.debug(2, self.grades[int(info['_vuosiluokkaKokonaisuus'])]['name'])
			
					if info['sisaltoalueinfo']:
						self.debug(3, info['sisaltoalueinfo']['otsikko']['fi'])

					# Targets
					self.debug(2, "Tavoitteet:")
					for target in info['tavoitteet']:
						self.debug(3, re.sub('<[^<]+?>', '', target['tavoite']['fi']))	

					# Content areas
					self.debug(2, "Sisältöalueet:")
					for area in info['sisaltoalueet']:
						self.debug(3, area['nimi']['fi'])


	def parse_metadata(self, items):
		"""Parse metadata"""
		self.debug(0, "Laaja-alaiset osaamiset:")
		for item in items:
			name = item['nimi']['fi']
			item['name'] = name
			self.debug(1, name)
			self.meta[item['id']] = item


	def parse_tree(self, items, depth=0):
		self.debug(0, "Suunnitelma:")
		self.recurse(items)

	def recurse(self, items, depth=0):
		for item in items:
			self.debug(depth + 1 , item['perusteenOsa']['nimi']['fi'])
			if 'lapset' in item:
				self.recurse(item['lapset'], depth+1)


	def get_subjects(self):
		"""Returns list of subjects"""	
		pass


	def get_grades(self):
		"""Returns list of grades"""	
		pass


	def get_subjects_by_grade(self, id):
		"""Returns list of subjects"""	
		pass


def main():

	with open('eperusteet.json') as file:    
		data = json.load(file)

	# Reader
	p = OpsParser()
	p.parse_grades(data['perusopetus']['vuosiluokkakokonaisuudet'])
	p.parse_subjects(data['perusopetus']['oppiaineet'])
	p.parse_metadata(data['perusopetus']['laajaalaisetosaamiset'])
	p.parse_tree(data['perusopetus']['sisalto']['lapset'])

if __name__ == "__main__":
	main()
	