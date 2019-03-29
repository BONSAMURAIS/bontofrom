from bontofrom.convert_metadata import get_metadata
from pyxlsb import open_workbook
from tqdm import tqdm
from bontofrom.rdf_formatter import format_supply_flow, format_domestic_use_flow, format_trade_flow
from .json_writer import StreamingCompressedJSONWriter
from arborist import get_metadata

import itertools

DATA_SHEET_INDEX = 2
TONNESTOKG = 1000
TJTOMJ = 1 / 1e06
MEUROTOEURO = 1e06


def associate_col_activity(activity_metadata, ws):
    """ Create dictionary of column index -> {activitytype, location}
    """
    entries = {}
    for index, row in enumerate(ws.rows()):
        if index not in [0, 1]:  # zero based indexing of rows
            break
        for c in row:
            if c.v:
                if index == 0:
                    entries[c.c] = {"location": c.v}
                if index == 1:  # the country code
                    entries[c.c]["activitytype"] = c.v
        continue
    return entries


def isdiagonal(c):
    return c.r + 1 == c.c


def isunitneedsconversion(u):
    return u == "tonnes" or u == "TJ" or u == "Meuro"

def isdomesticuse(c, entries, rowdata):
    column_country = entries[c.c]['location']
    row_country = rowdata[0]
    return column_country == row_country

def convertAmount(v, sourceunit):
    if sourceunit == "TJ":
        return v * TJTOMJ
    if sourceunit == "tonnes":
        return v * TONNESTOKG
    if sourceunit == "Meuro":
        return v * MEUROTOEURO


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
        # row_data will hold the following info from the file:
        #  Country code	| Product name | Product code 1| 	Product code 2 |	Unit |
        row_data = cells[:5]

        if "tonnes" == cells[4].v:
            unitURI = units["kilogram"]
        elif "TJ" == cells[4].v:
            unitURI = units["megajoule"]
        elif "Meuro" == cells[4].v:
            unitURI = units["euro"]
        else:
            unitURI = units[cells[4].v]

        flow_object = cells[1].v
        yearURI = times["2011"]

        for c in cells[5:]:
            locationURI = locations[entries[c.c]["location"]]
            activitytype = entries[c.c]["activitytype"]
            activity_typeURI = activitytypes[activitytype]
            flow_objectURI = flowobjects[flow_object]
            isdetermining_flow = False
            if isdiagonal(c):
                isdetermining_flow = True

            if isunitneedsconversion(cells[4]):
                amount = convertAmount(c.v, cells[4])
            else:
                amount = c.v
            supply_flow, dict = format_supply_flow(
                amount,
                unitURI,
                locationURI,
                activity_typeURI,
                flow_objectURI,
                yearURI,
                isdetermining_flow,
                a_counter,
                mapping_dict
            )
            writer.write_obj(supply_flow)
    writer.finish()
    return supply_flows, mapping_dict

def  process_use_row(index, row, entries, metadata, a_counter, mapping_dict):
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
        cells = [c for c in row if c.v !=0]
        row_data = cells[:5]

        if "tonnes" == cells[4].v:
            unitURI = units["kilogram"]
        elif "TJ" == cells[4].v:
            unitURI = units["megajoule"]
        elif "Meuro" == cells[4].v:
            unitURI = units["euro"]
        else:
            unitURI = units[cells[4].v]

        flow_object = cells[1].v
        yearURI = times["2011"]

        for c in cells[5:]:
            locationURI = locations[entries[c.c]["location"]]
            activitytype = entries[c.c]["activitytype"]
            activity_typeURI = activitytypes[activitytype]
            flow_objectURI = flowobjects[flow_object]

            if isunitneedsconversion(cells[4]):
                amount = convertAmount(c.v, cells[4])
            else:
                amount = c.v

            if isdomesticuse(c, entries, row_data):
                use_flow = format_domestic_use_flow(
                    amount,
                    unitURI,
                    locationURI, activity_typeURI, flow_objectURI, yearURI,
                    a_counter,
                    mapping_dict
                )
                domestic_flows.append(use_flow)
                writer = writer_domestic
            else: # Trade flow
                # from _row_ region to _column_ region
                from_locationURI = locations[cells[0].v]
                to_locationURI = locationURI
                use_flow = format_trade_flow(
                    amount,
                    unitURI,
                    from_locationURI,
                    to_locationURI,
                    activity_typeURI,
                    flow_objectURI,
                    yearURI,
                    a_counter,
                    mapping_dict
                )
                trade_flows.append(use_flow)
                writer = writer_trade
            writer.write_obj(use_flow)



def convert_supply_table(metadata, supplyfile, limit):
    mapping_dict = {}
    a_counter = itertools.count()
    with open_workbook(supplyfile) as wb:
        ws = wb.get_sheet(DATA_SHEET_INDEX)
        entries = associate_col_activity(metadata["activitytype"], ws)
        if limit == -1:
            limit = ws.dimension.h
        for index, row in tqdm(enumerate(ws.rows()), total=limit):
            if index < limit:
                process_supply_row(index, row, entries, metadata, a_counter, mapping_dict)
                continue
            break
    return mapping_dict


def convert_use_table(metadata, usefile, limit, mapping_dict):
    a_counter = itertools.count()
    with open_workbook(usefile) as wb:
        ws = wb.get_sheet(DATA_SHEET_INDEX)
        entries = associate_col_activity(metadata["activitytype"], ws)
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

def convert_exiobase(supplyfile, usefile, limit):
    metadata = get_metadata("../rdf")
    convert_tables(metadata, supplyfile, usefile, limit)
