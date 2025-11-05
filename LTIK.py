#!/usr/bin/env python3
# coding: utf-8
"""
dummy_app.py — File dummy untuk commit ke GitHub.

Contoh fitur:
- tipe hints
- dataclass
- fungsi utilitas dengan docstring + doctest
- CLI sederhana (argparse)
- logging
- contoh penggunaan di __main__
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List
import argparse
import logging
import sys
import json
import math

# ---------- konfigurasi logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("dummy_app")

# ---------- dataclass contoh ----------
@dataclass
class Item:
    """Contoh objek data sederhana."""
    id: int
    name: str
    value: float

    def as_dict(self) -> dict:
        """Kembalikan representasi dict."""
        return {"id": self.id, "name": self.name, "value": self.value}

# ---------- fungsi utilitas ----------
def normalize_values(items: List[Item]) -> List[Item]:
    """
    Normalisasi nilai item sehingga total nilai menjadi 1.0.
    Jika jumlah semua nilai = 0, kembalikan daftar asli tanpa perubahan.

    >>> items = [Item(1,'a',1.0), Item(2,'b',1.0)]
    >>> normalized = normalize_values(items)
    >>> round(sum(i.value for i in normalized), 6)
    1.0
    """
    total = sum(i.value for i in items)
    logger.debug("Total sebelum normalisasi: %s", total)
    if total == 0:
        logger.warning("Total value = 0, tidak melakukan normalisasi.")
        return items
    return [Item(i.id, i.name, i.value / total) for i in items]


def top_n_by_value(items: List[Item], n: int = 3) -> List[Item]:
    """
    Kembalikan top n item urut menurun berdasarkan value.
    Jika n <= 0, kembalikan daftar kosong.
    """
    if n <= 0:
        logger.debug("Requested top_n with n <= 0")
        return []
    sorted_items = sorted(items, key=lambda x: x.value, reverse=True)
    return sorted_items[:n]


def stats(items: List[Item]) -> dict:
    """
    Hitung beberapa statistik ringkas: count, sum, mean, stddev.
    Jika tidak ada item, nilai statistik numerik adalah None.
    """
    count = len(items)
    if count == 0:
        return {"count": 0, "sum": 0.0, "mean": None, "stddev": None}
    values = [i.value for i in items]
    s = sum(values)
    mean = s / count
    variance = sum((v - mean) ** 2 for v in values) / count
    stddev = math.sqrt(variance)
    return {"count": count, "sum": s, "mean": mean, "stddev": stddev}

# ---------- CLI ----------
def build_example_items() -> List[Item]:
    """Buat daftar Item contoh untuk demo CLI."""
    return [
        Item(1, "alpha", 10.0),
        Item(2, "beta", 5.0),
        Item(3, "gamma", 0.0),
        Item(4, "delta", 2.5),
        Item(5, "epsilon", 7.5),
    ]


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Dummy app untuk demo commit ke GitHub")
    p.add_argument("--top", "-t", type=int, default=3, help="Tampilkan top N item berdasarkan value")
    p.add_argument("--normalize", "-n", action="store_true", help="Normalisasikan nilai sehingga total = 1")
    p.add_argument("--json", "-j", action="store_true", help="Keluarkan hasil sebagai JSON")
    return p.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    logger.info("Memulai dummy_app dengan args: %s", args)
    items = build_example_items()

    if args.normalize:
        items = normalize_values(items)

    top = top_n_by_value(items, args.top)
    output = {
        "top": [it.as_dict() for it in top],
        "stats": stats(items),
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print("Top items:")
        for it in top:
            print(f" - ({it.id}) {it.name}: {it.value}")
        print()
        st = output["stats"]
        print(f"Stats — count: {st['count']}, sum: {st['sum']}, mean: {st['mean']}, stddev: {st['stddev']}")

    logger.info("Selesai.")
    return 0

# ---------- ketika dijalankan langsung ----------
if __name__ == "__main__":
    raise SystemExit(main())
