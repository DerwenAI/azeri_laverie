#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example API access to UK Companies House data
See <https://developer-specs.company-information.service.gov.uk/>
"""

from difflib import SequenceMatcher
import csv
import datetime as dt
import json
import pathlib
import sys
import time
import tomllib
import typing

from icecream import ic
import requests

ic.configureOutput(
    noColor = True,
)


def get_ukcoh (
    api_key: str,
    query: str,
    search: str,
    kept_fields: dict[ str, str ],
    *,
    debug: bool = True,
    base_url: str = "https://api.company-information.service.gov.uk",
    ) -> dict[ str, typing.Any ] | None:
    """
Access the UK Companies House API for the given search parameters.
    """
    url: str = f"{base_url}/{search}"

    response: requests.Response = requests.get(
        url.format(query),
        auth = (api_key, ""),
    )

    if not response.ok:
        ic(query, response.reason)
        return None

    dat: dict = response.json()

    if dat.get("total_results") < 1:
        return None

    for item in dat.get("items"):
        if debug:
            ic(item)

        result: dict[ str, typing.Any ] = {}

        if "title" in item:
            similar: float = SequenceMatcher(
                None,
                item.get("title").lower(),
                query.lower().strip(),
            ).ratio()

            result["lavie:similar"] = round(similar, 2)

        for field_key, field_iri in kept_fields.items():
            if field_key in item:
                result[field_iri] = item.get(field_key)

        result["lavie:query"] = query

        return result


def search_company (
    api_key: str,
    query: str,
    *,
    debug: bool = True,
    sim_thresh: float = 0.85,
    ) -> dict | None:
    """
Search one company.
    """
    search: str = f"search/companies?q={query}"

    kept_fields: dict[ str, str ] = {
        "title": "bods:fullName",
        "company_number": "bods:idString", 
        "address_snippet": "bods:streetAddress", 
        "date_of_cessation": "bods:dissolutionDate", 
        "date_of_creation": "bods:foundingDate", 
        "company_status": "ukcoh:status", 
    }

    result: dict[ str, typing.Any ] | None = get_ukcoh(
        api_key,
        query,
        search,
        kept_fields,
        debug = debug,
    )

    if result is None:
        return None

    if result.get("lavie:similar") < sim_thresh:
        ic(query, result.get("lavie:similar"))
        return None

    result["lavie:aliases"] = []
    result["bods:retrievedAt"] = f"{dt.datetime.now(dt.UTC).isoformat()}"
    result["bods:code"] = "codes:UK"
    result["bods:entityType"] = "codes:RegisteredEntity"
    result["bods:schemeName"] = "Companies House" 
    result["bods:scheme"] = "GB-COH"

    if result.get("lavie:similar") < 1.0:
        result["lavie:aliases"].append(query)

    # next, get the officers -- if any
    query = result.get("bods:idString")
    search = f"company/{query}/officers"

    kept_fields = {
        "address": "address",
        "appointed_on": "appointed_on",
        "identification": "identification",
        "name": "name",
        "officer_role": "officer_role",
        "person_number": "person_number",
    }

    officers: dict[ str, typing.Any ] | None = get_ukcoh(
        api_key,
        query,
        search,
        kept_fields,
        debug = debug,
    )

    if officers is not None:
        result["ukcoh:officers"] = officers

    if debug:
        ic(result)

    return result


if __name__ == "__main__":
    # set up configuration
    config: dict = {}
    config_path: pathlib.Path = pathlib.Path("config.toml")

    with open(config_path, mode = "rb") as fp:
        config = tomllib.load(fp)

    # search a list of likely UK-based companies
    api_key: str = config["api"]["ukcoh"]

    companies: list[ str ] = []
    uk_path: pathlib.Path = pathlib.Path("uk.tsv")

    with open(uk_path, mode = "r", encoding = "utf-8") as fp:
        reader = csv.reader(fp, delimiter = "\t")

        for name, _, _ in reader:
            companies.append(name)

    # rate limiting: API allows 600 requests within a 5 minute period
    out_data: list[dict] = []

    for name in companies:
        result: dict | None = search_company(
            api_key,
            name,
            debug = False, # True
        )

        time.sleep(1)

        if result is not None:
            out_data.append(result)

    out_path: pathlib.Path = pathlib.Path("out.json")

    with open(out_path, mode = "w", encoding = "utf-8") as fp:
        json.dump(
            out_data,
            fp,
            ensure_ascii = False,
            indent = 2,
        )
