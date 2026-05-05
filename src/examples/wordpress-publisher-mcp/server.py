#!/usr/bin/env python3
"""
Server MCP che pubblica articoli su WordPress via REST API.

Espone tre tool a Claude Code:
  - wp_create_post     : crea una bozza (o pubblica direttamente)
  - wp_publish_post    : promuove una bozza esistente a "publish"
  - wp_list_categories : elenca le categorie del sito

Esempio di utilizzo descritto nella Guida Pratica a Claude Code CLI,
capitolo 11.5 — https://github.com/miziomon/claude-code-guide
"""

import os
import base64
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Carica le credenziali da .env (mai hardcodare in repo)
load_dotenv()
BASE_URL = os.environ["WP_BASE_URL"].rstrip("/")
USERNAME = os.environ["WP_USERNAME"]
APP_PASS = os.environ["WP_APP_PASSWORD"]

# Auth Basic con Application Password (formato standard WP)
auth_token = base64.b64encode(
    f"{USERNAME}:{APP_PASS}".encode("utf-8")
).decode("ascii")
HEADERS = {
    "Authorization": f"Basic {auth_token}",
    "Content-Type": "application/json",
}

# Istanza FastMCP: il server si chiamerà "wordpress-publisher"
mcp = FastMCP("wordpress-publisher")


@mcp.tool()
def wp_create_post(
    title: str,
    content: str,
    status: str = "draft",
    categories: list[int] | None = None,
) -> dict:
    """
    Crea un nuovo articolo su WordPress.

    Args:
        title:      titolo del post
        content:    corpo HTML o Gutenberg-block
        status:     "draft" (default) o "publish"
        categories: lista di ID categoria (opzionale)

    Returns:
        Dict con id, status, link, modified del post creato.
    """
    payload = {"title": title, "content": content, "status": status}
    if categories:
        payload["categories"] = categories

    response = httpx.post(
        f"{BASE_URL}/wp-json/wp/v2/posts",
        headers=HEADERS,
        json=payload,
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id": data["id"],
        "status": data["status"],
        "link": data["link"],
        "modified": data["modified"],
    }


@mcp.tool()
def wp_publish_post(post_id: int) -> dict:
    """
    Promuove una bozza esistente a stato "publish".

    Args:
        post_id: ID del post da pubblicare

    Returns:
        Dict con id, status, link aggiornato.
    """
    response = httpx.post(
        f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}",
        headers=HEADERS,
        json={"status": "publish"},
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id": data["id"],
        "status": data["status"],
        "link": data["link"],
    }


@mcp.tool()
def wp_list_categories() -> list[dict]:
    """
    Elenca tutte le categorie del sito.

    Returns:
        Lista di dict con id, name, slug, count per ogni categoria.
    """
    response = httpx.get(
        f"{BASE_URL}/wp-json/wp/v2/categories",
        headers=HEADERS,
        params={"per_page": 100},
        timeout=30.0,
    )
    response.raise_for_status()
    return [
        {"id": c["id"], "name": c["name"], "slug": c["slug"], "count": c["count"]}
        for c in response.json()
    ]


if __name__ == "__main__":
    # Avvio del server in modalità stdio (default per MCP locali)
    mcp.run()
