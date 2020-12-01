"""Test met referentie gegevens van:
https://financieel.infonu.nl/hypotheek/102840-wat-zijn-de-voordelen-van-de-lineaire-hypotheek.html"""

from typing import NamedTuple

import pytest

import gegevens
from src import hypotheek


def test_bereken_rente_en_aflossing_linear() -> None:
    """Test voor de linearehypotheek: restschuld moet 0 zijn en aflossing constant."""
    class Gegevens(NamedTuple):
        """Simpele versie van het object in gegevens.py om zo andere waarden te kunnen zetten."""
        rente_vast_jaren: int = 30
        looptijd_hypotheek_jaren: int = 30
        hypotheek_vorm: gegevens.HypotheekVorm = gegevens.HypotheekVorm.Lineair
        hypotheek_rente_percentage: float = 4.75
        aflossingsvrij_deel: float = 0.0

    gegeven = Gegevens()
    originele_schuld: float = 115_000

    rest_schuld = originele_schuld
    totale_rente = 0.0
    for jaar in range(gegeven.looptijd_hypotheek_jaren):
        for _ in range(12):
            aflossing, rente, _ = hypotheek.bereken_aflossing_en_rente(gegeven, rest_schuld,  # type: ignore
                                                                       originele_schuld, jaar)
            rest_schuld -= aflossing
            totale_rente += rente
            assert aflossing == pytest.approx(319.44, abs=0.1)
    assert rest_schuld == pytest.approx(0.0, abs=0.1)
    assert totale_rente == pytest.approx(80428, abs=1)


def test_bereken_rente_en_aflossing_annuiteiten() -> None:
    """Test voor de annuiteitenhypotheek: restschuld moet 0 zijn en het totale maandbedrag constant."""
    class Gegevens(NamedTuple):
        """Simpele versie van het object in gegevens.py om zo andere waarden te kunnen zetten."""
        rente_vast_jaren: int = 30
        looptijd_hypotheek_jaren: int = 30
        hypotheek_vorm: gegevens.HypotheekVorm = gegevens.HypotheekVorm.Annuiteiten
        hypotheek_rente_percentage: float = 4.75
        aflossingsvrij_deel: float = 0.0

    gegeven = Gegevens()
    originele_schuld: float = 115_000

    rest_schuld = originele_schuld
    totale_rente = 0.0
    for jaar in range(gegeven.looptijd_hypotheek_jaren):
        for _ in range(12):
            aflossing, rente, _ = hypotheek.bereken_aflossing_en_rente(gegeven, rest_schuld,  # type: ignore
                                                                       originele_schuld, jaar)
            rest_schuld -= aflossing
            totale_rente += rente
            assert aflossing + rente == pytest.approx(592.90, abs=0.1)
    assert rest_schuld == pytest.approx(0.0, abs=0.1)
    assert totale_rente == pytest.approx(98464, abs=1)
