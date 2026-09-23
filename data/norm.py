#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract company names and countries from the base data.
"""

import pathlib
import sys

from icecream import ic
import polars as pl


ic.configureOutput(
    noColor = True,
)


if __name__ == "__main__":
    df = pl.read_csv("occrp_17k.csv")
    ic(df.head())

    for row in df.iter_rows(named = True):
        name: str = row["beneficiary_name"]
        norm: str = row["beneficiary_name_norm"]

        if name.lower() != norm.lower():
            print("\t".join([ row["beneficiary_jurisdiction"], name, norm ]))
            
