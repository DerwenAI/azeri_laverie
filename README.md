# azeri_laverie

Money laundering graph data analysis, based on leaked banking data
provided by OCCRP regarding the "Azerjaibani Laundromat" incident.


This repo includes a few primary resources:

  * [`ABSTRACT.md`](https://github.com/DerwenAI/azeri_laverie/blob/main/ABSTRACT.md):
an introduction to this material, descriptions of the processes involved, plus links to primary sources and other resources available online.
  * [`TIMELINE.md`](https://github.com/DerwenAI/azeri_laverie/blob/main/TIMELINE.md):
a reconstructed timeline for the events related to the Azerbaijani Laundromat and subsequent investigations.
  * [`TRADECRAFT.md`](https://github.com/DerwenAI/azeri_laverie/blob/main/TRADECRAFT.md):
detailed descriptions of how money laundering gets performed, plus excerpts from industry experts analyzing the Azerbaijani Laundromat case.
  * [`occrp.ipynb`](https://github.com/DerwenAI/azeri_laverie/blob/main/occrp.ipynb):
a Jupyter notebook which performs forensic auditing on the leaked bank records, using graph algorithms and network analytics to identify criminal tradecraft.


We have a few narratives to untangle, which tend to augment each other:

  * **process:** _money laundering_ plus analysis of the related FinCrime _tradecraft_ employed, leveraging investigative journalism based on two leaked datasets: the ["Azerbaijani Laundromat"](https://www.occrp.org/en/project/the-azerbaijani-laundromat) and the subsequent, larger ["FinCEN Files"](https://www.icij.org/investigations/fincen-files/global-banks-defy-u-s-crackdowns-by-serving-oligarchs-criminals-and-terrorists/)

  * **supply:** _Obscuring Beneficial Ownership as a Service_ (OBOaaS) where **Erik Lidmets** (Goldcraft Universal LLP), **Juri Kidjajev** (Beta Consult), et al., operated out of **Danske Bank A/S Eesti Filiaal** -- acquired from **Sampo Bank** of Finland in 2006, which had acquired **Optiva Bank** of Estonia in 2001 -- to provide "wealthy Russian businessmen" as _non-resident depositors_ with pre-built networks of shell companies whose officers were based in offshore tax havens, while skimming from their accounts

  * **demand:** analysis of the _Azerbaijani elite_ families **Aliyev**, **Suleymanov**, **Eyyubov**, **Feyziyev**, **Gasimov**/**Karimov**, **Mammadov**, **Naghiyev**, et al., plus their former-KGB colleagues, operating globally as "supply chain consultants" -- who were developing mechanisms for _sanctions evasion_ and _illegal political influence campaigns_ at global scale

  * **transparency:** the _corrupt officials_ they engaged, plus their enablers: **PACE**/**Council of Europe**, **UNESCO**, **Mossack Fonseca**, **Paul Manefort**, and so on, which have been exposed through investigative journalism


Toward that purporse, we will explore two knowledge graphs:

  * a core graph of ~\$3B in wire transfers: how were the shell companies used to obscure FinCrime tradecraft, and what signals should have been detected early, based on graph analytics?  (aka, `occrp.json`)

  * a larger KG built around that core, based on the BODS data model: exploring the network of _beneficial ownership_ and political/financial ties for what was used to construct the "Laundromat", mechanisms which are very much in use today, and how graph motifs can detect traces of this corruption?


In addition to open source Python libraries, this project leverages three sets of tooling which each have agentic capabilities:

  * [OpenCheck](https://opencheck.world/) -- conduct _due diligence_ based on open corporate data from many sources, collected into a knowledge graph using the [Beneficial Ownership Data Standard](https://standard.openownership.org/).

  * [Senzing](https://mcp.senzing.com/) -- perform _entity resolution_ as a foundation for _identity intelligence_ infrastructure, in other words
 determining consistent, explanable answers to the questions "Who is who?" and "Who is related to whom?" across an enterprise.

  * [Garphield](https://garphield.com/) -- an interactive network visualization and analysis workbench for human-sized graphs, which keeps graph data separate from the sources used to analyse, filter, and present it.


Data for the knowledge graph builds on:
<https://github.com/StephenAbbott/opencheck/releases/tag/dataset-azerbaijani-laundromat-2026-10-06>


## Disclaimer

Please note that the data used here may contain legitimate business
transactions, and that the presence of any name in this dataset does
not necessarily imply any intentional wrongdoing.


## Getting Started

To run the Jupyter notebook, first launch JupyterLab:

```bash
poetry run jupyter-lab
```

Then navigate in your browser to open the `occrp.ipynb` notebook.
Run each of the cells in the notebook to perform the analysis.


<details>
  <summary>License and Copyright</summary>
&nbsp;

Source code plus any logo, documentation, and coding examples have an
[MIT license](https://spdx.org/licenses/MIT.html) which is succinct
and simplifies use in commercial applications.

Unless otherwise noted, all other materials herein are Copyright © 2026 Senzing, Inc.

Datasets used are licensed by their respective data providers:

  - OpenCheck, [MIT License; Copyright (c) 2026 Stephen Abbott Pugh](https://github.com/StephenAbbott/opencheck?tab=License-1-ov-file); see `az/LICENSES.md` for the bundle of information about third-party data which is licensed per source
  - OCCRP, [Copyright (c) 2026 Journalism Development Network, Inc.](https://www.occrp.org/en/legal-notice)
  - UK gov, [OGLv3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

</details>
