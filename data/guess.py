#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Construct a thesaurus from the data to use to build a KG.
"""

import io
import json
import pathlib
import sys
import typing
import uuid

from icecream import ic
import polars as pl


ic.configureOutput(
    noColor = True,
)


def scrub_name (
    name: str,
    ) -> str:
    """
Scrub the text for people/company names, to get stable lookup keys
    """
    assert isinstance(name, str), name

    return name.replace("  ", " ").strip()


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

        if line.startswith("\t"):
	    # aliases
            yield False, line.strip()
        else:
	    # name @ beginning of a record
            yield True, line.strip()


def add_guess (
    guess_syn: dict[ str, str ],
    record: dict,
    name: str,
    *,
    report: bool = True,
    ) -> None:
    """
Attempt to collect another synonym.
    """
    key: str = name.lower()

    if key in guess_syn:
        if record["uuid"] != guess_syn[key]:
            if report:
                print("ALREADY!", key, record["uuid"], guess_syn[key])
    else:
        guess_syn[key] = record["uuid"]


if __name__ == "__main__":

    ######################################################################
    # expand the "normalized names" from the base data

    df: pl.DataFrame = pl.read_csv("occrp_17k.csv")
    norm_names: dict[ str, str ] = {}

    for row in df.iter_rows(named = True):
        name: str = scrub_name(row["beneficiary_name"])
        norm: str = scrub_name(row["beneficiary_name_norm"])

        if name != norm:
            norm_names[name] = norm


    ######################################################################
    # load the "guestimated" matches
    guess_dat: dict[ str, dict ] = {}
    guess_syn: dict[ str, str ] = {}
    norm_found: set[ str ] = set()

    guess_path: pathlib.Path = pathlib.Path("guess.tsv")

    with open(guess_path, mode = "r", encoding = "utf-8") as fp:
        record: dict = {}

        for start, name in reader(fp, debug = False):
            name = scrub_name(name)

            if start:
                if len(record) > 0:
                    guess_dat[record["uuid"]] = record

                uid_: str = str(uuid.uuid4())

                record = {
                    "name": name,
                    "uuid": uid_,
                    "alias": [],
                }
            else:
                record["alias"].append(name)

            add_guess(guess_syn, record, name)

            if name in norm_names:
                norm_found.add(name)
                record["alias"].append(norm_names[name])
                add_guess(guess_syn, record, norm_names[name])


    ######################################################################
    # data quality check: were the normalized names used correctly?

    for name, norm in norm_names.items():
        norm_key: str = norm.lower()

        if name not in norm_found and norm_key not in guess_syn:
            norm: str = norm_names[name]
            uid_: str = str(uuid.uuid4())

            record: dict = {
                "name": name,
                "uuid": uid_,
                "alias": [ norm ],
            }

            add_guess(guess_syn, record, norm_names[name], report = False)
            guess_dat[record["uuid"]] = record
            #print(record)

        if norm_key not in guess_syn:
            print("YIKES!", norm)


    ######################################################################
    # data quality check: do the `alias` values work as a proper set of keys?

    for uid_, record in guess_dat.items():
        name: str = record["name"]
        name_key: str = name.lower()
        new_alias: list[ str ] = []
        keys: set[ str ] = set()

        for alias in record["alias"]:
            key: str = alias.lower()

            if key != name:
                if key not in keys:
                    keys.add(key)
                    new_alias.append(alias)

        record["alias"] = new_alias


    ######################################################################
    # persist the combined "guesses" as a JSON file

    out_path: pathlib.Path = pathlib.Path("guess.json")

    out_data: dict = {
        "records": guess_dat,
        "synonyms": guess_syn,
    }

    with open(out_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            out_data,
            fp,
            ensure_ascii = False,
            indent = 4,
        )
