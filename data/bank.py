#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Re-format the bank entities.
"""

import datetime as dt
import io
import json
import logging
import pathlib
import sys
import typing

from icecream import ic


ic.configureOutput(
    noColor = True,
)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level = logging.INFO,
)


TARGET_SOURCE: str = "next.txt"


def reader (
    fp: io.TextIOWrapper,
    *,
    debug: bool = False,
    ) -> typing.Iterator[tuple[ bool, typing.Any ]]:
    """
Iterator for lines read from file in a bizarre YAML-ish format.
    """
    for line in fp:
        if debug:
            ic(line)

        if line.startswith("\t\t"):
            # properties
            key, val = line.split("\t")[2].strip().split(": ")

            if debug:
                ic(key, val)

            yield False, (key, val,)
        elif line.startswith("\t"):
	    # aliases
            yield False, line.strip()
        else:
	    # name @ beginning of a record
            yield True, line.split("\t")[1].strip()


def format_json (
    record: dict,
    *,
    debug: bool = False,
    ) -> dict:
    """
Transform the given data into annotated JSON for generating RDF.
    """
    if debug:
        ic(record)

    dat: dict = {
	"lavie:class": record["class"],
        "bods:fullName": record["name"],
        "lavie:aliases": record["alias"],
        "bods:code": "codes:" + record["country"],
        "bods:entityType": "codes:RegisteredEntity",
        "bods:retrievedAt": f"{dt.datetime.now(dt.UTC).isoformat()}",
	"lavie:edd": [],
	"lavie:sanction": [],
	"lavie:related": [],
        "lavie:officers": []
    }

    if "code" in record:
        dat["bods:idString"] = record["code"]

    if "addr" in record:
        dat["bods:streetAddress"] = record["addr"]

    if "reg" in record:
        dat["bods:foundingDate"] = record["reg"]

    if "dis" in record:
        dat["bods:dissolutionDate"] = record["dis"]

    if "source" in record:
        dat["bods:source"] = {
            "bods:url": record["source"],
            "bods:type": "bods:thirdParty",
        }

    if "lei" in record:
        dat["lavie:lei"] = {
            "bods:idString": record["lei"],
            "bods:scheme": "XI-LEI",
            "bods:schemeName": "Global Legal Entity Identifier Index",
        }

    if "officer" in record:
        dat["lavie:officers"] = record["officer"]

    if "edd" in record:
        dat["lavie:edd"].append(record["edd"])

    if "sanction" in record:
        dat["lavie:sanction"].append(record["sanction"])

    if "related" in record:
        dat["lavie:related"].append(record["related"])

    if "synopsis" in record:
        dat["lavie:synopsis"] = record["synopsis"]

    return dat


if __name__ == "__main__":
    # load the bank entities
    target_path: pathlib.Path = pathlib.Path(TARGET_SOURCE)

    out_data: list[ dict ] = []
    record: dict = {}

    start: bool = True
    has_run: bool = False
    debug: bool = False # True

    with open(target_path, mode = "r", encoding = "utf-8") as fp:
        for start, dat in reader(fp, debug = debug):
            has_run = True

            if start:
                if len(record) > 0:
                    out_data.append(format_json(record, debug = debug))

                record = {
                    "name": dat,
                    "alias": [],
                    "edd": [],
                    "officer": [],
                }
            elif isinstance(dat, str):
                record["alias"].append(dat)
            else:
                key, val = dat

                if key in record:
                    record[key].append(val)
                else:
                    record[key] = val


        # handle the last record in the input
        if has_run and len(record) > 0:
            out_data.append(format_json(record))


    # report
    out_path: pathlib.Path = pathlib.Path("out.json")

    with open(out_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            out_data,
            fp,
            ensure_ascii = False,
            indent = 4,
        )
