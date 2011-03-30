# sample script to show the API

from entity import Entity

# create an entity
e = Entity(entity_type='location', name='USA')
f = Entity(entity_type='hospital', name="St. Luke's")

# access entity properties
print "%s (%s)" % (e.name, e.id)
print "%s (%s)" % (f.name, f.id)

# update an entity
e.update(name="NYU Medical Center")
print "%s (%s)" % (e.name, e.id)

# delete an entity
f.delete()

# store data on an entity
