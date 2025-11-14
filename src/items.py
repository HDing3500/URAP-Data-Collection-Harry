# item_extractor.py
import re
from tempfile import template
from typing import Optional, Dict, List, Tuple, Set
from bs4 import BeautifulSoup, Tag
from dataclass import ItemSections


class Extract_Restructure:
    def __init__(self):
        pass
    
    #------------------- Helper Functions -----------------------###
    @staticmethod
    def _norm(s: str) -> str:
        s = (s or "").replace("\xa0", " ")
        s = re.sub(r"[\s–—\-:._]+", " ", s, flags=re.UNICODE)
        return s.strip()
    
    @staticmethod
    def stream_until_stop(start_tag):
        text_chunks = []
        
        for el in start_tag.next_elements:
             # Only work with tags (skip NavigableString etc.)
            if not isinstance(el, Tag):
                continue

            # Stop when we hit the next section heading
            t = el.get_text(" ", strip=True)
            if re.match(r"^\s*item\s*(7a|8|9)\b", t, re.I):
                break

            # Skip obvious non-content
            if el.name in ("script", "style"):
                continue

            # 1) Handle tables ONCE, and skip collecting their inner <p> separately
            if el.name == "table":
                for row in el.find_all("tr"):
                    cells = [
                        Extract_Restructure._norm(cell.get_text(" ", strip=True))
                        for cell in row.find_all(["td", "th"])
                    ]
                    if cells:
                        line = "\t".join(cells)
                        text_chunks.append(line)
                # continue so we don't also treat descendants as standalone blocks
                continue

            # 2) Handle paragraphs, but NOT those inside a table (avoid duplication)
            if el.name == "p" and not el.find_parent("table"):
                text_chunks.append(el.get_text(" ", strip=True))

            joined = "\n".join(text_chunks)
            return joined, len(joined)
    
    @staticmethod
    def find_real_item7(soup):
        candidates = []
        for b in soup.find_all(["b", "strong"]):
            txt = b.get_text(" ", strip=True)
            if re.match(r"^\s*item\s*7\b", txt, re.I):
                candidates.append(b)

        best_tag = None
        best_len = 0

        for tag in candidates:
            # skip TOC (Table Of Contents) entries
            if tag.find_parent(["ul", "ol", "table"]):
                continue

            # slice forward until 7A/8/9
            collected, n = Extract_Restructure.stream_until_stop(tag)
            if n > best_len:
                best_tag, best_len = tag, n
        return best_tag
    
    @staticmethod
    def find_real_item8(soup):
        candidates = []
        for b in soup.find_all(["b", "strong"]):
            txt = b.get_text(" ", strip=True)
            if re.match(r"^\s*item\s*8\b", txt, re.I):
                candidates.append(b)

        best_tag = None
        best_len = 0

        for tag in candidates:
            # skip TOC entries
            if tag.find_parent(["ul", "ol", "table"]):
                continue

            # slice forward until 7A/8/9
            collected, n = Extract_Restructure.stream_until_stop(tag)
            if n > best_len:
                best_tag, best_len = tag, n
        return best_tag
    ###-----------------------Helper functions end--------------------###
    
    
    def extract_items(self, html):
        #Take item 7 and 8 from the html document
        soup = BeautifulSoup(html, 'html.parser')

        item7_text, item7_count = Extract_Restructure.stream_until_stop(Extract_Restructure.find_real_item7(soup))
        item8_text, item8_count = Extract_Restructure.stream_until_stop(Extract_Restructure.find_real_item8(soup))

        return item7_text, item8_text
        
    def stream_blocks(self, meta : ItemSections):
        #Transform/Normalize item sections for simplicity (easier to analyze)
        
        None
    
    def score_block(self, block):
        #Give a score to a block based on relevancy to restructuring
        None
    
    def is_restructuring(self,block):
        #Determine if a block is about restructuring
        None
        
    def capture_hits(self, wanted_blocks):
        #Aggregate all relevant blocks within one section.
        None
    
    def merge_adjacent(self, blocks):
        #Merge adjacent blocks into one larger block.
        None
    
    def write_out(self, hits, filepath):
        #Write the extracted sections to an output file.
        None
        
    