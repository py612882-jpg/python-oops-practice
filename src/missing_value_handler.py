class MissingValueHandler:

    def __init__(self, data):
        self.data = data
        self.cleaned_data = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError("Dataset contains invalid values.")

        return True

    def find_missing_indexes(self):
        indexes = []

        for index, value in enumerate(self.data):
            if value is None:
                indexes.append(index)

        return indexes

    def count_missing_values(self):
        return len(self.find_missing_indexes())

    def calculate_mean(self):
        total = 0
        count = 0

        for value in self.data:
            if value is not None:
                total += value
                count += 1

        if count == 0:
            raise ValueError(
                "Cannot calculate mean because all values are missing."
            )

        return total / count

    def fill_missing_values(self):
        mean = self.calculate_mean()

        self.cleaned_data = []

        for value in self.data:
            if value is None:
                self.cleaned_data.append(mean)
            else:
                self.cleaned_data.append(value)

        return self.cleaned_data

    def display_report(self):
        missing_indexes = self.find_missing_indexes()
        missing_values = len(missing_indexes)
        total_values = len(self.data)
        available_values = total_values - missing_values
        mean = self.calculate_mean()
        cleaned_data = self.fill_missing_values()

        print("\n        MISSING VALUE REPORT")
        print("========================================")

        print("Original Data:")
        print(self.data)

        print()
        print(f"Total Values       : {total_values}")
        print(f"Missing Values     : {missing_values}")
        print(f"Missing Indexes    : {missing_indexes}")
        print(f"Available Values   : {available_values}")
        print(f"Mean               : {mean}")

        print()
        print("Cleaned Data:")
        print(cleaned_data)

        print("========================================")


def main():
    data = [25, 30, None, 40, None, 35, 28]

    try:
        obj = MissingValueHandler(data)

        obj.validate_input()

        obj.display_report()

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()