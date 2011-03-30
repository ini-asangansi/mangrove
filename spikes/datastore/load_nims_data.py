# script to load the NIMS data for locations

import csv
import uuid
import couchdb
import datetime
import string

from entity import Entity
from record import Record

print "Loading NIMS Data..."

reader = csv.reader(open('data/nims_data_loc.csv', 'r'))
couch = couchdb.Server('http://localhost:5984/')
if 'mangrove' in couch:
    print "Deleting old database (mangrove)..."
    del couch['mangrove']
print "Creating new database (mangrove)..."
db = couch.create('mangrove')

countries = {}
states = {}
lgas = {}

print "Parsing nims_data.csv..."
# COUNTRY (ISO), STATE, STATE ID, STATE LVL ID, LGA, LGA LVL ID, DENS90, POP90

for row in reader:
    country = row[0]
    state   = row[1]
    lga     = row[4]
    if country not in countries:
        print "...adding [%s]" % country
        _id = uuid.uuid4().hex
        entity = Entity(entity_type="location", name=country)
        countries[country] = _id
    if state not in states:
        print "...adding [%s, %s]" % (country, state)
        _id = uuid.uuid4().hex
        at = {'location': [country]}
        entity = Entity(entity_type="location", name=state, aggregation_trees=at)
        states[state] = _id
    if lga not in lgas:
        print "...adding [%s, %s, %s]" % (country, state, lga)
        _id = uuid.uuid4().hex
        at = {'location': [country, state]}
        entity = Entity(entity_type="location", name=lga, aggregation_trees=at)
        lgas[lga] = _id

print "Loaded countries (%d)" % len(countries)
print "Loaded states (%d)" % len(states)
print "Loaded lgas (%d)" % len(lgas)

reader = csv.reader(open('data/nims_data_pop.csv', 'r'))

print "Parsing nims_data_pop.csv..."
# STATE | SENATE DISTRICT | LGA | MEN | WOMEN | TOTAL | BLANK | MEN | WOMEN | BLANK | 0-4 | 5-14 | 15-29 | 30-44 | 45-59 | 60-64 | 65-69 | 70+ | BLANK | UNDER 5 MALE | UNDER 5 FEMALE

lga_pop_loaded = []
lga_pop_failed = []
for row in reader:
    lga              = row[2]
    pop              = string.replace(row[5], ",", "")
    pop_male         = int(string.replace(row[3], ",", ""))
    pop_female       = int(string.replace(row[4], ",", ""))
    pop_ratio_male   = str(pop_male / int(pop))
    pop_ratio_female = str(pop_female / int(pop))
    pop_ratio_u4     = row[10]
    pop_u5_male      = string.replace(row[19], ",", "")
    pop_u5_female    = string.replace(row[20], ",", "")
    if lga in lgas:
        lga_pop_loaded.append(lga)
        print "...adding report for entity [%s, %s]" % (lga, lgas[lga])
        print "\tPopulation: %s" % pop
        print "\tPopulation ratio (male): %s" % pop_ratio_male
        print "\tPopulation ratio (female): %s" % pop_ratio_female
        print "\tPopulation ratio (under 4): %s" % pop_ratio_u4
        print "\tPopulation (under 5, male): %s" % pop_u5_male
        print "\tPopulation (under 5, female): %s" % pop_u5_female
        _id = uuid.uuid4().hex
        #doc = {
        #    '_id': _id,
        #    'created_on': str(datetime.datetime.now()),
        #    'document_type': 'record',
        #    'attributes': {
        #        'population': {
        #            'value': pop,
        #            'source': '2008 Census',
        #            'type': 'static',
        #            'note': 'This is a note.'
        #        },
        #        'population_ratio_male': {
        #            'value': pop_ratio_male,
        #            'source': '2008 Census',
        #            'type': 'static',
        #            'note': 'This is a note.'
        #        },
        #        'population_ratio_female': {
        #            'value': pop_ratio_female,
        #            'source': '2008 Census',
        #            'type': 'static',
        #            'note': 'This is a note.'
        #        },
        #        'population_ratio_under_4': {
        #            'value': pop_ratio_u4,
        #            'source': '2008 Census',
        #            'type': 'static',
        #            'note': 'This is a note.'
        #        },
        #        'population_under_5_male': {
        #            'value': pop_u5_male,
        #            'source': '2008 Census',
        #            'type': 'static',
        #            'note': 'This is a note.'
        #        },
        #        'population_under_5_female': {
        #            'value': pop_u5_female,
        #            'source': '2008 Census',
        #            'type': 'static',
        #            'note': 'This is a note.'
        #        },
        #    },
        #    'entity_id': lgas[lga]
        #}
        #db.save(doc)
        attributes = {
            'population': {
                'value': pop,
                'source': '2008 Census',
                'type': 'static',
                'note': 'This is a note.'
            },
            'population_ratio_male': {
                'value': pop_ratio_male,
                'source': '2008 Census',
                'type': 'static',
                'note': 'This is a note.'
            },
            'population_ratio_female': {
                'value': pop_ratio_female,
                'source': '2008 Census',
                'type': 'static',
                'note': 'This is a note.'
            },
            'population_ratio_under_4': {
                'value': pop_ratio_u4,
                'source': '2008 Census',
                'type': 'static',
                'note': 'This is a note.'
            },
            'population_under_5_male': {
                'value': pop_u5_male,
                'source': '2008 Census',
                'type': 'static',
                'note': 'This is a note.'
            },
            'population_under_5_female': {
                'value': pop_u5_female,
                'source': '2008 Census',
                'type': 'static',
                'note': 'This is a note.'
            },
        }
        record = Record(
            _id = _id,
            entity_id = lgas[lga],
            attributes = attributes
        )
    else:
        lga_pop_failed.append(lga)
        print "...no LGA corresponsing to: %s" % lga

print "Loaded population data for %d out of %d LGAs" % (len(lga_pop_loaded), len(lga_pop_failed) + len(lga_pop_loaded))
if lga_pop_failed:
    print "%d LGAs failed to load:" % len(lga_pop_failed)
    for lga_failed in lga_pop_failed:
        print "\t%s" % lga_failed
