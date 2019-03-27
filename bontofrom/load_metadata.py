import csv
from pathlib import Path

metadata_dir = Path(__file__).parent / "meta"

metadata = {}

with open(metadata_dir / "exiobase_activitytype_URIs.csv", "r", encoding='utf-8') as f:
    reader = csv.reader(f)
    # Skip header
    next(reader)
    metadata['activity type'] = {row[0]: row[3] for row in reader if row}

with open(metadata_dir / "exiobase_flowobject_URIs.csv", "r", encoding='utf-8') as f:
    reader = csv.reader(f)
    # Skip header
    next(reader)
    metadata['flow objects'] = {row[0]: row[3] for row in reader if row}

get_location = lambda l: (l[0], l[1]) if l[1] else (l[0], l[2])

with open(metadata_dir / "exiobase_location_URIs.csv", "r", encoding='utf-8') as f:
    reader = csv.reader(f)
    # Skip header
    next(reader)
    metadata['locations'] = dict(get_location(row) for row in reader if row)


metadata['units'] = {
    'kilogram': 'http://www.ontology-of-units-of-measure.org/resource/om-2/kilogram',
    'megajoule': 'http://www.ontology-of-units-of-measure.org/resource/om-2/megajoule',
    'euro': 'http://www.ontology-of-units-of-measure.org/resource/om-2/euro',
}
