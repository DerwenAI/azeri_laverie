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
    mh: MinHash = MinHash(num_perm = 128)
    term_set: set[ str ] = set(name.strip().replace("  ", " ").lower().split(" "))

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

    for item in dat:
        name: str = item.get("bods:fullName")
        uid_: str = uuid.uuid4()

        if name in synonyms:
            logger.info(f"DUPLICATE: {name}")
        else:
            item["uuid"] = uid_
            synonyms[name] = uid_
            entities[uid_] = item

            for alias in item.get("lavie:aliases"):
                if alias in synonyms:
                    logger.info(f"DUPLICATE: {alias}")
                else:
                    synonyms[alias] = uid_


    # load the "guestimated" matches
    guess_path: pathlib.Path = pathlib.Path("alias.tsv")
    count: int = 0

    with open(guess_path, mode = "r", encoding = "utf-8") as fp:
        record: dict = {}

        for start, name in reader(fp, debug = False):
            count += 1

            if start:
                if len(record) > 0:
                    print(record)

                record = {
                    "name": name,
                    "alias": [],
                }
            else:
                record["alias"].append(name)


    print(count)
    sys.exit(0)


    # load the full list of entities, to idenity what remains unresolved
    entities_path: pathlib.Path = pathlib.Path("entities.tsv")
    todo: set = set()

    with open(entities_path, mode = "r", encoding = "utf-8") as fp:
        reader = csv.reader(fp, delimiter = "\t")
        next(reader)

        for name, kind, country in reader:
            if name not in synonyms:
                todo.add(( name, kind, country, ))

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
        if name not in synonyms:
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
