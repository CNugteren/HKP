"""Functies met betrekking tot de hypotheek"""
import math
from typing import Tuple

import gegevens


def bereken_aflossing_en_rente(gegeven: gegevens.Gegevens, rest_schuld: float, originele_schuld: float,
                               jaar: int) -> Tuple[float, float, float]:
    """Berekent de aflossing en rente voor een bepaald moment gegeven de originele schuld, de huidige schuld, en alle
    hypotheekgegevens. Het resultaat is een 3-tuple met de aflossing, aftrekbare rente, en de niet aftrekbare rente."""

    rente_percentage = gegeven.hypotheek_rente_percentage
    if jaar >= gegeven.rente_vast_jaren:
        rente_percentage = gegeven.rente_percentage_nadien

    maand_rente = math.pow(1 + (rente_percentage / 100.0), 1/12.0) - 1

    # Indien een deel aflossingsvrij is
    niet_aftrekbare_rente = 0.0
    if gegeven.aflossingsvrij_deel > 0.0:
        niet_aftrekbare_rente = (gegeven.aflossingsvrij_deel / 100.0) * rest_schuld * maand_rente
        originele_schuld = (1.0 - gegeven.aflossingsvrij_deel / 100.0) * originele_schuld
        rest_schuld = (1.0 - gegeven.aflossingsvrij_deel / 100.0) * rest_schuld

    # Hypotheekvorm: linear
    if gegeven.hypotheek_vorm == gegevens.HypotheekVorm.Lineair:
        aflossing = (originele_schuld / gegeven.looptijd_hypotheek_jaren) / 12.0
        rente = rest_schuld * maand_rente
        return aflossing, rente, niet_aftrekbare_rente

    # Hypotheekvorm: annuiteiten
    if gegeven.hypotheek_vorm == gegevens.HypotheekVorm.Annuiteiten:
        looptijd_hypotheek_maanden = gegeven.looptijd_hypotheek_jaren * 12
        maand_lasten = originele_schuld * maand_rente / (1 - math.pow(1 + maand_rente, -looptijd_hypotheek_maanden))
        rente = rest_schuld * maand_rente
        aflossing = maand_lasten - rente
        return aflossing, rente, niet_aftrekbare_rente

    # Hypotheekvorm: aflossingsvrij
    if gegeven.hypotheek_vorm == gegevens.HypotheekVorm.Aflossingsvrij:
        aflossing = 0
        niet_aftrekbare_rente = rest_schuld * maand_rente
        return aflossing, 0, niet_aftrekbare_rente

    raise NotImplementedError(f"De hypotheek vorm '{gegeven.hypotheek_vorm}' wordt niet ondersteund")
