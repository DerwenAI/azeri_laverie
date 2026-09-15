#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract company names and countries from the base data.
"""

import csv
import pathlib
import sys

from icecream import ic

ic.configureOutput(
    noColor = True,
)


if __name__ == "__main__":
    base_path: pathlib.Path = pathlib.Path("base.csv")
    pairs: set[tuple[ str, str, str ]] = set()

    with open(base_path, "r", encoding = "utf-8") as fp:
        reader = csv.reader(fp)
        next(reader)

        for row in reader:
            pay_name, pay_kind, pay_country, ben_name, ben_kind, ben_country = row
            pairs.add(( pay_name, pay_kind, pay_country, ))
            pairs.add(( ben_name, ben_kind, ben_country, ))

    todo_path: pathlib.Path = pathlib.Path("todo.tsv")

    with open(todo_path, "w", encoding = "utf-8") as fp:
        fp.write("name\tkind\tcountry\n")

        for name, kind, country in sorted(pairs):
            fp.write(f"{name}\t{kind}\t{country}\n")
