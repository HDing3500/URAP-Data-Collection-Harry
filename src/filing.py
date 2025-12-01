import requests
import re
import time
import pandas as pd

from dataclass import FilingMeta

# Intance variables
SEC_BASE = "https://data.sec.gov"
ARCHIVES_BASE = "https://www.sec.gov/Archives"

VALID_10K_FORMS = {"10-K", "10-k"}


class Extract_Filing:
    def __init__(self, cik, fiscal_year, company, timeout=30, max_retries=3, retry_sleep=0.5):
        self.header = {"User-Agent": "iamaudreylin@gmail.com"}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep
        self.cik = str(int(cik)).zfill(10)
        self.fiscal_year = int(fiscal_year)
        self.company = str(company)
        

    def get_html(self) -> str | None:
        """Run the full pipeline to obtain the 10-K HTML for this CIK/fiscal year.

        Steps:
        - fetch submissions JSON
        - choose the appropriate 10-K metadata
        - fetch the HTML document

        Returns the document text on success or None when no candidate exists.
        Raises RequestException on network errors.
        """
        # 1) get submissions
        submissions = self.get_submissions()

        # 2) choose 10-K meta
        meta = self.choose_10k(submissions)
        if meta is None:
            # No 10-K found for requested fiscal year
            return None

        # 3) fetch HTML
        html = self.fetch_10k(meta)
        return html
        

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
    
    #call request with retry and timeout
    def request_web(self, url: str):
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
        r = self.request_web(url)
        return r.json()

    # ------------------------------
    # 2. Helper: collect 10-K candidates from a 'recent' block
    # ------------------------------
    def collect_10k(
        self,
        company: str,
        cik: str,
        fiscal_year: int,
        jsonFile: dict,
    ) -> list[FilingMeta]:
        forms = jsonFile.get("form", []) or []
        accessions = jsonFile.get("accessionNumber", []) or []
        primary_docs = jsonFile.get("primaryDocument", []) or []
        report_dates = jsonFile.get("reportDate", []) or []

        candidates: list[FilingMeta] = []

        for form, acc, doc, rdate in zip(forms, accessions, primary_docs, report_dates):
            if form not in VALID_10K_FORMS:
                continue
            if not rdate:
                continue

            rdate_str = str(rdate)

            # Extract the first 4 digits as a year
            m = re.match(r"(\d{4})", rdate_str)
            if not m:
                continue

            try:
                year = int(m.group(1))
            except ValueError:
                continue

            if year != fiscal_year:
                continue

            candidates.append(
                self.build_meta(company, cik, fiscal_year, form, acc, doc, rdate_str)
            )

        return candidates

    # ------------------------------
    # 3. Choose the 10-K (recent + older files)
    # ------------------------------
    def choose_10k(self, *args) -> FilingMeta | None:
        """Choose the 10-K filing.

        Calling conventions supported:
        - choose_10k(company, submissions, fiscal_year)
        - choose_10k(submissions)  # uses self.company/self.fiscal_year
        """
        if len(args) == 1:
            submissions = args[0]
            company = self.company
            fiscal_year = self.fiscal_year
        elif len(args) == 3:
            company, submissions, fiscal_year = args
        else:
            raise TypeError("choose_10k expects either (submissions) or (company, submissions, fiscal_year)")

        filings = submissions.get("filings", {}) or {}

        all_candidates: list[FilingMeta] = []

        # --- from main "recent" ---
        recent = filings.get("recent", {}) or {}
        all_candidates.extend(
            self.collect_10k(
                company, self.cik, fiscal_year, recent
            )
        )

        # --- from older "files" snapshots ---
        files = filings['files'] or []
        for f in files:
            name = f.get("name")
            if not name:
                continue

            older_url = f"{SEC_BASE}/submissions/{name}"

            try:
                older_json = self.request_web(older_url).json()
            except Exception:
                # swallow individual file errors; move on
                continue

            all_candidates.extend(
                self.collect_10k(
                    self.company, self.cik, self.fiscal_year, older_json
                )
            )

        if not all_candidates:
    # Collect available years for debugging
            available_years = set()

            # Examine main recent block
            recent_forms = recent.get("form", []) or []
            recent_rdates = recent.get("reportDate", []) or []
            for form, rdate in zip(recent_forms, recent_rdates):
                if form in VALID_10K_FORMS and rdate:
                    m = re.match(r"(\d{4})", str(rdate))
                    if m:
                        available_years.add(int(m.group(1)))

            # Examine older files
            for f in files:
                name = f.get("name")
                if not name:
                    continue
                older_url = f"{SEC_BASE}/submissions/{name}"
                try:
                    older_json = self.request_web(older_url).json()
                except:
                    continue
                older_recent = older_json.get("filings", {}).get("recent", {}) or {}
                o_forms = older_recent.get("form", []) or []
                o_rdates = older_recent.get("reportDate", []) or []
                for form, rdate in zip(o_forms, o_rdates):
                    if form in VALID_10K_FORMS and rdate:
                        m = re.match(r"(\d{4})", str(rdate))
                        if m:
                            available_years.add(int(m.group(1)))

            #Print debug message
            print(f"[DEBUG][CIK={self.cik}] No 10-K found for fiscal year {self.fiscal_year}.")
            if available_years:
                print(f"[DEBUG][CIK={self.cik}] Available 10-K years: {sorted(available_years)}")
                print(f"[DEBUG][CIK={self.cik}] Oldest 10-K year: {min(available_years)}")
                print(f"[DEBUG][CIK={self.cik}] Newest 10-K year: {max(available_years)}")
            else:
                print(f"[DEBUG][CIK={self.cik}] No 10-K filings found at all!")

            #No candidates found for the requested fiscal year — return None
            return None


        # Prefer plain '10-K' over amendments, then earliest report_date
        all_candidates.sort(key=lambda m: (m.form != "10-K", m.report_date))
        return all_candidates[0]

    # ------------------------------
    # 4. Build Meta
    # ------------------------------
    @staticmethod
    def build_meta(
        company: str,
        cik: str,
        fiscal_year: int,
        form: str,
        accession: str,
        primary_doc: str,
        report_date: str,
    ) -> FilingMeta:
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
    # 5. Fetch the actual document
    # ------------------------------
    def fetch_10k(self, meta: FilingMeta) -> str:
        r = self.request_web(meta.url)
        return r.text
    
    def debug_print_all_10ks(self, submissions: dict):
        """
        Debug helper: print all 10-K-like filings (form + reportDate)
        from both 'recent' and the older 'files' JSONs.
        """
        print(f"\n[DEBUG] CIK={self.cik}")

        filings = submissions.get("filings", {})

        # --- recent ---
        recent = filings.get("recent", {})
        forms = recent.get("form", [])
        report_dates = recent.get("reportDate", [])

        print("[DEBUG] Recent 10-K-like filings:")
        for f, rd in zip(forms, report_dates):
            if f and rd and f.startswith("10-K"):
                print(f"    form={f}, reportDate={rd}")

        files = filings.get("files", [])
        print(f"[DEBUG] Older files entries: {len(files)}")

        for file_info in files:
            name = file_info.get("name")
            if not name:
                continue

            older_url = f"{SEC_BASE}/submissions/{name}"
            print(f"[DEBUG]  Checking older file: {older_url}")

            try:
                older_json = requests.get(
                    older_url, headers=self.header, timeout=self.timeout
                ).json()
            except Exception as e:
                print(f"[DEBUG]   ERROR fetching older file: {e}")
                continue

            older_recent = older_json.get("filings", {}).get("recent", {})
            o_forms = older_recent.get("form", [])
            o_report_dates = older_recent.get("reportDate", [])

            for f, rd in zip(o_forms, o_report_dates):
                if f and rd and f.startswith("10-K"):
                    print(f"    (older) form={f}, reportDate={rd}")


