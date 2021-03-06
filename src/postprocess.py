import ast
from datetime import datetime
import sys

from lib import HelperFunctions as hf

""" Global variables """
family = ''
fingerprints = {}
resultsDirectory = ''


def absoluteThreshold():
	"""
	Calculate fingerprints who appear more than the threshold in family's strings, and write results to file
	"""
	start = datetime.now()
	numOfStrings = hf.getCountOfStrings(fingerprints)
	threshold = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8]
	for x in range(len(threshold)):
		thresholdFingerprints = hf.getAboveThreshold(threshold[x], numOfStrings, fingerprints)
		relevantFingerprints = hf.findFingerprintsWithCogs({}, thresholdFingerprints)

		if len(thresholdFingerprints.keys()) > 0:
			with open(resultsDirectory + family + '_fingerprint_' + str(threshold[x]) + '.txt', 'w+') as file:
				file.write('Total number of strings in family: {}.\n'.format(numOfStrings))

				for fingerprint in relevantFingerprints:
					fpStrings = ', '.join(relevantFingerprints[fingerprint])
					fpNumOfStrings = len(relevantFingerprints[fingerprint])
					line = '--- fingerprint: {} : numOfStrings: {}\n------in strings: {}\n'
					file.write(line.format(fingerprint, fpNumOfStrings, fpStrings))

	# Record time passed.
	print('Threshold calculation runtime: {}.'.format(datetime.now() - start))


def cogsProcess(cogsString):
	"""
	Calculate fingerprints who have COGs with the function list provided, calculate thresholds and write results to file
	:param cogsString: the provided function list for COGs
	"""
	if cogsString:
		start = datetime.now()
		cogsList = []
		try:
			cogsList = ast.literal_eval(cogsString)

		except ValueError:
			print('You have to provide a valid cogs list in the form ["S","V","V"]. You provided {}.'.format(cogsString))
			exit()

		cogs = hf.getCogsFunctions(cogsList)
		cogsFingerprints = hf.analyzeCogsFingerprints(cogs, fingerprints)
		numOfStrings = hf.getCountOfStrings(cogsFingerprints)

		print('Checking thresholds for the {} different strings in relevant fingerprints.'.format(numOfStrings))
		threshold = [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8]

		filename = family + '_with_cogs'
		for cog in cogs:
			for i in range(cogs[cog]['repeat']):
				filename += '_' + cog

		for x in range(len(threshold)):
			thresholdFingerprints = hf.getAboveThreshold(threshold[x], numOfStrings, cogsFingerprints)

			if len(thresholdFingerprints.keys()) > 0:
				if threshold[x] == 0:
					path = resultsDirectory + filename + '_fingerprints.txt'
				else:
					path = resultsDirectory + filename + '_fingerprint_' + str(threshold[x]) + '.txt'

				with open(path, 'w+') as file:
					list = ';'.join(cogsList)
					file.write('Total number of strings in family with COGs function [{}] : {}.\n\n'.format(list, numOfStrings))

					for fingerprint in thresholdFingerprints:
						fpStrings = ', '.join(thresholdFingerprints[fingerprint])
						line = '--- fingerprint: {} : numOfStrings: {}\n------in strings: {}\n'
						file.write(line.format(fingerprint, len(thresholdFingerprints[fingerprint]), fpStrings))

		print('Cogs calculation runtime: {}.'.format(datetime.now() - start))


def findProcess(findString):
	"""
	Calculate fingerprints who have the COGs provided and write results to file
	:param findString: the provided list for COGs
	"""
	if findString:
		start = datetime.now()
		cogsList = []
		try:
			cogsList = ast.literal_eval(findString)

		except ValueError:
			print('You have to provide a valid cogs list in the form [1054, 3049, 3769]. You provided {}.'.format(findString))
			exit()

		cogs = hf.getCogsList(cogsList)
		cogsFingerprints = hf.findFingerprintsWithCogs(cogs, fingerprints)
		numOfStrings = hf.getCountOfStrings(cogsFingerprints)

		filename = family + '_with_cogs'
		for cog in cogs:
			for i in range(cogs[cog]):
				filename += '_' + cog

		with open(resultsDirectory + filename + '_fingerprints_list.txt', 'w+') as file:
			list = ';'.join(cogsList)
			file.write('Total number of strings in family with COGs [{}] : {}.\n\n'.format(list, numOfStrings))

			for fingerprint in cogsFingerprints:
				fpStrings = ', '.join(cogsFingerprints[fingerprint])
				line = '--- fingerprint: {} : numOfStrings: {}\n------in strings: {}\n'
				file.write(line.format(fingerprint, len(cogsFingerprints[fingerprint]), fpStrings))

		print('Find calculation runtime: {}.'.format(datetime.now() - start))


def findWithLenProcess(findString, length):
	"""
	Calculate fingerprints who have the COGs provided with length constrain of fingerprints length and write results to file
	:param findString: the provided list for COGs
	:param length: the length constrain
	"""
	if findString:
		start = datetime.now()
		cogsList = []
		try:
			cogsList = ast.literal_eval(findString)

		except ValueError:
			print('You have to provide a valid cogs list in the form [1054, 3049, 3769]. You provided {}.'.format(findString))
			exit()

		cogs = hf.getCogsList(cogsList)
		cogsFingerprints = hf.findFingerprintsWithCogs(cogs, fingerprints)
		relevantFingerprints = {}

		for fingerprint in cogsFingerprints:
			fpLength = len(fingerprint.split(':')[0].split(';'))
			if fpLength == int(length):
				relevantFingerprints[fingerprint] = cogsFingerprints[fingerprint]

		numOfStrings = hf.getCountOfStrings(relevantFingerprints)

		filename = '{}_length_{}_with_cogs'.format(family, length)
		for cog in cogs:
			for i in range(cogs[cog]):
				filename += '_' + cog

		with open(resultsDirectory + filename + '_fingerprints_list.txt', 'w+') as file:
			list = ';'.join(cogsList)
			file.write('Total number of strings in family with COGs [{}] and length {} : {}.\n\n'.format(list, numOfStrings, length))

			for fingerprint in relevantFingerprints:
				fpStrings = ', '.join(relevantFingerprints[fingerprint])
				line = '--- fingerprint: {} : numOfStrings: {}\n------in strings: {}\n'
				file.write(line.format(fingerprint, len(relevantFingerprints[fingerprint]), fpStrings))

		print('Find calculation runtime: {}.'.format(datetime.now() - start))


options = {
	'-threshold': absoluteThreshold,
	'-cogs': cogsProcess,
	'-find': findProcess,
	'-findWithLen': findWithLenProcess
}

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print('Not enough arguments!')

	else:
		resultsDirectory = sys.argv[1] + '/'
		args = sys.argv[2:]
		family = args[0]
		filepath = resultsDirectory + family + '_fingerprints.txt'
		with open(filepath, 'r+') as file:
			# Read fingerprint file
			print('Getting fingerprints for family {}.'.format(family))
			fingerprints = hf.getFingerprints(file)

			# Read options
			x = 1
			while x < len(args):
				option = hf.argInOption(args[x], options)
				if option:
					print('Starting {} post process option.'.format(args[x]))
					if args[x] == '-threshold':
						options[args[x]]()
						x += 1

					elif args[x] == '-findWithLen' and args[x+1] and args[x+2]:
						options[args[x]](args[x+1], args[x+2])
						x += 3

					elif args[x+1]:
						options[args[x]](args[x+1])
						x += 2
