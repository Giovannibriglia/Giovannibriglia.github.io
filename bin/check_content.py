#!/usr/bin/env python3
"""Check the homepage content files before the site is built.

Validates _pages/about.md, _data/publications.yml, _data/research.yml,
_data/talks.yml and the front matter of every _news/*.md file: required
fields, allowed values, unique ids, cross-references and local files.

Usage: python3 bin/check_content.py [repo_root]
Needs PyYAML (pip install pyyaml). Exits with status 1 if anything is wrong.
"""

import datetime
import os
import re
import sys

import yaml

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
IN_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"

PUB_TAGS = {"selected", "causal", "multi", "earlier"}
BADGE_KINDS = {"oral", "award"}
HIGHLIGHT_KINDS = {"award", "oral", "plain"}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

errors = []


def error(path, message):
    errors.append((path, message))


def load_yaml(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        error(rel, "file is missing")
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        error(rel, f"is not valid YAML: {exc}")
        return None


def load_front_matter(rel):
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not match:
        error(rel, "has no front matter (a block between two --- lines at the top)")
        return None
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        error(rel, f"front matter is not valid YAML: {exc}")
        return None


def is_blank(value):
    return value is None or (isinstance(value, str) and not value.strip())


def require(rel, where, entry, fields):
    for field in fields:
        if is_blank(entry.get(field)):
            error(rel, f"{where}: '{field}' is missing or empty")


def check_local_path(rel, where, url):
    """Local links like /assets/pdf/x.pdf must point at a file in the repo."""
    if not isinstance(url, str) or "://" in url or url.startswith(("#", "mailto:")):
        return
    target = url.split("#")[0].split("?")[0]
    if not target.startswith("/"):
        error(rel, f"{where}: local link '{url}' should start with /")
        return
    if target.startswith("/blog/"):
        return  # generated from _posts/, not a file in the repo
    if not os.path.exists(os.path.join(ROOT, target.lstrip("/"))):
        error(rel, f"{where}: '{url}' does not exist in the repository")


def check_links(rel, where, links):
    if links is None:
        return
    if not isinstance(links, list):
        error(rel, f"{where}: 'links' must be a list")
        return
    for i, link in enumerate(links, 1):
        if not isinstance(link, dict):
            error(rel, f"{where}: link {i} must have 'label' and 'url'")
            continue
        require(rel, f"{where}, link {i}", link, ["label", "url"])
        check_local_path(rel, f"{where}, link {i}", link.get("url"))


def check_publications():
    rel = "_data/publications.yml"
    data = load_yaml(rel)
    if data is None:
        return set()
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        error(rel, "must have a top-level 'items:' list")
        return set()
    if is_blank(data.get("me")):
        error(rel, "'me' is missing (the author name to show in bold)")

    ids = set()
    for n, pub in enumerate(data["items"], 1):
        if not isinstance(pub, dict):
            error(rel, f"item {n} is not a mapping")
            continue
        where = f"item {n} ({pub.get('id') or pub.get('title') or 'no id'})"
        require(rel, where, pub, ["id", "title", "authors", "venue", "year", "tags"])

        pub_id = pub.get("id")
        if isinstance(pub_id, str):
            if not ID_PATTERN.match(pub_id):
                error(rel, f"{where}: id '{pub_id}' may only use lowercase letters, digits and dashes")
            if pub_id in ids:
                error(rel, f"{where}: id '{pub_id}' is used more than once")
            ids.add(pub_id)

        authors = pub.get("authors")
        if authors is not None and (not isinstance(authors, list) or not authors):
            error(rel, f"{where}: 'authors' must be a non-empty list, e.g. [G. Briglia, S. Mariani]")

        year = pub.get("year")
        if year is not None and not (isinstance(year, int) and 1990 <= year <= 2100):
            error(rel, f"{where}: 'year' must be a four-digit number")

        tags = pub.get("tags")
        if tags is not None:
            if not isinstance(tags, list):
                error(rel, f"{where}: 'tags' must be a list")
            else:
                unknown = sorted(set(map(str, tags)) - PUB_TAGS)
                if unknown:
                    error(rel, f"{where}: unknown tags {unknown}; use {sorted(PUB_TAGS)}")

        if not is_blank(pub.get("badge")) and pub.get("badge_kind", "oral") not in BADGE_KINDS:
            error(rel, f"{where}: 'badge_kind' must be one of {sorted(BADGE_KINDS)}")

        if not is_blank(pub.get("image")):
            check_local_path(rel, f"{where}, image", pub["image"])
            if is_blank(pub.get("image_alt")):
                error(rel, f"{where}: add 'image_alt' describing the thumbnail")

        check_links(rel, where, pub.get("links"))

        bibtex = pub.get("bibtex")
        if not is_blank(bibtex) and not str(bibtex).lstrip().startswith("@"):
            error(rel, f"{where}: 'bibtex' should start with @article{{...}} or similar")

    return ids


def check_research(pub_ids):
    rel = "_data/research.yml"
    data = load_yaml(rel)
    if data is None:
        return
    if not isinstance(data, list):
        error(rel, "must be a list of questions")
        return
    for n, q in enumerate(data, 1):
        if not isinstance(q, dict):
            error(rel, f"question {n} is not a mapping")
            continue
        where = f"question {n} ({q.get('label', 'no label')})"
        require(rel, where, q, ["label", "question"])
        for i, paper in enumerate(q.get("papers") or [], 1):
            if not isinstance(paper, dict):
                error(rel, f"{where}, paper {i}: needs 'id' and 'label'")
                continue
            require(rel, f"{where}, paper {i}", paper, ["id", "label"])
            if paper.get("id") and paper["id"] not in pub_ids:
                error(rel, f"{where}, paper {i}: id '{paper['id']}' is not in _data/publications.yml")


def check_talks():
    rel = "_data/talks.yml"
    data = load_yaml(rel)
    if data is None:
        return
    if not isinstance(data, list):
        error(rel, "must be a list of talks")
        return
    for n, talk in enumerate(data, 1):
        if not isinstance(talk, dict):
            error(rel, f"talk {n} is not a mapping")
            continue
        where = f"talk {n} ({talk.get('title', 'no title')})"
        require(rel, where, talk, ["when", "title", "where"])
        check_local_path(rel, where, talk.get("url"))


def check_about():
    rel = "_pages/about.md"
    fm = load_front_matter(rel)
    if fm is None:
        return
    if fm.get("layout") != "onepage":
        error(rel, "'layout' must be 'onepage' for the one-page homepage")
    require(rel, "front matter", fm, ["title", "role", "headline", "intro"])
    limit = fm.get("news_limit")
    if limit is not None and not (isinstance(limit, int) and limit > 0):
        error(rel, "'news_limit' must be a positive whole number")
    for n, h in enumerate(fm.get("highlights") or [], 1):
        if not isinstance(h, dict):
            error(rel, f"highlight {n} is not a mapping")
            continue
        require(rel, f"highlight {n}", h, ["label", "text"])
        if h.get("kind", "plain") not in HIGHLIGHT_KINDS:
            error(rel, f"highlight {n}: 'kind' must be one of {sorted(HIGHLIGHT_KINDS)}")


def check_news():
    folder = os.path.join(ROOT, "_news")
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".md"):
            continue
        rel = f"_news/{name}"
        fm = load_front_matter(rel)
        if fm is None:
            continue
        date = fm.get("date")
        if not isinstance(date, (datetime.date, datetime.datetime)):
            error(rel, "'date' is missing or not a date like 2026-11-15")
        if not fm.get("inline") and is_blank(fm.get("title")):
            error(rel, "news items without 'inline: true' need a 'title'")


def main():
    pub_ids = check_publications()
    check_research(pub_ids)
    check_talks()
    check_about()
    check_news()

    if not errors:
        print("Content check passed.")
        return 0
    for path, message in errors:
        if IN_ACTIONS:
            print(f"::error file={path}::{message}")
        else:
            print(f"{path}: {message}")
    print(f"\n{len(errors)} problem(s) found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
