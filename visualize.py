import matplotlib.pyplot as plt
import pandas as pd
from rich.console import Console
from rich.table import Table

LABELS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def pie_chart(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()

    counts = [df[df["key"] == key].shape[0] for key in LABELS]

    ax.pie(
        counts,
        labels=LABELS,
        autopct="%1.1f%%",
        explode=[0, 0, 0, 0.1, 0, 0.1, 0, 0.1, 0, 0, 0.1, 0],
    )
    ax.axis("equal")
    plt.show()
    fig.savefig("result.png")


def rich_table(df: pd.DataFrame) -> None:
    table = Table(show_header=True)
    table.add_column("Key", style="bold")
    table.add_column("Total(percent)", justify="right")
    table.add_column("Chinese", justify="right")
    table.add_column("Foreign", justify="right")
    table.add_column("Instrumental", justify="right")

    total = df.shape[0]
    chn_count = df[df["lang"] == "国语"].shape[0]
    for_count = df[df["lang"] == "外语"].shape[0]
    ins_count = df[df["lang"] == "纯音乐"].shape[0]

    for key in LABELS:
        key_total = df[df["key"] == key].shape[0]
        key_percent = float(key_total) / total
        chn = df[(df["key"] == key) & (df["lang"] == "国语")].shape[0]
        frn = df[(df["key"] == key) & (df["lang"] == "外语")].shape[0]
        ins = df[(df["key"] == key) & (df["lang"] == "纯音乐")].shape[0]
        cp, fp, ip = (
            float(chn) / chn_count,
            float(frn) / chn_count,
            float(ins) / chn_count,
        )
        table.add_row(
            f"{key}",
            f"{key_total:>5} ({key_percent * 100:>5.2f}%)",
            f"{chn:>6} ({cp * 100:>5.2f}%)",
            f"{frn:>6} ({fp * 100:>5.2f}%)",
            f"{ins:>6} ({ip * 100:>5.2f}%)",
            end_section=key == "G#",
        )
    table.add_row("Total", str(total), str(chn_count), str(for_count), str(ins_count))
    console = Console()
    console.print(table)


if __name__ == "__main__":
    csv_file = "songs.csv"
    df = pd.read_csv(csv_file)
    pie_chart(df)
    rich_table(df)
