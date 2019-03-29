import csv
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDFS

metadata_dir = Path(__file__).parent / "meta"


def get_turtle_labels(filepath):
    if isinstance(filepath, Path):
        filepath = filepath.absolute()

    g = Graph()
    g.parse(str(filepath), format="turtle")

    label = URIRef('http://www.w3.org/2000/01/rdf-schema#label')

    for x, y, z in g:
        if y == label:
            # Flip to go from label to URI
            yield str(z), str(x)

def get_metadata(rdf_base):
    if not isinstance(rdf_base, Path):
        rdf_base = Path(rdf_base)

    metadata = {}

    _ = lambda x: x if x.startswith("http://") else "http://" + x

    exiobase_activity_types = dict(get_turtle_labels(
        rdf_base / "activitytype" / "exiobase3_3_17" / "exiobase3_3_17.ttl"
    ))
    grid_activity_types = dict(get_turtle_labels(
        rdf_base / "activitytype" / "core" / "electricity_grid" / "electricity_grid.ttl"
    ))

    metadata["activitytype"] = exiobase_activity_types
    metadata["activitytype"].update(grid_activity_types)

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
        metadata['elem_flows'] = {row[0]: _(row[1]) for row in reader if row}

    with open(metadata_dir / "lcia_activitytype_uri.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        metadata['lcia_activitytype'] = {row[0]: _(row[1]) for row in reader if row}

    with open(metadata_dir / "lcia_flowobject_uri.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        metadata['lcia_fo'] = {row[0]: _(row[1]) for row in reader if row}

    metadata['unit'] = {
        'kilogram': 'http://www.ontology-of-units-of-measure.org/resource/om-2/kilogram',
        'megajoule': 'http://www.ontology-of-units-of-measure.org/resource/om-2/megajoule',
        'euro': 'http://www.ontology-of-units-of-measure.org/resource/om-2/euro',
        'hectare': 'http://www.ontology-of-units-of-measure.org/resource/om-2/hectare',
        'cubic meters': '',
    }

    metadata['time'] = {
        '2011': "http://rdf.bonsai.uno/time/2011",
        '2015': "http://rdf.bonsai.uno/time/2015",
        '2016': "http://rdf.bonsai.uno/time/2016",
        '2017': "http://rdf.bonsai.uno/time/2017",
        '2018': "http://rdf.bonsai.uno/time/2018",
    }

    return metadata
