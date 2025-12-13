import requests
from bs4 import BeautifulSoup

URL="https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"

URL2="https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"

def print_grid_google(URL:str) -> None:
    resp = requests.get(URL)
    resp.raise_for_status()
    html = resp.text

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("No table found in the document")

    points = []  # list of (x, y, char) tuples (better)

    rows = table.find_all("tr")
    if not rows:
        raise ValueError("Table has no rows")

    for row in rows[1:]:  
        cells = row.find_all("td")

        x_text = cells[0].get_text(strip=True)
        char_text = cells[1].get_text(strip=True)
        y_text = cells[2].get_text(strip=True)

        x = int(x_text)
        y = int(y_text)
        ch = char_text[0] 

        points.append((x, y, ch))

    if not points:
        raise ValueError("No data rows found in table, please check table")

    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)

    width = max_x + 1
    height = max_y + 1

    grid = [[" " for _ in range(width)] for _ in range(height)]

    for x, y, ch in points:
        grid[y][x] = ch

    for y in range(height-1,0,-1):
        print("".join(grid[y]))
        

print_grid_google(URL2)