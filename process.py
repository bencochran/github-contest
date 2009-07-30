#!/usr/bin/env python
# encoding: utf-8
"""
process.py

You probably shouldn't even be looking here unless it's August 31st. Just sayin.

Created by Ben Cochran on 2009-07-29.
"""

from __future__ import with_statement
import sys
import pickle
from optparse import OptionParser

def loadData(infile):
	watched = {}
	repos = {}
	with open(infile, 'rt') as f:
		for line in f:
			(user, repo) = [int(part.strip()) for part in line.split(':')]
			if not watched.has_key(user):
				watched[user] = set()
			watched[user].add(repo)
			repos[repo] = repos.get(repo,0) + 1
			# print "%i : %i" % (user, repo)
	return (watched, repos)

def loadTestUsers(infile):
	with open(infile, 'rt') as f:
		return [int(line.strip()) for line in f]

def mostWatched(repos, n = 12):
	def compare_values(a, b):
		return b[1] - a[1]
	
	repos = zip(repos.keys(),repos.values())
	repos.sort(compare_values)
	return repos[:n]

def giveReposToUsers(userSet, repoSet):
	watched = {}
	for user in userSet:
		watched[user] = repoSet
	
	return watched

def outputSuggestions(outfile, suggestions):
	with open(outfile, 'wt') as f:
		for (user,suggestedSet) in zip(suggestions.keys(),suggestions.values()):
			f.write("%i:%s\n" % (user,",".join(['%i'%i for i in suggestedSet])))

def main():
	p = OptionParser(usage='%prog test_file output_file [options]\nRun %prog --help for more help.')
	
	p.add_option('-v','--verbose', action="store_true", dest="verbose", default=False, help="provide verbose output at runtime")
	p.add_option('-d','--data_file', dest="data_filename", default=None, help="use data file")
	p.add_option('-p','--pickle_file', dest="pickle_filename", default=None, help="use pickle file for data")
	p.add_option('-P','--write_pickle_file', dest="write_pickle_filename", default=None, help="write inported data to pickle file")
	
	# Parse the arguments
	(options, args) = p.parse_args()
	
	if len(args) != 2:
		p.error("You must specify test and output files")
	
	(test_filename, output_filename) = args
	
	if (options.pickle_filename):
		with open(options.pickle_filename, 'r') as f:
			(usersWatched, repos) = pickle.load(f)
	elif (options.data_filename):
		(usersWatched, repos) = loadData(options.data_filename)
		if (options.write_pickle_filename):
			with open(options.write_pickle_filename, 'w') as f:
				data = (usersWatched, repos)
				pickle.dump(data, f)
	else:
		p.error("You must supply either a data file or a pickle")
	
	testUsers = loadTestUsers(test_filename)
	
	topRepoSet = set([repo for (repo,count) in mostWatched(repos)])
	
	suggestions = giveReposToUsers(set(testUsers), topRepoSet)
	
	outputSuggestions(output_filename,suggestions)

if __name__ == "__main__":
	sys.exit(main())
