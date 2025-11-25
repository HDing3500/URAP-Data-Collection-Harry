# Automating Data Collection
A Python project for extracting and analyzing restructuring-related disclosures from SEC 10-K filings.
This tool uses the EDGAR API to retrieve company filings, extract Item 7 (Management’s Discussion & Analysis) and Item 8 (Financial Statements), and filter for text specifically related to restructuring activities.

## 🚀 Project Goals

1.Automatically fetch 10-K filings from the SEC’s EDGAR database.

2.Parse and isolate Item 7 and Item 8 sections.

3.Identify sentences discussing restructuring, realignment, severance, and related activities.

4.Output structured snippets for later testing against manually collected datasets.

5.Serve as a foundation for an NLP model to evaluate disclosure accuracy and completeness.

## Steps
1. Get the CIK by using the CSV that contains the ticker and using the JSON well map out all the cik

2. Locate the 10k url location

3. Get item 7 and 8 and save it in text form
   
4. Filter out restructuring-related information

## Classes

### Extractor
dataclasses.py :	Defines FilingMeta, ItemSections, and Snippet dataclasses used throughout the pipeline.

Extract_File.py	: Fetch the 10k File

Extract_Items.py : Fetch item 7 & 8 and extract the information we need

main.py :	To pilot test the code

