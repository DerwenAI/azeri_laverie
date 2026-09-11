# Money laundering fundamentals

This material describes some of the heuristics used by fraud analysts
to spot not-so-legit things happening during financial transactions.
These heuristics help assess whether a bank account is being used for
money laundering.

In other words, this is helpful info for someone who is new to
_anti-money laundering_ (AML) or, for that matter, anyone thinking
about **becoming a money launderer**.


## Nut and bolts

Money laundering generally follows three stages:

* **placement** (getting illicit cash into the financial system)
* **layering** (obscuring its origin through complex transactions)
* **integration** (reintroducing it as apparently legitimate funds)

Most specific techniques are variations on those stages. The following
practices are commonly discussed in AML literature, investigative
journalism, and regulatory guidance.


### Placement techniques

1. **Structuring (or "smurfing")** — breaking large cash deposits into many smaller ones, each kept below the reporting threshold (e.g. $10,000 in the US, €10,000 in the EU). Often spread across multiple branches, accounts, or "smurfs" (people acting on behalf of the launderer).

2. **Cash-intensive front businesses** — running illicit cash through legitimate-looking businesses that genuinely take a lot of cash (car washes, laundromats, nail bars, bars and nightclubs, parking lots, vending machines), inflating their reported revenues.

3. **Currency exchanges and money service businesses** — using bureaux de change, remittance firms, or unregistered hawala-style networks to convert or move cash with weaker KYC than a bank.

4. **Cash smuggling** — physically transporting bulk cash across borders to a jurisdiction with looser controls, then depositing it there.

5. **Mixing illicit cash with legitimate takings** — depositing dirty cash alongside the genuine receipts of a business so the totals look plausible.


### Layering techniques

6. **Shell companies** — anonymous entities (often LLCs, LLPs, or international business companies) with nominee directors and registered agents, used to hold accounts and move funds while hiding beneficial ownership.

7. **Chains of wire transfers across jurisdictions** — moving funds through multiple banks in multiple countries, especially using secrecy or weakly-regulated jurisdictions, to break the audit trail.

8. **Correspondent and "nested" banking relationships** — exploiting the fact that a small foreign bank's transactions are bundled through a larger correspondent bank that doesn't see the underlying customers.

9. **Trade-based money laundering (TBML)** — over- or under-invoicing goods, multiple invoicing for the same shipment, phantom shipments, or misdescribing goods so that value moves between countries disguised as trade payments.

10. **Mirror trades** — buying securities in one country/currency and simultaneously selling equivalent securities in another, moving value across borders without an obvious wire transfer.

11. **Back-to-back loans** — laundering money by "lending" it to yourself: dirty money is placed offshore, then a related entity in another jurisdiction takes out a loan secured against it, so the funds appear as legitimate borrowings.

12. **Round-tripping** — sending funds offshore and bringing them back as foreign "investment," often through tax havens.

13. **Casinos and gambling** — buying chips with cash, gambling minimally, then cashing out for a check or wire as "winnings." Online gambling and prepaid betting accounts are modern variants.

14. **Real estate transactions** — buying property (often through shells or trusts), sometimes in cash, and reselling it; or using rapid resales ("flipping") with manipulated prices.

15. **High-value goods** — jewelry, gold, art, antiques, classic cars, and luxury watches, which can store value, move physically, and trade through opaque markets.

16. **Cryptocurrency techniques** — using mixers/tumblers, chain-hopping between coins, privacy coins, peel chains, decentralized exchanges, and unhosted wallets to break blockchain traceability.

17. **Prepaid cards and stored-value instruments** — loading funds onto cards that can be used or cashed out across borders with limited KYC.

18. **Insurance products** — buying single-premium life insurance or annuities and then surrendering them early, often at a loss, to receive an apparently clean payout.


### Integration techniques

19. **Property purchases for personal use** — once layered, funds buy houses, apartments, or commercial real estate held in the launderer's or a relative's name.

20. **Investing in legitimate businesses** — acquiring or capitalizing real companies, sometimes loss-making ones, to provide ongoing "income."

21. **Loan-back schemes** — the launderer's offshore vehicle "lends" them money domestically; loan repayments then look like normal financial activity.

22. **Salaries, fees, and consulting payments to insiders or family members** — paying associates from a controlled company so the money arrives as ordinary employment income.

23. **Fake legal settlements, lawsuits, or gambling winnings** — manufacturing a paper reason for a large, "clean" lump sum to appear in someone's account.

24. **Charitable foundations and non-profits** — abusing NGOs or foundations as conduits, particularly across borders.


### Cross-cutting facilitators

These aren't tradecraft techniques, per se, though be sure to
recognize how these persona recur in most schemes:

1. **professional enablers** (lawyers, accountants, company-formation agents, real-estate agents) who set up structures and provide a veneer of respectability

2. **politically exposed persons (PEPs)** whose status discourages scrutiny

3. **complicit insiders** at banks who suppress alerts

4. **secrecy jurisdictions** which combine corporate anonymity with weak information-sharing. Large-scale schemes — the Russian Laundromat, the Azerbaijani Laundromat, Danske Estonia, 1MDB, and so on — almost always combining several of the above rather than relying on a single method


---

## Tradecraft in the wild

The following points have been excerpted from:  

_The Data Money Files_ S1:E3  
"The Billion Dollar Shuffle"  
<https://youtu.be/Gtp7U0iq-2I?feature=shared>

The authors Ray Blake and Graham Barrow describe this as:
> "Simple and obvious clues that a given account is laundering money that if you know what you're looking for, stick out a mile."


### total volume and daily volumes

Is the *volume of transactions* typical for the type and age of
business or whether there are any red flags. For example, if it's a
long established building contractor, there will be a typical level of
transactional activity, which will look very different from, say, a
newly formed computer consultancy.

As a rule of thumb, a new business is likely to have fewer *account
activities* than a well-established and successful one.

So is the business transacting on a consistent daily basis or do its
transactions seem relatively unpredictable?

For example, a retail business is more likely to have regular payments
both in and out, even though it may vary by season or even by day of
the week -- compared with a management consultancy, which may be more
ad hoc.

Newly formed companies typically require some amount of time before
they've built up their client list and substantial volumes of cash
flow. If a new commercial bank account suddenly has large volumes
flowing through it, this is highly suspicious.


### total and daily values for both debits and credits

A successful business should take in more than it pays out unless it
is running at a loss, which means you would expect that the amount you
receive by way of invoices would be more than the amount you pay out
in invoices. The difference between the two would then be made up of
other business expenses, rent, wages and other costs, leaving you
hopefully with a surplus at the end.

One of the hallmarks of a "laundromat" scheme is the _rapid movement
of funds_ into and out of an account. After all, you don't want to
risk your money getting frozen in an account if you happen to get
spotted. The idea is to move it as soon as possible.

Look for evenly matched daily credits and debits.

Within the individual transaction amounts, look for amounts
consistently just below a threshold like `9,000` or `99,000`, and so
on. Because banks often have limits at which their alerts kick
in. Some are prescribed by law and others are simply based on the
bank's own risk appetite.

If the launderers have someone working inside a bank, they may be
aware of these limits and consistently pay just below them. Or they
might have guessed the likely limits, or arrived at them through trial
and error in accounts that they've set up specifically to test the
limits and see whether these get flagged.


### round-numbered amounts in large transactions

Often money launderers are lazy and move money around the system in
big round figures. If you examine the average honest business account,
big round figures are quite rare -- except maybe when partners or
owners draw from the company.

Consistent appearance of *round figure amounts* on a bank statement,
unless there are good business reasons for them to appear, are highly
suggestive of money laundering.


### closing daily balances, compared with total activity

If money launderers move individual sums in and out in quick
succession, consistently across the entire account activity, the
*overnight balance* will be very low in comparison to the *total
activity*.

Look at the ratio of average overnight balance to total activity.

A regular customer will usually not virtually empty a very active
account overnight each day, but a money launderer often will.


### remitters and receivers of payments

Is there any obvious connection between the *remitters*, the account
in question and the *receivers*? If the account's being used for money
laundering, it might well be part of the *layering* stage of money
laundering.

  * **Layering**: _moving money rapidly between different accounts and usually different jurisdictions to disguise its origins._

All three elements of the transaction, the remitter, the account
holder and the onward receiver, must be under the control of the
launderers or otherwise they'd lose their money. They will go out of
their way to mask these connections. It's the job of the investigator
to find them.


### nature of the business

You wouldn't expect a fine art company to be doing business with the
manufacturer of parts for a motor car, or at least not on a regular
basis.

You wouldn't expect a firm that's consistently paid by you to
consistently also send you money. Some firms pay as if they were
suppliers and some firms pay as if they were customers. Normally these
are two different populations. It's possible, I guess, that you both
send and receive money from the same company, but it wouldn't be
common.


### data exhaust

In this day and age, almost all firms have some sort of Internet
presence. The more successful they are, the more likely they'll have
some sort of online business.

If you come across a commercial firm that has absolutely no Internet
presence at all, that's suspicious.


## Key points from _The Dark Money Files_

A homework assignment for the interested reader is to listen to the
full S1:E2 and S1:E3 podcast episodes: <https://www.thedarkmoneyfiles.com/podcast>
... or better yet, listen closely to their entire multi-year series!

To help get you started, we've summarized key points from these
episode transcripts:


### The Launching of a Laundromat (Episode 2)

Focusing on structural set-up, not the transaction-level mechanics:
<https://youtu.be/-ahmWY-mFEM?si=2M7o-cMjgTdW7C_d>

1. **"Non-resident portfolio" banking** — running a dedicated stream of accounts at the Estonian branch for customers based outside Estonia (largely Russian and other Central/Eastern European clients), keeping the activity at arm's length from the bank's home jurisdiction.

2. **Pure "flow" business** — accounts that take in money and send it on, with no lending and almost no credit risk, so the branch needs minimal capital and attracts less prudential scrutiny.

3. **Cross-border corporate layering of the bank itself** — Danish parent → acquired Finnish bank (Sampo) → Estonian branch → Russian-and-CIS customers, so supervision is split across multiple regulators who each see only part of the picture.

4. **Volume wildly disproportionate to the local economy** — flows peaking around €32bn/year through one branch in a country whose entire GDP was ~€38bn (roughly 90% of GDP through a single branch).

5. **Ignoring early-warning signals from foreign regulators** — the Russian Central Bank's alert (via the Danish FSA) about "criminal activity in its pure form, including money laundering" estimated at billions of rubles a month was effectively not acted on.

6. **Connection to other known laundromats** — the Estonian flows are linked to the Russian Laundromat and the Azerbaijani Laundromat schemes.
Mirror trades — flagged but deferred to a later episode (buying a security in one currency/country and simultaneously selling it in another to move value across borders).

7. **Mirror trades** — flagged but deferred to a later episode (buying a security in one currency/country and simultaneously selling it in another to move value across borders).


### *The Billion Dollar Shuffle* (Episode 3)
Walking through transaction-level red flags found within the leaked bank documents:
<https://youtu.be/Gtp7U0iq-2I?feature=shared>

1. **Rapid in-and-out flow** — funds moved on almost immediately to avoid being frozen if spotted; matched credits and debits each day.

2. **Very low average overnight balance** relative to total daily turnover — accounts repeatedly emptied at end of day despite huge throughput.

3. **Structuring / smurfing** — transactions kept consistently just below reporting thresholds (e.g., just under $9,000, $99,000, or €1,000,000), sometimes implying inside knowledge of bank-specific limits.

4. **Round-figure transactions** — large round-number transfers (e.g., €50,000, €300,000, $987,000) that don't match the messy numbers of genuine commercial invoicing.

5. **Layering** — moving money through chains of accounts in multiple jurisdictions to obscure origin (described as "shuffling the cards").

6. **Integration** — reinjecting laundered funds into the legitimate economy in non-round amounts to specific recipients, e.g., private school/college fees, property purchases ("entrusting of money for the paying of property").

7. **UK Limited Liability Partnerships as shell vehicles** — LLPs used because they offer corporate-style anonymity with limited filing obligations.

8. **Address clustering of shells** — 23 of 29 frequently-recurring LLPs registered at just two addresses (a mansion flat in Earl's Court and a nail bar in Cardiff).

9. **Common nominee designated members** — the same two corporate designated members (Ireland & Overseas Acquisitions Ltd and Milltown Corporate Services Ltd) used across 2,184 LLPs, themselves registered in secrecy jurisdictions (BVI, Belize).

10. **Bland, meaningless company names** that give no indication of any actual business.

11. **Mismatch between registered and trading addresses** — registered in West London, trading address in Moscow.

12. **Mismatched payment descriptions** — credit narratives ("construction equipment") not matching debit narratives ("electronic techniques") on near-identical amounts passing straight through.

13. **Counterparty business mismatch** — entities supposedly trading with each other whose stated industries make no commercial sense as trading partners.

14. **Same counterparty acting as both payer and payee** — the same firm sending money in and receiving money out, atypical of genuine supplier/customer relationships.

15. **No internet or commercial footprint** for ostensibly trading companies.

16. **Heavy activity from day one** — large transactions starting within days of account opening, before any normal business could have been built up.

17. **Multi-currency activity** disproportionate to the entity's apparent size (one LLP transacting in Swiss francs, Estonian crowns, euros, pounds, rubles, and dollars).

18. **Huge gap between filed accounts and bank flows** — LLPs filing Companies House accounts showing £12k–£36k of annual income while moving tens of millions of euros and dollars through their bank accounts in the same period.

19. **Self-dealing networks** — remitter, account holder, and ultimate receiver all controlled by the same parties (necessary so the launderers don't lose the money), with deliberate effort to mask the connections.

The authors also note how "red flags" compound exponentially, not additively.
A few of these occurring together is substantially more suspicious
than any one in isolation, which is what eventually let whistleblower
Howard WILKINSON identify the scheme by examining a handful of UK
LLPs.

\# # #
