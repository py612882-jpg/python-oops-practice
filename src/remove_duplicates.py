class RemoveDuplicates:
    """
    Class to remove duplicate values from a list.
    """

    def __init__(self, numbers):
        """
        Constructor to initialize the list.
        """
        self.numbers = numbers

    def validate_input(self):
        """
        Validate that input is a list.
        """
        if not isinstance(self.numbers, list):
            raise TypeError("Input must be a list.")

    def remove_duplicates(self):
        """
        Remove duplicate values while keeping order.
        """
        unique_numbers = []

        for number in self.numbers:
            if number not in unique_numbers:
                unique_numbers.append(number)

        return unique_numbers

    def display_result(self):
        """
        Display original and unique lists.
        """
        unique = self.remove_duplicates()

        print("Original List :", self.numbers)
        print("Unique List   :", unique)


def main():
    numbers = [10, 20, 10, 30, 40, 20, 50, 30]

    obj = RemoveDuplicates(numbers)

    try:
        obj.validate_input()
        obj.display_result()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()