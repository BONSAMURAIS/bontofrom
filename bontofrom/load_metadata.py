import csv
from pathlib import Path

metadata_dir = Path(__file__).parent / "meta"

def get_metadata():
    metadata = {}

    _ = lambda x: x if x.startswith("http://") else "http://" + x

    with open(metadata_dir / "exiobase_activitytype_URIs.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        metadata['activitytype'] = {row[0]: _(row[3]) for row in reader if row}

    with open(metadata_dir / "exiobase_flowobject_URIs.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        metadata['flowobject'] = {row[0]: _(row[3]) for row in reader if row}

    with open(metadata_dir / "exiobase_location_URIs.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        metadata['location'] = {row[0]: _(row[2]) for row in reader if row}

    with open(metadata_dir / "USEPA_URI.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        metadata['location'] = {row[0]: _(row[1]) for row in reader if row}
        
    with open(metadata_dir / "lcia_activitytype_uri.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        metadata['location'] = {row[0]: _(row[1]) for row in reader if row}
        
    with open(metadata_dir / "lcia_flowobject_uri.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        metadata['location'] = {row[0]: _(row[1]) for row in reader if row}

    metadata['unit'] = {
        'kilogram': 'http://www.ontology-of-units-of-measure.org/resource/om-2/kilogram',
        'megajoule': 'http://www.ontology-of-units-of-measure.org/resource/om-2/megajoule',
        'euro': 'http://www.ontology-of-units-of-measure.org/resource/om-2/euro',
        'hectare': 'http://www.ontology-of-units-of-measure.org/resource/om-2/hectare',
        'cubic meters': '',
    }

    metadata['time']: {
        '2011': "http://rdf.bonsai.uno/time/2011",
        '2015': "http://rdf.bonsai.uno/time/2015",
        '2016': "http://rdf.bonsai.uno/time/2016",
        '2017': "http://rdf.bonsai.uno/time/2017",
        '2018': "http://rdf.bonsai.uno/time/2018",
    }

    return metadata
