class StatisticalAnalyzer:
    def __init__(self, numbers):
        self.numbers = numbers

    def validate_input(self):
        if not isinstance(self.numbers, list):
            raise ValueError("Input must be a list.")

        if len(self.numbers) == 0:
            raise ValueError("Input list cannot be empty.")

        for number in self.numbers:
            if not isinstance(number, (int, float)):
                raise ValueError(
                    "Input must contain only numerical values."
                )

        return True
    def calculate_mean(self):
        total = 0

        for number in self.numbers:
            total += number

        return total / len(self.numbers)

    def calculate_median(self):
        sorted_numbers = sorted(self.numbers)
        n = len(sorted_numbers)

        if n % 2 == 1:
            return sorted_numbers[n // 2]
        else:
            middle1 = sorted_numbers[(n // 2) - 1]
            middle2 = sorted_numbers[n // 2]

            return (middle1 + middle2) / 2

    def calculate_mode(self):
        frequency = {}

        for number in self.numbers:
            if number in frequency:
                frequency[number] += 1
            else:
                frequency[number] = 1

        max_frequency = max(frequency.values())

        if max_frequency == 1:
            return "No unique mode"

        modes = []

        for number, count in frequency.items():
            if count == max_frequency:
                modes.append(number)

        return modes

    def find_minimum(self):
        minimum = self.numbers[0]

        for number in self.numbers:
            if number < minimum:
                minimum = number

        return minimum

    def find_maximum(self):
        maximum = self.numbers[0]

        for number in self.numbers:
            if number > maximum:
                maximum = number

        return maximum

    def count_unique_values(self):
        unique_values = []

        for number in self.numbers:
            if number not in unique_values:
                unique_values.append(number)

        return len(unique_values)

    def display_result(self):
        print("\n================================")
        print("       STATISTICAL REPORT")
        print("================================")

        print(f"Original Data : {self.numbers}")
        print(f"Mean          : {self.calculate_mean():.2f}")
        print(f"Median        : {self.calculate_median()}")
        print(f"Mode          : {self.calculate_mode()}")
        print(f"Minimum       : {self.find_minimum()}")
        print(f"Maximum       : {self.find_maximum()}")
        print(f"Unique Values : {self.count_unique_values()}")

        print("================================")


def main():
    numbers = [10, 20, 20, 30, 40, 50]

    try:
        analyzer = StatisticalAnalyzer(numbers)

        analyzer.validate_input()

        analyzer.display_result()

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()