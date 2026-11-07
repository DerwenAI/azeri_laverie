#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pull the officer links from the thesaurus
"""

from collections import Counter
import json
import pathlib
import re
import sys

from icecream import ic

from lavie import make_uuid, scrub_name, \
    LOGGER, OFFICER_PAT


NAME_PAT = re.compile(r"([A-Z\-\s]+)\,\s+(.*)")

CC_CODE: dict[ str, str ] = {
    "Azerbaijan": "AZ",
    "Azerbijan": "AZ",
    "Bangladesh": "BD",
    "Belize": "BZ",
    "British Virgin Islands": "VG",
    "Canada": "CA",
    "China": "CN",
    "Commonwealth Of Dominica": "DM",
    "Cyprus": "CY",
    "Dominica": "DM",
    "England": "GB",
    "France": "FR",
    "Georgia": "GE",
    "Germany": "DE",
    "Gibraltar": "GI",
    "Great Britain": "GB",
    "Greece": "GR",
    "Hong Kong": "HK",
    "Ireland": "IE",
    "Latvia": "LV",
    "Malaysia": "MY",
    "Marshall Islands": "MH",
    "Mauritius": "MU",
    "Monaco": "MC",
    "Netherlands": "NL",
    "Nevis": "KN",
    "Nevis, West Indies": "KN",
    "Norway": "NO",
    "Panama": "PA",
    "Republic Of Korea": "KR",
    "Russia": "RU",
    "Scotland": "GB",
    "Seychelles": "SC",
    "Singapore": "SG",
    "South Africa": "SA",
    "South Korea": "KR",
    "Spain": "ES",
    "Switzerland": "CH",
    "Taiwan": "TW",
    "Turkey": "TR",
    "Turks & Caicor": "TC",
    "Uae": "AE",
    "Ukraine": "UA",
    "United Kingdom": "GB",
    "United States": "US",
    "Usa": "US",
    "Vanuatu": "VU",
    "Virgin Islands, British": "VG",
    "West Indies": "KN",
}

ROLE_KEYS: set[ str ] = set([
    "appointed_on",
    "identification",
    "officer_role",
    "person_number",
])

ADDR_KEYS: list[ str ] = [
    "care_of",
    "po_box",
    "address_line_1",
    "address_line_2",
    "premises",
    "locality",
    "region",
    "postal_code",
    "country",
]


if __name__ == "__main__":
    thes_path: pathlib.Path = pathlib.Path("thesaurus.json")

    with open(thes_path, "rb") as fp:
        dat: dict = json.load(fp)
        thes_ent: dict = dat["entities"]
        thes_syn: dict = dat["synonyms"]


    ######################################################################
    # tally the hand-curated officers

    lavie_name_map: dict[ str, dict ] = {}

    for uid_, ent_rec in thes_ent.items():
        lavie_officers: list | None = ent_rec.get("lavie:officers")

        if lavie_officers is not None:
            for officer in lavie_officers:
                if OFFICER_PAT.search(officer) is None:
                    continue

                name, country = officer.strip(")").split(" (")
                name_key: str = scrub_name(name).lower()
                name_uid: str = thes_syn.get(name_key)

                if name_uid is not None:
                    # found a reference
                    #print(name_uid)
                    continue

                if name_key not in lavie_name_map:
                    lavie_name_map[name_key] = {
                        "lavie:class": "unknown",
                        "lavie:aliases": [],
                        "bods:entityType": "codes:UnknownPerson",
                        "bods:fullName": scrub_name(name),
                        "bods:code": "codes:" + country,
                        "uuid": make_uuid(),
                        "refs": [ uid_ ],
                    }
                else:
                    lavie_name_map[name_key]["refs"].append(uid_)


    ######################################################################
    # tally the officers from UK Companies House

    guess_path: pathlib.Path = pathlib.Path("off_guess.json")

    with open(guess_path, "rb") as fp:
        guess_syn: dict = json.load(fp)

    ukcoh_name_map: dict[ str, dict ] = {}
    keys: set[ str ] = set()
   
    for uid_, ent_rec in thes_ent.items():
        ukcoh_officers: list | None = ent_rec.get("ukcoh:officers")

        if ukcoh_officers is not None:
            for officer in ukcoh_officers:
                addr_rec: dict = officer["address"]
                addr: str = ""
                country: str = "GB"

                for key in ADDR_KEYS:
                    if key in addr_rec:
                        val: str = addr_rec[key].strip().strip(",")

                        if len(val) > 0 and val not in [ "FOREIGN", ".", ]:
                            if key == "country":
                                country = CC_CODE[val]

                                if country == "GB":
                                    val = "UK"
                                elif val == "Virgin Islands, British":
                                    val = "BVI"

                            addr = addr + ", " + val

                addr = addr.removeprefix(", ")
                name: str = officer["name"]
                aliases: list[ str ] = []

                if name.endswith(", Mr."):
                    name = name.removesuffix(", Mr.")
                elif name.endswith(", Mrs."):
                    name = name.removesuffix(", Mrs.")
                elif name.endswith(", Miss."):
                    name = name.removesuffix(", Miss.")

                if ", " in name:
                    kind = "codes:KnownPerson"
                    m = NAME_PAT.search(name)

                    if m is None:
                        print("---MISSED---")

                    canonical = m.group(2) + " " + m.group(1)

                else:
                    kind = "KnownEntity"

                    if name in guess_syn:
                        canonical = guess_syn[name]
                    else:
                        canonical = name

                if canonical != officer["name"]:
                    aliases.append(officer["name"])

                name_key: str = scrub_name(canonical).lower()
                name_uid: str = thes_syn.get(name_key)

                if name_uid is not None:
                    # found a reference
                    #print(name_uid)
                    continue

                record: dict = {
                    "lavie:class": "officer",
                    "lavie:aliases": aliases,
                    "bods:entityType": kind,
                    "bods:fullName": scrub_name(canonical),
                    "bods:code": "codes:" + country,
                    "bods:streetAddress": addr,
                    "uuid": make_uuid(),
                    "roles": {},
                }                

                if name_key not in ukcoh_name_map:
                    ukcoh_name_map[name_key] = record

                ukcoh_name_map[name_key]["roles"][uid_] = {
                    key: officer[key]
                    for key in ROLE_KEYS
                    if key in officer
                }


    ######################################################################
    # persist the results

    dat: dict = {
        "lavie": list(sorted(
            lavie_name_map.values(),
            key = lambda x: x["bods:fullName"],
        )),
        "ukcoh": list(sorted(
            ukcoh_name_map.values(),
            key = lambda x: x["bods:fullName"],
        )),
    }

    persist_path: pathlib.Path = pathlib.Path("out.json")

    with open(persist_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            dat,
            fp,
            ensure_ascii = False,
            sort_keys = True,
            indent = 4,
        )
