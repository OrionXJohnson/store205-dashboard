"""
test_sales_analytics.py

Manual testing for sales analytics functions.

Run from project root:
    python analytics/test_sales_analytics.py
"""

from sales_analytics import (
    get_department_sales_breakdown,
    get_store_sales_summary,
    get_no_sales_id_summary,
    get_store_sales_rank,
    get_store_sales_comparison,
)

def print_summary(period_type: str) -> None:
    """Print Store 205 sales summary."""
    summary = get_store_sales_summary(
        store_id=205,
        period_type=period_type,
    )

    print(f"\nStore 205 Sales Summary - {period_type}")
    print("----------------------------------------")

    if not summary:
        print("No data found.")
        return

    print(f"Sales: ${summary['sales_amount']:,.2f}")
    print(f"Transactions: {summary['transaction_count']}")
    print(
        f"Average transaction: "
        f"${summary['average_transaction']:,.2f}"
    )
    print(
        f"Service plan sales: "
        f"${summary['service_plan_sales']:,.2f}"
    )
    print(f"ESET quantity: {summary['eset_quantity']}")
    print(f"Office quantity: {summary['office_quantity']}")

def print_department_breakdown(period_type: str) -> None:
    """Print Store 205 department sales breakdown."""
    departments = get_department_sales_breakdown(
        store_id=205,
        period_type=period_type,
    )

    print(f"\nStore 205 Department Breakdown - {period_type}")
    print("----------------------------------------")

    if not departments:
        print("No department totals found.")
        return

    for department in departments:
        print(
            f"{department['department_name']} "
            f"({department['department_code']}) | "
            f"Sales: ${department['sales_amount']:,.2f} | "
            f"Transactions: {department['transaction_count']} | "
            f"SP Sales: ${department['service_plan_sales']:,.2f}"
        )

def print_no_sales_id_summary(period_type: str) -> None:
    """Print No Sales ID / unattributed sales summary."""
    summary = get_no_sales_id_summary(
        store_id=205,
        period_type=period_type,
    )

    print(f"\nStore 205 No Sales ID Summary - {period_type}")
    print("----------------------------------------")

    if not summary:
        print("No No Sales ID row found.")
        return

    print(f"No Sales ID sales: ${summary['no_sales_amount']:,.2f}")
    print(f"No Sales ID transactions: {summary['no_sales_transactions']}")
    print(f"Share of store sales: {summary['sales_share']:.2%}")
    print(f"Share of store transactions: {summary['transaction_share']:.2%}")

def print_store_sales_ranks(period_type: str) -> None:
    """Print Store 205 sales ranks for key metrics."""
    metrics = [
        "sales_amount",
        "transaction_count",
        "average_transaction",
        "no_sales_share",
    ]

    print(f"\nStore 205 Sales Ranks - {period_type}")
    print("----------------------------------------")

    for metric in metrics:
        rank_info = get_store_sales_rank(
            store_id=205,
            period_type=period_type,
            metric=metric,
        )

        if not rank_info["found"]:
            print(f"{metric}: Store 205 not found")
            continue

        value = rank_info["metric_value"]

        if metric == "no_sales_share":
            formatted_value = f"{value:.2%}"
        elif metric in {"sales_amount", "average_transaction"}:
            formatted_value = f"${value:,.2f}"
        else:
            formatted_value = f"{value:,.0f}"

        print(
            f"{metric}: "
            f"#{rank_info['rank']} of {rank_info['total_stores']} | "
            f"Value: {formatted_value}"
        )

def print_store_sales_comparison(period_type: str) -> None:
    """Print top stores by total sales."""
    stores = get_store_sales_comparison(
        period_type=period_type,
        limit=10,
        order_by="sales_amount",
    )

    print(f"\nTop Stores by Total Sales - {period_type}")
    print("----------------------------------------")

    if not stores:
        print("No store total rows found.")
        return

    for index, store in enumerate(stores, start=1):
        marker = " <= Store 205" if store["store_id"] == 205 else ""

        print(
            f"{index}. Store {store['store_id']} | "
            f"Sales: ${store['sales_amount']:,.2f} | "
            f"Transactions: {store['transaction_count']:,} | "
            f"Avg Transaction: ${store['average_transaction']:,.2f} | "
            f"No Sales ID: {store['no_sales_share']:.2%}"
            f"{marker}"
        )


def main() -> None:
    """Run sales analytics tests."""
    for period_type in [
        "daily",
        "pay_period_to_date",
        "month_to_date",
        "quarter_to_date",
    ]:
        print_summary(period_type)
        print_department_breakdown(period_type)
        print_no_sales_id_summary(period_type)
        print_store_sales_ranks(period_type)
        print_store_sales_comparison(period_type)


if __name__ == "__main__":
    main()