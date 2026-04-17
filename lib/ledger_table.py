from typing import List, TypedDict
from datetime import date
import bs4


class MissingTableError(RuntimeError):
    pass


# 'Tarikh Transaksi', 'Kod Transaksi', 'Rujukan Dokumen', 'Debit', 'Kredit', 'Baki'
class LedgerData(TypedDict):
    tx_date: date
    tx_code: str
    doc_ref: str
    debit: float
    credit: float
    balance: float


def _get_currency_value(s: str):
    return float("".join(c for c in s if c.isdigit() or c == "."))


def _load_ledger_table(raw_data: str, query: str):
    soup = bs4.BeautifulSoup(raw_data, "html.parser")
    table = soup.select_one(query)
    if not table:
        raise MissingTableError("")
    result: List[LedgerData] = []

    # Skips the following:
    #  - table heading
    #  - prev-year closing balance
    rows = table.find_all("tr")[2:]

    cell_count = len(LedgerData.__annotations__.keys())
    for row in rows:
        cols = row.find_all("td")

        if len(cols) != cell_count:
            continue

        _tx_date, _tx_code, _doc_ref, _debit, _credit, _balance = [
            ele.text.strip() for ele in cols
        ]

        result.append(
            {
                "tx_date": date.strptime(_tx_date, "%d/%m/%Y"),
                "tx_code": _tx_code,
                "doc_ref": _doc_ref,
                "debit": _get_currency_value(_debit),
                "credit": _get_currency_value(_credit),
                "balance": _get_currency_value(_balance),
            }
        )
    return result


def load_previous_ledger_table(raw_data: str):
    return _load_ledger_table(raw_data, "table#MainContent_gvPreviousLejar")


def load_current_ledger_table(raw_data: str):
    return _load_ledger_table(raw_data, "table#MainContent_gvPenyata")
