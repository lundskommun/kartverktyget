import json

from pprint import pprint


def export_to_geojson(contributions):
    document = {
        "type": "FeatureCollection",
        "features": []
    }

    for contribution in contributions:
        properties = json.loads(contribution.questionnaire_data)
        feature = json.loads(contribution.geometry_data)
        feature['properties'] = properties
        pprint(feature)
        document['features'].append(feature)

    return json.dumps(document)
