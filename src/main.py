"""In deze module zitten de hoofd-functies van het programma"""
import math
from pathlib import Path
from typing import List

import gegevens
from src import belasting
from src import data
from src import hypotheek
from src import io
from src import plot


def exp_stijging(basis: float, stijging_jaarlijks: float, jaar: int) -> float:
    """Exponentiele stijging van een basis waarde per jaar, waarbij de stijging in procenten is uitgedrukt."""
    return basis * math.pow(1.0 + stijging_jaarlijks / 100.0, jaar)


def bereken_gegevens(gegeven: gegevens.Gegevens) -> List[data.MaandData]:
    """Alle gegevens worden in deze functie berekend. Het resultaat is een lijst van data per maand voor de duur van de
    hypotheek."""
    # pylint: disable=too-many-locals, too-many-statements

    # Kosten bij aanschaf (kosten koper plus meer)
    kosten_belasting = (gegeven.kk_belasting_percentage / 100.0) * gegeven.kosten_huis
    kosten_niet_aftrekbaar = gegeven.kosten_notaris + gegeven.kosten_makelaar + kosten_belasting + gegeven.kosten_overig
    kosten_aftrekbaar = (gegeven.kosten_hypotheek + gegeven.kosten_taxatie + gegeven.kosten_bouwkundig_rapport +
                         gegeven.kosten_overig_aftrekbaar)
    bel_voordeel_koop = (gegeven.hoogste_belasting_percentage_inkomen / 100.0) * kosten_aftrekbaar
    kosten_bruto = gegeven.kosten_huis + kosten_niet_aftrekbaar + kosten_aftrekbaar
    kosten_netto = kosten_bruto - bel_voordeel_koop

    # Hypotheek gegevens
    hypotheek_schuld = kosten_bruto - gegeven.eigen_inleg

    # Check voor valide input
    if gegeven.eigen_inleg < kosten_niet_aftrekbaar:
        raise RuntimeError(f"De eigen inleg moet minstens de kosten koper a {kosten_niet_aftrekbaar:0.2f} euro zijn")

    # Overzichtje van de gegevens en daaruit afgeleidde data
    print("*----------------- AANKOOP --------------*")
    print(f"*         Huisprijs: {gegeven.kosten_huis:7.0f} euro        *")
    print(f"*         Belasting: {kosten_belasting:7.0f} euro ({gegeven.kk_belasting_percentage:.1f}%) *")
    print(f"*           Notaris: {gegeven.kosten_notaris:7.0f} euro        *")
    print(f"*          Makelaar: {gegeven.kosten_makelaar:7.0f} euro        *")
    print(f"*         Hypotheek: {gegeven.kosten_hypotheek:7.0f} euro        *")
    print(f"*           Taxatie: {gegeven.kosten_taxatie:7.0f} euro        *")
    print(f"*     Bouwk.rapport: {gegeven.kosten_bouwkundig_rapport:7.0f} euro        *")
    print(f"*           Overige: {gegeven.kosten_overig + gegeven.kosten_overig_aftrekbaar:7.0f} euro        *")
    print("*                    ------- +           *")
    print(f"*             Bruto: {kosten_bruto:7.0f} euro ({((kosten_bruto / gegeven.kosten_huis) - 1) * 100:4.1f}%)*")
    print(f"* Belastingvoordeel: {bel_voordeel_koop:7.0f} euro        *")
    print("*                    ------- +           *")
    print(f"*             Netto: {kosten_netto:7.0f} euro ({((kosten_netto / gegeven.kosten_huis) - 1) * 100:4.1f}%)*")
    print("*----------------------------------------*")
    print("") # 400 * (1 + x) = 410 =----> x = 410 / 400 - 1
    print("*----------------- HYPOTHEEK ------------*")
    print(f"*              Vorm: {gegeven.hypotheek_vorm.value:20s}*")
    print(f"*          Looptijd: {gegeven.looptijd_hypotheek_jaren:2.0f} jaar             *")
    print(f"*          Rente #1: {gegeven.hypotheek_rente_percentage:4.2f}% (tot {gegeven.rente_vast_jaren} jaar) *")
    print(f"*          Rente #2: {gegeven.rente_percentage_nadien:4.2f}% (na {gegeven.rente_vast_jaren} jaar)  *")
    if gegeven.aflossingsvrij_deel != 0.0:
        print(f"*    Aflossingsvrij: {gegeven.aflossingsvrij_deel:4.2f}% a {gegeven.rente_percentage_aflossingsvrij:4.2f}% rente *")  # pylint: disable=line-too-long
    print("*                                        *")
    print(f"*      Bruto kosten: {kosten_bruto:7.0f} euro        *")
    print(f"*       Eigen inleg: {gegeven.eigen_inleg:7.0f} euro        *")
    print("*                    ------- -           *")
    print(f"*         Hypotheek: {hypotheek_schuld:7.0f} euro        *")
    print("*----------------------------------------*")

    # Loop over alle maanden tot de aflossing nul is
    alle_data = []
    rest_schuld = hypotheek_schuld
    voordeel_kopen_ipv_huren = 0.0
    for jaar in range(gegeven.looptijd_hypotheek_jaren):
        for maand in range(12):

            # Bereken de nieuwe data voor deze maand
            aflossing, rente = hypotheek.bereken_aflossing_en_rente(gegeven, rest_schuld, hypotheek_schuld, jaar)
            rest_schuld = rest_schuld - aflossing
            hypotheek_rente_aftrek = belasting.bereken_hra(gegeven, rente, jaar)
            woz_waarde = exp_stijging(gegeven.woz_waarde, gegeven.woz_stijging_jaarlijks_percentage, jaar)
            eigenwoningforfait_belasting = belasting.bereken_ewf(gegeven, woz_waarde, jaar)
            onderhoud = exp_stijging(gegeven.onderhoud_per_maand, gegeven.inflatie_jaarlijks_percentage, jaar)
            rente_netto = rente - hypotheek_rente_aftrek
            kosten_zonder_aflossing = rente_netto + eigenwoningforfait_belasting + onderhoud

            # Verschil ten opzichte van huren
            oude_huur = exp_stijging(gegeven.huur_per_maand, gegeven.huurstijging_jaarlijks_percentage, jaar)
            voordeel_kopen_ipv_huren += oude_huur - kosten_zonder_aflossing
            eenmalige_kosten_kopen = kosten_niet_aftrekbaar + kosten_aftrekbaar - bel_voordeel_koop

            # Sla de data op
            alle_data.append(data.MaandData(
                jaar=jaar,
                maand=maand,
                aflossing=aflossing,
                restschuld=rest_schuld,
                rente=rente,
                hypotheek_rente_aftrek=hypotheek_rente_aftrek,
                rente_netto=rente_netto,
                woz_waarde=woz_waarde,
                eigenwoningforfait_belasting=eigenwoningforfait_belasting,
                onderhoudskosten=onderhoud,
                lasten=kosten_zonder_aflossing + aflossing,
                oude_huur=oude_huur,
                voordeel_nu_kopen_ipv_voorlopig_huren=voordeel_kopen_ipv_huren,
                voordeel_nu_kopen_ipv_altijd_huren=voordeel_kopen_ipv_huren - eenmalige_kosten_kopen,
            ))

    # Overzichtje van gegevens achteraf
    print("")
    print(f"*----------------- NA {gegeven.looptijd_hypotheek_jaren} JAAR -----------*")
    print(f"*            Restschuld: {math.ceil(alle_data[-1].restschuld):7.0f} euro    *")
    print("*                                        *")
    print(f"*  Betaalde rente bruto: {sum(d.rente for d in alle_data):7.0f} euro    *")
    print(f"*            Totaal HRA: {sum(d.hypotheek_rente_aftrek for d in alle_data):7.0f} euro    *")
    print("*                        ------- -       *")
    print(f"*  Betaalde rente netto: {sum(d.rente_netto for d in alle_data):7.0f} euro    *")
    print("*----------------------------------------*")
    return alle_data


def main() -> None:
    """De hoofdfunctie met de logica van het programma op hoog niveau."""
    gegeven = gegevens.Gegevens()

    # Bereken alle data
    alle_data = bereken_gegevens(gegeven)

    # Sla alle data op als CSV
    csv_bestand = Path("hkp.csv")
    io.schrijf_naar_csv(alle_data, csv_bestand)

    # En plot de gegevens
    plot_bestand = Path("hkp.png")
    plot.plot(alle_data, plot_bestand, plot_jaren=gegeven.looptijd_hypotheek_jaren)

    # Einde van het programma
    print("")
    print("*------------------- OUTPUT -------------*")
    print(f"*     Alle data als CSV: {str(csv_bestand):15s} *")
    print(f"*      Data als grafiek: {str(plot_bestand):15s} *")
    print("*----------------------------------------*")
