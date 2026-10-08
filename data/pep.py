#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Construct a thesaurus from the data to use to build a KG.
"""

from collections import defaultdict
import csv
import io
import json
import logging
import pathlib
import re
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


TRANSLATE: dict[ str, str ] = {
    "addr": "bods:streetAddress",
    "birth": "bods:birthDate",
    "country": "bods:code",
    "edd": "lavie:edd",
    "sanction": "lavie:sanction",
    "source": "lavie:source",
    "synopsis": "lavie:synopsis",
    "wiki": "lavie:wiki",
    "related": "skos:related",
}


def reader (
    fp: io.TextIOWrapper,
    *,
    debug: bool = False,
    ) -> typing.Iterator[ dict ]:
    """
Iterator for lines read from file in a bizarre YAML-ish format.
    """
    pat = re.compile(r"(\w+)\:\s+(\S.*)")

    record: dict = {}
    in_rec: bool = True

    for line in fp:
        if debug:
            ic(line)

        if line.startswith("\t"):
	    # data
            in_rec = True

            match_obj = pat.match(line.strip())

            if match_obj is not None:
                key: str = TRANSLATE[match_obj.group(1)]
                val: str = match_obj.group(2)

                if key in [ "lavie:edd", "lavie:sanction", "skos:related", ]:
                    record[key].append(val)
                elif key in [ "bods:code", ]:
                    record[key] = "bods:" + val
                else:
                    record[key] = val
            else:
                print("ERROR", line)

        else:
	    # name @ beginning of a record
            if in_rec:
                # emit `record`
                if len(record) > 0:
                    yield record

                record = {
                    "bods:personType": "codes:knownPerson",
                    "bods:fullName": line.strip(),
                    "lavie:aliases": [],
                    "lavie:edd": [],
                    "lavie:sanction": [],
                    "skos:related": [],
                }
            else:
                record["lavie:aliases"].append(line.strip())

            in_rec = False

if __name__ == "__main__":
    # load the "PEP" entries
    pep_path: pathlib.Path = pathlib.Path("pep.txt")
    out_data: list = []

    with open(pep_path, mode = "r", encoding = "utf-8") as fp:
        for record in reader(fp, debug = False):
            out_data.append(record)

    # report
    out_path: pathlib.Path = pathlib.Path("out.json")

    with open(out_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            out_data,
            fp,
            ensure_ascii = False,
            indent = 4,
        )
