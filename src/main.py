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
    
    


if __name__ == "__main__":
    main()
