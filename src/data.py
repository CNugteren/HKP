"""In deze module worden de data-structuren gedefinieerd."""
from typing import NamedTuple


class MaandData(NamedTuple):
    """Hierin zitten alle berekende waarden voor een bepaalde maand"""
    jaar: int
    maand: int
    aflossing: float
    restschuld: float
    rente: float
    hypotheek_rente_aftrek: float
    rente_netto: float
    woz_waarde: float
    eigenwoningforfait_belasting: float
    onderhoudskosten: float
    lasten: float
    oude_huur: float
    voordeel_nu_kopen_ipv_altijd_huren: float
    voordeel_nu_kopen_ipv_voorlopig_huren: float


MAANDELIJKSE_WAARDEN = ("aflossing", "rente", "hypotheek_rente_aftrek", "rente_netto",
                        "eigenwoningforfait_belasting", "onderhoudskosten", "lasten", "oude_huur")
MAANDELIJKSE_PLOT1 = ("aflossing", "rente_netto", "eigenwoningforfait_belasting", "onderhoudskosten")
MAANDELIJKSE_PLOT2 = ("oude_huur",)
TOTALE_WAARDEN = ("restschuld", "voordeel_nu_kopen_ipv_altijd_huren", "voordeel_nu_kopen_ipv_voorlopig_huren",
                  "woz_waarde")
