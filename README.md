the csv file contains a list of companies with corresponding Central Index Keys, Bloomberg IDs, Crunchbase IDs, and websites that was manually created by me.

the python script does the following...

for each item in "wikidata-update-list.csv":
	-check to see if item has property
	-if it does have the property then continue without doing anything
	-if it does not have the property then assign the property

the properties being assigned are:
	-(P5531) Central Index Key
	-(P3357) Bloomberg company ID
	-(P2088) Crunchbase organization ID
	-(P856) official website