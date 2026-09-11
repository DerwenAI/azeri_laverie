## TODOs

  - represent `firms.txt` as BODS RDF and as Sz JSON -- as a thesaurus
  - use thesaurus for resolved entities who were parties in transactions
  - convert transaction amounts from various currencies to USD
  - build a graph which has the full set of entities and relations
  - calculate how much % coverage can be obtained through each AML rule


# How to get started in money laundering

**Paco Nathan**, [Senzing](https://senzing.com/)  
2026-09-11

In general, this tutorial is about the "weapons of mass corruption" --
to paraphrase author [Gil Durán](https://www.gilduran.com/).
One underlying issue is that financial crimes plus other fraud and
corruption conducted by criminal networks tend to leverage systematic
problems in data infrastructure.
Means for rectifying these problems are described by
[*identity intelligence*](https://senzing.com/what-is-identity-intelligence/).

The primary dataset used here comes from:

 - <https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-raw-data>

These are leaked wire transfer transactions from the _Azerbaijani
Laundromat_ case during 2012-2014 at the Estonian branch of Danske
Bank involving thousands of "non-resident accounts", i.e., from
Russia.

Our analysis builds on a prior project led by Clair Sullivan:

 - <https://github.com/cj2001/senzing_occrp_mapping_demo/>


## Legal fallout

Danske Bank subsequently pleaded guilty to fraud charges by the
US DOJ in Dec 2022 and paid ~$2B fines and settlements across
US and EU authorities. Two Lithuanian facilitators connected to
the scheme, Irene ELLERT and Arūnas MAČĖNAS, were sentenced to
9 and 7 years respectively in Feb 2024.

For detailed analysis of this incident, see _The Data Money Files_ S1:E3
["The Billion Dollar Shuffle"](https://youtu.be/Gtp7U0iq-2I?feature=shared)
where authors Ray Blake and Graham Barrow describe
> "Simple and obvious clues that a given account is laundering money that if you know what you're looking for, stick out a mile."

Additional analysis by The Sentry is available at
<https://atlas.thesentry.org/azerbaijan-aliyev-empire/>


## Data caveats

Of the 438 entities named in the wire transfers, 45 are duplicates.
In other words, more than 10% duplicates rate -- where the typical
rate of entity mismatch is 10-30% in enterprise data.

Be cautious about any use AI services, agents, and related search
engines (e.g., Google) to research this kind of data, since core
elements of fraud tradecraft rely on "one letter off" or "one word
off" changes to names to make shell companies appear legit -- and this
is precisely the mistake which the "AI" services tend to amplify.


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

Most of the data described above is available through [OpenSanctions](https://www.opensanctions.org/).
However in some cases, manual curation will be required.

With these data sources available, one can run
[*entity resolution*](https://senzing.com/what-is-entity-resolution/) (ER),
for example by using a [Senzing MCP server](https://mcp.senzing.com/) with 
Anthropic Claude or other AI services.
The ER process resolves the mentioned entities and identifies potential relationships among them.
Results can then construct a [thesaurus](https://moderndata101.substack.com/p/the-semantic-infrastructure-opportunity) as a knowledge asset.

Applying the ER results in a thesaurus to the wire transfer transactions produces the elements needed for constructing an 
[*entity resolved knowledge graph*](https://senzing.com/entity-resolved-knowledge-graphs/), namely as *nodes*, *edges*, and *properties*.

We will use a knowledge graph construction process known as the
[*Ontology Pipeline*](https://technicspub.com/ontology-pipeline/)
by author Jessica Talisman, leveraging a few data models which are based on
[*Simple Knowledge Organization System Reference*](https://www.w3.org/TR/skos-reference/) (SKOS):

  * [Follow The Money](https://followthemoney.tech/)
  * [Beneficial Data Ownership Standard](https://standard.openownership.org/)
  * [sz-semantics](https://github.com/senzing-garage/sz-semantics/wiki/ns)

This produces a *semantic graph*, based on the [*semantic web standards*](https://www.w3.org/RDF/),
which can be transformed into a *property graph* in [`NetworkX`](https://networkx.org/) using a
small library <https://github.com/DerwenAI/xandergraph> which is available as open source.

Graph algorithms and network analytics based on using `NetworkX` and [`Polars`](https://pola.rs/)
allow us to develop measures and classifiers to identify money laundering
[*tradecraft*](https://en.wikipedia.org/wiki/Tradecraft),
in other words to spot the fraud.

Then we can visualize all of this graph-based analysis using [Garphfield](https://garphield.com/).


## Anti-fraud measures

All of this begs a question: "What should the bank have been doing to
identity money laundering when it was happening?"

When accountants or other auditors look at financial transactions,
they tend to leverage
[*generally accepted accounting principles*](https://fasab.gov/accounting-standards/) (GAAP).
This involves comparing transaction dates and amounts, matching invoice numbers, and so on.

Given the criminal nature of money laundering, especially at large scale, one can assume that
accounting standards are not being followed. In fact there appear to be "simple mistakes"
intended to obscure an accountant's audit.

Instead we can work backwords from the known tradecraft, following the trail of
[*beneficial ownership*](https://www.beneficialownership.co.uk/)
to _follow the money_ in contexts which don't quite pass the "smell test":

  1. Many companies and some individuals are based in Azerbaijan, where we can assume (in hindsight) that many of these may have collaborated in the corruption scheme.

  2. The-opposite-of-vector-search: red-flag companies with "no visible means of support", such as `BAKTELEKOM MMC`, i.e., which have no public presence though may *appear* similar to known companies.

  3. Sanctions: red-flag companies (such as banks) which have sanctions or other risks identified:
      + [OpenCheck](https://opencheck.world/)
      + [OpenAleph](https://search.openaleph.org/)

  4. Graph query pattern: red-flag companies which are limited partnerships (LLP or LP) registered in the UK (where it's inexpensive, quick, simple, and deliberately permissive) which have officers in offshore tax havens such as Belize, Seychelles, British Virgin Islands, Marshall Islands, and so on -- plus often quite vague [*Standard Industrial Classification*](https://www.sec.gov/search-filings/standard-industrial-classification-sic-code-list) (SIC) codes describing their business activities.

  5. Several companies are based in Turkey and Cyprus -- engaged in import/export or construction, which may be legit -- though this can also be a vector for obscuring money laundering activities.

## Key takeaways

Overall, the tradecraft measures from our graph analysis serve to
identify suspicious activities within this data.
Banks are required to file a
[*suspicious activity report*](https://www.fincen.gov/suspicious-activity-reports-sars) (SAR)
when they identify such behaviors.
These SARs and other related reports get routed through
[*financial investigation units*](https://www.congress.gov/crs_external_products/IF/PDF/IF12488/IF12488.2.pdf) (FIU),
then distributed through a [global network](https://egmontgroup.org/)
to the intelligenc community, tax authorities, law enforcement, etc.

Consider that large scale criminal activities -- such as influence
campaigns, human trafficking, weapons trade, illegal fishing,
mercenaries, and so on -- requires financing.

Money laundering is how criminal networks get their
[dark money](https://verafin.com/wp-content/uploads/2026/03/global-financial-crime-report-2026-nasdaq-verafin-20260316.pdf)
moved into seemingly legitimate accounts, for example to use in
bribing corrupt officials or purchasing luxury items.
This is generally associated with tax fraud and sanctions evasion.
The scope of this problem is estimated at $4.4T/year for B2B dark money
flows, with +19% annual growth since 2023.

For a variety of reasons, criminal networks tend to use
external professionals for money laundering.
These professionals are incentivised not to use crypto currencies,
In other words, what professional scammer wants to tell
a Russian oligarch that 20% of their laundered funds were
lost due to rapid fluctuations in value? "Oops, my bad."

Consequently there are small armies of (corrupt) professional
cadre dedicated to money laundering and related activities:
law firms, accounting firms, wealth management, title escrow,
trusts, property management, import/export, etc.
Dedicated corporate services exist which may be legit -- or not --
acting as *registered agents* to provide addresses, handle
corporate filings, and serve as intermediaries in other ways.
In some cases, banks and other financial service firms provide
[*nominees*](https://www.investopedia.com/terms/n/nominee.asp)
which may obscure transactions and money flows.

Even so, current costs for a bank to process a SAR are estimated at
$50K on average (2024), so these reports are not casual practices.
Banks may face criminal liabilities for under-reporting SARs and
civil liabilities for over-reporting -- even as double-jeopardy
within the same case!

Compounding these tensions and inherent conflicts, there are other
structural issues which interfere with efforts to identity money
laundering and other finanicial crime:

  * *data quality*: enterprise data generally has an entity mismatch rate of ~10% (up to 30% in some instances)
  * *customer relations*: bank executives are often reluctant to report their top customers for potential crimes
  * *global banking*: international wire transfers sometimes must go through intermediaries in jurisdictions which are sus
  * *legacy analytics*: fraud analyst teams which don't use ER and graph analytics tend to lose sight of crimes

We cannot solve all of these problems, though clearly an anti-fraud
analyst using graph analytics on a laptop could have spotted $3B of
money laundering within 17,000 wire transfers.
By augmenting graph technologies with properly combined ER engines (as
tools) and AI services (for summarizing), anti-fraud teams can
accelerate their collaborations with FIUs, tax authorities, the IC,
and so on.


## Related news articles

- <https://committees.parliament.uk/writtenevidence/107143/pdf/>
- <https://committees.parliament.uk/writtenevidence/18567/pdf/>
- <https://dataharvest.eu/wp-content/uploads/2019/11/Eva-Jung-Money-laundering-at-Danske-Bank.pdf>
- <https://en.wikipedia.org/wiki/Danske_Bank_money_laundering_scandal>
- <https://hetq.am/en/article/84283>
- <https://kyc-chain.com/the-azerbaijani-laundromat/>
- <https://news.am/en/news/408615>
- <https://news.bloomberglaw.com/bloomberg-law-analysis/analysis-there-is-something-rotten-in-the-state-of-denmark>
- <https://offshoreleaks.icij.org/nodes/10047636>
- <https://wikitia.com/wiki/Ruslan_Aliyev>
- <https://www.amlc.eu/the-azerbaijani-laundromat-a-new-money-laundering-machine-in-a-familiar-guise/>
- <https://www.bbc.com/news/uk-60203664>
- <https://www.delfi.ee/artikkel/74691745/osa-magnitski-surmaga-seotud-rahast-vois-jouda-eesti-firmadeni>
- <https://www.fi.ee/en/news/liquidation-danske-bank-estonian-branch-has-started>
- <https://www.occrp.org/en/project/the-azerbaijani-laundromat/avromed-company-llp>
- <https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-core-companies>
- <https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-origin-of-the-money>
- <https://www.occrp.org/en/project/the-fincen-files/rinse-profit-repeat-how-a-small-team-of-estonians-turned-a-danish-bank-into-a-laundromat>

