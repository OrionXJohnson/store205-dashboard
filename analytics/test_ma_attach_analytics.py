"""
test_ma_attach_analytics.py

Manual test for MA Attach analytics.

Run from project root:
    python analytics/test_ma_attach_analytics.py
"""

from ma_attach_analytics import (
    get_ma_attach_store_summary,
    get_top_ma_attach_associates,
)


def print_summary(period_type: str) -> None:
    """Print Store 205 MA Attach summary for one period."""
    summary = get_ma_attach_store_summary(
        store_id=205,
        period_type=period_type,
    )

    print(f"\nStore 205 MA Attach Summary - {period_type}")
    print("----------------------------------------")

    if summary is None:
        print("No store summary found.")
        return

    print(f"Computers: {summary['computers']}")
    print(f"UPT: {summary['upt']:.2f}")
    print(f"Attach revenue: ${summary['attach_revenue']:,.2f}")
    print(f"Attach GM$: ${summary['attach_gm']:,.2f}")
    print(f"ESET quantity: {summary['eset_quantity']}")
    print(f"Office quantity: {summary['office_quantity']}")
    print(f"Service plan quantity: {summary['service_plan_quantity']}")


def print_top_associates(period_type: str) -> None:
    """Print top Store 205 MA Attach associates."""
    associates = get_top_ma_attach_associates(
        store_id=205,
        period_type=period_type,
        limit=5,
        order_by="attach_revenue",
        minimum_computers=1,
    )

    print(f"\nTop Store 205 MA Attach Associates - {period_type}")
    print("----------------------------------------")

    if not associates:
        print("No associate rows found.")
        return

    for index, associate in enumerate(associates, start=1):
        print(
            f"{index}. {associate['associate_name']} | "
            f"Computers: {associate['computers']} | "
            f"UPT: {associate['upt']:.2f} | "
            f"Attach revenue: ${associate['attach_revenue']:,.2f} | "
            f"Attach GM$: ${associate['attach_gm']:,.2f}"
        )


def main() -> None:
    """Run MA Attach analytics tests."""
    for period_type in [
        "daily",
        "pay_period_to_date",
        "month_to_date",
    ]:
        print_summary(period_type)
        print_top_associates(period_type)


if __name__ == "__main__":
    main()