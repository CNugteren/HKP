"""Deze module bevat de 'input' van de gebruiker: alle gegevens die nodig zijn voor de berekening"""
from enum import Enum
from typing import NamedTuple


class HypotheekVorm(Enum):
    """Type hypotheek die door deze software ondersteund worden."""
    Lineair = "Lineairehypotheek"
    Annuiteiten = "Annuïteitenhypotheek"
    Aflossingsvrij = "Aflossingsvrij"


class Gegevens(NamedTuple):
    """In dit object zitten alle gegevens die als gebruikers-input gezien worden en dus aanbasbaar zijn. Het is in twee
    secties opgesplits: een eerste sectie met waarden die vrijwel zeker aangepast worden en een tweede sectie waarin
    waarden staan die al een redelijke waarde hebben maar aangepast worden voor een nauwkeurige berekening."""
    # ------------------------------------------------------------------------------------------------------------------
    # Alles in deze eerste sectie moet veranderd worden naar de situatie, dit zijn slechts voorbeelden
    # ------------------------------------------------------------------------------------------------------------------

    # De kosten voor de aankoop van het huis in euro, bijvoorbeeld de vraagprijs op Funda of het geboden bedrag
    kosten_huis: float = 400_000

    # De hoeveelheid eigen inleg in euro om de aanschaf te financieren. Dit is inclusief de kosten koper en andere
    # aanschafkosten. Dit bedrag moet minstens die kosten bedragen, omdat een hypotheek maar op 100% van de taxatitie-
    # waarde afgesloten mag worden. Overwaarde van een vorige woning mag hier ook bij opgeteld worden.
    eigen_inleg: float = 50_000

    # Hier kan de hypotheekvorm gekozen worden (zie hierboven voor de opties onder 'HypotheekVorm') en de initiele
    # rente gezet worden. De rente is afhankelijk van de bank, maar ook van de hoogte van de financiering en looptijd en
    # of er wel of geen NHG is. Zie hier om een idee te krijgen wat een goede schatting voor de rente is:
    # https://www.ing.nl/particulier/hypotheken/actuele-hypotheekrente/index.html
    hypotheek_vorm: HypotheekVorm = HypotheekVorm.Annuiteiten
    hypotheek_rente_percentage: float = 1.45

    # Dit is het hoogste belastingpercentage wat je nu betaalt op je inkomen. Dat zal meestal of 37 of 49 procent zijn.
    # Dit wordt gebruikt om bijvoorbeeld de HRA en eigenwoningforfait te berekenen.
    hoogste_belasting_percentage_inkomen: float = 49.5

    # Om een schatting te kunnen maken wat het voordeel is ten opzichte van huren, is het mogelijk om hier de huidige
    # huur per maand in euro inclusief servicekosten te specifieren. Dit kan op 0 gezet worden indien dit niet van
    # toepassing is.
    huur_per_maand: float = 1100

    # ------------------------------------------------------------------------------------------------------------------
    # Alles hieronder kan aangepast worden naar de situatie maar is meestal al een typische waarde of goede schatting
    # ------------------------------------------------------------------------------------------------------------------

    # Voor een aantal regelingen (HRA, eigenwoningforfait) veranderen de gegevens per jaar. Dit moet minimaal 2019 zijn.
    aankoopjaar: int = 2021

    # Het belastingpercentage wat betaald wordt over de kosten van het huis (deel van de kosten-koper). Dit kan
    # bijvoorbeeld 8% zijn (niet eigen bewoning), 2% (eigen bewoning), 0% (starters of V.O.N.).
    kk_belasting_percentage: float = 2.0

    # Dit zijn de extra kosten die bij de aanschaf van een woning horen. Sommigen kunnen op nul gezet worden afhankelijk
    # van de situatie. Sommigen zijn aftrekbaar: daar is al rekening mee gehouden in de berekeningen, hier moeten de
    # bruto kosten gespecifieerd worden.
    kosten_notaris: float = 1000  # voor zowel hypotheek als koopacte
    kosten_makelaar: float = 0  # voor een eventuele aankoopmakelaar
    kosten_hypotheek: float = 3000  # aftrekbaar, inclusief hypotheekadvies en eventuele NHG kosten
    kosten_taxatie: float = 500  # aftrekbaar
    kosten_bouwkundig_rapport: float = 500  # aftrekbaar
    kosten_overig: float = 0
    kosten_overig_aftrekbaar: float = 0  # aftrekbaar

    # Geschatte maandelijkse onderhoudskosten voor bijvoorbeeld schilderen en dakonderhoud. Dit kan heel erg varieren
    # afhankelijk van het type en bouwjaar van het huis, zie hier voor een schatting afhankelijk van de situatie:
    # https://www.eigenhuis.nl/wonen/onderhoud/kosten#/
    # In dit maandbedrag zit ook de eventuele VVE kosten bij, die ook meestal ook voor onderhoud gebruikt worden.
    onderhoud_per_maand: float = 300

    # De hypotheekgegevens, inclusief het aantal jaren dat de rente vastgezet wordt. De rente daarna is natuurlijk een
    # grote onbekende, dus wordt hier standaard op hetzelfde percentage gezet, maar hier kan mee gespeeld worden. De
    # looptijd staat hier ook op de typische 30 jaar, maar dat kan ook aangepast worden.
    rente_vast_jaren: int = 10
    rente_percentage_nadien: float = hypotheek_rente_percentage
    looptijd_hypotheek_jaren: int = 30

    # Eventueel kan er ook een percentage van de hypotheek als aflossingsvrij gezet worden. Daar hoort vaak wel een
    # hoger rente-percentage bij, dat moet hier dan opgegeven worden.
    aflossingsvrij_deel: float = 0.0
    rente_percentage_aflossingsvrij: float = hypotheek_rente_percentage

    # De schatting van de WOZ-waarde van het huis, bijvoorbeeld nodig voor het berekenen van de eigenwoningforfait.
    # Aangenomen wordt dat dit jaar met een bepaald percentage stijgt.
    woz_waarde: float = kosten_huis * 0.8  # meestal ligt dit een stuk onder de eigenlijk verkoopprijs
    woz_stijging_jaarlijks_percentage: float = 3.0

    # Voor de vergelijking met huren wordt ook aangenomen dat de huur inclusief servicekosten met een percentage stijgt.
    huurstijging_jaarlijks_percentage: float = 3.0

    # Om de onderhoudskosten te schatten over een x-aantal jaar moet de inflatie geschat worden.
    inflatie_jaarlijks_percentage: float = 2.0

    # ------------------------------------------------------------------------------------------------------------------
