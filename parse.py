# encoding=utf8
import json
from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class OpsParser:

	debug = False
	grades = {}
	subjects = []
	meta = {}

	def parse_grades(self, items):
		"""Parse grades"""
		for item in items:
			name = item['nimi']['fi']	
			item['name'] = name  					# Default name for faster access 
			self.grades[int(item['id'])] = item     


	def parse_subjects(self, items):
		"""Parse subjects"""
		for item in items:
			name = item['nimi']['fi']
			item['name'] = name
			self.subjects.append(item)  
			print name

			# Loop target areas 
			if "kohdealueet" in item:
				for area in item['kohdealueet']:
					print (' ' * 3) + area['nimi']['fi']

			# Loop target areas 
			if "oppimaarat" in item:
				for tmp in item['oppimaarat']:
					print (' ' * 3) + tmp['nimi']['fi']

			# Get grades material 
			if 'vuosiluokkakokonaisuudet' in item:
				for info in item['vuosiluokkakokonaisuudet']:

					# Print target grades
					print (' ' * 3) + self.grades[int(info['_vuosiluokkaKokonaisuus'])]['name']
			
					#pprint(pack)
					if info['sisaltoalueinfo']:
						print (' ' * 6) + info['sisaltoalueinfo']['otsikko']['fi']

					# Targets
					#for target in info['tavoitteet']:
					#	print (' ' * 6) + target['tavoite']['fi']	

					# Content areas
					for area in info['sisaltoalueet']:
						print (' ' * 9) + area['nimi']['fi'] 


	def parse_metadata(self, items):
		"""Parse metadata"""
		for item in items:
			name = item['nimi']['fi']
			item['name'] = name
			self.meta[item['id']] = item


	def parse_tree(self, items, depth=0):
		for item in items:
			print (' ' * (depth *3)) + item['perusteenOsa']['nimi']['fi']
			if 'lapset' in item:
				self.parse_tree(item['lapset'], depth+1)


	def getGrades(self):
		pass


	def getSubjectsByGrade(self, id):
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
	