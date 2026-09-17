#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Decode and validate Russian Tax IDs (INN / ИНН)
<https://www.nalog.gov.ru/eng/inn/>

There are two lengths for Russian INN numbers:
  * 10 digits - legal entities / organizations (юридические лица)

  10-digit INN:  NNNN XXXXX C
    - NNNN  (positions 1-4): tax authority code (region code + inspection number)
    - XXXXX (positions 5-9): sequential taxpayer record number
    - C     (position 10):   checksum digit

  * 12 digits - individuals and sole proprietors (физические лица, ИП)

  12-digit INN:  NNNN XXXXXX C1 C2
    - NNNN   (positions 1-4):  tax authority code
    - XXXXXX (positions 5-10): sequential taxpayer record number
    - C1 C2  (positions 11-12): two checksum digits
"""

from dataclasses import dataclass
import logging
import sys

from icecream import ic


ic.configureOutput(
    noColor = True,
)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level = logging.INFO,
)


# weight tables published by FNS
WEIGHTS_10: list[ int ] = [ 2, 4, 10, 3, 5, 9, 4, 6, 8 ]           # single checksum digit of a 10-digit INN
WEIGHTS_12_C1: list[ int ] = [ 7, 2, 4, 10, 3, 5, 9, 4, 6, 8 ]     # 1st checksum digit of a 12-digit INN
WEIGHTS_12_C2: list[ int ] = [ 3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8 ]  # 2nd checksum digit of a 12-digit INN

REGIONS: dict[ str, str ] = {
    "01": "Adygea",
    "02": "Bashkortostan",
    "03": "Buryatia",
    "04": "Altai Republic",
    "05": "Dagestan",
    "06": "Ingushetia",
    "07": "Kabardino-Balkaria",
    "08": "Kalmykia",
    "09": "Karachay-Cherkessia",
    "10": "Karelia",
    "11": "Komi Republic",
    "12": "Mari El",
    "13": "Mordovia",
    "14": "Sakha (Yakutia)",
    "15": "North Ossetia–Alania",
    "16": "Tatarstan",
    "17": "Tuva (Tyva)",
    "18": "Udmurtia",
    "19": "Khakassia",
    "20": "Chechnya",
    "21": "Chuvashia",
    "22": "Altai Krai",
    "23": "Krasnodar Krai",
    "24": "Krasnoyarsk Krai",
    "25": "Primorsky Krai",
    "26": "Stavropol Krai",
    "27": "Khabarovsk Krai",
    "28": "Amur Oblast",
    "29": "Arkhangelsk Oblast",
    "30": "Astrakhan Oblast",
    "31": "Belgorod Oblast",
    "32": "Bryansk Oblast",
    "33": "Vladimir Oblast",
    "34": "Volgograd Oblast",
    "35": "Vologda Oblast",
    "36": "Voronezh Oblast",
    "37": "Ivanovo Oblast",
    "38": "Irkutsk Oblast",
    "39": "Kaliningrad Oblast",
    "40": "Kaluga Oblast",
    "41": "Kamchatka Krai",
    "42": "Kemerovo Oblast – Kuzbass",
    "43": "Kirov Oblast",
    "44": "Kostroma Oblast",
    "45": "Kurgan Oblast",
    "46": "Kursk Oblast",
    "47": "Leningrad Oblast",
    "48": "Lipetsk Oblast",
    "49": "Magadan Oblast",
    "50": "Moscow Oblast",
    "51": "Murmansk Oblast",
    "52": "Nizhny Novgorod Oblast",
    "53": "Novgorod Oblast",
    "54": "Novosibirsk Oblast",
    "55": "Omsk Oblast",
    "56": "Orenburg Oblast",
    "57": "Oryol Oblast",
    "58": "Penza Oblast",
    "59": "Perm Krai",
    "60": "Pskov Oblast",
    "61": "Rostov Oblast",
    "62": "Ryazan Oblast",
    "63": "Samara Oblast",
    "64": "Saratov Oblast",
    "65": "Sakhalin Oblast",
    "66": "Sverdlovsk Oblast",
    "67": "Smolensk Oblast",
    "68": "Tambov Oblast",
    "69": "Tver Oblast",
    "70": "Tomsk Oblast",
    "71": "Tula Oblast",
    "72": "Tyumen Oblast",
    "73": "Ulyanovsk Oblast",
    "74": "Chelyabinsk Oblast",
    "75": "Zabaykalsky Krai",
    "76": "Yaroslavl Oblast",
    "77": "Moscow",
    "78": "St. Petersburg",
    "79": "Jewish Autonomous Oblast",
    "80": "Zabaykalsky Krai (legacy: former Aginsky Buryat Okrug)",
    "81": "(gap, former Komi-Permyak Okrug, merged into Perm Krai in 2005)",
    "82": "(gap, former Koryak Okrug, merged into Kamchatka Krai in 2007)",
    "83": "Nenets Autonomous Okrug",
    "84": "(gap, former Taymyr Okrug, merged into Krasnoyarsk Krai in 2007)",
    "85": "Irkutsk Oblast (legacy: former Ust-Ordynsky Buryat Okrug)",
    "86": "Khanty-Mansi Autonomous Okrug – Yugra",
    "87": "Chukotka Autonomous Okrug",
    "88": "(gap, former Evenki Okrug, merged into Krasnoyarsk Krai in 2007)",
    "89": "Yamalo-Nenets Autonomous Okrug",
    "90": "Zaporizhzhia Oblast",
    "91": "Republic of Crimea",
    "92": "Sevastopol",
    "93": "Donetsk People's Republic",
    "94": "Luhansk People's Republic",
    "95": "Kherson Oblast",
    "96": "never assigned",
    "97": "never assigned",
    "98": "never assigned",
    "99": "Other territories (incl. Baikonur); also the prefix for interregional/largest-taxpayer inspectorates",
}

@dataclass
class InnResult:
    inn: str
    valid: bool
    length: int
    entity_type: str
    tax_authority_code: str
    region_code: str
    inspection_code: str
    record_number: str
    checksum_digits_given: str
    checksum_digits_expected: str
    errors: list[ str ]


def _checksum (
    digits: str,
    weights: list[ int ],
    ) -> int:
    """
Each checksum digit is computed as:
      checksum = (sum(digit[i] * weight[i] for i in significant_digits) % 11) % 10

using a fixed set of weights defined by the Russian Federal Tax Service (FNS)
    """
    total = sum(int(d) * w for d, w in zip(digits, weights))

    return (total % 11) % 10


def decode_inn (
    inn: str,
    ) -> InnResult:
    """
Decode and validate a Russian INN tax ID given as a string. 
Returns an `InnResult` object
"""
    inn = (inn or "").strip().replace("INN", "")
    errors: list[ str ] = []

    if not inn.isdigit():
        errors.append("INN must contain only digits.")

        return InnResult(
            inn,
            False,
            len(inn),
            "unknown",
            "",
            "",
            "",
            "",
            "",
            "",
            errors,
        )

    length: int = len(inn)

    if length == 10:
        entity_type: str = "Legal entity (organization)"
        region_code: int = inn[0:2]
        inspection_code: int = inn[2:4]
        tax_authority_code: int = inn[0:4]
        record_number: int = inn[4:9]

        given: int = inn[9]
        expected: str = str(_checksum(inn[0:9], WEIGHTS_10))

        if given != expected:
            errors.append(f"Checksum mismatch: expected {expected}, found {given}.")

        return InnResult(
            inn,
            True,
            length,
            entity_type,
            tax_authority_code,
            region_code,
            inspection_code,
            record_number,
            given,
            expected,
            errors,
        )

    elif length == 12:
        entity_type = "Individual (natural person / sole proprietor)"
        region_code = inn[0:2]
        inspection_code = inn[2:4]
        tax_authority_code = inn[0:4]
        record_number = inn[4:10]
        given = inn[10:12]

        c1 = str(_checksum(inn[0:10], WEIGHTS_12_C1))
        c2 = str(_checksum(inn[0:11], WEIGHTS_12_C2))
        expected = c1 + c2

        if given[0] != c1:
            errors.append(f"First checksum digit mismatch: expected {c1}, found {given[0]}.")

        if given[1] != c2:
            errors.append(f"Second checksum digit mismatch: expected {c2}, found {given[1]}.")

        return InnResult(
            inn,
            given == expected,
            length,
            entity_type,
            tax_authority_code,
            region_code,
            inspection_code,
            record_number,
            given,
            expected,
            errors,
        )

    else:
        errors.append(f"Invalid length: {length} digits (must be 10 or 12).")

        return InnResult(
            inn,
            False,
            length,
            "unknown",
            "",
            "",
            "",
            "",
            "",
            "",
            errors,
        )


if __name__ == "__main__":
    targets: list[ str ] = [
        "INN3016043171",
    ]

    for target in targets:
        result: InnResult = decode_inn(target)
        ic(result)
        ic(REGIONS.get(result.region_code))
