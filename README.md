# Automating Data Collection
A Python project for extracting and analyzing restructuring-related disclosures from SEC 10-K filings.
This tool uses the EDGAR API to retrieve company filings, extract Item 7 (Management’s Discussion & Analysis) and Item 8 (Financial Statements), and filter for text specifically related to restructuring activities.

## 🚀 Project Goals

1.Automatically fetch 10-K filings from the SEC’s EDGAR database.

2.Parse and isolate Item 7 and Item 8 sections.

3.Identify sentences discussing restructuring, realignment, severance, and related activities.

4.Output structured snippets for later testing against manually collected datasets.

5.Serve as a foundation for an NLP model to evaluate disclosure accuracy and completeness.

## Workflow
1. Retrieve meta data from submission file

2. Fetch 10-k and locate item 7 and 8

3. Pick out restructuring information from item 7 and 8
   
4. Feed to LLM then generate answers

## Classes

### Extractor
dataclasses.py :	Defines FilingMeta, ItemSections, and Snippet dataclasses used throughout the pipeline.

Extract_File.py	: 
1. For each CIK 

Extract_Items.py : Fetch item 7 & 8 and extract the information we need

main.py :	To pilot test the code

### Unittest
#### Core Idea --> Be able to check that the code can run through all 20,000 companies and get the right information.

sample_data : Datas we need to evaluate our code, test our model and get CIK (JSON, CSV, .txt)

test_clean_name 

test_get_cik 

test_get_file = check if we get the right 10k or not, also test it using 20,000 sample.

test_get_item = check item 7 and 8

### Note

“The file data/company_tickers.json was downloaded from https://www.sec.gov/files/company_tickers.json
 on [DATE].”
