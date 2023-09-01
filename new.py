import open3d as o3d
import json
from geonav_conversions import xy2ll 
import yaml

def read_config(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def pcd_to_geojson(input_pcd, output_geojson, config_file):
    config = read_config(config_file)
    orglat = config.get('map_origin', {}).get('latitude', 0.0)
    orglon = config.get('map_origin', {}).get('longitude', 0.0)
    pcd = o3d.io.read_point_cloud(input_pcd)
    points = pcd.points
    

    # features = []  # List to store GeoJSON features
    
    # for point in points:
    #     x, y, _ = point
    #     lat, lon = xy2ll(x, y, orglat, orglon)

    #     # Create a GeoJSON feature with "Point" geometry for each point
    #     feature = {
    #         "type": "Feature",
    #         "geometry": {
    #             "type": "Point",
    #             "coordinates": [lon, lat]  # Longitude, Latitude
    #         }
    #     }

    #     features.append(feature)

    # # Create a GeoJSON feature collection
    # geojson_data = {
    #     "type": "FeatureCollection",
    #     "features": features
    # }
    coordinates = []
    for point in points:
        x, y, _ = point
        lat,lon = xy2ll(x, y, orglat, orglon)
        coordinates.append([lon, lat])

    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "Name": "demo" 
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordinates]
                },
                "id": 0
            }
        ]
    }

    with open(output_geojson, "w") as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2)

if __name__ == "__main__":
    input_pcd = "/home/sanjay/Downloads/pointcloud_map.pcd" 
    output_geojson = "output2.geojson" 
    config_file = "/home/sanjay/Downloads/map_config.yaml" 

    pcd_to_geojson(input_pcd, output_geojson, config_file)

