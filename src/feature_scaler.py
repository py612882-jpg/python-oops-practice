class FeatureScaler:
    """
    A class to perform Min-Max Feature Scaling.
    """

    def __init__(self, data):
        self.data = data
        self.scaled_data = None

    def validate_input(self):
        """
        Validate that input is a non-empty list
        containing only numerical values.
        """
        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if not isinstance(value, (int, float)):
                raise ValueError("Dataset contains invalid values.")

    def find_minimum(self):
        """
        Find and return the minimum value.
        """
        return min(self.data)

    def find_maximum(self):
        """
        Find and return the maximum value.
        """
        return max(self.data)

    def scale_data(self):
        """
        Apply Min-Max Scaling to the data.
        Formula:
        (value - minimum) / (maximum - minimum)
        """
        minimum = self.find_minimum()
        maximum = self.find_maximum()

        if minimum == maximum:
            raise ValueError(
                "Cannot scale data because all values are identical."
            )

        self.scaled_data = []

        for value in self.data:
            scaled_value = (value - minimum) / (maximum - minimum)
            self.scaled_data.append(scaled_value)

        return self.scaled_data

    def display_report(self):
        """
        Display the feature scaling report.
        """
        minimum = self.find_minimum()
        maximum = self.find_maximum()
        scaled = self.scale_data()

        print("\n========================================")
        print("       FEATURE SCALING REPORT")
        print("========================================")

        print(f"Original Data : {self.data}")
        print(f"Minimum       : {minimum}")
        print(f"Maximum       : {maximum}")
        print(f"Scaled Data   : {scaled}")

        print("========================================")


def main():
    data = [10, 20, 30, 40, 50]

    try:
        obj = FeatureScaler(data)

        obj.validate_input()
        obj.display_report()

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()