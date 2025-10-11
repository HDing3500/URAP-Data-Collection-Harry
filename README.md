# Automating Data Collection
A Python project for extracting and analyzing restructuring-related disclosures from SEC 10-K filings.
This tool uses the EDGAR API to retrieve company filings, extract Item 7 (Management’s Discussion & Analysis) and Item 8 (Financial Statements), and filter for text specifically related to restructuring activities.

## 🚀 Project Goals

1.Automatically fetch 10-K filings from the SEC’s EDGAR database.

2.Parse and isolate Item 7 and Item 8 sections.

3.Identify sentences discussing restructuring, realignment, severance, and related activities.

4.Output structured snippets for later testing against manually collected datasets.

5.Serve as a foundation for an NLP model to evaluate disclosure accuracy and completeness.

models.py :	Defines FilingMeta, ItemSections, and Snippet dataclasses used throughout the pipeline./n
extractor.py	: Core logic for fetching filings, extracting Items 7 & 8, and filtering restructuring-related snippets.
main.py :	Example script showing how to run the extractor for a specific company and year.
utils.py :	Helper functions (e.g., cleaning company names, retry logic).

