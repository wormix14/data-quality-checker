import great_expectations as gx
from main import load_df
from datetime import datetime


def prepare_gx(layer: str):
    context = gx.get_context(mode="ephemeral")
    df = load_df(layer)

    data_source = context.data_sources.add_pandas("pandas")
    data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")

    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch definition")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    suite = context.suites.add(
        gx.core.expectation_suite.ExpectationSuite(name="expectations")
    )
    return batch, suite, list(df.columns)

def format_report(layer_name: str, validation_result) -> str:
    status = "✅ PASSED" if validation_result.success else "❌ FAILED"
    lines = [f"<b>Layer: {layer_name}</b> — {status}\n"]

    for res in validation_result.results:
        col = res.expectation_config.kwargs.get("column", "table")
        exp_type = res.expectation_config.type.replace("expect_column_values_to_", "")
        bad_count = res.result.get("unexpected_count", 0)
        bad_pct = res.result.get("unexpected_percent", 0.0)
        mark = "🟢" if res.success else "🔴"

        lines.append(f"{mark} <code>{col}</code> ({exp_type}): {bad_count} bad ({bad_pct:.2f}%)")

    return "\n".join(lines)

def validate_bronze():
    batch, suite, _ = prepare_gx("bronze_taxi")

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="passenger_count",
            min_value= 1,
            severity="warning",
            mostly=0.95
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="total_amount",
            min_value=0,
            strict_min=True,
            mostly=0.95
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="fare_amount",
            min_value=0,
            mostly=0.95
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="trip_distance",
            min_value=0,
            strict_min=True,
            mostly=0.95
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="tpep_pickup_datetime",
            min_value=datetime(2024, 1, 1),
            max_value=datetime(2025, 1, 1),
            strict_max=True,
            mostly=0.95
        )
    )

    validation_result = batch.validate(suite)
    return format_report("bronze_taxi", validation_result)

def validate_silver():
    batch, suite, columns = prepare_gx("silver_taxi")

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="passenger_count",
            min_value= 0,
            severity="warning",
            mostly=1.0
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="total_amount",
            min_value=0,
            strict_min=True,
            mostly=1.0
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="fare_amount",
            min_value=0,
            mostly=1.0
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="trip_distance",
            min_value=0,
            strict_min=True,
            mostly=1.0
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="tpep_pickup_datetime",
            min_value=datetime(2024, 1, 1),
            max_value=datetime(2025, 1, 1),
            strict_max=True,
            mostly=1.0
        )
    )
    
    for col in columns:
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(
                column=col,
                mostly=1.0
            )
        )
    validation_result = batch.validate(suite)

    return format_report("silver_taxi", validation_result)

def validate_gold():
    batch, suite, columns = prepare_gx("gold_taxi")

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="date",
            min_value=datetime(2024, 1, 1).date(),
            max_value=datetime(2025, 1, 1).date(),
            strict_max=True,
            mostly=1.0
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="total_revenue",
            min_value=0,
            strict_min=True,
            mostly=1.0,
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="avg_distance",
            min_value=0,
            strict_min=True,
            mostly=1.0
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="trip_count",
            min_value=1,
            mostly=1.0
        )
    )

    for col in columns:
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(
                column=col,
                mostly=1.0
            )
        )
    validation_result = batch.validate(suite)
    return format_report("gold_taxi", validation_result)

