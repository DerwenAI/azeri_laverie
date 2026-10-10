#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Library for transforming the manually curated entity data.
"""

import logging
import uuid

from datasketch import MinHashLSHEnsemble, MinHash
from icecream import ic


ic.configureOutput(
    noColor = True,
)


LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    level = logging.INFO,
)


SIM_THRESH: float = 0.9


def make_uuid (
    ) -> str:
    """
Generate a unique identifier.
    """
    return str(uuid.uuid4())


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


def scrub_name (
    name: str,
    ) -> str:
    """
Scrub the text for people/company names, to get stable lookup keys
    """
    assert isinstance(name, str), name

    return name.replace("  ", " ").strip()
