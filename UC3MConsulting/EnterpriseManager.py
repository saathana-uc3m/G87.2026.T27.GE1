import json
from .EnterpriseManagementException import EnterpriseManagementException
from .EnterpriseRequest import EnterpriseRequest

class EnterpriseManager:
    def __init__(self):
        pass

    def ValidateCIF(self, CiF):
        """
        Validates the Spanish CIF (Tax Identification Number) based on
        the organization type and control character calculation.
        """
        # Basic format check: Must be 9 characters [cite: 23]
        if not CiF or len(CiF) != 9:
            return False

        letter = CiF[0].upper()
        block_of_numbers = CiF[1:8]
        control_char = CiF[8].upper()

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

    def ReadproductcodefromJSON(self, fi):
        try:
            with open(fi, encoding="utf-8") as f:
                DATA = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from e

        try:
            T_CIF = DATA["cif"]
            T_PHONE = DATA["phone"]
            E_NAME = DATA["enterprise_name"]
            req = EnterpriseRequest(T_CIF, T_PHONE, E_NAME)
        except KeyError as e:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from e

        # Updated validation call and error message
        if not self.ValidateCIF(T_CIF):
            raise EnterpriseManagementException("Invalid CIF format")

        return req

# TASK 4: Verification Examples [cite: 79]
if __name__ == "__main__":
    manager = EnterpriseManager()

    # 1. Valid CIF Example (A58818501 from the problem statement) [cite: 47]
    valid_cif = "A58818501"
    print(f"Testing Valid CIF ({valid_cif}): {manager.ValidateCIF(valid_cif)}")

    # 2. Non-valid CIF Example
    invalid_cif = "S1234567A"
    print(f"Testing Invalid CIF ({invalid_cif}): {manager.ValidateCIF(invalid_cif)}")