def format_supply_flow(amount, unit, location, activity_type, flow_object,
                       time, determining_flow, counter, mapping_dict={}):
    """Return a list of RDF triples as Python for a supply ``Flow``.

    ``amount`` is a float.

    The following are strings **with URI prefixes already substituted**:

        * ``unit``
        * ``location``
        * ``activity_type``
        * ``unit``
        * ``flow_object``
        * ``time``

    ``determining_flow`` is a boolean indicating whether the flow is a determining flow.

    ``counter`` is an instance of ``collections.Counter`` used to count blank nodes.

    ``mapping_dict`` is a dictionary that we keep to do lookups in the future. It has the form:

    .. code-block:: python

        {
            "flows": {(flow_object, location): flow_uri},
            "activities: {(activity_type_uri, location_uri): activity_uri}
        }

    Where ``activity_uri`` and ``flow_uri`` are generated by this function.

    This mapping dictionary is needed for the use functions, as we need the URI references.

    """
    activity_uri = "brdfsuex:{}".format(next(counter))
    flow_uri = "brdfsuex:{}".format(next(counter))
    output = [{
        # Activity instance
        "@id" : activity_uri,
        "@type" : "bont:Activity",
        "bont:activityType" : activity_type,
        "bont:location": location,
        "bont:temporalExtent": time,
    }, {
        # Flow instance
        "@id": flow_uri,
        "@type" : "bont:Flow",
        "bont:outputOf": activity_uri,
        "om2:hasNumericalValue": amount,
        "bont:objectType" : flow_object,
        "om2:hasUnit" : "om2:" + unit
    }]
    if determining_flow:
        output[0]["bont:determiningFlow"] = flow_uri

    if "activities" not in mapping_dict.keys():
        mapping_dict["activities"] = dict()
    if "flows" not in mapping_dict.keys():
        mapping_dict["flows"] = dict()

    mapping_dict["activities"][(activity_type, location)] = activity_uri
    mapping_dict["flows"][(flow_object, location)] = flow_uri

    return output, mapping_dict


def format_domestic_use_flow(amount, unit, location, activity_type, flow_object, time, counter, mapping_dict):
    """Return a list of RDF triples as Python for a domestic use ``Flow``.

    ``amount`` is a float.

    The following are strings **with URI prefixes already substituted**:

        * ``unit``
        * ``location``
        * ``activity_type``
        * ``flow_object``
        * ``time``

    ``counter`` is an instance of ``collections.Counter`` used to count blank nodes.

    ``mapping_dict`` is generated by ``format_supply_flow``, and is not modified.

    """
    activity_uri = mapping_dict["activities"][(activity_type, location)]
    flow_uri = "brdfsuex:{}".format(next(counter))
    input_ = [{
        # Flow instance
        "@id": flow_uri,
        "@type" : "bont:Flow",
        "bont:inputOf": activity_uri,
        "om2:hasNumericalValue": amount,
        "bont:objectType" : flow_object,
        "om2:hasUnit" : "om2:" + unit
    }]
    return input_


def format_trade_flow(amount, unit, from_location, to_location, activity_type, flow_object, time, counter, mapping_dict):
    """

    :param amount:
    :param unit:
    :param from_location:
    :param to_location:
    :param activity_type:
    :param flow_object:
    :param time:
    :param counter:
    :param mapping_dict:

    Model trade using a separate `transport activity <https://schema.org/TransferAction>`__. We need two ``flow`` instances for each trade: one is the production flow in the originating country (that we look up in ``mapping_dict``). The other is created, and links the trade activity to the consuming activity (which we also look up in ``mapping_dict``).

    Note: This function makes several assumptions that are specific to a first deliverable using EXIOBASE, and should not be used in the future! Specifically, we only know how much of a flow object is imported into a country, but not its distribution among different industries."""
    # New trade activity
    trade_activity_uri = "brdfsuex:{}".format(next(counter))
    flow_uri = "brdfsuex:{}".format(next(counter))
    if (activity_type, from_location) not in mapping_dict["activities"].keys() :
        mapping_dict["activities"][(activity_type, from_location)] = "brdfsuex:{}".format(next(counter))
    if (activity_type, to_location) not in mapping_dict["activities"].keys() :
        mapping_dict["activities"][(activity_type, to_location)] = "brdfsuex:{}".format(next(counter))
    if (flow_object, from_location) not in mapping_dict["flows"].keys() :
        mapping_dict["flows"][(flow_object, from_location)] = "brdfsuex:{}".format(next(counter))

    output = [{
        # Activity instance
        "@id": trade_activity_uri,
        "@type": "bont:Activity",
        "@type": "schema:TransferAction",
        "schema:toLocation": to_location,
        "schema:fromLocation": from_location,
        "bont:activityType" : "brdfcore:Transport",
        "bont:temporalExtent": time,
    }, {
        # Flow from production activity into trade
        "@id": mapping_dict["flows"][(flow_object, from_location)],
        "@type": "bont:Flow",
        # WARNING: Assumes that activity type labels are the same across regions!
        # Not generally applicable.
        "bont:outputOf": mapping_dict["activities"][(activity_type, from_location)],
        "bont:inputOf": trade_activity_uri,
        "om2:hasNumericalValue": amount,
        "bont:objectType": flow_object,
        "om2:hasUnit": "om2:" + unit
    }, {
        # Flow from trade activity into consuming activity
        "@id": flow_uri,
        "@type": "bont:Flow",
        "bont:outputOf": trade_activity_uri,
        "bont:inputOf": mapping_dict["activities"][(activity_type, to_location)],
        "om2:hasNumericalValue": amount,
        "bont:objectType": flow_object,
        "om2:hasUnit": "om2:" + unit
    }]
    return output
