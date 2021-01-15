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
    hoogte_eigenwoningforfait: float  # pure eigenwoningforfait (EWF) zonder te kijken naar HRA en wet Hillen
    belasting_voordeel: float  # hypotheekrenteaftrek (HRA) minus eigenwoningforfait (EWF)
    rente_netto: float
    woz_waarde: float
    belasting_nadeel: float  # eigenwoningforfait (EWF) minus hypotheekrenteaftrek (HRA) volgens wet Hillen
    onderhoudskosten: float
    extra_spaarinleg_per_maand: float
    lasten: float
    oude_huur: float
    voordeel_nu_kopen_ipv_altijd_huren: float
    voordeel_nu_kopen_ipv_voorlopig_huren: float
    gespaard_geld: float


MAANDELIJKSE_WAARDEN = ("aflossing", "rente", "hypotheek_rente_aftrek", "hoogte_eigenwoningforfait",
                        "belasting_voordeel", "rente_netto", "belasting_nadeel",
                        "onderhoudskosten", "extra_spaarinleg_per_maand", "lasten", "oude_huur")
MAANDELIJKSE_PLOT1 = ("aflossing", "rente_netto", "belasting_nadeel", "onderhoudskosten", "extra_spaarinleg_per_maand")
MAANDELIJKSE_PLOT2 = ("oude_huur",)
TOTALE_WAARDEN = ("restschuld", "voordeel_nu_kopen_ipv_altijd_huren", "voordeel_nu_kopen_ipv_voorlopig_huren",
                  "woz_waarde", "gespaard_geld")
