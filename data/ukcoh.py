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
import logging
import pathlib
import sys
import time
import tomllib
import typing

from icecream import ic
import requests


SEARCH_NAMES: bool = False # True
TARGET_SOURCE: str = "uk.tsv"


ic.configureOutput(
    noColor = True,
)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level = logging.INFO,
)


def get_ukcoh (
    api_key: str,
    query: str,
    search: str,
    kept_fields: dict[ str, str ],
    *,
    debug: bool = False,
    base_url: str = "https://api.company-information.service.gov.uk",
    ) -> typing.Iterator[ dict[ str, typing.Any ]]:
    """
Access the UK Companies House API for the given search parameters.
    """
    url: str = f"{base_url}/{search}"

    response: requests.Response = requests.get(
        url.format(query),
        auth = (api_key, ""),
    )

    if not response.ok:
        logging.info(f"{query} - {response.reason}")
        return

    dat: dict = response.json()

    if debug:
        ic(dat)

    if "items" in dat:
        if dat.get("total_results") < 0:
            return

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

            yield result

    else:
        result: dict[ str, typing.Any ] = {}
        result["lavie:similar"] = 1.0
        item = dat

        for field_key, field_iri in kept_fields.items():
            if field_key in item:
                result[field_iri] = item.get(field_key)

        yield result


def populate_officers (
    api_key: str,
    query: str,
    result: dict,
    *,
    debug: bool = False,
    ) -> dict | None:
    """
Pouplate the officers, if any.
    """
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

    uk_iter = get_ukcoh(
        api_key,
        query,
        search,
        kept_fields,
        debug = debug,
    )

    result["ukcoh:officers"] = []

    for officer in uk_iter:
        result["ukcoh:officers"].append(officer)

    if debug:
        ic(result)

    return result


def search_company_name (
    api_key: str,
    query: str,
    *,
    debug: bool = False,
    sim_thresh: float = 0.85,
    max_date: str = "2014-12-31",
    ) -> dict | None:
    """
Search one company by name.
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

    iter_uk = get_ukcoh(
        api_key,
        query,
        search,
        kept_fields,
        debug = debug,
    )

    for result in iter_uk:
        name: str = result.get("bods:fullName")
        sim: float = result.get("lavie:similar")
        founding: str | None = result.get("bods:foundingDate")

        if founding is not None and founding > max_date:
            logging.info(f"{query} founded too late: {founding}")

            if debug:
                ic(result)

            continue

        if sim < sim_thresh:
            logging.info(f"{query} differs {name}: {sim}")

            if debug:
                ic(result)

            continue

        populate_officers(
            api_key,
            query,
            result,
            debug = debug,
        )

        return result


def search_company_code (
    api_key: str,
    code: str,
    *,
    debug: bool = False,
    ) -> dict | None:
    """
Search one company by code.
    """
    search: str = f"company/{code}"

    kept_fields: dict[ str, str ] = {
        "company_name": "bods:fullName",
        "company_number": "bods:idString", 
        "registered_office_address": "bods:streetAddress", 
        "date_of_cessation": "bods:dissolutionDate", 
        "date_of_creation": "bods:foundingDate", 
        "company_status": "ukcoh:status", 
    }

    iter_uk = get_ukcoh(
        api_key,
        code,
        search,
        kept_fields,
        debug = debug, # True,
    )

    for result in iter_uk:
        populate_officers(
            api_key,
            code,
            result,
            debug = debug, # True,
        )

        return result


if __name__ == "__main__":
    # set up configuration
    config: dict = {}
    config_path: pathlib.Path = pathlib.Path("config.toml")

    with open(config_path, mode = "rb") as fp:
        config = tomllib.load(fp)

    api_key: str = config["api"]["ukcoh"]

    # CUSTOMIZED SEARCHES
    #search: str = f"company/{query}"


    # search a list of likely UK-based companies
    targets: list[ str ] = []
    target_path: pathlib.Path = pathlib.Path(TARGET_SOURCE)

    with open(target_path, mode = "r", encoding = "utf-8") as fp:
        reader = csv.reader(fp, delimiter = "\t")

        for row in reader:
            targets.append(row[0])

    # rate limiting: API allows 600 requests within a 5 minute period
    out_data: list[dict] = []

    for target in targets:
        result: dict | None = None

        if SEARCH_NAMES:
            result = search_company_name(
                api_key,
                target,
                debug = False, # True
            )
        else:
            result = search_company_code(
                api_key,
                target,
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
            indent = 4,
        )
