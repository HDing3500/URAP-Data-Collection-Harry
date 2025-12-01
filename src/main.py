from filing import Extract_Filing
from items import Extract_Restructure
from dataclass import FilingMeta
from bs4 import BeautifulSoup
import pandas as pd
import os

def main():
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATA_PATH = os.path.join(ROOT, "data", "sample_all.csv")
    

    filing = Extract_Filing("0000001750", fiscal_year=2019, company="AIR")
    item = Extract_Restructure()
    html = filing.get_html()
    
    print(item.get_restructure(html))
    
    # Separate item 7 and 8 restructure blocks
    # Write out 2 .txt files with a name gvkey_fyear_item7.txt and gvkey_fyear_item8.txt
    # Test out end to end process with a couple of rows from sample_all.csv
    # Add case when item 8 is on a different page
    
    
    


if __name__ == "__main__":
    main()
