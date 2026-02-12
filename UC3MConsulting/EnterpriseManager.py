"""
This module contains the EnterpriseManager class which provides
functionality for managing enterprise data and validating Spanish
Tax Identification Numbers (CIF).
"""
import json
from .EnterpriseManagementException import EnterpriseManagementException
from .EnterpriseRequest import EnterpriseRequest

class EnterpriseManager:
    """
    EnterpriseManager handles the business logic for enterprise
    registration, including JSON data retrieval and CIF validation
    based on the Spanish organization type rules.
    """
    def __init__(self):
        pass

    def ValidateCIF(self, cif):
        """
            Validates a Spanish CIF code based on official organization rules.

            :param CIF_VAL: A 9-character string representing the CIF to validate.
            :return: True if the CIF follows the calculation rules, False otherwise.
        """
        # Basic format check: Must be 9 characters [cite: 23]
        if not cif or len(cif) != 9:
            return False

        letter = cif[0].upper()
        block_of_numbers = cif[1:8]
        control_char = cif[8].upper()

        # Ensure the central body is 7 digits [cite: 26]
        if not block_of_numbers.isdigit():
            return False

        # Step 1: Add digits in even positions (indices 1, 3, 5) [cite: 30]
        even_sum = sum(int(block_of_numbers[i]) for i in [1, 3, 5])

        # Step 2: Process odd positions (indices 0, 2, 4, 6) [cite: 31]
        odd_sum = 0
        for i in [0, 2, 4, 6]:
            digit = int(block_of_numbers[i])
            multiplied = digit * 2
            # If result is two digits, add them (e.g., 16 -> 1+6=7) [cite: 35]
            if multiplied > 9:
                multiplied = (multiplied // 10) + (multiplied % 10)
            odd_sum += multiplied

        # Step 3: Total Sum [cite: 36]
        total_sum = even_sum + odd_sum

        # Step 4: Base Digit calculation [cite: 37]
        unit_digit = total_sum % 10
        base_digit = 0 if unit_digit == 0 else 10 - unit_digit

        # Step 5: Determination of control character [cite: 38]
        # For A, B, E, H: control is the base digit [cite: 39]
        if letter in ['A', 'B', 'E', 'H']:
            return control_char == str(base_digit)

        # For K, P, Q, S: control is a letter from the mapping table [cite: 40]
        if letter in ['K', 'P', 'Q', 'S']:
            mapping = {
                0: 'J', 1: 'A', 2: 'B', 3: 'C', 4: 'D',
                5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'
            }
            return control_char == mapping.get(base_digit)

        return False

    def ReadProductCodeFromJSON(self, fi):
        """
            Parses a JSON file to extract enterprise data and validate its CIF.

            :param PATH: String representing the file system path to the JSON file.
            :return: An EnterpriseRequest object containing the validated data.
            :raises EnterpriseManagementException: If the file is invalid or
                                                   validation fails.
        """
        try:
            with open(fi, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("Wrong JSON Format") from e

        try:
            t_cif = data["cif"]
            t_phone = data["phone"]
            e_name = data["enterprise_name"]
            req = EnterpriseRequest(t_cif, t_phone, e_name)
        except KeyError as e:
            raise EnterpriseManagementException("Invalid JSON Key") from e

        # Updated validation call and error message
        if not self.ValidateCIF(t_cif):
            raise EnterpriseManagementException("Invalid CIF format")

        return req

# TASK 4: Verification Examples [cite: 79]
if __name__ == "__main__":
    manager = EnterpriseManager()

    # 1. Valid CIF Example (A58818501 from the problem statement) [cite: 47]
    VALID_CIF = "A58818501"
    print(f"Testing Valid CIF ({VALID_CIF}): {manager.ValidateCIF(VALID_CIF)}")

    # 2. Non-valid CIF Example
    INVALID_CIF = "S1234567A"
    print(f"Testing Invalid CIF ({INVALID_CIF}): {manager.ValidateCIF(INVALID_CIF)}")
