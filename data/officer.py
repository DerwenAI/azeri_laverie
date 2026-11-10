#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pull the officer links from the thesaurus
"""

from collections import defaultdict
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

ROLE_KEYS: set[ str ] = set([
    "appointed_on",
    "identification",
    "person_number",
])


def parse_location (
    officer: dict,
    ) -> tuple[ str, str ]:
    """
Parse the location metadata
    """
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

    return country, addr


def parse_name (
    officer: dict,
    ) -> tuple[ str, str, str ]:
    """
Parse the name metadata
    """
    aliases: list[ str ] = []
    name: str = officer["name"]

    if name.endswith(", Mr."):
        name = name.removesuffix(", Mr.")
    elif name.endswith(", Mrs."):
        name = name.removesuffix(", Mrs.")
    elif name.endswith(", Miss."):
        name = name.removesuffix(", Miss.")

    if ", " in name and not name.lower().strip(".").endswith(", inc"):
        kind = "codes:KnownPerson"
        m = NAME_PAT.search(name)

        if m is None:
            LOGGER.info(f"MISSED: {name}")

        canonical = m.group(2) + " " + m.group(1)

    else:
        kind = "codes:KnownEntity"

        if name in guess_syn:
            canonical = guess_syn[name]
        else:
            canonical = name

    if canonical != officer["name"]:
        aliases.append(officer["name"])

    return kind, canonical, aliases


if __name__ == "__main__":
    ######################################################################
    # load the persisted state for parsing officer links

    off_guess_path: pathlib.Path = pathlib.Path("off_guess.json")

    with open(off_guess_path, "rb") as fp:
        guess_syn: dict = json.load(fp)

    off_link_path: pathlib.Path = pathlib.Path("off_link.json")

    with open(off_link_path, "rb") as fp:
        name_map: dict = json.load(fp)

    resolved_path: pathlib.Path = pathlib.Path("resolved.json")

    with open(resolved_path, "rb") as fp:
        dat: dict = json.load(fp)
        res_ent: dict = {
            scrub_name(ent["bods:fullName"]).lower() : ent
            for ent in dat
        }


    ######################################################################
    # tally the hand-curated officers
    # these have no metadata other than `country`

    for org_key, org_ent in res_ent.items():
        lavie_officers: list | None = org_ent.get("lavie:officers")

        if lavie_officers is not None:
            for officer in lavie_officers:
                if not isinstance(officer, str):
                    continue
                elif OFFICER_PAT.search(officer) is None:
                    continue

                name, country = officer.strip(")").split(" (")
                name_key: str = scrub_name(name).lower()

                if name_key not in name_map:
                    name_map[name_key] = {
                        "lavie:class": "officer",
                        "roles": defaultdict(lambda: defaultdict(str)),
                        "bods:fullName": scrub_name(name),
                    }

                    # was this officer entity previously known?
                    if res_ent.get(name_key) is None:
                        name_map[name_key].update({
                            "bods:code": "codes:" + country,
                            "uuid": make_uuid(),
                            "lavie:aliases": aliases,

                            #"bods:entityType": kind,
                            #"bods:streetAddress": addr,
                        })

                # default to generic role "officer"
                role: str = "officer"
                name_map[name_key]["roles"][org_key][role] = {}


    ######################################################################
    # tally the officers from UK Companies House
    # these have substantial amounts of metadata

    for org_key, org_ent in res_ent.items():
        ukcoh_officers: list | None = org_ent.get("ukcoh:officers")

        if ukcoh_officers is not None:
            for officer in ukcoh_officers:
                country, addr = parse_location(officer)
                kind, name, aliases = parse_name(officer)
                name_key: str = scrub_name(name).lower()

                if name_key not in name_map:
                    name_map[name_key] = {
                        "lavie:class": "officer",
                        "lavie:aliases": aliases,
                        "bods:entityType": kind,
                        "bods:fullName": scrub_name(name),
                        "bods:code": "codes:" + country,
                        "bods:streetAddress": addr,
                        "uuid": make_uuid(),
                        "roles": defaultdict(lambda: defaultdict(str)),
                    }

                # TODO: what if an entity has more than one role?
                if "officer_role" not in officer:
                    ic("MISS", officer)
                else:
                    role: str = officer["officer_role"]

                    name_map[name_key]["roles"][org_key][role] = {
                        key: officer[key]
                        for key in ROLE_KEYS
                        if key in officer
                    }


    ######################################################################
    # data quality tests

    counts: list = sorted(
        [
            ( len(officer["roles"]), name_key, )
            for name_key, officer in name_map.items()
        ],
        reverse = True,
    )

    ic(counts[:20])


    ######################################################################
    # persist the results

    with open(off_link_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            name_map,
            fp,
            ensure_ascii = False,
            sort_keys = True,
            indent = 4,
        )
