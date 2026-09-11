## TODO

  - represent `firms.txt` as BODS RDF and as Sz JSON -- as a thesaurus
  - use thesaurus for resolved entities who were parties in transactions
  - convert transaction amounts from various currencies to USD
  - build a graph which has the full set of entities and relations
  - calculate how much % coverage can be obtained through each AML rule


## Replicating results

Starting with the OCCRP dataset, we can augment with other data sources to resolve the entities named as payers and beneficiaries in the transactions:

  1. Some payers are international banks, for example claiming to refund prior payments on clients' invoices. The [ISO 9362-2022 codes](https://www.iso9362.org/isobic/overview.html) for banks, also known as *Business Identifier Codes* (BIC), are managed by [SWIFT](https://www.swift.com/).

  2. Banks and other firms involved in global financial markets will often have a *Legal Entity Identifier* (LEI), managed by [GLEIF](https://www.gleif.org/).

  3. Many of companies named are registered in countries (EE, UK, DE, CY, VG, TR, etc.) which make portions of their corporate registries data available for public search, or have import/export registries and other corporate directories online -- for example:

      + CN: [HK Companies](https://hkg.databasesets.com/)
      + CY: [Cyprus DRCIP](https://data.gov.cy/)
      + DE: [OpenRegister.de](https://offeneregister.de/)
      + EE: [Estonia RIK](https://avaandmed.ariregister.rik.ee/en/downloading-open-data)
      + SG: [SG Company Directory](https://sg.ltddir.com/)
      + TR: [ISI EMIS](https://isimarkets.com/emis/)
      + UK: [Companies House](https://find-and-update.company-information.service.gov.uk/)
      + VG: [BVI Comapny Search](https://i-bvi.com/)

  4. Additional data about some of the shell companies involved are available through [IJIC Offshore Leaks](https://offshoreleaks.icij.org/pages/database).

Most of the data above is available through [OpenSanctions](https://www.opensanctions.org/).
In some cases, manual curation will be required.


## Anti-fraud measures

  1. Many companies and some individuals are based in Azerbaijan, where we can assume (in hindsight) that many of these may have collaborated in the corruption scheme.

  2. The-opposite-of-vector-search: red-flag companies with "no visible means of support", such as `BAKTELEKOM MMC`, i.e., which have no public presence though may *appear* similar to known companies.

  3. Sanctions: red-flag companies (such as banks) which have sanctions or other risks identified:
      + [OpenCheck](https://opencheck.world/)
      + [OpenAleph](https://search.openaleph.org/)

  4. Graph query pattern: red-flag companies which are limited partnerships (LLP or LP) registered in the UK (where it's inexpensive, quick, simple, and deliberately permissive) which have officers in offshore tax havens such as Belize, Seychelles, British Virgin Islands, Marshall Islands, and so on -- plus often quite vague [*Standard Industrial Classification*](https://www.sec.gov/search-filings/standard-industrial-classification-sic-code-list) (SIC) codes describing their business activities.

  5. Several companies are based in Turkey and Cyprus -- engaged in import/export or construction, which may be legit -- though this can also be a vector for obscuring money laundering activities.


----------------------------------------------------------------------

# How to get started in money laundering

In general, this tutorial is about the "weapons of mass corruption" --
to paraphrase author [Gil Durán](https://www.gilduran.com/).

Analysis here builds on a prior project led by Clair Sullivan:

 - <https://github.com/cj2001/senzing_occrp_mapping_demo/>

The primary dataset used here comes from:

 - <https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-raw-data>

These are leaked wire transfer transactions from the _Azerbaijani
Laundromat_ case during 2012-2014 at the Estonian branch of Danske
Bank involving thousands of "non-resident accounts", i.e., from
Russia.


## legal fallout

Danske Bank subsequently pleaded guilty to fraud charges by the
US DOJ in Dec 2022 and paid ~$2B fines and settlements across
US and EU authorities. Two Lithuanian facilitators connected to
the scheme, Irene ELLERT and Arūnas MAČĖNAS, were sentenced to
9 and 7 years respectively in Feb 2024.


## data caveats

Of the 438 entities named in the wire transfers, 45 are duplicates.
In other words, more than 10% duplicates rate -- where the typical
rate of entity mismatch is 10-30% in enterprise data.

Be cautious about any use AI services, agents, and related search
engines (e.g., Google) to research this kind of data, since core
elements of fraud tradecraft rely on "one letter off" or "one word
off" changes to names to make shell companies appear legit -- and this
is precisely the mistake which the "AI" services tend to amplify.


## news articles

https://committees.parliament.uk/writtenevidence/107143/pdf/
https://committees.parliament.uk/writtenevidence/18567/pdf/
https://dataharvest.eu/wp-content/uploads/2019/11/Eva-Jung-Money-laundering-at-Danske-Bank.pdf
https://en.wikipedia.org/wiki/Danske_Bank_money_laundering_scandal
https://hetq.am/en/article/84283
https://kyc-chain.com/the-azerbaijani-laundromat/
https://news.am/en/news/408615
https://news.bloomberglaw.com/bloomberg-law-analysis/analysis-there-is-something-rotten-in-the-state-of-denmark
https://offshoreleaks.icij.org/nodes/10047636
https://wikitia.com/wiki/Ruslan_Aliyev
https://www.amlc.eu/the-azerbaijani-laundromat-a-new-money-laundering-machine-in-a-familiar-guise/
https://www.bbc.com/news/uk-60203664
https://www.delfi.ee/artikkel/74691745/osa-magnitski-surmaga-seotud-rahast-vois-jouda-eesti-firmadeni
https://www.fi.ee/en/news/liquidation-danske-bank-estonian-branch-has-started
https://www.occrp.org/en/project/the-azerbaijani-laundromat/avromed-company-llp
https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-core-companies
https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-origin-of-the-money
https://www.occrp.org/en/project/the-fincen-files/rinse-profit-repeat-how-a-small-team-of-estonians-turned-a-danish-bank-into-a-laundromat
