"""
test_systems_analytics.py

Manual test for Systems analytics.

Run from project root:
    python analytics/test_systems_analytics.py
"""

from systems_analytics import (
    get_store_systems_summary,
    get_top_rpu_associates,
    get_top_attach_rpu_associates,
    get_store_rpu_comparison,
    get_store_systems_rank,
)


def print_summary(period_type: str) -> None:
    """Print Store 205 Systems summary for one period."""
    summary = get_store_systems_summary(
        store_id=205,
        period_type=period_type,
    )

    print(f"\nStore 205 Systems Summary - {period_type}")
    print("----------------------------------------")

    if not summary["found"]:
        print("No store total row found.")
        return

    print(f"Primary units: {summary['primary_units']}")
    print(f"ASP: ${summary['asp']:,.2f}")
    print(f"RPU: ${summary['rpu']:,.2f}")
    print(f"Total attach RPU: ${summary['total_attach_rpu']:,.2f}")
    print(
        "Service plans attach: "
        f"{summary['service_plans_attach_percent']:.2%}"
    )
    print(f"ESET attach: {summary['eset_attach_percent']:.2%}")
    print(f"Office attach: {summary['office_attach_percent']:.2%}")

def print_top_rpu_associates(period_type: str) -> None:
    """Print top Store 205 Systems associates by RPU."""
    associates = get_top_rpu_associates(
        store_id=205,
        period_type=period_type,
        limit=5,
    )

    print(f"\nTop Store 205 RPU Associates - {period_type}")
    print("----------------------------------------")

    if not associates:
        print("No associate rows found.")
        return

    for index, associate in enumerate(associates, start=1):
        print(
            f"{index}. {associate['associate_name']} | "
            f"Units: {associate['primary_units']} | "
            f"RPU: ${associate['rpu']:,.2f} | "
            f"Attach RPU: ${associate['total_attach_rpu']:,.2f}"
        )

def print_top_attach_rpu_associates(period_type: str) -> None:
    """Print top Store 205 Systems associates by attach RPU."""
    associates = get_top_attach_rpu_associates(
        store_id=205,
        period_type=period_type,
        limit=5,
        minimum_primary_units=3,
    )

    print(f"\nTop Store 205 Attach RPU Associates - {period_type}")
    print("----------------------------------------")

    if not associates:
        print("No associate rows found.")
        return

    for index, associate in enumerate(associates, start=1):
        print(
            f"{index}. {associate['associate_name']} | "
            f"Units: {associate['primary_units']} | "
            f"Attach RPU: ${associate['total_attach_rpu']:,.2f} | "
            f"RPU: ${associate['rpu']:,.2f} | "
            f"ESET: {associate['eset_attach_percent']:.2%}"
        )

def print_store_rpu_comparison(period_type: str) -> None:
    """Print store-level Systems RPU comparison."""
    stores = get_store_rpu_comparison(
        period_type=period_type,
        limit=10,
    )

    print(f"\nTop Stores by Systems RPU - {period_type}")
    print("----------------------------------------")

    if not stores:
        print("No store total rows found.")
        return

    for index, store in enumerate(stores, start=1):
        marker = " <= Store 205" if store["store_id"] == 205 else ""

        print(
            f"{index}. Store {store['store_id']} | "
            f"Units: {store['primary_units']} | "
            f"RPU: ${store['rpu']:,.2f} | "
            f"Attach RPU: ${store['total_attach_rpu']:,.2f}"
            f"{marker}"
        )

def print_store_rank(period_type: str) -> None:
    """Print Store 205 Systems ranks for key metrics."""
    metrics = [
        "rpu",
        "total_attach_rpu",
        "asp",
        "primary_units",
    ]

    print(f"\nStore 205 Systems Ranks - {period_type}")
    print("----------------------------------------")

    for metric in metrics:
        rank_info = get_store_systems_rank(
            store_id=205,
            period_type=period_type,
            metric=metric,
        )

        if not rank_info["found"]:
            print(f"{metric}: Store 205 not found")
            continue

        print(
            f"{metric}: "
            f"#{rank_info['rank']} of {rank_info['total_stores']} | "
            f"Value: {rank_info['metric_value']:,.2f}"
        )

def main() -> None:
    """Run test summaries."""
    for period_type in [
        "daily",
        "pay_period_to_date",
        "month_to_date",
    ]:
        print_summary(period_type)
        print_top_rpu_associates(period_type)
        print_top_attach_rpu_associates(period_type)
        print_store_rpu_comparison(period_type)
        print_store_rank(period_type)


if __name__ == "__main__":
    main()