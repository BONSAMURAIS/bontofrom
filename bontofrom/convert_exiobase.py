"""
Parse exiobase xlsb USE and SUP files, and produce jsonld bz2 archives.
"""
from pyxlsb import open_workbook
from tqdm import tqdm
import logging
import itertools

from .json_writer import StreamingCompressedJSONWriter
from .load_metadata import get_metadata
from .rdf_formatter import (
    format_supply_flow,
    format_domestic_use_flow,
    format_trade_flow,
)

# Exiobase comes with tonnes, TJ and Meuro values, but BONSAI uses kg, MJ & €
DATA_SHEET_INDEX = 2
TONNESTOKG = 1000
TJTOMJ = 1 / 1e06
MEUROTOEURO = 1e06

TONNES = "tonnes"
TJ = "TJ"
MEURO = "Meuro"


def associate_col_activity(work_sheet):
    """ Create dictionary of column index -> {activitytype, location}

    """
    entries = {}
    for index, row in enumerate(work_sheet.rows()):
        if index not in [0, 1]:  # zero based indexing of rows
            break
        for cell in row:
            if cell.v:
                if index == 0:
                    entries[cell.c] = {"location": cell.v}
                if index == 1:  # the country code
                    entries[cell.c]["activitytype"] = cell.v
        continue
    return entries


def isdiagonal(cell):
    return cell.r + 1 == cell.c


def isunitneedsconversion(unit):
    return unit in [TONNES, TJ, MEURO]


def isdomesticuse(cell, entries, rowdata):
    """
    In the USE exiobase tables, domestic use cells are those of the diagonal
    belonging to a same country. In the scheme blow, domesticuse cells are
    those of the box of `#` surrounding a country code.::

    ######············
    # AT #············
    ######············
    ······######······
    ······# AU #······
    ······######······
    ············######
    ::
    """
    column_country = entries[cell.c]["location"]
    row_country = rowdata[0]
    return column_country == row_country


def convert_amount(value, sourceunit):
    if sourceunit not in [TJ, TONNES, MEURO]:
        raise Exception("sourceunit unit must be TJ, tonnes or Meuro")
    factor = 1

    if sourceunit == TJ:
        factor = TJTOMJ
    if sourceunit == TONNES:
        factor = TONNESTOKG
    if sourceunit == MEURO:
        factor = MEUROTOEURO
    return value * factor


def get_unit_uri(cell, units):
    """
    Provide the Bonsai unit for a given exiobase unit.
    Bonsai uses kilogram, megajoule and euro as units.
    """
    if cell.v == TONNES:
        unit_uri = units["kilogram"]
    elif cell.v == TJ:
        unit_uri = units["megajoule"]
    elif cell.v == MEURO:
        unit_uri = units["euro"]
    else:
        unit_uri = units[cell.v]

    return unit_uri


def process_supply_row(index, row, entries, metadata, a_counter, mapping_dict):
    writer = StreamingCompressedJSONWriter("supply_flows")
    supply_flows = []
    units = metadata["unit"]
    locations = metadata["location"]
    activitytypes = metadata["activitytype"]
    flowobjects = metadata["flowobject"]
    times = metadata["time"]
    if index > 3:
        cells = [c for c in row if c.v != 0]

        flow_object = cells[1].v
        unit_uri = get_unit_uri(cells[4], units)
        year_uri = times["2011"]

        for cell in cells[5:]:
            location_uri = locations[entries[cell.c]["location"]]
            activitytype = entries[cell.c]["activitytype"]
            activity_type_uri = activitytypes[activitytype]
            flow_object_uri = flowobjects[flow_object]
            isdetermining_flow = isdiagonal(cell)
            amount = get_amount(cells[4], cell)

            supply_flow, supply_flow_ids_dict = format_supply_flow(
                amount,
                unit_uri,
                location_uri,
                activity_type_uri,
                flow_object_uri,
                year_uri,
                isdetermining_flow,
                a_counter,
                mapping_dict,
            )
            supply_flows.append(supply_flow)
            writer.write_obj(supply_flow)
    writer.finish()
    return supply_flows, mapping_dict


def get_amount(base_unit, cell):
    """ Return the value of the cell, converted to Bonsai units if necessary"""
    if isunitneedsconversion(base_unit):
        return convert_amount(cell.v, base_unit)
    return cell.v


def process_use_row(index, row, entries, metadata, a_counter, mapping_dict):
    writer_domestic = StreamingCompressedJSONWriter("domestic_flows")
    writer_trade = StreamingCompressedJSONWriter("trade_flows")
    domestic_flows = []
    trade_flows = []

    units = metadata["unit"]
    locations = metadata["location"]
    activitytypes = metadata["activitytype"]
    flowobjects = metadata["flowobject"]
    times = metadata["time"]

    if index > 3:
        cells = [c for c in row if c.v != 0]
        row_data = cells[:5]
        unit_uri = get_unit_uri(cells[4], units)

        flow_object = cells[1].v
        year_uri = times["2011"]

        for cell in cells[5:]:
            location_uri = locations[entries[cell.c]["location"]]
            activitytype = entries[cell.c]["activitytype"]
            activity_type_uri = activitytypes[activitytype]
            flow_object_uri = flowobjects[flow_object]

            amount = get_amount(cells[4], cell)

            if isdomesticuse(cell, entries, row_data):
                use_flow = format_domestic_use_flow(
                    amount,
                    unit_uri,
                    location_uri,
                    activity_type_uri,
                    flow_object_uri,
                    year_uri,
                    a_counter,
                    mapping_dict,
                )
                domestic_flows.append(use_flow)
                writer = writer_domestic
            else:  # Trade flow
                # from _row_ region to _column_ region
                from_location_uri = locations[cells[0].v]
                to_location_uri = location_uri
                use_flow = format_trade_flow(
                    amount,
                    unit_uri,
                    from_location_uri,
                    to_location_uri,
                    activity_type_uri,
                    flow_object_uri,
                    year_uri,
                    a_counter,
                    mapping_dict,
                )
                trade_flows.append(use_flow)
                writer = writer_trade
            writer.write_obj(use_flow)
    writer_domestic.finish()
    writer_trade.finish()


def convert_supply_table(metadata, supplyfile, limit):
    mapping_dict = {}
    a_counter = itertools.count()
    with open_workbook(supplyfile) as work_book:
        work_sheet = work_book.get_sheet(DATA_SHEET_INDEX)
        entries = associate_col_activity(work_sheet)
        if limit == -1:
            limit = work_sheet.dimension.h
        for index, row in tqdm(enumerate(work_sheet.rows()), total=limit):
            if index < limit:
                process_supply_row(
                    index, row, entries, metadata, a_counter, mapping_dict
                )
                continue
            break
    return mapping_dict


def convert_use_table(metadata, usefile, limit, mapping_dict):
    a_counter = itertools.count()
    with open_workbook(usefile) as wb:
        ws = wb.get_sheet(DATA_SHEET_INDEX)
        entries = associate_col_activity(ws)
        if limit == -1:
            limit = ws.dimension.h
        for index, row in tqdm(enumerate(ws.rows()), total=limit):
            if index < limit:
                process_use_row(index, row, entries, metadata, a_counter, mapping_dict)
                continue
            break


def convert_tables(metadata, supplyfile, usefile, limit):
    mapping_dict = convert_supply_table(metadata, supplyfile, limit)
    convert_use_table(metadata, usefile, limit, mapping_dict)


def convert_exiobase(supplyfile, usefile, limit, rdfpath):
    metadata = get_metadata(rdfpath)
    convert_tables(metadata, supplyfile, usefile, limit)
