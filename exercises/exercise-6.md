# Exercise 6 - Implement Bulk Import

1. Add a new endpoint to the Colors API performs a bulk import of colors. The colors to import are in a file named `html_colors.csv`.

Use the imports:

```python
from pathlib import Path
import csv
import json
```

Read the CSV Code:

```python
html_colors: list[tuple[str, str]] = []
with Path("html_colors.csv").open("r", encoding="utf-8") as file:
    csv_file = csv.reader(file)
    next(csv_file)
    for row in csv_file:
        html_colors.append((row[0], row[1]))
```

To call the REST API Endpoint:

```python
new_colors = [
    {"name": color_name, "hex_code": color_hexcode}
    for color_name, color_hexcode in html_colors
]

requests.post("http://127.0.0.1:8000/colors/bulk", json=new_colors)
```

2. The path for the new endpoint will be `/colors/bulk`. The post data will be a list of ColorCreate schemas.

3. The bulk import will be implemented with the following code. This code does not represent the whole function, just the SqlAlchemy part.

    ```python
    self.__db_session.add_all(color_models)
    await self.__db_session.commit()
    for color_model in color_models:
        await self.__db_session.refresh(color_model)
    ```

4. Return back a list of inserted colors. Each color should have an `id`.

5. If no colors are passed to the endpoint, return an error.

## When Done

Send me an email [eric@cloudcontraptions.com](mailto:eric@cloudcontraptions.com) when you are done.
