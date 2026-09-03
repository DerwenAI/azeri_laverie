## title
How to get started in money laundering

## abstract
What if you understood how to run a money laundering scam at scale? In this one hour, hands-on tutorial, we'll explore exactly that. Think: "We must train like we fight" for anti-fraud with AI.

We'll start with leaked bank transactions from a $3B money laundering case, and build some simple forensic account using `Polars` dataframes and `NetworkX` graphs. We will explore the basics of how to perform money laundering, based on experts' investigations of this $3B case, and talk about current trends. Then we'll build a simple network analysis and drive a graph visualization from the results -- in other words, employ just a few steps within a `Jupyter` notebook to pin-point where to spot the fraud, even when you've started from a view of thousands of transactions amongst hundreds of shell companies.

Next we'll merge the bank transactions with other reference data, leveraging open data used for investigative journalism about FinCrime and corruption. Using entity resolution to merge the data, we'll surface entities and relations for a high-quality knowledge graph which is linked to evidence. Then adding some computable semantics ("a little ontology goes a long way"), we'll enhance our analysis -- in other words, leverage ontology to assist investigators with better details about the fraud and who's involved.

Finally, we'll use this knowledge graph along with the Claude AI personal assistant to access Senzing as a tool to audit and explain the fraud patterns detected.

The workshop covers a full through-line of anti-fraud investigation: event data, reference data, entity resolution, graph analytics and visualization, computable semantics, and LLM-based exploration of fraud. The tutorial uses open source Python packages, where everything runs in Docker containers with Jupyter notebooks, and all code and setup instructions will be provided in a GitHub repository so you can reuse this for your own applications.


## What makes your session unique?
A portion of this tutorial have been run in two other conferences, where participants were startled to learn how money laundering works, and how much they may be witnessing fraud activity within their daily lives. Again, it's building on the "train like you fight" principle, using real banking transactions and expert analysis of the fraud tradecraft as the foundations. Plus we're showing how AI tooling combined with effective use of ontology, entity resolution, graph visualization, etc., help "focus the lens" such that while most people wouldn't be able to spot the crime obscured within thousands of transactions, we can apply current technology to make real-world fraud and corruption much more transparent, within minutes.

## track
Technical

## format
tutorial, 1 hour

## which data science languages will be used
Python

## which data science tools will be used
NetworkX, Polars, Jupyter, Docker, Senzing, Vis.js, Claude MCP

## how familiar attendees should be
Some hands-on experience with Python is the main prerequisite

## level of difficulty
beginner

## indicate why the topic difficulty level has been selected
Given some hands-on experience with Python, we will build on this -- mostly visual

## session focus
entity resolution (identity intelligence, data quality, graph construction, etc.)

## which industry your session will address
especially for Public Sector, Finance, Retail
