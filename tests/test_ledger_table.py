from datetime import date
from ledger_sync.lib.ledger_table import (
    MissingTableError,
    load_current_ledger_table,
    load_previous_ledger_table,
)
import pytest


def test_valid_html_prev():
    data = load_previous_ledger_table("""
<table id="MainContent_gvPreviousLejar">
	<tr style="color:#FFFFCC;background-color:#990000;font-weight:bold;">
		<th scope="col">Tarikh Transaksi</th><th scope="col">Kod Transaksi</th><th scope="col">Rujukan Dokumen</th><th scope="col">Debit</th><th scope="col">Kredit</th><th scope="col">Baki</th>
	</tr><tr style="color:#330099;background-color:White;">
		<td align="center">
                        <span id="MainContent_gvPreviousLejar_Label1_0">01/12/2024</span>
                    </td><td align="center">
                        <span id="MainContent_gvPreviousLejar_Label2_0"></span>
                    </td><td align="center">
                        <span id="MainContent_gvPreviousLejar_Label4_0">Baki B/K</span>
                    </td><td align="right">&nbsp;</td><td align="right">&nbsp;</td><td align="right">RM 120,421.44</td>
	</tr><tr style="color:#330099;background-color:White;">
		<td align="center">
                        <span id="MainContent_gvPreviousLejar_Label1_1">16/11/2018</span>
                    </td><td align="center">
                        <span id="MainContent_gvPreviousLejar_Label2_1">DLYD</span>
                    </td><td align="center">
                        <span id="MainContent_gvPreviousLejar_Label4_1">90013444  </span>
                    </td><td align="right">RM 3,212.39</td><td align="right">(RM 0.00)</td><td align="right">RM 122,683.83</td>
	</tr><tr style="color:#330099;background-color:White;">
		<td align="center">
                        <span id="MainContent_gvPreviousLejar_Label1_2">14/01/2025</span>
                    </td><td align="center">
                        <span id="MainContent_gvPreviousLejar_Label2_2">KA  </span>
                    </td><td align="center">
                        <span id="MainContent_gvPreviousLejar_Label4_2">  000000  </span>
                    </td><td align="right">RM 0.00</td><td align="right">(RM 100.00)</td><td align="right">RM 120,321.44</td>
	</tr>
</table>""")
    assert data[0]["tx_code"] == "DLYD"
    assert data[1]["credit"] == float(100.00)
    assert data[1]["debit"] == float(0.00)
    assert data[1]["tx_date"] == date(2025, 1, 14)


def test_invalid_html_prev():
    with pytest.raises(MissingTableError):
        load_previous_ledger_table("<table></table>")


def test_valid_html_curr():
    data = load_current_ledger_table("""
<table id="MainContent_gvPenyata">
	<tr style="color:#FFFFCC;background-color:#990000;font-weight:bold;">
		<th scope="col">Tarikh Transaksi</th><th scope="col">Kod Transaksi</th><th scope="col">Rujukan Dokumen</th><th scope="col">Debit</th><th scope="col">Kredit</th><th scope="col">Baki</th>
	</tr><tr style="color:#330099;background-color:White;">
		<td align="center">
                        <span id="MainContent_gvPenyata_Label1_0">01/12/2024</span>
                    </td><td align="center">
                        <span id="MainContent_gvPenyata_Label2_0"></span>
                    </td><td align="center">
                        <span id="MainContent_gvPenyata_Label4_0">Baki B/K</span>
                    </td><td align="right">&nbsp;</td><td align="right">&nbsp;</td><td align="right">RM 120,421.44</td>
	</tr><tr style="color:#330099;background-color:White;">
		<td align="center">
                        <span id="MainContent_gvPenyata_Label1_1">16/11/2018</span>
                    </td><td align="center">
                        <span id="MainContent_gvPenyata_Label2_1">DLYD</span>
                    </td><td align="center">
                        <span id="MainContent_gvPenyata_Label4_1">90013444  </span>
                    </td><td align="right">RM 3,212.39</td><td align="right">(RM 0.00)</td><td align="right">RM 122,683.83</td>
	</tr><tr style="color:#330099;background-color:White;">
		<td align="center">
                        <span id="MainContent_gvPenyata_Label1_2">14/01/2025</span>
                    </td><td align="center">
                        <span id="MainContent_gvPenyata_Label2_2">KA  </span>
                    </td><td align="center">
                        <span id="MainContent_gvPenyata_Label4_2">  000000  </span>
                    </td><td align="right">RM 0.00</td><td align="right">(RM 100.00)</td><td align="right">RM 120,321.44</td>
	</tr>
</table>""")
    assert data[0]["tx_code"] == "DLYD"
    assert data[1]["credit"] == float(100.00)
    assert data[1]["debit"] == float(0.00)
    assert data[1]["tx_date"] == date(2025, 1, 14)


def test_invalid_html_curr():
    with pytest.raises(MissingTableError):
        load_current_ledger_table("<table></table>")
