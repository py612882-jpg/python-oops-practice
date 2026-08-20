import numbers

import numpy as np


class NumpyDatasetAnalyzer:
    """Analyze and prepare a numerical 2D dataset for machine learning."""

    def __init__(self, data):
        self.data = data
        self.array = None

    def validate_input(self):
        """Validate that the dataset is a non-empty rectangular numeric list."""
        if not isinstance(self.data, list):
            raise TypeError("Dataset must be a list of rows.")

        if not self.data:
            raise ValueError("Dataset cannot be empty.")

        if not all(isinstance(row, list) for row in self.data):
            raise TypeError("Each row must be a list.")

        column_count = len(self.data[0])
        if column_count == 0:
            raise ValueError("Dataset must contain at least one column.")

        if any(len(row) != column_count for row in self.data):
            raise ValueError(
                "All rows must contain the same number of columns."
            )

        if any(
            isinstance(value, bool)
            or not isinstance(value, numbers.Number)
            for row in self.data
            for value in row
        ):
            raise TypeError("Dataset contains non-numeric values.")

    def convert_to_array(self):
        """Convert the validated Python list to a NumPy array."""
        self.array = np.array(self.data)
        return self.array

    def _require_array(self):
        if self.array is None:
            self.convert_to_array()

    def get_dataset_info(self):
        """Return and display the basic dimensions and storage information."""
        self._require_array()
        info = {
            "rows": self.array.shape[0],
            "columns": self.array.shape[1],
            "dimensions": self.array.ndim,
            "size": self.array.size,
            "data_type": self.array.dtype,
        }

        print("Rows:", info["rows"])
        print("Columns:", info["columns"])
        print("Dimensions:", info["dimensions"])
        print("Size:", info["size"])
        print("Data Type:", info["data_type"])
        return info

    def get_column(self, column_index):
        """Return one feature column by index."""
        self._require_array()
        return self.array[:, column_index]

    def get_row(self, row_index):
        """Return one dataset row by index."""
        self._require_array()
        return self.array[row_index, :]

    def calculate_column_mean(self):
        self._require_array()
        return np.mean(self.array, axis=0)

    def calculate_column_minimum(self):
        self._require_array()
        return np.min(self.array, axis=0)

    def calculate_column_maximum(self):
        self._require_array()
        return np.max(self.array, axis=0)

    def calculate_column_std(self):
        self._require_array()
        return np.std(self.array, axis=0)

    def scale_features(self):
        """Apply independent Min-Max scaling to every feature column."""
        self._require_array()
        minimum = self.calculate_column_minimum()
        maximum = self.calculate_column_maximum()
        ranges = maximum - minimum

        scaled = np.zeros_like(self.array, dtype=float)
        np.divide(
            self.array - minimum,
            ranges,
            out=scaled,
            where=ranges != 0,
        )
        return scaled

    def feature_summary(self):
        """Return feature-wise mean, minimum, maximum, and standard deviation."""
        summary = {
            "mean": self.calculate_column_mean(),
            "minimum": self.calculate_column_minimum(),
            "maximum": self.calculate_column_maximum(),
            "standard_deviation": self.calculate_column_std(),
        }

        print("Feature Summary:")
        for name, values in summary.items():
            print(f"{name.replace('_', ' ').title()}: {values}")
        return summary

    def split_features_target(self, target_index=-1):
        """Return the remaining columns as X and the selected column as y."""
        self._require_array()
        if not isinstance(target_index, (int, np.integer)):
            raise TypeError("Target index must be an integer.")

        column_count = self.array.shape[1]
        if target_index < -column_count or target_index >= column_count:
            raise IndexError("Target index is out of range.")

        target_column = target_index % column_count
        features = np.delete(self.array, target_column, axis=1)
        target = self.array[:, target_column]
        return features, target

    def display_report(self):
        """Display the complete dataset analysis report."""
        self._require_array()
        print("=" * 55)
        print("          NUMPY DATASET ANALYSIS REPORT")
        print("=" * 55)
        print("\nOriginal Data:")
        print(self.array)
        print("\nDataset Information:")
        self.get_dataset_info()
        print("\nFeature Summary:")
        summary = {
            "Mean": self.calculate_column_mean(),
            "Minimum": self.calculate_column_minimum(),
            "Maximum": self.calculate_column_maximum(),
            "Standard Deviation": self.calculate_column_std(),
        }
        for name, values in summary.items():
            print(f"{name}: {np.round(values, 4)}")
        print("\nScaled Features:")
        print(np.round(self.scale_features(), 4))
        print("\n" + "=" * 55)


def main():
    data = [
        [25, 30000, 2],
        [30, 45000, 5],
        [35, 60000, 8],
        [40, 80000, 12],
        [45, 100000, 15],
    ]

    try:
        analyzer = NumpyDatasetAnalyzer(data)
        analyzer.validate_input()
        analyzer.convert_to_array()
        analyzer.display_report()
    except (TypeError, ValueError, IndexError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()