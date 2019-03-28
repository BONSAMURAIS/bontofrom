def format_supply_flow(amount, unit, location, activity_type, flow_object, unit, counter):
    """Return a list of RDF triples as Python for a supply ``Flow``.

    ``amount`` is a float.

    ``unit``, ``location``, ``activity_type``, ``unit``, and ``flow_object`` are strings **with URI prefixes already substituted**.

    ``counter`` is an instance of ``collections.Counter`` used to count blank nodes."""
    activity_uri = "brdfsu:{}".format(next(counter))
    flow_uri = "brdfsu:{}".format(next(counter))
    return [{
        # Activity instance
        "@id" : activity_uri,
        "@type" : "bont:Activity",
        "bont:activityType" : activity_type,
        "bont:location": location,
        "bont:temporalExtent": "TBD",
        "bont:determiningFlow": flow_uri,
    }, {
        # Flow instance
        "@id": "brdfsu:{}".format(next(counter)),
        "@type" : "bont:Flow",
        "bont:outputOf": activity_uri,
        "om2:hasNumericalValue": amount,
        "bont:objectType" : flow_object,
        "om2:hasUnit" : "om2:" + unit
    }]
