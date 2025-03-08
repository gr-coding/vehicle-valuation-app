import pytest

from helpers.car_valuation_helper import CarValuationHelper
from helpers.file_helper import FileHelper
from pages.car_details_page import CarDetailsPage
from pathlib import Path


from utils.custom_log import CustomLog

c_logger = CustomLog.log_gen()


def get_input_files():
    """
    Returns list of input text file paths as string from the following location -  'test_data/input'

    """
    file_path = Path("test_data/input")
    input_files = [str(file) for file in file_path.glob("*txt")]
    return input_files


class TestCarDetails:
    @pytest.mark.parametrize('input_file', get_input_files())
    def test_car_details_by_reg(self, t_config, input_file):
        """
        Test verifies given UK vehicle registration numbers from one or more input files, by extracting and comparing
        the unique reg numbers with the expected test data from the given output file,gets the vehicle details by searching using
        vehicle reg numbers in confused.com and validates any data mismatch, reg number not found errors.
        """

        # url details
        url = t_config.url

        # path to expected output test data
        exp_output_file_path = Path("test_data/exp_output")
        exp_output_file = exp_output_file_path / "car_output - V5.txt"

        file_helper = FileHelper()
        car_valuation_helper = CarValuationHelper()

        # unpacking input and output test data
        expected_file_data = file_helper.read_csv_file(exp_output_file, ["VARIANT_REG", "MAKE_MODEL", "YEAR"])
        uk_vehicle_reg_data = file_helper.extract_uk_vehicle_reg_num(input_file)

        # checking UK vehicle registration number(s) exist
        if not uk_vehicle_reg_data:
            pytest.fail(f"No UK Registration numbers found in {input_file}")

        reg_not_found_list = []
        mismatch_list = []
        match_list = []
        exp_vehicle_data = {}

        # comparing input and output data for valid UK reg data
        for vehicle in expected_file_data:
            vehicle_reg_number = vehicle["VARIANT_REG"].replace(" ", "")
            exp_vehicle_data[vehicle_reg_number] = vehicle

        t_config.driver.get(url)
        car_details_page = CarDetailsPage(t_config.driver)

        # verifying vehicle details for matching records
        for reg_number in uk_vehicle_reg_data:
            reg_number = reg_number.replace(" ", "")
            matching_vehicle = exp_vehicle_data.get(reg_number, None)

            if matching_vehicle:
                data_passed = car_valuation_helper.verify_vehicle_details(
                    car_details_page, reg_number, matching_vehicle, mismatch_list, reg_not_found_list)

                if not data_passed:
                    mismatch_list.append(reg_number)
                else:
                    match_list.append(reg_number)
            else:
                reg_not_found_list.append(reg_number)

        # checking for any mismatched, not found UK reg numbers
        if not reg_not_found_list and not mismatch_list:
            c_logger.info(f"All reg number(s) passed verification - {match_list}")

        if reg_not_found_list or mismatch_list:
            # failing for not found UK reg records in confused.com
            if reg_not_found_list:
                c_logger.info(f"Following reg number(s) not found in the expected output file - {reg_not_found_list}")
                if not car_valuation_helper.verify_records_with_no_match(car_details_page, reg_not_found_list):
                    pytest.fail("Reg number(s) not found in gocoma")

            # failing for mismatched reg records
            if mismatch_list:
                c_logger.info(f"data mismatch found - {mismatch_list}")
            pytest.fail("Reg number(s) failed verification")
