"""In deze module bevinden zich functies die data inlezen of wegschrijven."""
from pathlib import Path
from typing import List

from src import data


def schrijf_naar_csv(alle_data: List[data.MaandData], file_name: Path) -> None:
    """Schrijft alle data weg naar een CSV bestand met een komma als separator."""
    with file_name.open("w") as file:

        header = ["Jaar", "Maand"]
        for naam in data.MAANDELIJKSE_WAARDEN + data.TOTALE_WAARDEN:
            header.append(naam.capitalize().replace("_", ""))
        file.write(",".join(header) + "\n")

        for maand_data in alle_data:
            data_lijst = [str(maand_data.jaar), str(maand_data.maand)]
            for naam in data.MAANDELIJKSE_WAARDEN + data.TOTALE_WAARDEN:
                data_lijst.append(f"{getattr(maand_data, naam):.0f}")
            file.write(",".join(data_lijst) + "\n")
