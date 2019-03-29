from .json_writer import StreamingCompressedJSONWriter
from .rdf_formatter import format_supply_flow, format_trade_flow
from arborist import get_metadata
from beebee.convert_entsoe_to_numpy import ACTIVITY_MAPPING, FLOW_MAPPING
from bentso.iterators import iterate_generation, iterate_trade, COUNTRIES
from itertools import count


def convert_entsoe_to_jsonld(year, filepath, rdf_base_dir):
    metadata = get_metadata(rdf_base_dir)
    writer = StreamingCompressedJSONWriter(filepath)
    counter = count(1)

    # Get grid mixes
    for technology, country, amount in iterate_generation(year):
        mapping = {}

        if country not in metadata['location']:
            # Skip countries which don't match EXIOBASE world
            continue

        data, mapping = format_supply_flow(
            amount,
            metadata['unit']['megajoule'],
            metadata['location'][country],
            metadata['activitytype'][ACTIVITY_MAPPING[technology]],
            metadata['flowobject'][FLOW_MAPPING[technology]],
            metadata['time'][str(year)],
            True,
            counter,
            mapping
        )
        writer.write_obj(data)

    writer.finish()
