from .json_writer import StreamingCompressedJSONWriter
from bentso.iterators import iterate_generation, iterate_trade, COUNTRIES
from .load_metadata import get_metadata
from .rdf_formatter import format_supply_flow, format_trade_flow
from itertools import count


# Generated from
# https://github.com/BONSAMURAIS/Correspondence-tables/blob/master/final_tables/tables/exiobase_to_bentso_activities.csv
ACTIVITY_MAPPING = {
    'Fossil Hard coal': 'Production of electricity by coal',
    'Fossil Brown coal/Lignite': 'Production of electricity by coal',
    'Fossil Gas': 'Production of electricity by gas',
    'Fossil Coal-derived gas': 'Production of electricity by gas',
    'Nuclear': 'Production of electricity by nuclear',
    'Hydro Pumped Storage': 'Production of electricity by hydro',
    'Hydro Run-of-river and poundage': 'Production of electricity by hydro',
    'Hydro Water Reservoir': 'Production of electricity by hydro',
    'Wind Offshore': 'Production of electricity by wind',
    'Wind Onshore': 'Production of electricity by wind',
    'Fossil Oil': 'Production of electricity by petroleum and other oil derivatives',
    'Biomass': 'Production of electricity by biomass and waste',
    'Waste': 'Production of electricity by biomass and waste',
    'Solar': 'Production of electricity by solar thermal',
    'Other renewable': 'Production of electricity by tide, wave, ocean',
    'Geothermal': 'Production of electricity by Geothermal',
    'Other': 'Production of electricity nec',
}
FLOW_MAPPING = {
    'Fossil Hard coal': 'Electricity by coal',
    'Fossil Brown coal/Lignite': 'Electricity by coal',
    'Fossil Gas': 'Electricity by gas',
    'Fossil Coal-derived gas': 'Electricity by gas',
    'Nuclear': 'Electricity by nuclear',
    'Hydro Pumped Storage': 'Electricity by hydro',
    'Hydro Run-of-river and poundage': 'Electricity by hydro',
    'Hydro Water Reservoir': 'Electricity by hydro',
    'Wind Offshore': 'Electricity by wind',
    'Wind Onshore': 'Electricity by wind',
    'Fossil Oil': 'Electricity by petroleum and other oil derivatives',
    'Biomass': 'Electricity by biomass and waste',
    'Waste': 'Electricity by biomass and waste',
    'Solar': 'Electricity by solar thermal',
    'Other renewable': 'Electricity by tide, wave, ocean',
    'Geothermal': 'Electricity by Geothermal',
    'Other': 'Electricity nec',
}

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
