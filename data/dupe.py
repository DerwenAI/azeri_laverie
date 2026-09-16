#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Check for duplicates within the database.
"""

import csv
import json
import logging
import pathlib
import sys

from icecream import ic

ic.configureOutput(
    noColor = True,
)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level = logging.INFO,
    )

    # first, collect the resolved entity names and their aliases
    ORIG_COUNT: int = 3881
    MAX_DATE: str = "2014-12-31"

    names: set[ str ] = set()
    alias: set[ str ] = set()

    json_path: pathlib.Path = pathlib.Path("resolved.json")

    with open(json_path, "rb") as fp:
        dat: dict = json.load(fp)

    for item in dat:
        name: str = item.get("bods:fullName")
        founding: str | None = item.get("bods:foundingDate")

        if founding is not None and founding > MAX_DATE:
            logging.info(f"{name} founded too late: {founding}")

        if name in names:
            logger.info(f"DUPLICATE: {name}")
        else:
            names.add(name)

        for name in item.get("lavie:aliases"):
            if name in names:
                logger.info(f"DUPLICATE: {name}")
            else:
                alias.add(name)

    # next, load the full list of entities, then report what remains unresolved
    entities_path: pathlib.Path = pathlib.Path("entities.tsv")
    todo: set = set()

    with open(entities_path, mode = "r", encoding = "utf-8") as fp:
        reader = csv.reader(fp, delimiter = "\t")
        next(reader)

        for name, kind, country in reader:
            if name not in names and name not in alias:
                todo.add(( name, kind, country ))

    out_path: pathlib.Path = pathlib.Path("out.tsv")

    with open(out_path, "w", encoding = "utf-8") as fp:
        fp.write("name\tkind\tcountry\n")

        for name, kind, country in sorted(todo):
            fp.write(f"{name}\t{kind}\t{country}\n")

    # report the progress
    logger.info(f"{len(names)} names resolved")
    logger.info(f"{len(alias)} aliases found")
    logger.info(f"{len(todo)} remain unresolved")

    dupe_rate: float = round(float(len(alias)) / float(len(names)) * 100.0, 2)
    done_rate: float = round(100.0 - (float(len(todo)) / float(ORIG_COUNT) * 100.0), 2)

    logger.info(f"{dupe_rate}% duplicates")
    logger.info(f"{done_rate}% completed")
