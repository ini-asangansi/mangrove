from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Loads the NMIS dataset from the 'NIMS Data' Google Doc."

    def handle(self, *args, **options):
        self._import_data()

    def _slugify(self, text, delim=u'_'):
        '''Generates an ASCII-only slug.'''
        import re
        from unicodedata import normalize

        _punct_re = re.compile(r'[\t :;!"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
        result = []
        for word in _punct_re.split(text.lower()):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(delim.join(result))

    def _import_data(self):
        '''Script to load the NIMS dataset.'''
        import couchdb
        import datetime
        import string

        from mangrove.datastore.database import DatabaseManager
        from mangrove.datastore.entity import Entity
        import mangrove.datastore.entity
        from mangrove.utils import GoogleSpreadsheetsClient

        print "Loading 'NIMS Data'..."

        dbm = DatabaseManager(server='http://localhost:5984', database='nmis')

        user_spreadsheets = GoogleSpreadsheetsClient(settings.GMAIL_USERNAME, settings.GMAIL_PASSWORD)
        nims_data = user_spreadsheets['NIMS Data']

        countries = {}
        states = {}
        locations = {}

        print "Importing location entities from 'Nigeria LGAs ALL' worksheet"
        for row in nims_data['Nigeria LGAs ALL']:
            country  = row['country']
            state    = row['states']
            lga      = row['lga']
            location = (country, state, lga)
            if country not in countries:
                e = Entity(dbm, entity_type=["Location", "Country"], location=[country])
                locations[(country)] = e.save()
                countries[country] = e.id
            if state not in states:
                e = Entity(dbm, entity_type=["Location", "State"], location=[country, state])
                locations[(country, state)] = e.save()
                states[state] = e.id
            e = Entity(dbm, entity_type=["Location", "LGA"], location=[country, state, lga])
            locations[location] = e.save()

        print "Countries (%d)" % len(countries)
        print "States (%d)" % len(states)
        print "LGAs (%d)" % (len(locations) - len(countries) - len(states))
        print "Total locations (%d)" % len(locations)

        print "Adding data from 'Population' worksheet"
        lga_loaded = []
        lga_failed = []
        keys = {'childrenunderfive', '_ddv49', 'genderratios', '_chk2m', '_dkvya', '_db1zf', '_cre1l', '_dcgjs', '_d9ney', '_df9om', '_cokwr', '_cn6ca', 'agegroups', '_d415a', '_ciyn3', '_d5fpr', '_cpzh4', '_cx0b9'}
        first_row = True
        for row in nims_data['Population']:
            if first_row:
                first_row = False
                continue
            data_row = True
            for key in keys:
                if not key in row:
                    data_row = False
                    break
            if not data_row:
                continue
            lga              = row['_cpzh4']
            state            = row['_cn6ca']
            location         = ("Nigeria", state, lga)
            pop              = int(row['_ciyn3'])
            pop_male         = int(row['_cre1l'])
            pop_female       = int(row['_chk2m'])
            pop_ratio_male   = float(pop_male) / float(pop)
            pop_ratio_female = float(pop_female) / float(pop)
            pop_ratio_u4     = float(row['agegroups'])
            pop_u5_male      = int(float(row['childrenunderfive']))
            pop_u5_female    = int(float(row['_dkvya']))
            if location in locations:
                lga_loaded.append(lga)
                data = [
                    ('population', pop),
                    ('population_ratio_male', pop_ratio_male),
                    ('population_ratio_female', pop_ratio_female),
                    ('population_ratio_under_4', pop_ratio_u4),
                    ('population_under_5_male', pop_u5_male),
                    ('population_under_5_female', pop_u5_female)
                ]
                e = mangrove.datastore.entity.get(dbm, locations[location])
                e.add_data(data)
            else:
                #print "...no LGA corresponsing to: %s" % lga
                if not lga in lga_failed:
                    lga_failed.append(lga)

        print "Loaded data for %d out of %d LGAs" % (len(lga_loaded), len(lga_failed) + len(lga_loaded))
        if lga_failed:
            print "%d LGAs failed to load:" % len(lga_failed)
            for lga in lga_failed:
                print "\t%s" % lga

        print "Adding MDG indicator data..."
        indicators = {}

        print "Adding data from 'Education MDG Data' worksheet"
        lga_loaded = []
        lga_failed = []
        for row in nims_data['Education MDG Data']:
            slug = str(self._slugify(unicode(row['indicator'], 'utf-8')))
            data_type = 'numeric'
            lga = row['lga']
            state = row['state']
            location = ("Nigeria", state, lga)
            #if not slug in indicators:
            #    indicator = {
            #        'slug': slug,
            #        'name': row['indicator'],
            #        'description': row['indicatordefinition'],
            #        'type': data_type,
            #        'tags': ['Education']
            #    }
            #    indicators[slug] = indicator
            data = [(slug , row['value'])]
            if location in locations:
                lga_loaded.append(lga)
                e = mangrove.datastore.entity.get(dbm, locations[location])
                e.add_data(data)
            else:
                if not lga in lga_failed:
                    lga_failed.append(lga)

        print "Loaded data for %d out of %d LGAs" % (len(lga_loaded), len(lga_failed) + len(lga_loaded))
        if lga_failed:
            print "%d LGAs failed to load:" % len(lga_failed)
            for lga in lga_failed:
                print "\t%s" % lga

        print "Adding data from 'Infrastructure MDG Data' worksheet"
        lga_loaded = []
        lga_failed = []
        for row in nims_data['Infrastructure MDG Data']:
            slug = str(self._slugify(unicode(row['indicator'], 'utf-8')))
            data_type = 'numeric'
            lga = row['lga']
            state = row['state']
            location = ("Nigeria", state, lga)
            #if not slug in indicators:
            #    indicator = {
            #        'slug': slug,
            #        'name': row['indicator'],
            #        'description': row['indicatordefinition'],
            #        'type': data_type,
            #        'tags': ['Infrastructure']
            #    }
            #    indicators[slug] = indicator
            data = [(slug , row['value'])]
            if location in locations:
                lga_loaded.append(lga)
                e = mangrove.datastore.entity.get(dbm, locations[location])
                e.add_data(data)
            else:
                if not lga in lga_failed:
                    lga_failed.append(lga)

        print "Loaded data for %d out of %d LGAs" % (len(lga_loaded), len(lga_failed) + len(lga_loaded))
        if lga_failed:
            print "%d LGAs failed to load:" % len(lga_failed)
            for lga in lga_failed:
                print "\t%s" % lga

        print "Adding data from 'Health MDG Data' worksheet"
        lga_loaded = []
        lga_failed = []
        for row in nims_data['Health MDG Data']:
            slug = str(self._slugify(unicode(row['indicator'], 'utf-8')))
            data_type = 'numeric'
            lga = row['lga']
            state = row['state']
            location = ("Nigeria", state, lga)
            #if not slug in indicators:
            #    indicator = {
            #        'slug': slug,
            #        'name': row['indicator'],
            #        'description': row['indicatordefinition'],
            #        'type': data_type,
            #        'tags': ['Infrastructure']
            #    }
            #    indicators[slug] = indicator
            data = [(slug , row['value'])]
            if location in locations:
                lga_loaded.append(lga)
                e = mangrove.datastore.entity.get(dbm, locations[location])
                e.add_data(data)
            else:
                if not lga in lga_failed:
                    lga_failed.append(lga)

        print "Loaded data for %d out of %d LGAs" % (len(lga_loaded), len(lga_failed) + len(lga_loaded))
        if lga_failed:
            print "%d LGAs failed to load:" % len(lga_failed)
            for lga in lga_failed:
                print "\t%s" % lga