"""Functies met betrekking tot de belastingdienst: zowel belastingen als teruggaves."""
from typing import Tuple

import gegevens


def bereken_hra(gegeven: gegevens.Gegevens, maand_rente: float, jaar: int) -> float:
    """De hypotheekrenteaftrek (HRA): Aftrek op het inkomen bij betaling van rente. De gebruikte gegevens komen van:
    https://www.eigenhuis.nl/hypotheken/verhuizen-naar-een-volgende-woning/hypotheekrenteaftrek#/"""
    maximum_aftrek = {2019: 0.49, 2020: 0.46, 2021: 0.43, 2022: 0.40, 2023: 0.371}  # verder blijft dit op 37.1%
    huidig_jaar = gegeven.aankoopjaar + jaar
    aftrek_percentage = maximum_aftrek.get(huidig_jaar, 0.371)
    aftrek_percentage = min(aftrek_percentage, (gegeven.hoogste_belasting_percentage_inkomen / 100.0))
    aftrek = maand_rente * aftrek_percentage
    return aftrek


def bereken_ewf(gegeven: gegevens.Gegevens, woz_waarde: float, jaar: int) -> float:
    """Het Eigenwoningforfait (EWF): Belasting te betalen als eigenaar van een woning. De gebruikte gegevens komen van:
    https://nl.wikipedia.org/wiki/Eigenwoningforfait"""
    ewf_percentage = {2019: 0.0065, 2020: 0.0060, 2021: 0.0050, 2022: 0.0050, 2023: 0.0045}  # verder op 0.45%
    huidig_jaar = gegeven.aankoopjaar + jaar
    ewf = (ewf_percentage.get(huidig_jaar, 0.0045) * woz_waarde) / 12.0
    ewf_belasting = ewf * (gegeven.hoogste_belasting_percentage_inkomen / 100.0)
    return ewf_belasting


def bereken(gegeven: gegevens.Gegevens, hypotheek_rente_aftrek: float, eigenwoningforfait: float,
            jaar: int) -> Tuple[float, float]:
    """Bereken het totale belastingvoordeel (HRA) en nadeel (EWF). Het voordeel is de HRA minus de EWF als dit niet
    negatief is. Als de EWF hoger is dan de HRA, dan was er vroeger netto geen effect. Echter met de wet Hillen is er
    sinds 2019 in stapjes elk jaar steeds meer EWF te betalen. Zie voor meer informatie:
    https://www.consumentenbond.nl/hypotheek/starter/eigenwoningforfait
    Deze functie retourneerd twee getallen (belasting voordeel, belasting nadeel), waarvan er 1 altijd 0 is. De ander is
    de te betalen of te ontvangen belasting."""

    # Meer HRA dan EWF: belastingvoordeel
    if hypotheek_rente_aftrek >= eigenwoningforfait:
        return hypotheek_rente_aftrek - eigenwoningforfait, 0

    # Meer EWF dan HRA en wet Hillen nog niet in werking: geen nadeel, geen voordeel
    huidig_jaar = gegeven.aankoopjaar + jaar
    if huidig_jaar <= 2019:
        return 0, 0

    # Meer EWF dan HRA en wet Hillen in werken: belastingnadeel
    if huidig_jaar > 2049:  # EWF is vanaf nu gewoon te betalen
        return 0, eigenwoningforfait - hypotheek_rente_aftrek
    jaar_sinds_2019 = huidig_jaar - 2019
    return 0, (eigenwoningforfait - hypotheek_rente_aftrek) * (jaar_sinds_2019 * (1 / 30))
