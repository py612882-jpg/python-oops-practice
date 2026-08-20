import numbers

import pandas as pd


class PandasDataAnalyzer:
    """Create, clean, inspect, and analyze customer data with Pandas."""

    REQUIRED_COLUMNS = ["Customer", "Age", "Income", "Experience", "Purchased"]

    def __init__(self, data):
        self.data = data
        self.df = None
        self.cleaned_df = None

    def validate_input(self):
        """Validate the input records and required customer fields."""
        if not isinstance(self.data, list):
            raise TypeError("Dataset must be a list of records.")
        if not self.data:
            raise ValueError("Dataset cannot be empty.")
        if not all(isinstance(record, dict) for record in self.data):
            raise TypeError("Each record must be a dictionary.")

        first_columns = set(self.data[0])
        if any(set(record) != first_columns for record in self.data):
            raise ValueError("All records must contain the same columns.")

        missing_columns = [
            column for column in self.REQUIRED_COLUMNS if column not in first_columns
        ]
        if missing_columns:
            raise ValueError(
                "Missing required columns: " + ", ".join(missing_columns)
            )

        for record in self.data:
            for column in ("Age", "Income", "Experience", "Purchased"):
                value = record[column]
                if pd.notna(value) and (
                    isinstance(value, bool) or not isinstance(value, numbers.Number)
                ):
                    raise TypeError(f"{column} must contain numeric values.")

        return True

    def create_dataframe(self):
        """Convert the input records to the original DataFrame."""
        self.df = pd.DataFrame(self.data, columns=self.REQUIRED_COLUMNS)
        return self.df

    def _require_dataframe(self):
        if self.df is None:
            self.create_dataframe()

    def _require_cleaned_dataframe(self):
        self._require_dataframe()
        if self.cleaned_df is None:
            self.cleaned_df = self.df.copy()

    def get_dataset_info(self):
        """Display and return the original DataFrame structure."""
        self._require_dataframe()
        info = {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "column_names": list(self.df.columns),
            "dtypes": self.df.dtypes,
            "shape": self.df.shape,
        }
        print("Rows:", info["rows"])
        print("Columns:", info["columns"])
        print("Column Names:", info["column_names"])
        print("Data Types:\n", info["dtypes"])
        print("Shape:", info["shape"])
        return info

    def find_missing_values(self):
        """Return the original rows containing at least one missing value."""
        self._require_dataframe()
        missing_rows = self.df[self.df.isna().any(axis=1)]
        print("Missing Values:\n", self.df.isna())
        return missing_rows

    def count_missing_values(self):
        """Return missing-value counts for every original column."""
        self._require_dataframe()
        counts = self.df.isna().sum()
        print("Missing Value Counts:\n", counts)
        return counts

    def find_duplicates(self):
        """Return duplicate records beyond their first occurrence."""
        self._require_dataframe()
        duplicates = self.df[self.df.duplicated(keep="first")]
        print("Duplicate Records:\n", duplicates)
        return duplicates

    def remove_duplicates(self):
        """Remove duplicates into a copy while preserving the original DataFrame."""
        self._require_dataframe()
        self.cleaned_df = self.df.drop_duplicates().reset_index(drop=True)
        return self.cleaned_df

    def fill_missing_values(self):
        """Impute missing Income values with the cleaned Income mean."""
        self._require_cleaned_dataframe()
        income_mean = self.cleaned_df["Income"].mean()
        self.cleaned_df.loc[:, "Income"] = self.cleaned_df["Income"].fillna(
            income_mean
        )
        return self.cleaned_df

    def filter_customers(self, min_income):
        """Return cleaned customers whose income meets the minimum."""
        self._require_cleaned_dataframe()
        if not isinstance(min_income, numbers.Number):
            raise TypeError("Minimum income must be numeric.")
        return self.cleaned_df[self.cleaned_df["Income"] >= min_income]

    def sort_by_income(self, ascending=True):
        """Return cleaned records sorted by Income."""
        self._require_cleaned_dataframe()
        if not isinstance(ascending, bool):
            raise TypeError("Ascending must be a boolean.")
        return self.cleaned_df.sort_values("Income", ascending=ascending).reset_index(
            drop=True
        )

    def calculate_statistics(self):
        """Return mean, minimum, maximum, and standard deviation by numeric column."""
        self._require_cleaned_dataframe()
        numeric_columns = ["Age", "Income", "Experience", "Purchased"]
        statistics = pd.DataFrame(
            {
                "Mean": self.cleaned_df[numeric_columns].mean(),
                "Minimum": self.cleaned_df[numeric_columns].min(),
                "Maximum": self.cleaned_df[numeric_columns].max(),
                "Std Dev": self.cleaned_df[numeric_columns].std(),
            }
        )
        return statistics

    def analyze_features(self):
        """Display and return statistics for all requested numeric features."""
        statistics = self.calculate_statistics()
        print("Feature Statistics:\n", statistics)
        return statistics

    def analyze_target(self):
        """Count purchased and not-purchased customers."""
        self._require_cleaned_dataframe()
        counts = {
            "Purchased": int((self.cleaned_df["Purchased"] == 1).sum()),
            "Not Purchased": int((self.cleaned_df["Purchased"] == 0).sum()),
        }
        print("Purchase Analysis:", counts)
        return counts

    def perform_eda(self):
        """Return the main business metrics for the cleaned dataset."""
        self._require_cleaned_dataframe()
        eda = {
            "customer_count": len(self.cleaned_df),
            "average_age": self.cleaned_df["Age"].mean(),
            "average_income": self.cleaned_df["Income"].mean(),
            "highest_income": self.cleaned_df["Income"].max(),
            "average_experience": self.cleaned_df["Experience"].mean(),
            "number_of_purchasers": int(
                (self.cleaned_df["Purchased"] == 1).sum()
            ),
        }
        print("EDA Summary:", eda)
        return eda

    def group_by_purchase_status(self):
        """Summarize customer metrics separately by purchase status."""
        self._require_cleaned_dataframe()
        grouped = self.cleaned_df.groupby("Purchased").agg(
            Customer_Count=("Customer", "count"),
            Average_Age=("Age", "mean"),
            Average_Income=("Income", "mean"),
            Average_Experience=("Experience", "mean"),
        )
        print("Purchase Status Groups:\n", grouped)
        return grouped

    def display_report(self):
        """Display the complete customer analysis report."""
        self._require_cleaned_dataframe()
        statistics = self.calculate_statistics()
        target_counts = self.analyze_target()
        print("=" * 60)
        print("CUSTOMER DATA ANALYSIS")
        print("=" * 60)
        print("Original Dataset Shape:", self.df.shape)
        print("Missing Income Values:", int(self.count_missing_values()["Income"]))
        print("Duplicate Records:", len(self.find_duplicates()))
        print("Rows After Cleaning:", len(self.cleaned_df))
        print("\nFeature Statistics:")
        print(statistics.round(4))
        print("\nPurchase Analysis:")
        print("Purchased:", target_counts["Purchased"])
        print("Not Purchased:", target_counts["Not Purchased"])
        print("=" * 60)


def main():
    data = [
        {"Customer": "C001", "Age": 25, "Income": 30000, "Experience": 2, "Purchased": 0},
        {"Customer": "C002", "Age": 30, "Income": 45000, "Experience": 5, "Purchased": 1},
        {"Customer": "C003", "Age": 35, "Income": None, "Experience": 8, "Purchased": 1},
        {"Customer": "C004", "Age": 40, "Income": 80000, "Experience": 12, "Purchased": 1},
        {"Customer": "C005", "Age": 45, "Income": 100000, "Experience": 15, "Purchased": 0},
        {"Customer": "C002", "Age": 30, "Income": 45000, "Experience": 5, "Purchased": 1},
    ]

    try:
        analyzer = PandasDataAnalyzer(data)
        analyzer.validate_input()
        analyzer.create_dataframe()
        analyzer.get_dataset_info()
        analyzer.find_missing_values()
        analyzer.find_duplicates()
        analyzer.remove_duplicates()
        analyzer.fill_missing_values()
        print("\nFiltered Customers:\n", analyzer.filter_customers(50000))
        print("\nSorted Customers:\n", analyzer.sort_by_income())
        analyzer.analyze_features()
        analyzer.perform_eda()
        analyzer.analyze_target()
        analyzer.display_report()
    except (TypeError, ValueError, KeyError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()