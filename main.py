from dashboard.aggregator import aggregate_all
from dashboard.transformer import transform_all
from dashboard.summary import generate_summary, print_summary
from dashboard.exporter import export_all


if __name__ == "__main__":
    print("=" * 60)
    print("  OBSERVABILITY DASHBOARD")
    print("=" * 60)

    # Step 1: Aggregate
    print("\n📥 Aggregating data sources...")
    aggregated = aggregate_all()

    # Step 2: Transform
    print("\n⚙️  Transforming data...")
    transformed = transform_all(aggregated)

    # Step 3: Summarize
    print("\n📊 Generating ecosystem summary...")
    summary = generate_summary(transformed)

    # Step 4: Export
    print("\n📤 Exporting outputs...")
    export_all(summary, transformed)

    # Step 5: Print Dashboard
    print_summary(summary)

    print("\n  Exports available in /exports:")
    print("    → dashboard_summary.json  — Full JSON summary")
    print("    → dashboard_export.csv    — Power BI ready CSV")
    print("    → powerbi_dataset.json    — Power BI JSON dataset")
    print("=" * 60)