import pandas as pd
import plotly.express as px

def _is_numeric(series):
    return pd.api.types.is_numeric_dtype(series)

def _is_date_like(col_name, series):
    if any(k in col_name.lower() for k in ("date", "year", "month", "time")):
        return True
    return pd.api.types.is_datetime64_any_dtype(series)

def auto_visualize(df: pd.DataFrame):
    """Type-aware chart selection: returns a Plotly fig, markdown string, or DataFrame."""
    if df.empty:
        return "No data returned for this query."

    cols = df.columns.tolist()

    # KPI: exactly one cell
    if df.shape == (1, 1):
        return f"### 📊 Result: **{df.iloc[0, 0]}**"

    numeric_cols = [c for c in cols if _is_numeric(df[c])]
    date_cols    = [c for c in cols if _is_date_like(c, df[c])]
    cat_cols     = [c for c in cols if c not in numeric_cols and c not in date_cols]

    # 1) Time series: date column + numeric column(s)
    if date_cols and numeric_cols:
        return px.line(df, x=date_cols[0], y=numeric_cols,
                       title="Trend over time", markers=True)

    # 2) Bar chart: category + numeric  (ONLY when a number exists!)
    if cat_cols and numeric_cols:
        return px.bar(df, x=cat_cols[0], y=numeric_cols[0],
                      title=f"{numeric_cols[0]} by {cat_cols[0]}", text_auto=True)

    # 3) All-text result (names, emails, lists) → clean table
    return df