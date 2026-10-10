#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Construct a thesaurus from the data to use to build a KG.
"""

from collections import defaultdict
import csv
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

    # load the unique identifiers per subject from OpenCheck

    seed_path: pathlib.Path = pathlib.Path("seed.json")
    seed_uid: dict[ str, str ] = {}

    with open(seed_path, "rb") as fp:
        dat: dict = json.load(fp)

        for record in dat["subjects"]:
            uid_: str = record["key"]
            key: str = scrub_name(record["name"]).lower()
            seed_uid[key] = uid_

    # collect the resolved entity names and their aliases
    entities: dict[ str, dict ] = {}
    synonyms: dict[ str, str ] = {}

    resolved_path: pathlib.Path = pathlib.Path("resolved.json")

    with open(resolved_path, "rb") as fp:
        dat: dict = json.load(fp)

    for record in dat:
        name: str = scrub_name(record.get("bods:fullName"))
        name_key: str = name.lower()
        uid_: str = str(uuid.uuid4())

        if name_key in synonyms:
            logger.info(f"DUPLICATE name: {name}")
        else:
            record["uuid"] = uid_
            synonyms[name_key] = uid_
            entities[uid_] = record

            for alias in record.get("lavie:aliases"):
                alias = scrub_name(alias)
                alias_key: str = alias.lower()

                if alias_key in synonyms:
                    logger.info(f"DUPLICATE alias: {alias}")
                else:
                    synonyms[alias_key] = uid_

    # load the "guestimated" matches
    guess_path: pathlib.Path = pathlib.Path("guess.json")

    with open(guess_path, "rb") as fp:
        dat: dict = json.load(fp)
        guess_dat: dict[ str, dict ] = dat["records"]
        guess_syn: dict[ str, str ] = dat["synonyms"]

    ic(len(guess_syn))
    ic(len(guess_dat))


    # load the full list of entities, to idenity what remains unresolved
    entities_path: pathlib.Path = pathlib.Path("entities.tsv")
    guess_use: set[ str ] = set()
    todo: set = set()

    with open(entities_path, mode = "r", encoding = "utf-8") as fp:
        reader = csv.reader(fp, delimiter = "\t")
        next(reader)

        for name, kind, country in reader:
            name: str = scrub_name(name)
            name_key: str = name.lower()

            if name_key not in synonyms:
                if name_key in guess_syn:
                    uid_: str = guess_syn[name_key]
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

                guess_use.add(uid_)

    # knock out the unused guesses
    guess_key: set[ str ] = set(guess_dat.keys())

    for key in guess_key:
        if key not in guess_use:
            del guess_dat[key]

    out_path: pathlib.Path = pathlib.Path("out.json")

    with open(out_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            guess_dat,
            fp,
            ensure_ascii = False,
            indent = 4,
        )

    # transform unresolved entities using the same intermediate/temorary
    # format as the thesaurus, stored as `thesaurus.json`
    for uid_, record in guess_dat.items():
        #print(record)

        newrec: dict = {
            "bods:fullName": record["name"],
	    "lavie:aliases": record["alias"],
        }

        if "country" in record:
            if record["country"] != "UNKNOWN":
                newrec["bods:code"] = "codes:" + record["country"]

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


    ######################################################################
    # data quality check: do the `alias` values work as a proper set of keys?
    # data quality check: use the OpenCheck unique identifiers, where available

    for uid_, record in entities.items():
        record["uuid"] = uid_

        name: str = record["bods:fullName"]
        name_key: str = name.lower()
        new_alias: list[ str ] = []
        keys: set[ str ] = set()

        for alias in record["lavie:aliases"]:
            key: str = alias.lower()

            if key != name:
                if key not in keys:
                    keys.add(key)
                    new_alias.append(alias)

        record["lavie:aliases"] = new_alias

        keys.add(name_key)

        for key in keys:
            if key in seed_uid:
                record["uuid"] = seed_uid[key]
                #print(name_key, seed_uid[key])


    ######################################################################
    # report

    thes_path: pathlib.Path = pathlib.Path("thesaurus.json")

    with open(thes_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            entities,
            fp,
            ensure_ascii = False,
            indent = 4,
        )

    # build a synonym map for the thesaurus
    syn_map: dict[ str, str ] = {}

    for record in entities.values():
        if "uuid" not in record:
            print("NO UUID:", record)
            continue

        uid_: str = record["uuid"]

        name: str = scrub_name(record["bods:fullName"])
        name_key: str = name.lower()
        keys: set[ str ] = { scrub_name(alias).lower() for alias in record["lavie:aliases"] }
        keys.add(name_key)

        for key in keys:
            syn_map[key] = uid_

    map_path: pathlib.Path = pathlib.Path("syn_map.json")

    with open(map_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            syn_map,
            fp,
            ensure_ascii = False,
            indent = 4,
            sort_keys = True,
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
