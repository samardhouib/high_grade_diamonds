"""
Scraper for Fay Jewelry's diamond semi mount products.

This script crawls the **Diamond Semi Mounts** category on the Fay Jewelry
website and gathers information from each product page.  For every product
encountered the scraper extracts the following fields:

* **title** – the product name from the right‐hand header on the page.
* **description** – the short description displayed under the title on the
  product page.  This is typically a couple of sentences explaining the
  design and options available.
* **details** – a dictionary of attributes taken from the right section
  labelled *DESCRIPTION*.  Each row of the table on the page becomes a
  key/value pair.  Common keys include ``Ring Mounting``, ``Side Diamond``
  and ``Primary Stone``.
* **images** – a list of image URLs.  These come from the structured
  ``application/ld+json`` block on the product page which lists one or more
  pictures of the item.
* **url** – the absolute URL of the product page.

The scraper works by first building a list of product page URLs from all
pagination pages under ``/diamond-semi-mounts``.  On each listing page it
looks for ``a`` elements with the CSS class ``btn`` and the text
"Read More".  These links lead to the individual product pages.  Duplicate
links are removed.

Once all product links have been collected, each page is requested and
parsed with BeautifulSoup.  The title and description are extracted from
``div.shown_products_a_right``.  The descriptive table is found within
``div#Descrip``, and the table rows are converted into a dictionary.
Images are obtained by parsing the JSON LD block on the page and reading
the ``Image`` field of the ``Product`` object.

At the end of the run the scraper writes the results into a JSON file
called ``fayjewelry_products.json`` in the current working directory.  If
you want CSV or some other format you can adapt the code accordingly.

The script relies only on the standard library and the third‑party
``beautifulsoup4`` module.  Install dependencies with ``pip install
beautifulsoup4 requests`` before running the script.

Example usage::

    python fayjewelry_scraper.py

This will fetch all 22 listing pages, parse each product page and create
``fayjewelry_products.json``.
"""

import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Helpers for image handling and safe file naming

def slugify(text: str) -> str:
    """Simplify a string into a safe filename component.

    Replaces any sequence of non‑alphanumeric characters with a single
    underscore and lower‑cases the result.

    Args:
        text: Input string to slugify.

    Returns:
        A slug suitable for use in filenames.
    """
    text = text.strip().lower()
    # Replace non alphanumerics with underscores
    text = re.sub(r"[^a-z0-9]+", "_", text)
    # Collapse consecutive underscores
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def download_image(session: requests.Session, url: str, dest_dir: Path, prefix: str = "") -> Optional[str]:
    """Download an image to ``dest_dir`` if it does not already exist.

    The file name is derived from the URL and an optional prefix to avoid
    collisions.  If the download is successful, the relative path to the
    saved file is returned; otherwise ``None`` is returned.

    Args:
        session: The ``requests.Session`` used to fetch images.
        url: The remote image URL.
        dest_dir: Directory where images should be stored.  It will be
            created if it does not exist.
        prefix: An optional prefix (e.g. product slug) to prepend to the
            image file name.

    Returns:
        The relative path (string) to the saved image file or ``None`` on
        failure.
    """
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    # Derive a filename from the URL and prefix
    name = url.split("/")[-1].split("?")[0]
    if prefix:
        name = f"{prefix}_{name}"
    file_path = dest_dir / name
    # Skip download if file already exists
    if file_path.exists():
        return str(file_path)
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        file_path.write_bytes(resp.content)
        return str(file_path)
    except Exception:
        return None


# Base URL for the site.  This can be changed if Fay Jewelry moves to a
# different domain.  Note that specific category URLs are defined in
# ``main()``.
BASE_CATEGORY_URL = "https://www.fayjewelry.com"

# Total number of pagination pages within the chosen category.  The
# website currently displays 22 pages but this may change over time.
MAX_PAGES = 22


def get_product_links(session: requests.Session, base_url: str) -> List[Tuple[str, Optional[str]]]:
    """
    Collect product URLs and their hero images from a given category.

    This helper walks through pagination pages under ``base_url`` and
    locates product links via "Read More" buttons.  For each product
    discovered it also tries to extract the single image shown on the
    listing page by parsing the page's JSON‑LD ``Product`` objects.

    Args:
        session: A configured ``requests.Session`` used for HTTP calls.
        base_url: The root URL of the category being scraped (e.g.
            ``https://www.fayjewelry.com/semi-mount-rings``).  The
            function will request ``base_url`` for page 1 and
            ``{base_url}/p2``, ``{base_url}/p3`` etc. up to ``MAX_PAGES``.

    Returns:
        A list of tuples ``(product_url, listing_image_url)``.  The
        ``listing_image_url`` may be ``None`` if no image was found.
    """
    results: List[Tuple[str, Optional[str]]] = []
    seen: set[str] = set()
    for page in range(1, MAX_PAGES + 1):
        page_url = base_url if page == 1 else f"{base_url}/p{page}"
        try:
            response = session.get(page_url)
            response.raise_for_status()
        except Exception:
            # stop paging if a page fails (likely no more pages)
            break
        soup = BeautifulSoup(response.content, "html.parser")
        # map product URL -> listing image using JSON‑LD Product blocks
        ld_map: Dict[str, str] = {}
        for script in soup.find_all("script", type="application/ld+json"):
            if not script.string:
                continue
            try:
                data = json.loads(script.string)
            except Exception:
                continue
            objs = data if isinstance(data, list) else [data]
            for obj in objs:
                if not isinstance(obj, dict):
                    continue
                if obj.get("@type") != "Product":
                    continue
                prod_url = obj.get("@id") or obj.get("url")
                prod_img = obj.get("Image") or obj.get("image")
                if not prod_url or not prod_img:
                    continue
                # pick the first image if a list is provided
                img_url = prod_img[0] if isinstance(prod_img, list) else prod_img
                ld_map[str(prod_url)] = str(img_url)
        # extract Read More links and associate listing images
        for a in soup.find_all("a", class_="btn"):
            if a.string and "Read More" in a.string:
                href = a.get("href")
                if not href or href == "/message.html":
                    continue
                abs_url = href
                if abs_url.startswith("/"):
                    abs_url = f"https://www.fayjewelry.com{abs_url}"
                if abs_url in seen:
                    continue
                seen.add(abs_url)
                listing_img = ld_map.get(abs_url)
                results.append((abs_url, listing_img))
        # brief delay between pages
        time.sleep(0.05)
    return results


def parse_product_page(
    session: requests.Session,
    url: str,
    listing_image: Optional[str] = None,
    images_dir: Optional[Path] = None,
) -> Dict[str, object]:
    """
    Parse a single product page and return structured data with optional
    image downloading and category extraction.

    In addition to scraping the title, description and details table,
    this function collects images from three sources: the JSON‑LD Product
    object, the visible gallery (div.shown_products_a_left) and the
    OpenGraph ``og:image`` meta tag.  If a listing image from the
    catalogue page is provided via ``listing_image`` it is added to the
    front of the image list.  When ``images_dir`` is supplied,
    downloaded copies of each image are saved into that directory and
    the list in the returned dictionary contains the local file paths.

    The function also extracts the product and subproduct categories by
    parsing the breadcrumb JSON‑LD ``BreadcrumbList``, where the
    category following ``Products`` is considered the product and the
    next category the subproduct.

    Args:
        session: The ``requests.Session`` used to fetch the page.
        url: The absolute product URL.
        listing_image: Optional URL of the image displayed on the
            category listing page.
        images_dir: Optional directory into which images will be
            downloaded.  If provided, remote image URLs are replaced with
            local file paths in the returned data.

    Returns:
        A dictionary containing the product fields and categories.
    """
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")

    # default values
    title: Optional[str] = None
    description: Optional[str] = None
    details: Dict[str, str] = {}
    images: List[str] = []
    product_category: Optional[str] = None
    subproduct_category: Optional[str] = None

    # Extract title and short description
    right_div = soup.find("div", class_="shown_products_a_right")
    if right_div:
        h1 = right_div.find("h1")
        if h1:
            title = h1.get_text(strip=True)
        desc_div = right_div.find("div", class_="p-short")
        if desc_div:
            description = desc_div.get_text(" ", strip=True)

    # Extract attributes from the DESCRIPTION table
    desc_section = soup.find("div", id="Descrip")
    if desc_section:
        table = desc_section.find("table")
        if table:
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 2:
                    key = tds[0].get_text(strip=True)
                    value_lines: List[str] = []
                    for p in tds[1].find_all("p"):
                        text_val = p.get_text(strip=True)
                        if text_val:
                            text_val = re.sub(r"\s+", " ", text_val)
                            value_lines.append(text_val)
                    if value_lines:
                        details[key] = "; ".join(value_lines)

    # Prepend the listing image if provided
    if listing_image:
        images.append(listing_image)

    # Parse JSON‑LD for product images and breadcrumb categories
    for script in soup.find_all("script", type="application/ld+json"):
        if not script.string:
            continue
        try:
            data = json.loads(script.string)
        except Exception:
            continue
        objs = data if isinstance(data, list) else [data]
        for obj in objs:
            if not isinstance(obj, dict):
                continue
            if obj.get("@type") == "Product":
                imgs = obj.get("Image") or obj.get("image")
                if imgs:
                    if isinstance(imgs, list):
                        images.extend(imgs)
                    else:
                        images.append(str(imgs))
            if obj.get("@type") == "BreadcrumbList":
                # Extract dynamic categories from breadcrumb.  Typically
                # a product page has a breadcrumb like:
                # [Home, Products, Category, Subcategory, Product].
                # We treat the second‑to‑last element as the main product
                # category and the third‑to‑last as the parent category.
                elements = obj.get("ItemListElement", [])
                if not isinstance(elements, list):
                    continue
                try:
                    if len(elements) >= 4:
                        # There are at least Home, Products, Category, Subcategory, Product
                        subproduct_category = elements[-3].get("Name")  # parent category
                        product_category = elements[-2].get("Name")     # subcategory
                    elif len(elements) == 3:
                        # Only Home, Products, Category present.  Use the last
                        # category as the product category and leave the
                        # subcategory undefined.
                        product_category = elements[-1].get("Name")
                        subproduct_category = None
                    # else: leave categories as None
                except Exception:
                    # ignore any errors extracting names
                    pass

    # Visible gallery images
    gallery = soup.find("div", class_="shown_products_a_left")
    if gallery:
        for img_tag in gallery.find_all("img"):
            src = img_tag.get("src") or img_tag.get("data-src")
            if not src:
                continue
            if src.startswith("/"):
                src = f"https://www.fayjewelry.com{src}"
            images.append(src)

    # OpenGraph hero image
    for meta in soup.find_all("meta", attrs={"property": "og:image"}):
        content = meta.get("content")
        if content:
            images.append(content)

    # Deduplicate while preserving order
    seen_imgs: set[str] = set()
    unique_imgs: List[str] = []
    for img_url in images:
        if img_url and img_url not in seen_imgs:
            seen_imgs.add(img_url)
            unique_imgs.append(img_url)
    images = unique_imgs

    # Download images if requested and replace URLs with local paths
    if images_dir is not None:
        # Use slugified title or fallback slug from URL as prefix
        prefix = slugify(title) if title else slugify(Path(url).stem)
        local_paths: List[str] = []
        for img_url in images:
            local = download_image(session, img_url, images_dir, prefix=prefix)
            # fall back to remote URL if download fails
            local_paths.append(local or img_url)
        images = local_paths

    return {
        "url": url,
        "title": title,
        "description": description,
        "details": details,
        "images": images,
        "product_category": product_category,
        "subproduct_category": subproduct_category,
    }


def main() -> None:
    """Entry point for the scraper.

    This function orchestrates the full scraping workflow: it collects all
    product URLs along with their listing images, downloads all images
    into a local directory, parses each product page to extract
    structured data and then groups the items by product and
    subproduct categories.  The resulting grouped dataset is written
    to ``fayjewelry_products.json`` in the current directory.

    Grouping is performed such that the top‑level keys correspond to
    high‑level product categories (e.g. "Ring Mountings") and the
    values are dictionaries keyed by subproduct category (e.g. "Emerald
    Cut") containing lists of product objects.  Products without
    recognised categories are placed under the key ``"Uncategorized"``.
    """
    session = requests.Session()
    # Set a browser‑like user agent to avoid potential blocking.
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        )
    })

    print("Collecting product links…", file=sys.stderr)
    # Determine which categories to scrape.  Start with the base
    # 'Diamond Semi Mounts' category and its immediate sub‑categories
    # (e.g. Semi Mount Rings/Earrings/Pendants).  These are specified
    # explicitly here but could also be scraped dynamically from the
    # navigation.  You can modify this list to include other
    # categories such as fine jewelry, engagement rings, etc.
    # List of category pages to scrape.  This includes top‑level product
    # categories and their immediate subcategories so that all
    # products available under "Products" are captured.  If Fay
    # Jewelry add new categories in the future you can extend this
    # list accordingly.
    category_paths = [
        # Diamond Semi Mounts and its subcategories
        "https://www.fayjewelry.com/diamond-semi-mounts",
        "https://www.fayjewelry.com/semi-mount-rings",
        "https://www.fayjewelry.com/semi-mount-earrings",
        "https://www.fayjewelry.com/semi-mount-pendants",
        # Fine Jewelry and its subcategories
        "https://www.fayjewelry.com/fine-jewelry",
        "https://www.fayjewelry.com/ruby-jewelry",
        "https://www.fayjewelry.com/sapphire-jewelry",
        "https://www.fayjewelry.com/emerald-jewelry",
        "https://www.fayjewelry.com/tanzanite-jewelry",
        "https://www.fayjewelry.com/aquamarine-jewelry",
        "https://www.fayjewelry.com/morganite-jewelry",
        "https://www.fayjewelry.com/garnet-jewelry",
        "https://www.fayjewelry.com/pearl-jewelry",
        "https://www.fayjewelry.com/quartz-jewelry",
        "https://www.fayjewelry.com/men-jewelry",
        "https://www.fayjewelry.com/moissanite-jewelry",
        "https://www.fayjewelry.com/other-diamond-jewelry",
        # Engagement and Wedding Jewelry
        "https://www.fayjewelry.com/engagement-wedding-jewelry",
        "https://www.fayjewelry.com/engagement-rings",
        "https://www.fayjewelry.com/wedding-bands",
        # Lab-Grown Diamonds Jewelry
        "https://www.fayjewelry.com/lab-grown-diamonds-jewelry",
    ]
    product_links: List[Tuple[str, Optional[str]]] = []
    for cat_url in category_paths:
        print(f"  Processing category {cat_url}", file=sys.stderr)
        links = get_product_links(session, cat_url)
        print(f"    Found {len(links)} products", file=sys.stderr)
        product_links.extend(links)
    # Deduplicate links across categories
    unique_links: Dict[str, Optional[str]] = {}
    for url, listing_img in product_links:
        if url not in unique_links:
            unique_links[url] = listing_img
    consolidated_links = list(unique_links.items())
    print(f"Total unique products collected: {len(consolidated_links)}", file=sys.stderr)

    # Directory to store downloaded images
    images_dir = Path("fayjewelry_images")

    # Collect scraped product data
    raw_results: List[Dict[str, object]] = []
    for idx, (url, listing_img) in enumerate(consolidated_links, 1):
        print(f"[{idx}/{len(consolidated_links)}] Scraping {url}", file=sys.stderr)
        try:
            data = parse_product_page(
                session,
                url,
                listing_image=listing_img,
                images_dir=images_dir,
            )
        except Exception as exc:
            print(f"Error scraping {url}: {exc}", file=sys.stderr)
            continue
        raw_results.append(data)
        # polite delay between requests
        time.sleep(0.05)

    # Group by product and subproduct categories
    grouped: Dict[str, Dict[str, List[Dict[str, object]]]] = {}
    for item in raw_results:
        # Extract and remove category fields from item
        product_cat = item.pop("product_category", None) or "Uncategorized"
        subproduct_cat = item.pop("subproduct_category", None) or "Uncategorized"
        grouped.setdefault(product_cat, {}).setdefault(subproduct_cat, []).append(item)

    # Write grouped data to JSON file
    out_path = Path("fayjewelry_products.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(grouped, f, ensure_ascii=False, indent=2)
    print(f"Saved grouped data for {len(raw_results)} products to {out_path}")


if __name__ == "__main__":
    main()