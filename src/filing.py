import requests
import re
import time
import pandas as pd

from dataclass import FilingMeta, ItemSections

# URLS
SEC_BASE = "https://data.sec.gov"
ARCHIVES_BASE = "https://www.sec.gov/Archives"

VALID_10K_FORMS = {"10-K", "10-K/A", "10-K405", "10-KT"}


class Extractor:
    def __init__(self, cik, timeout=30, max_retries=3, retry_sleep=0.5):
        self.header = {"User-Agent": "iamaudreylin@gmail.com"}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep
        self.cik = str(int(cik)).zfill(10)

    @staticmethod
    def clean_name(s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r'[,.\-&/]+', ' ', s)
        s = re.sub(
            r'\b(incorporated|inc|corp|corporation|co|ltd|plc|llc|holdings?|group)\b',
            '',
        )
        s = re.sub(r'\s+', ' ', s)
        return s.strip()

    def _get_with_retry(self, url: str):
        last_exc = None
        for _ in range(self.max_retries):
            try:
                r = requests.get(url, headers=self.header, timeout=self.timeout)
                r.raise_for_status()
                return r
            except requests.RequestException as e:
                last_exc = e
                time.sleep(self.retry_sleep)
        raise last_exc

    # ------------------------------
    # 1. Fetch Submissions
    # ------------------------------
    def get_submissions(self) -> dict:
        url = f"{SEC_BASE}/submissions/CIK{self.cik}.json"
        r = self._get_with_retry(url)
        return r.json()

    # ------------------------------
    # 2. Choose the 10-K (modern + old)
    # ------------------------------
    def choose_10k(self, company: str, submissions: dict, fiscal_year: int) -> FilingMeta | None:
        # Try modern recent filings first
        meta = self._choose_from_recent(company, submissions, fiscal_year)
        if meta:
            return meta

        # Fallback: try older filings ("files")
        return self._choose_from_older_files(company, submissions, fiscal_year)

    # ------------------------------
    # 2a. Choose from recent filings
    # ------------------------------
    def _choose_from_recent(self, company: str, submissions: dict, fiscal_year: int):
        recent = submissions.get("filings", {}).get("recent", {})

        forms = recent.get("form", [])
        accessions = recent.get("accessionNumber", [])
        primary_docs = recent.get("primaryDocument", [])
        report_dates = recent.get("reportDate", [])

        candidates = []

        for form, acc, doc, rdate in zip(forms, accessions, primary_docs, report_dates):
            if form not in VALID_10K_FORMS:
                continue
            if not rdate:
                continue

            try:
                year = int(str(rdate)[:4])
            except ValueError:
                continue

            if year != fiscal_year:
                continue

            candidates.append(
                self.build_meta(company, self.cik, fiscal_year, form, acc, doc, rdate)
            )

        # No match
        if not candidates:
            return None

        # Prefer plain '10-K' over amendments
        candidates.sort(key=lambda m: (m.form != "10-K", m.report_date))
        return candidates[0]

    # ------------------------------
    # 2b. Choose from older "files"
    # ------------------------------
    def _choose_from_older_files(self, company: str, submissions: dict, fiscal_year: int):
        files = submissions.get("filings", {}).get("files", [])
        if not files:
            return None

        all_candidates = []

        for f in files:
            name = f.get("name")
            if not name:
                continue

            # Example name: "CIK0000320193-2010.json"
            older_url = f"{SEC_BASE}/submissions/{name}"

            try:
                older_json = self._get_with_retry(older_url).json()
            except Exception:
                continue

            recent = older_json.get("filings", {}).get("recent", {})
            forms = recent.get("form", [])
            accessions = recent.get("accessionNumber", [])
            primary_docs = recent.get("primaryDocument", [])
            report_dates = recent.get("reportDate", [])

            for form, acc, doc, rdate in zip(forms, accessions, primary_docs, report_dates):
                if form not in VALID_10K_FORMS:
                    continue
                if not rdate:
                    continue

                try:
                    year = int(str(rdate)[:4])
                except ValueError:
                    continue

                if year != fiscal_year:
                    continue

                all_candidates.append(
                    self.build_meta(company, self.cik, fiscal_year, form, acc, doc, rdate)
                )

        if not all_candidates:
            return None

        all_candidates.sort(key=lambda m: (m.form != "10-K", m.report_date))
        return all_candidates[0]

    # ------------------------------
    # 3. Build Meta
    # ------------------------------
    @staticmethod
    def build_meta(company: str, cik: str, fiscal_year: int, form: str, accession: str,
                   primary_doc: str, report_date: str) -> FilingMeta:
        acc_nodash = accession.replace("-", "")
        url = f"{ARCHIVES_BASE}/edgar/data/{int(cik)}/{acc_nodash}/{primary_doc}"
        return FilingMeta(
            company=company,
            cik=cik,
            fiscal_year=fiscal_year,
            form=form,
            accession=accession,
            primary_doc=primary_doc,
            report_date=report_date or None,
            url=url,
        )

    # ------------------------------
    # 4. Fetch the actual document
    # ------------------------------
    def fetch_10k(self, meta: FilingMeta) -> str:
        r = self._get_with_retry(meta.url)
        return r.text
