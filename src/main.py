from filing import Extract_Filing
from items import Extract_Restructure
from dataclass import FilingMeta
from bs4 import BeautifulSoup
import pandas as pd
import os

def main():
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATA_PATH = os.path.join(ROOT, "data", "sample_all.csv")
    
    df = pd.read_csv(DATA_PATH)
    
    print(int(df['cik'][0]))
    


if __name__ == "__main__":
    main()
