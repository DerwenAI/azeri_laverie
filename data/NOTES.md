This directory is a hodgepodge of scripts being used to analyze the
"payer" and "beneficiary" entities in the Azerbaijani Laundromat wire
transfer data leaked from Danske Bank.

On the one hand, there are automated means of open data retrieval,
entity resolution, and enhanced due diligence which can be leveraged
here:
<https://github.com/StephenAbbott/opencheck/releases#release-dataset-azerbaijani-laundromat-2026-10-06>

On the other hand, there has been substantial efforts published
regarding investigative journalism, prosecutions and court trials, and
so on. This latter category requires some analysis to connect the
mentioned entities and collect data from unstructured sources.

Tossing the entire collection of documents could be one approach,
though it was quite important to go through manually first, to
understand what could possibly be represented or explored via a
knowledge graph.

Data quality is quite poor within the wire tranfer data, and it's
important to resolve entities first -- by generating a thesaurus,
effectively -- then the aggregate calculations used for forensic
accounting with graph analytics will be much more accurate. We need to
be able to map from "keys" (names of people and organizations, or
other identifiers) to some unique identifiers used for IRIs.

Ultimately, this needs to:

  1. Fix the wire transfer entity mismatches first, using a thesaurus
  2. Visualize the fraud tradecraft using Garphfield (for ODSC/West)
  3. Link to the automated ER+EDD results to build a KG (for CDL)
  4. Stretch goal: dump the documents into GraphRAG


## TODOs

  - represent the unresolved records in `backfill.json`
  - entity linking to bring in OpenCheck release data set
  - use thesaurus for resolved entities who were parties in transactions

  - follow the property BODS data models for generated RDF
  - build a graph which has the full set of entities and relations
  - calculate how much % coverage can be obtained through each AML rule


## API example access

  - <https://github.com/dannykellett/ukcompanies>
  - <https://broadoakdata.uk/how-to-get-companies-house-data-using-rest-api/>
  - <https://github.com/RegistrumUK/companies-house-api-python-starter/blob/master/example.py>
