# How to get started in money laundering

**Paco Nathan**, [Senzing](https://senzing.com/)  
2026-09-11

It's been said that almost any kind of financial transaction can be
turned into a *money laundering* scam.

This material is about confronting the "weapons of mass corruption" --
to paraphrase author [Gil Durán](https://www.gilduran.com/).
Notably, financial crimes and other fraud and corruption conducted by
criminal networks which tend to leverage systematic problems in data
infrastructure as well as shortcomings of human nature and perception.
Means for rectifying these problems are described by the practices of
[*identity intelligence*](https://senzing.com/what-is-identity-intelligence/).

The primary dataset used here comes from:

 - <https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-raw-data>

These are wire transfer transactions from the _Azerbaijani Laundromat_
incident at the Estonian branch of Danske Bank during 2012-2014, which
involved thousands of "non-resident accounts", i.e., from Russia.
Our analysis builds on a prior project led by Clair Sullivan:

 - <https://github.com/cj2001/senzing_occrp_mapping_demo/>


## Legal fallout

These transactions were leaked in 2018 by a bank employee at the
Estonian branch named
[Howard WILKINSON](https://kkc.com/whistleblower-case-archive/howard-wilkinson/),
acting as a whistleblower.
Subsequent investigations found that upwards of $800 billion was
laundered through **one branch of Danske Bank in Estonia** during the
early/mid 2010s.

Danske Bank plead guilty to fraud charges by the US DOJ in Dec 2022
and paid ~$2B fines and settlements across US and EU authorities.
Two Lithuanian facilitators connected to the scheme, Irene ELLERT and
Arūnas MAČĖNAS, were sentenced to 9 and 7 years respectively in Feb
2024.

For detailed analysis of this incident, see _The Data Money Files_ S1:E3
["The Billion Dollar Shuffle"](https://youtu.be/Gtp7U0iq-2I?feature=shared)
where authors Ray Blake and Graham Barrow describe
> "Simple and obvious clues that a given account is laundering money that if you know what you're looking for, stick out a mile."

Additional analysis by *The Sentry* is available at
<https://atlas.thesentry.org/azerbaijan-aliyev-empire/>


## Data caveats

Of the 438 entities named in the wire transfers, 45 are duplicates.
In other words, more than 10% duplicates rate -- where the typical
rate of entity mismatch is 10-30% in enterprise data.

Be cautious about use of AI services, agents, and related search
engines (e.g., Google) to research this kind of data.
Core elements of fraud techniques rely on "one letter off" or "one
word off" changes to names, to make shell companies seem more legit.
This is **precisely** the kind of mistake which AI services amplify.
In other words, use agents properly -- via "tools" -- or the agents
may compound identity errors which can cause serious legal liabilities
at machine speed at scale.


## The tutorial

Earlier versions of this "How to get started in money laundering"
tutorial were standing-room-only at other conferences. Apparently,
people want to learn how to break into the business? (pun intended)
We'll take the high road with "We must train like we fight" as our
motto -- along with a wink and a nod.

An estimated $4.4 trillion moves across the world annually as B2B
"dark money" flows. While in many areas the rates of violent crimes
have been dropping, fraud has skyrocketed. For example, more than 40%
of UK crime is now fraud. It makes sense, if you want to do crimes for
a living. Why go out and pull a knife on someone in the street to
demand their wallet, when you could be working on a laptop in a comfy
coffeehouse, overtaking the victim's bank account instead? While
sipping Pumpkin Spice!

In this tutorial, based on the
[https://github.com/DerwenAI/azeri\_laverie](https://github.com/DerwenAI/azeri_laverie)
GitHub repo, we'll explore data from the
[Azerbaijani Laundromat](https://www.occrp.org/en/project/the-azerbaijani-laundromat)
incident which were leaked in 2018 by Howard Wilkinson.

Russia's federal bank had asked the US and EU to check suspicious
activity at this branch **twice**, while regulators had their hands
full following the 2009 global financial crisis. Some obscure Baltic
bank branch with loads of cash balance (from Russia) posed little
interest at the time since it had almost no outstanding loans that
might default. Having confirmed their opportunity, Russian finance
operatives toasted the EU with "Спасибо, мои друзья!" and released the
kraken.

Our dataset includes 4K wire transfers, which entail
[nearly $3 billion in money laundering](https://gijn.org/stories/how-they-did-it-the-azerbaijani-laundromat/)
-- a mere 0.36% of the alleged damage, though it's the part which
became open data. We'll discuss typical ways to devise money
laundering schemes, then look at how to identify financial crime
"tradecraft" within these wire transfers by reframing them as a graph

**TL;DR:* large criminal networks do the crimes, though typically not
the laundering. For that part they hire professionals: large armies of
"kinda sus" law firms, financial advisors, CPAs, real estate, title
companies, property management, and so on.
These shadowy services exist worldwide to fulfill the needs of bad
guys, such as oligarchs who become billionaires by profiting from
human trafficking, illegal weapons trade, ransomware against
hospitals, political influence campaigns, illegal fishing fleets, and
so on. Using external professionals is much like hiring an Uber driver
for your getaway car, then tipping well -- except the driver
specializes in obscured crimes at scale.

By leveraging graph algorithms and visualizations, we'll perform some
forensic accounting on the leaked data, showing how to spot the
schemes, like, on your laptop.
This is something any bank *could* afford to do, just that some would
rather not accuse their largest and most profitable customers of
conducting dirty deeds ... *through the bank*.
Perhaps we can assist with the necessary analytics, help stick it to
the oligarchs and their billionaire-bully friends?

We'll also talk about the elephant in the room. Once you identify
money laundering, how do you find the people orchestrating it? In
other words, who's making a cash withdrawal at the laundered end of a
scheme? Because without that you won't *catch* any arch-villains at
the top. Three words: **follow the money**.

This gets us into more complex issues:

  - [*identity intelligence*](https://senzing.com/what-is-identity-intelligence/)
  - [*entity resolution*](https://senzing.com/what-is-entity-resolution/)
  - [*ultimate beneficial ownership*](https://www.beneficialownership.co.uk/)
  - [*sanctions*](https://sanctionslist.ofac.treas.gov/Home/SdnList)

... where graph technologies and AI tooling help investigators
confront the global kleptocracy.

This problem is massive. It's been gaining momentum, and isn't going
away anytime soon. Check out a sampler of sources about recent money
laundering scams and their interdictions:

  - TD Bank (2024)  
    [https://www.justice.gov/criminal/case/united-states-america-v-td-bank-na](https://www.justice.gov/criminal/case/united-states-america-v-td-bank-na)
  - Bulgarian attacks on UK gov (2025)  
    [https://www.reuters.com/world/uk/romania-arrests-13-phishing-scam-targeting-british-tax-office-2025-07-10/](https://www.reuters.com/world/uk/romania-arrests-13-phishing-scam-targeting-british-tax-office-2025-07-10/)
  - UBS (2026)  
    [https://www.fincen.gov/news/news-releases/fincen-assesses-historic-125-million-penalty-against-ubs-financial-services-inc](https://www.fincen.gov/news/news-releases/fincen-assesses-historic-125-million-penalty-against-ubs-financial-services-inc)
  - Maple Finance (2026)  
    [https://www.cbc.ca/news/canada/canadian-banking-company-linked-to-sanctioned-money-laundering-network-9.7331482](https://www.cbc.ca/news/canada/canadian-banking-company-linked-to-sanctioned-money-laundering-network-9.7331482)

Graph Enhanced AI track, 1 hour, beginner level:

  * Some background coding in Python is needed
  * Integrates [NetworkX](https://networkx.org/en/), [Polars](https://pola.rs/), [Jupyter](https://jupyter.org/), [Senzing](https://mcp.senzing.com/), [Garphield](https://garphield.com/), [OpenCheck](https://opencheck.world/), [Placekey](https://www.placekey.io/), and more
  * This material especially well suited for Public Sector, Finance, Retail


## Replicating results

Starting with the OCCRP dataset, we can augment with other data sources to resolve the entities named as payers and beneficiaries in the transactions:

  1. Several transactions have beneficiaries with names which are codes beginning with `INN` followed by a 10 digit number -- such as `INN3016043171` -- and these are [Russian tax identifiers](https://www.nalog.gov.ru/eng/inn/) were 10 digits signifies a company or foreign organization.

  2. Several companies and individuals are based in Azerbaijain, where business registries are not especially transparent, and moreover these may have personal ties with the Aliyev family which dominates in politics and was the main beneficiary.

  3. Some payers are international banks, for example claiming to refund prior payments on clients' invoices. The [ISO 9362-2022 codes](https://www.iso9362.org/isobic/overview.html) for banks, also known as *Business Identifier Codes* (BIC), are managed by [SWIFT](https://www.swift.com/).

  4. Banks and other firms involved in global financial markets will often have a *Legal Entity Identifier* (LEI), managed by [GLEIF](https://www.gleif.org/).

  5. Many of the companies named are registered in countries (EE, UK, DE, CY, VG, TR, etc.) which make portions of their corporate registries data available for public search, or have import/export registries and other corporate directories online -- for example:

      + CN: [HK Companies](https://hkg.databasesets.com/)
      + CY: [Cyprus DRCIP](https://data.gov.cy/)
      + DE: [OpenRegister.de](https://offeneregister.de/)
      + EE: [Estonia RIK](https://avaandmed.ariregister.rik.ee/en/downloading-open-data)
      + SG: [SG Company Directory](https://sg.ltddir.com/)
      + TR: [ISI EMIS](https://isimarkets.com/emis/)
      + UK: [Companies House](https://find-and-update.company-information.service.gov.uk/)
      + VG: [BVI Company Search](https://i-bvi.com/)

  6. Additional data about shell companies and their intermediaries is available through [IJIC Offshore Leaks](https://offshoreleaks.icij.org/pages/database).

Most of the data described above is available through [OpenSanctions](https://www.opensanctions.org/).
However in some cases, additional curation will be required.
Banks used the term
[*enhanced due diligence*](https://legal.thomsonreuters.com/blog/enhanced-due-diligence-edd-an-overview/)
to describe thorough background investigations conducted on high-risk
business relationships and their transactions.
Tools such as [OpenCheck](https://opencheck.world/) can be leveraged via 
[API or an MCP server](https://opencheck.world/api).
However, in some cases manual searches through company registries may be needed.

Note that when using data from a registry, such as Companies House, be
sure to check the dates of incorporation. Shell companies tend to have
relatively generic names, quite deliberately to blend into the
landscape. You might find "ELECTRON ENTERPRISES LTD" in the data,
however if that's a firm incorporated in 2016, funds would not have
been transferred to it in 2012 -- so that's likely a different
company.

With these data sources collected, one can run
[*entity resolution*](https://senzing.com/what-is-entity-resolution/) (ER),
for example by using a [Senzing MCP server](https://mcp.senzing.com/) with 
Anthropic Claude or other AI services.
The ER process resolves the mentioned entities and identifies potential
relationships among them.
Results can then construct a
[thesaurus](https://moderndata101.substack.com/p/the-semantic-infrastructure-opportunity)
as a knowledge asset.

We can enrich this thesaurus with geospatial analysis, in other words
to identify where entities' addresses overlap geographically,
using [Placekey](https://www.placekey.io/) to generate unique
identifiers for physical places.

Applying this thesaurus to these wire transfer transactions produces
the elements needed for constructing an 
[*entity resolved knowledge graph*](https://senzing.com/entity-resolved-knowledge-graphs/),
namely as *nodes*, *edges*, and *properties*.

We will use a knowledge graph construction process known as the
[*Ontology Pipeline*](https://technicspub.com/ontology-pipeline/)
by author Jessica Talisman, leveraging a few data models which are based on
[*Simple Knowledge Organization System Reference*](https://www.w3.org/TR/skos-reference/) (SKOS):

  * [Follow The Money](https://followthemoney.tech/)
  * [Beneficial Data Ownership Standard](https://standard.openownership.org/)
  * [sz-semantics](https://github.com/senzing-garage/sz-semantics/wiki/ns)

Note: Jessica Talisman also assisted on defining the semantics used in
the `sz-semantics` data model.

This produces a *semantic graph*, based on the [*semantic web standards*](https://www.w3.org/RDF/),
which can be transformed into a *property graph* in [`NetworkX`](https://networkx.org/) using a
small library <https://github.com/DerwenAI/xandergraph> which is available as open source.

Graph algorithms and network analytics based on using `NetworkX` and [`Polars`](https://pola.rs/)
allow us to develop measures and classifiers to identify money laundering
[*tradecraft*](https://en.wikipedia.org/wiki/Tradecraft),
in other words to spot the fraud.

Then we can visualize all of this graph-based analysis using [Garphield](https://garphield.com/).


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

Instead we can work backwards from the known tradecraft, following the trail of
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
to the intelligence community, tax authorities, law enforcement, etc.

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
These professionals are incentivized not to use crypto currencies,
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
structural issues which impede efforts to identity money laundering
and other financial crime:

  * *data quality*: enterprise data generally has an entity mismatch rate of ~10% (up to 30% in some instances)
  * *customer relations*: bank executives are often reluctant to report their top customers for potential crimes
  * *global banking*: some wire transfers must go through intermediaries, e.g., *correspondent banks*, in jurisdictions which tend to be sus
  * *legacy analytics*: fraud analyst teams which don't use ER and graph analytics tend to miss financial crimes
  * *influence campaigns*: organized crime in some jurisdictions (US, IT, etc.) lobby corrupt officials to erode *corporate transparency*

While we cannot solve all of these problems, clearly an anti-fraud
analyst equipped with graph analytics on a laptop could have spotted
$3B of money laundering within 17,000 wire transfers.
By augmenting graph technologies with properly combined ER engines (as
tools) and AI services (for summarizing), anti-fraud teams can
accelerate their collaborations with FIUs, tax authorities, the IC,
and so on, to overcome obstacles created by the tradecraft.

Ultimately, what's desperately needed is for more jurisdictions to
make their company registry data available for public use of
beneficial ownership disclosures.
Initiatives such as [Open Ownership](https://www.openownership.org/)
seek to promote and achieve exactly this.


## Related news articles

- <https://committees.parliament.uk/writtenevidence/107143/pdf/>
- <https://committees.parliament.uk/writtenevidence/18567/pdf/>
- <https://dataharvest.eu/wp-content/uploads/2019/11/Eva-Jung-Money-laundering-at-Danske-Bank.pdf>
- <https://en.wikipedia.org/wiki/Danske_Bank_money_laundering_scandal>
- <https://hetq.am/en/article/84283>
- <https://kkc.com/whistleblower-case-archive/howard-wilkinson/>
- <https://kyc-chain.com/the-azerbaijani-laundromat/>
- <https://news.am/en/news/408615>
- <https://news.bloomberglaw.com/bloomberg-law-analysis/analysis-there-is-something-rotten-in-the-state-of-denmark>
- <https://offshoreleaks.icij.org/nodes/10047636>
- <https://wikitia.com/wiki/Ruslan_Aliyev>
- <https://www.amlc.eu/the-azerbaijani-laundromat-a-new-money-laundering-machine-in-a-familiar-guise/>
- <https://www.bbc.com/news/uk-60203664>
- <https://www.businessday.co.za/bd/world/europe/2021-07-14-london-couples-high-life-sheds-light-on-azerbaijani-laundromat/>
- <https://www.delfi.ee/artikkel/74691745/osa-magnitski-surmaga-seotud-rahast-vois-jouda-eesti-firmadeni>
- <https://www.fi.ee/en/news/liquidation-danske-bank-estonian-branch-has-started>
- <https://www.occrp.org/en/project/the-azerbaijani-laundromat/avromed-company-llp>
- <https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-core-companies>
- <https://www.occrp.org/en/project/the-azerbaijani-laundromat/the-origin-of-the-money>
- <https://www.occrp.org/en/project/the-fincen-files/rinse-profit-repeat-how-a-small-team-of-estonians-turned-a-danish-bank-into-a-laundromat>
