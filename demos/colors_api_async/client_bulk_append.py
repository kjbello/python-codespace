import requests
from pathlib import Path
import csv


NewColor = tuple[str, str]
NewColorList = list[NewColor]


def bulk_append_colors(colors: NewColorList) -> None:
    new_colors = [
        {"name": color_name, "hex_code": color_hexcode}
        for color_name, color_hexcode in colors
    ]

    print(new_colors)

    requests.post("http://127.0.0.1:8000/colors/bulk", json=new_colors)


def read_html_colors_file() -> NewColorList:
    html_colors: NewColorList = []
    with Path("html_colors.csv").open("r", encoding="utf-8") as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for row in csv_file:
            html_colors.append((row[0], row[1]))
    return html_colors


def main() -> None:
    html_colors = read_html_colors_file()
    bulk_append_colors(html_colors)


if __name__ == "__main__":
    main()
