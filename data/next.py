#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Re-format the YAML-ish curated entities into intermediate JSON.
"""

from collections import defaultdict
import datetime as dt
import csv
import io
import json
import pathlib
import re
import sys
import typing

from icecream import ic

from lavie import make_hash, make_uuid, scrub_name, \
    LOGGER, SIM_THRESH


PAT_KEYVAL: re.Pattern = re.compile(r"(\w+)\:\s+(\S.*)")


TRANSLATE: dict[ str, str ] = {
    "addr": "bods:streetAddress",
    "birth": "bods:birthDate",
    "class": "lavie:class",
    "code": "bods:idString",
    "country": "bods:code",
    "dis": "bods:dissolutionDate",
    "edd": "lavie:edd",
    "lei": "lavie:lei",
    "officer": "lavie:officers",
    "reg": "bods:foundingDate",
    "related": "skos:related",
    "sanction": "lavie:sanction",
    "source": "lavie:source",
    "synopsis": "lavie:synopsis",
    "wiki": "lavie:wiki",
}
	

MULTI_FIELD: list[ str ] = [
    "lavie:edd",
    "lavie:officers",
    "lavie:sanction",
    "skos:related",
]


def reader (
    fp: io.TextIOWrapper,
    *,
    kind: str = "person",
    debug: bool = False, # True
    ) -> typing.Iterator[ dict ]:
    """
Iterator for lines read from file in a bizarre YAML-ish format.
    """
    record: dict = {}
    in_rec: bool = True

    for line in fp:
        if debug:
            ic(line)

        if line.startswith("\t"):
            in_rec = True
            match_obj = PAT_KEYVAL.match(line.strip())

            if match_obj is not None:
                key: str = TRANSLATE[match_obj.group(1)]
                val: str = match_obj.group(2)

                if key in MULTI_FIELD:
                    if key not in record:
                        record[key] = []

                    record[key].append(val)

                elif key in [ "bods:code", ]:
                    record[key] = "codes:" + val

                elif key in [ "lavie:source," ]:
                    record["bods:source"] = {
                        "bods:url": val,
                        "bods:type": "bods:thirdParty",
                    }

                elif key in [ "lavie:lei", ]:
                    record["lavie:lei"] = {
                        "bods:idString": val,
                        "bods:scheme": "XI-LEI",
                        "bods:schemeName": "Global Legal Entity Identifier Index",
                    }

                else:
                    # simple key/value attribute
                    record[key] = val

            else:
                # an alias
                name: str = line.strip()
                record["lavie:aliases"].append(scrub_name(name))

        else:
	    # name @ beginning of a record
            if in_rec:
                if len(record) > 0:
                    # finalize record and emit
                    match kind:
                        case "person":
                            record["bods:personType"] = "codes:knownPerson"
                        case "company":                        
                            record["bods:entityType"] = "codes:RegisteredEntity"
                        case _:
                            LOGGER.error(f"UNKNOWN kind: {kind}")

                    record["bods:retrievedAt"] = dt.datetime.now(dt.UTC).isoformat()

                    if debug:
                        print(record)

                    yield record


                # initialize a new record, or quit?
                if line.lower().strip() == "caboose":
                    return
                else:
                    name: str = line.split("\t")[1].strip()

                    record = {
                        "bods:fullName": scrub_name(name),
                        "lavie:aliases": [],
                    }

            in_rec = False


if __name__ == "__main__":

    ######################################################################
    # load the manually curated entities

    curated_source: str = "next.txt"
    kind: str = "company" # "person"

    curated_path: pathlib.Path = pathlib.Path(curated_source)
    persist_data: list = []

    with open(curated_path, mode = "r", encoding = "utf-8") as fp:
        for record in reader(fp, kind = kind):
            persist_data.append(record)


    ######################################################################
    # persist the results

    persist_path: pathlib.Path = pathlib.Path("out.json")

    with open(persist_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            persist_data,
            fp,
            ensure_ascii = False,
            indent = 4,
        )
