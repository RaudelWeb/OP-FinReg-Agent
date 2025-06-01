#!/usr/bin/env python3
"""
fetch_finreg_docs.py

Lataa finanssivalvonnan MOK-dokumentit sekä EBA:n viimeisimmät
ESG-riskiohjeet ja Fit-for-55 -ilmastoskenaariotemplaatit.

Käyttö:
    python fetch_finreg_docs.py --out ./downloads
"""
import argparse
import pathlib
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# --- Kiinteät URL-osoitteet ---------------------------------------------------
FIVA_MOK_PAGE = (
    "https://www.finanssivalvonta.fi/saantely/maarays-ja-ohjekokoelma/"
)

EBA_URLS = {
    # ESG-riskien hallinnan lopulliset ohjeet (9 Jan 2025)
    "ESG_Guidelines_2025.pdf": (
        "https://www.eba.europa.eu/sites/default/files/2025-01/"
        "fb22982a-d69d-42cc-9d62-1023497ad58a/"
        "Final%20Guidelines%20on%20the%20management%20of%20ESG%20risks.pdf"
    ),
    # Fit-for-55 -templaatit (17 Nov 2023)
    "Fit55_Templates.xlsx": (
        "https://www.eba.europa.eu/sites/default/files/2023-11/"
        "cdc9ffd1-76f9-4711-ae2b-7d4247c85749/FF55%20-%20Templates.xlsx"
    ),
    "Fit55_Template_Guidance.pdf": (
        "https://www.eba.europa.eu/sites/default/files/2023-11/"
        "39f91f76-23b5-4a69-a50d-b3154022e62e/FF55%20-%20Template%20guidance_0.pdf"
    ),
}


# --- Apu-funktiot -------------------------------------------------------------
def download(url: str, outfile: pathlib.Path) -> None:
    """Lataa url → outfile, jos sitä ei ole jo olemassa."""
    outfile.parent.mkdir(parents=True, exist_ok=True)
    if outfile.exists():
        print(f"✓ {outfile.name} (cached)")
        return

    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=outfile.name,
            leave=False,
        ) as bar, open(outfile, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
    print(f"✔ {outfile.name} saved")


def scrape_fiva_mok_links() -> list[str]:
    """Palauttaa kaikki MOK-PDF-linkit Fivan sivulta."""
    resp = requests.get(FIVA_MOK_PAGE, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    pdf_links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Etsitään polut, jotka selvästi viittaavat MOK-pdf:iin
        if href.lower().endswith(".pdf") and "/maarayskokoelma/" in href:
            pdf_links.add(urljoin(FIVA_MOK_PAGE, href))

    return sorted(pdf_links)


# --- Pääohjelma ---------------------------------------------------------------
def main(out_dir: pathlib.Path) -> None:
    # 1) Fiva MOK
    mok_dir = out_dir / "fiva_mok"
    print("==> Downloading Fiva MOK documents")
    for url in scrape_fiva_mok_links():
        filename = pathlib.Path(url).name
        download(url, mok_dir / filename)

    # 2) EBA-dokumentit
    eba_dir = out_dir / "eba"
    print("\n==> Downloading EBA ESG & Fit-for-55 documents")
    for fname, url in EBA_URLS.items():
        download(url, eba_dir / fname)

    print("\nAll files downloaded to", out_dir.resolve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Fiva & EBA docs")
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=pathlib.Path("./downloads"),
        help="Kohdekansio (oletus: ./downloads)",
    )
    args = parser.parse_args()
    try:
        main(args.out)
    except KeyboardInterrupt:
        sys.exit("Interrupted by user")