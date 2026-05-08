import pandas as pd
import io

def process_csv(file_content):
    try:
        df = pd.read_csv(io.BytesIO(file_content))
        result = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "data_types": df.dtypes.astype(str).to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "numeric_summary": {}
        }
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            for col in numeric_df.columns:
                result["numeric_summary"][col] = {
                    "mean": float(numeric_df[col].mean()),
                    "min": float(numeric_df[col].min()),
                    "max": float(numeric_df[col].max()),
                    "std": float(numeric_df[col].std())
                }
        return result
    except Exception as e:
        return {"error": str(e)}
