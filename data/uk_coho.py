#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example API access to UK Companies House data
See <https://developer-specs.company-information.service.gov.uk/>
"""

from difflib import SequenceMatcher
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


BASE_URL: str = "https://api.company-information.service.gov.uk"


def get_uk_coho (
    api_key: str,
    query: str,
    search: str,
    kept_fields: dict[ str, str ],
    *,
    debug: bool = True,
    ) -> dict[ str, typing.Any ] | None:
    """
Access the UK Companies House API for the given search parameters.
    """
    url: str = f"{BASE_URL}/{search}"

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
        result: dict[ str, typing.Any ] = {}

        if "title" in item:
            similar: float = SequenceMatcher(
                None,
                item.get("title").lower(),
                query.lower().strip(),
            ).ratio()

            result["similar"] = round(similar, 2)

        for field_key, field_iri in kept_fields.items():
            if field_key in item:
                result[field_iri] = item.get(field_key)

        if debug:
            ic(item)

        return result


def search_company (
    api_key: str,
    query: str,
    *,
    debug: bool = True,
    ) -> None:
    """
Search one company.
    """
    search: str = f"search/companies?q={query}"

    kept_fields: dict[ str, str ] = {
        "address_snippet": "bods:streetAddress", 
        "company_number": "code", 
        "company_status": "status", 
        "date_of_cessation": "dis", 
        "date_of_creation": "reg", 
        "title": "bods:fullName",
    }

    result: dict[ str, typing.Any ] | None = get_uk_coho(
        api_key,
        query,
        search,
        kept_fields,
        debug = debug,
    )

    if result is not None and result.get("similar") > 0.99:
        query = result.get("code")
        search = f"company/{query}/officers"

        kept_fields = {
            "address": "address",
            "appointed_on": "appointed_on",
            "identification": "identification",
            "name": "name",
            "officer_role": "officer_role",
            "person_number": "person_number",
        }

        officers: dict[ str, typing.Any ] | None = get_uk_coho(
            api_key,
            query,
            search,
            kept_fields,
            debug = debug,
        )

        if officers is not None:
            result["officers"] = officers

    result["bods:code"] = "UK"
    result["bods:entityType"] = "codes:RegisteredEntity"
    result["oc:sourceId"] = "uk_companies_house" 

    ic(result)


if __name__ == "__main__":
    # set up configuration
    config: dict = {}
    config_path: pathlib.Path = pathlib.Path("config.toml")

    with open(config_path, mode = "rb") as fp:
        config = tomllib.load(fp)

    # search a list of likell UK-based companies
    api_key: str = config["api"]["uk_coho"]

    companies: list[ str ] = [
        "ALLYSON SOLUTIONS LLP",
        "ALSATEC LLP",
        "ARBA MANAGEMENT LLP",
        "ARIONA TRADING LLP",
        "BRANDHOLD ALLIANCE LLP",
        "BUILDCO SUPPLIES LLP",
        "Captron Merchants LLP",
        "CARLEX TECHNOLOGY LLP",
    ]

    # API allows up to 600 requests within a 5 minute period.
    for name in companies:
        search_company(
            api_key,
            name,
            debug = False,
        )

        time.sleep(1)
