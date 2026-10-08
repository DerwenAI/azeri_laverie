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
import sys
import typing
import uuid

from datasketch import MinHashLSHEnsemble, MinHash
from icecream import ic


ic.configureOutput(
    noColor = True,
)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level = logging.INFO,
)


SIM_THRESH: float = 0.9


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


def make_hash (
    mh_index: list,
    name: str,
    ) -> None:
    """
Compute a `MinHash` entry to use in `LSH`
    """
    name = scrub_name(name).lower()

    mh: MinHash = MinHash(num_perm = 128)
    term_set: set[ str ] = set(name.split(" "))

    for term in term_set:
        mh.update(term.encode("utf-8"))

    mh_index.append(( name, mh, len(term_set), ))


if __name__ == "__main__":
    # first, collect the resolved entity names and their aliases
    entities: dict[ str, dict ] = {}
    synonyms: dict[ str, str ] = {}

    json_path: pathlib.Path = pathlib.Path("thesaurus.json")

    with open(json_path, "rb") as fp:
        dat: dict = json.load(fp)

    for record in dat:
        name: str = scrub_name(record.get("bods:fullName"))
        uid_: str = str(uuid.uuid4())

        if name.lower() in synonyms.keys():
            logger.info(f"DUPLICATE: {name}")
        else:
            record["uuid"] = uid_
            synonyms[name.lower()] = uid_
            entities[uid_] = record

            for alias in record.get("lavie:aliases"):
                alias = scrub_name(alias)

                if alias.lower() in synonyms.keys():
                    logger.info(f"DUPLICATE: {alias}")
                else:
                    synonyms[alias.lower()] = uid_

    # load the "guestimated" matches
    guess_dat: dict[ str, dict ] = {}
    guess_syn: dict[ str, str ] = {}
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

            guess_syn[name.lower()] = record["uuid"]

    ic(len(guess_syn))
    ic(len(guess_dat))


    # load the full list of entities, to idenity what remains unresolved
    entities_path: pathlib.Path = pathlib.Path("entities.tsv")
    todo: set = set()

    with open(entities_path, mode = "r", encoding = "utf-8") as fp:
        reader = csv.reader(fp, delimiter = "\t")
        next(reader)

        for name, kind, country in reader:
            name = scrub_name(name)

            if name.lower() in synonyms.keys():
                # already resolved
                pass
            elif name.lower() in guess_syn.keys():
                uid_: str = guess_syn[name.lower()]
                guess_dat[uid_]["kind"] = kind
                guess_dat[uid_]["country"] = country
            else:
                uid_ = str(uuid.uuid4())

                guess_dat[uid_] = {
                    "name": name,
                    "uuid": uid_,
                    "alias": [],
                    "kind": kind,
                    "country": country,
                }

    out_path: pathlib.Path = pathlib.Path("out.json")

    with open(out_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            guess_dat,
            fp,
            ensure_ascii = False,
            indent = 4,
        )

    # transform unresolved entities using the same intermediate/temorary
    # format as the thesaurus, stored as `backfill.json`
    for uid_, record in guess_dat.items():
        #print(record)

        newrec: dict = {
            "bods:fullName": record["name"],
	    "lavie:aliases": record["alias"],
        }

        if "country" in record:
            if record["country"] != "UNKNOWN":
                newrec["bods:code"] = "bods:" + record["country"]

        if "kind" not in record:
            name = record["name"].lower()
            print("NO KIND:", name, record)
            newrec["bods:personType"] = "codes:UnknownPerson"
        else:
            match record["kind"]:
                case "Person":
                    newrec["bods:personType"] = "codes:UnknownPerson"
                case "Company":
                    newrec["bods:entityType"] = "codes:UnknownEntity"
                case _:
                    newrec["bods:entityType"] = "codes:UnknownEntity"

        entities[uid_] = newrec

    # report
    back_path: pathlib.Path = pathlib.Path("backfill.json")

    with open(back_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            entities,
            fp,
            ensure_ascii = False,
            indent = 4,
        )

    # build a map for the thesaurus
    syn_map: dict[ str, str ] = {}

    for name, uid_ in synonyms.items():
        syn_map[name] = uid_

    for uid_, record in guess_dat.items():
        syn_map[scrub_name(record["name"]).lower()] = uid_

        for alias in record["alias"]:
            syn_map[scrub_name(alias).lower()] = uid_

    map_path: pathlib.Path = pathlib.Path("syn_map.json")

    with open(map_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            syn_map,
            fp,
            ensure_ascii = False,
            indent = 4,
        )

    sys.exit(0)


    ######################################################################
    ## extras

    # run MinHash + LSH to compute simple similarities
    mh_index: list[ tuple ] = []

    lsh: MinHashLSHEnsemble = MinHashLSHEnsemble(
        threshold = SIM_THRESH,
        num_perm = 128,
        num_part = 32,
    )

    for name, uid_ in synonyms.items():
        make_hash(mh_index, name)

    for name, kind, country in todo:
        make_hash(mh_index, name)

    lsh.index(mh_index)

    similar: dict[ str, list[ str ] ] = defaultdict(list)
   
    for name, mh, term_len in mh_index:
        if name not in synonyms.keys():
            for aka in lsh.query(mh, term_len):
                if name != aka:
                    similar[name].append(aka)

    out_path: pathlib.Path = pathlib.Path("out.tsv")

    with open(out_path, "w", encoding = "utf-8") as fp:
        for name, aliases in sorted(similar.items()):
            fp.write(f"{name}\n")

            for aka in aliases:
                if aka in synonyms:
                    fp.write(f"*\t{aka}\n")
                else:
                    fp.write(f"\t{aka}\n")
