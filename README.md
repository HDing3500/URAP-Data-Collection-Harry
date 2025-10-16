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
models.py :	Defines FilingMeta, ItemSections, and Snippet dataclasses used throughout the pipeline.

extractor.py	: Core logic for fetching filings, extracting Items 7 & 8, and filtering restructuring-related snippets.

main.py :	Example script showing how to run the extractor for a specific company and year.

### Unittest
sample_data : Datas we need to evaluate our code, test our model and get CIK (JSON, CSV, .txt)

test_clean_name 

test_get_cik 

test_get_file = check if we get the right 10k or not

test_get_item = check item 7 and 8

### Note

“The file data/company_tickers.json was downloaded from https://www.sec.gov/files/company_tickers.json
 on [DATE].”
