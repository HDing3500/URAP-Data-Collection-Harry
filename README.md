# Automating Data Collection
A Python project for extracting and analyzing restructuring-related disclosures from SEC 10-K filings.
This tool uses the EDGAR API to retrieve company filings, extract Item 7 (Management’s Discussion & Analysis) and Item 8 (Financial Statements), and filter for text specifically related to restructuring activities.

## 🚀 Project Goals

1.Automatically fetch 10-K filings from the SEC’s EDGAR database.

2.Parse and isolate Item 7 and Item 8 sections.

3.Identify sentences discussing restructuring, realignment, severance, and related activities.

4.Output structured snippets for later testing against manually collected datasets.

5.Serve as a foundation for an NLP model to evaluate disclosure accuracy and completeness.




IMPROVEMENT NEEDED NOT ALL TEST CASE WORK

If further work is to be done we need to set version control and redesign code in a OOP manner



Failed when there's more than one appearance of the subject title of item 7 


