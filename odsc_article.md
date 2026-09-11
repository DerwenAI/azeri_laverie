**Wash enough times, and it gets clean**

[Paco Nathan](https://sessionize.com/pacoid/)  
Principal DevRel Engineer, Senzing  
2026-09-05

It’s been said that almost any kind of financial transaction can be turned into a *money laundering* scam.

Earlier versions of this “How to get started in money laundering” tutorial were standing-room-only at other conferences. Apparently, people want to learn how to break into the business? (pun intended) We’ll take the high road with “We must train like we fight” as our motto – along with a wink and a nod.

An estimated $4.4 trillion moves across the world annually as B2B “Dark Money” flows. While in many areas the rates of violent crimes have been dropping, fraud has skyrocketed. For example, more than 40% of UK crime is now fraud. It makes sense, if you want to do crimes for a living. Why go out and pull a knife on someone in the street to demand their wallet, when you could be working on a laptop in a comfy coffeehouse, overtaking the victim’s bank account instead? While sipping Pumpkin Spice!

In this tutorial, based on the [https://github.com/DerwenAI/azeri\_laverie](https://github.com/DerwenAI/azeri_laverie) GitHub repo, we’ll explore data from the [Azerbaijani Laundromat](https://www.occrp.org/en/project/the-azerbaijani-laundromat) incident, leaked by a whistleblower. Subsequent investigations found that upwards of $800 billion was laundered through **one branch of Danske Bank in Estonia** during the early/mid 2010s. Russia’s federal bank had asked the US and EU to check suspicious activity at this branch **twice**, while regulators had their hands full following the 2009 global financial crisis. Some obscure Baltic bank branch with loads of cash balance (from Russia) posed little interest at the time since it had almost no outstanding loans that might default. Having confirmed their opportunity, Russian finance operatives toasted the EU with “Спасибо, мои друзья!” and released the kraken.

Our dataset includes 4K wire transfers, which entail [nearly $3 billion in money laundering](https://gijn.org/stories/how-they-did-it-the-azerbaijani-laundromat/) – a mere 0.36% of the alleged damage, though it’s the part which became open data. We’ll discuss typical ways to devise money laundering schemes, then look at how to identify financial crime “tradecraft” within these wire transfers by reframing them as a graph.

TL;DR: large criminal networks do the crimes, though typically not the laundering. For that part they hire professionals: large armies of “kinda sus” law firms, financial advisors, CPAs, title companies, property management, and so on. These shadowy services exist worldwide to fulfill the needs of bad guys, such as oligarchs who become billionaires by profiting from human trafficking, illegal weapons trade, ransomware against hospitals, political influence campaigns, illegal fishing fleets, and so on. Using external professionals is much like hiring an Uber driver for your getaway car, then tipping well – except the driver specializes in obscured crimes at scale.

By leveraging graph algorithms and visualizations, we’ll show how to spot the schemes, like, on your laptop. This is something any bank *could* afford to do, just that some would rather not accuse their largest and most profitable customers of conducting dirty deeds … *through the bank*. Perhaps we can assist with the necessary analytics, help stick it to the oligarchs and their billionaire-bully friends?

We’ll also talk about the elephant in the room. Once you identify money laundering, how do you find the people orchestrating it? In other words, who’s making a cash withdrawal at the laundered end of a scheme? Because without that you won’t *catch* any arch-villains at the top. Three words: follow the money. This gets into more complex issues of [*sanctions*](https://sanctionslist.ofac.treas.gov/Home/SdnList), [*identity intelligence*](https://senzing.com/what-is-identity-intelligence/), [*entity resolution*](https://senzing.com/what-is-entity-resolution/), [*ultimate beneficial ownership*](https://www.beneficialownership.co.uk/), and more, where AI tooling is helping investigators confront the global kleptocracy.

This problem is massive. It’s been gaining momentum, and isn’t going away anytime soon. Check out a sampler of sources about recent money laundering scams and their interdictions:

-   TD Bank (2024)
    [https://www.justice.gov/criminal/case/united-states-america-v-td-bank-na](https://www.justice.gov/criminal/case/united-states-america-v-td-bank-na)
-   Bulgarian attacks on UK gov (2025)
    [https://www.reuters.com/world/uk/romania-arrests-13-phishing-scam-targeting-british-tax-office-2025-07-10/](https://www.reuters.com/world/uk/romania-arrests-13-phishing-scam-targeting-british-tax-office-2025-07-10/)
-   UBS (2026)
    [https://www.fincen.gov/news/news-releases/fincen-assesses-historic-125-million-penalty-against-ubs-financial-services-inc](https://www.fincen.gov/news/news-releases/fincen-assesses-historic-125-million-penalty-against-ubs-financial-services-inc)
-   Maple Finance (2026)
    [https://www.cbc.ca/news/canada/canadian-banking-company-linked-to-sanctioned-money-laundering-network-9.7331482](https://www.cbc.ca/news/canada/canadian-banking-company-linked-to-sanctioned-money-laundering-network-9.7331482)

Graph Enhanced AI track, 1 hour, beginner level – using Python, [NetworkX](https://networkx.org/en/), [Polars](https://pola.rs/), [Jupyter](https://jupyter.org/), [Senzing](https://mcp.senzing.com/), [Garphield](https://garphield.com/), and more – especially for Public Sector, Finance, Retail.

\# # #