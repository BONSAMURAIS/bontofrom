from .json_writer import StreamingCompressedJSONWriter
from .load_metadata import get_metadata
from .rdf_formatter import format_supply_flow, format_trade_flow
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
        data, mapping = format_supply_flow(
            amount,
            metadata['units']['megajoule'],
            metadata['locations'][country],
            activity_type,
            flow_object,
            metadata['year'][str(year)],
            True,
            counter,
            mapping
        )
        writer.write_obj(data)

    writer.finish()
