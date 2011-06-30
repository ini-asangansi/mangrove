Setting Up the POSTGIST and importing location data
======================================

In order to get postgis configured and import location data - this is what you need to do:

* Install Spatial Database PostgreSQL (with PostGIS),
* Install Geospatial Libraries¶
* Create Spatial Database Template for PostGIS
* Create spatial database using the template
* Import the shape files in the spatial database


Details
-------

* Install Spatial Database PostgreSQL (with PostGIS)::

    $ sudo apt-get install postgresql

    for details visit the url https://help.ubuntu.com/community/PostgreSQL

* Install Geospatial Libraries & Create Spatial Database Template for PostGIS::

    follow the instructions from the url: https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#spatialdb-template


* Create spatial database using the template::

    follow the instructions from the url: https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#setting-up

* Import the shape files in the spatial database::

    datawinners/location/utils.py has function load_from_shp_file to import the shape files. shape are files are store at git://github.com/mangroveorg/shape_files.git

