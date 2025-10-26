# item_extractor.py
import re
from tempfile import template
from typing import Optional, Dict, List, Tuple, Set
from bs4 import BeautifulSoup, Tag
from dataclass import ItemSections


class Extract_Restructure:
    def __init__(self):
        pass
    
    #Helper functions
    @staticmethod
    def _norm(s: str) -> str:
        s = (s or "").replace("\xa0", " ")
        s = re.sub(r"[\s–—\-:._]+", " ", s, flags=re.UNICODE)
        return s.strip()
    
    @staticmethod
    def stream_until_stop(start_tag):
        text_chunks = []
        
        for el in start_tag.next_elements:
            if isinstance(el, Tag):
                t = el.get_text(" ", strip=True)
                if re.match(r"^\s*item\s*(7a|8|9)\b", t, re.I):
                    break
            if isinstance(el, Tag) and el.name == "p":
                text_chunks.append(el.get_text(" ", strip=True))
            if el.name == "table":
                for row in el.find_all("tr"):
                    cells = [Extract_Restructure._norm(cell.get_text(" ", strip=True)) for cell in row.find_all(["td","th"])]
                    if cells:
                        line = "\t".join(cells)
                        text_chunks.append(line)

        joined = "\n".join(text_chunks)
        return joined, len(joined)
    
    @staticmethod
    def find_real_item7(soup):
        item7_candidates = []
        for b in soup.find_all(["b", "strong"]):
            txt = b.get_text(" ", strip=True)
            if re.match(r"^\s*item\s*7\b", txt, re.I):
                item7_candidates.append(b)

        best_tag = None
        best_len = 0

        for tag in item7_candidates:
            # skip TOC entries
            if tag.find_parent(["ul", "ol", "table"]):
                continue

            # slice forward until 7A/8/9
            collected, n = Extract_Restructure.stream_until_stop(tag)
            if n > best_len:
                best_tag, best_len = tag, n
        return best_tag
    
    
    def extract_items(self, html):
        #Take item 7 and 8 from the html document
        soup = BeautifulSoup(html, 'html.parser')

        item7_text, item7_count = Extract_Restructure.stream_until_stop(Extract_Restructure.find_real_item7(soup))


        None
        
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
        
    ### ---- Helper Functions ---- ###
    def _looks_like_item7_full_title(self, text: str) -> bool:
    
        t = self._norm(text).lower()

        # Replace common separators with a single hyphen for normalization
        t = re.sub(r"[–—\-:]+", "-", t)  # em/en dash/colon/hyphen -> "-"
        # Collapse multiple spaces
        t = re.sub(r"\s+", " ", t).strip()

        # Build a simple normalized template to compare against
        template = (
            r"item.+7.+management'?s? discussion and analysis of financial condition (and|&) results of operations"
        )
        return bool(re.match(template, t, re.I))

    def _visual_weight(self, tag: Tag) -> float:
        """
        Estimate 'visual weight' of a tag:
        - heading level gets a base weight
        - bold adds weight
        - inline font-size (px/pt) adds proportional weight
        """
        weight = 0.0

        # Heading level (h1 > h6)
        if tag.name and re.match(r"^h[1-6]$", tag.name, re.I):
            lvl = int(tag.name[1])
            weight += (7 - lvl) * 2.0  # h1=12, h2=10, ... h6=2

        # Boldness
        if self._is_visibly_bold(tag):
            weight += 3.0

        # Inline font-size if present
        style = (tag.get("style") or "").lower()
        m = re.search(r"font-size\s*:\s*([0-9.]+)\s*(px|pt|em|rem)", style)
        if m:
            size_val = float(m.group(1))
            # Convert roughly to a comparable bump; px dominant in EDGAR HTML
            if m.group(2) == "px":
                weight += min(size_val / 4.0, 8.0)  # cap contribution
            elif m.group(2) == "pt":
                weight += min(size_val / 3.0, 8.0)
            else:
                weight += 4.0  # crude bump for em/rem

        return weight

    def _full_title_item7_candidates(self, soup: BeautifulSoup) -> List[Tag]:
        """
        Find nodes whose rendered text looks like the full Item 7 title.
        We check common block tags; descendants' text is concatenated by get_text().
        """
        cands: List[Tag] = []
        for tag in soup.find_all(BLOCK_TAGS):
            txt = tag.get_text(" ", strip=True)
            if not txt:
                continue
            if self._looks_like_item7_full_title(txt):
                cands.append(tag)
        return cands

    def _pick_best_by_visual_weight(self, nodes: List[Tag]) -> Optional[Tag]:
        """
        Choose the visually 'heaviest' node among candidates.
        """
        best, best_w = None, float("-inf")
        for n in nodes:
            w = self._visual_weight(n)
            if w > best_w:
                best, best_w = n, w
        return best
