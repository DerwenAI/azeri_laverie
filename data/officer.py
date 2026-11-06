#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pull the officer links from the thesaurus
"""

from collections import Counter
import json
import pathlib
import re

from icecream import ic

from lavie import make_uuid, scrub_name, \
    LOGGER


if __name__ == "__main__":
    thes_path: pathlib.Path = pathlib.Path("thesaurus.json")

    with open(thes_path, "rb") as fp:
        dat: dict = json.load(fp)
        thes_ent: dict = dat["entities"]
        thes_syn: dict = dat["synonyms"]

    # tally the hand-curated officers
    pat = re.compile(r"[\w\s]+\s\(", re.IGNORECASE)

    name_map: dict[ str, dict ] = {}
    who_count: Counter = Counter()

    for ent_uid, ent_rec in thes_ent.items():
        lavie_officers: list | None = ent_rec.get("lavie:officers")

        if lavie_officers is not None:
            for officer in lavie_officers:
                if pat.search(officer) is None:
                    continue

                name, country = officer.strip(")").split(" (")
                name_key: str = scrub_name(name).lower()
                name_uid: str = thes_syn.get(name_key)

                if name_uid is not None:
                    # found a reference
                    print(name_uid)
                elif name_key not in name_map:
                    name_map[name_key] = {
                        "lavie:class": "unknown",
                        "lavie:aliases": [],
                        "bods:entityType": "codes:UnknownPerson",
                        "bods:fullName": scrub_name(name),
                        "bods:code": "codes:" + country,
                        "uuid": make_uuid(),
                        "refs": [ ent_uid ],
                    }
                else:
                    name_map[name_key]["refs"].append(ent_uid)

                who_count[name_key] += 1

    for name_key, count in sorted(who_count.items()):
        ic(name_key, count)

    ic(sorted(name_map.items()))


    ######################################################################
    # persist the results

    persist_path: pathlib.Path = pathlib.Path("out.json")

    with open(persist_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            list(name_map.values()),
            fp,
            ensure_ascii = False,
            sort_keys = True,
            indent = 4,
        )
