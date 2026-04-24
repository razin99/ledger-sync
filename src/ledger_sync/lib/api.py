import os
import niquests
import bs4

from .ledger_table import load_current_ledger_table, load_previous_ledger_table


class EbakiError(RuntimeError):
    pass


FAKE_ASS_HEADER_BRUH = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en-GB;q=0.9,en-MY;q=0.8,en;q=0.7,id;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Windowsx86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


class Ebaki:
    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password
        self.sess = niquests.Session(
            base_url="https://apps.mara.gov.my/ebakiv2/", headers=FAKE_ASS_HEADER_BRUH
        )
        self.sess.verify = os.path.join(
            os.path.dirname(__file__), "../ssl/_.mara.gov.pem"
        )

    def login(self):
        res = self.sess.get(url="_signIneBaki.aspx").raise_for_status()
        aspnet = self._get_aspnet_state(res.text or "")

        res = self.sess.post(
            url="_signIneBaki.aspx",
            data={
                **aspnet,
                "txtNoKP": self._username,
                "txtPwd": self._password,
                "__EVENTTARGET": "btnMasuk",
                "__EVENTARGUMENT": "",
                "myHField": "",
                "myHField2": "",
            },
        ).raise_for_status()

        res = self.sess.get("frmMainPeminjam.aspx").raise_for_status()
        tag = bs4.BeautifulSoup(res.text or "", "html.parser").select_one(
            "#MainContent_gvPenyata_HLInfo_0"
        )
        if not tag:
            raise EbakiError("Acc No not found on page")
        self._acc_no = tag.get_text().strip()

    def _assert_logged_in(self):
        if not self._acc_no:
            raise EbakiError("Not logged in, no account number detected")

    def current_year_ledger(self):
        self._assert_logged_in()
        res = self.sess.get(
            "frmPenyataAkaunTahunan.aspx", params={"AccNo": self._acc_no}
        ).raise_for_status()
        return load_current_ledger_table(res.text or "")

    def past_year_ledger(self, year: str):
        self._assert_logged_in()
        res = self.sess.get(
            "frmPrevLedger.aspx", params={"AccNo": self._acc_no}
        ).raise_for_status()
        aspnet = self._get_aspnet_state(res.text or "")
        res = self.sess.post(
            "frmPrevLedger.aspx",
            params={"AccNo": self._acc_no},
            data={
                **aspnet,
                "ctl00$MainContent$ddlThnPenyata": year,
                "ctl00$MainContent$BtnCariThn": "Papar",
            },
        ).raise_for_status()
        return load_previous_ledger_table(res.text or "")

    def _get_aspnet_state(self, html: str):
        soup = bs4.BeautifulSoup(html, "html.parser")
        elems = [t for t in soup.select("input[type=hidden]")]
        return {str(e["id"]): str(e.get("value") or "") for e in elems}
