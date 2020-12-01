"""Deze module bevat functies om grafieken te plotten"""
from pathlib import Path
from typing import List

import numpy as np
from matplotlib import pyplot as plt

from src import data


def plot_maandelijks(plot_data: List[data.MaandData], x_waarden: np.ndarray, x_labels: List[str]) -> None:
    """De plot met de maandelijkse waarden (in de honderden tot duizenden euro)"""
    plt.subplot(211)
    axis = plt.gca()

    alle_kleuren = ["moccasin", "skyblue", "lightcoral", "palegreen", "purple"]

    plt.title("[HKP] HuisKoopPlot, gemaakt met 'https://github.com/CNugteren/huiskoopplot'")
    plt.figtext(0.35, 0.93, "Veel gegevens zijn schattingen, zie gegevens.py voor meer informatie")

    y_waarden = [[getattr(maand_data, naam) for maand_data in plot_data] for naam in data.MAANDELIJKSE_PLOT1]

    labels = [naam.capitalize().replace("_", " ") for naam in data.MAANDELIJKSE_PLOT1]
    plt.stackplot(x_waarden, *y_waarden, labels=labels,
                  colors=alle_kleuren[:len(data.MAANDELIJKSE_PLOT1)])

    y_max = max([max(y) for y in y_waarden])
    for index, naam in enumerate(data.MAANDELIJKSE_PLOT2):
        y_waarden = [getattr(maand_data, naam) for maand_data in plot_data]
        plt.plot(x_waarden, y_waarden, label=naam.capitalize().replace("_", " "),
                 color=alle_kleuren[len(data.MAANDELIJKSE_PLOT1) + index])
        y_max = max(y_max, max(y_waarden))

    plt.ylabel("Maandelijks bedrag in euro")
    plt.xticks(x_waarden[::12], labels=x_labels)
    plt.yticks(list(range(0, int(y_max), 250)), labels=[str(v) for v in range(0, int(y_max), 250)])
    axis.set_xlim(xmin=0, xmax=len(x_waarden))
    plt.grid(True, axis="y")
    plt.legend(loc="upper left")


def plot_totaal(plot_data: List[data.MaandData], x_waarden: np.ndarray, x_labels: List[str]) -> None:
    """De plot met de totale bedragen (in de honderdduizenden euro)"""
    plt.subplot(212)
    axis = plt.gca()

    y_max = 0
    for naam in data.TOTALE_WAARDEN:
        y_waarden = [getattr(maand_data, naam) for maand_data in plot_data]
        plt.plot(x_waarden, y_waarden, label=naam.capitalize().replace("_", " "))
        y_max = max(y_max, max(y_waarden))

    plt.xlabel("Jaar na aankoop")

    plt.ylabel("Totaal bedrag in euro (x1000)")
    plt.xticks(x_waarden[::12], labels=x_labels)
    plt.yticks(list(range(0, int(y_max), 100_000)), labels=[str(v) for v in range(0, int(y_max / 1000), 100)])
    axis.set_xlim(xmin=0, xmax=len(x_waarden))
    plt.grid(True, axis="y")
    plt.legend(loc="upper left")


def plot(alle_data: List[data.MaandData], file_name: Path, plot_jaren: int) -> None:
    """De hoofdplot functie om de twee grafieken te plotten."""
    plot_data = alle_data[:(plot_jaren * 12)]

    # De dimensies van de plot
    plot_grootte_y = 800
    plot_grootte_x = plot_grootte_y * 16 / 9
    plt.figure(figsize=(plot_grootte_x / 100, plot_grootte_y / 100))

    # De waarden voor de x-as
    x_waarden = np.arange(0, len(plot_data))
    x_labels = [f"{jaar}" for jaar in range(0, len(plot_data) // 12)]

    # De twee plots
    plot_maandelijks(plot_data, x_waarden, x_labels)
    plot_totaal(plot_data, x_waarden, x_labels)

    # Stel de margins in
    plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.10, hspace=0.1)

    # Sla het resultaat op als bestand
    plt.savefig(file_name, dpi=100)
