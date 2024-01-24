# Use the tool

Inspired from https://github.com/piebro/map2svg, thanks to [piebro](https://github.com/piebro) !

## startup

1. start the postgres container with `docker-compose up -d postgres`

2. copy your .osm.pbf file into the `data` folder `wget http://download.geofabrik.de/europe/andorra-latest.osm.pbf -O data/http://download.geofabrik.de/europe/andorra-latest.osm.pbf`
  
    * you can get .osm.pbf files them from <http://download.geofabrik.de/>

3. import OSM datas with `docker-compose run import-osm`


## create svg

To create an svg run with the wanted table, bbox and filename. Check `config-example.yaml` file to set your own bbox.

```bash
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 map2svg.py config-example.yaml mymap.svg
```

## helpful

### pgadmin

1. to acces pgadmin, start pgadmin containers with `docker-compose up -d pgadmin`

2. open `http://localhost:8432`, login is `admin@admin.org`, password in `admin`

3. To visualize imported tables OSM > Databases > openmatiles > Schemas > public > Tables

### log into postgres

to log into postgres db run `PGPASSWORD=openmaptiles psql -h localhost -U openmaptiles -d openmaptiles` there you can use `\d` to check for all table and `\d+ table_name` to check out the columns of a table

run `select * from table_name limit 1;` to checkout a table or `select ST_AsGeoJSON(ST_Transform(geometry, 4326)) from table_name limit 1;` to checkout the goemetry of a table

### common tables

- osm_building_multipolygon
- osm_building_polygon
- osm_building_polygon_gen1
- osm_highway_linestring
- osm_highway_linestring_gen1
- osm_highway_linestring_gen2
- osm_highway_polygon
- osm_island_polygon
- osm_landcover_polygon
- osm_landuse_polygon
- osm_park_polygon
- osm_peak_point
- osm_railway_linestring
- osm_water_polygon
- osm_waterway_linestring

### all possible tables

- osm_aerialway_linestring
- osm_aerialway_linestring_gen1
- osm_aerodrome_label_point
- osm_aeroway_linestring
- osm_aeroway_linestring_gen1
- osm_aeroway_linestring_gen2
- osm_aeroway_linestring_gen3
- osm_aeroway_polygon
- osm_aeroway_polygon_gen1
- osm_aeroway_polygon_gen2
- osm_aeroway_polygon_gen3
- osm_building_multipolygon
- osm_building_polygon
- osm_building_polygon_gen1
- osm_building_street
- osm_city_point
- osm_continent_point
- osm_country_point
- osm_highway_linestring
- osm_highway_linestring_gen1
- osm_highway_linestring_gen2
- osm_highway_polygon
- osm_housenumber_point
- osm_island_point
- osm_island_polygon
- osm_landcover_polygon
- osm_landcover_polygon_gen1
- osm_landcover_polygon_gen2
- osm_landcover_polygon_gen3
- osm_landcover_polygon_gen4
- osm_landcover_polygon_gen5
- osm_landcover_polygon_gen6
- osm_landcover_polygon_gen7
- osm_landuse_polygon
- osm_landuse_polygon_gen1
- osm_landuse_polygon_gen2
- osm_landuse_polygon_gen3
- osm_landuse_polygon_gen4
- osm_landuse_polygon_gen5
- osm_marine_point
- osm_park_polygon
- osm_park_polygon_gen1
- osm_park_polygon_gen2
- osm_park_polygon_gen3
- osm_park_polygon_gen4
- osm_park_polygon_gen5
- osm_park_polygon_gen6
- osm_park_polygon_gen7
- osm_park_polygon_gen8
- osm_peak_point
- osm_poi_point
- osm_poi_polygon
- osm_railway_linestring
- osm_railway_linestring_gen1
- osm_railway_linestring_gen2
- osm_railway_linestring_gen3
- osm_railway_linestring_gen4
- osm_railway_linestring_gen5
- osm_shipway_linestring
- osm_shipway_linestring_gen1
- osm_shipway_linestring_gen2
- osm_state_point
- osm_water_polygon
- osm_water_polygon_gen1
- osm_water_polygon_gen2
- osm_water_polygon_gen3
- osm_water_polygon_gen4
- osm_water_polygon_gen5
- osm_water_polygon_gen6
- osm_waterway_linestring
- osm_waterway_linestring_gen1
- osm_waterway_linestring_gen2
- osm_waterway_linestring_gen3
