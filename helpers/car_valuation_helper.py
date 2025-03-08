
from utils.custom_log import CustomLog

c_logger = CustomLog.log_gen()


class CarValuationHelper:

    @staticmethod
    def verify_vehicle_details(car_details_page, reg_number, vehicle_data, mismatch_list, reg_not_found_list):
        """
        Verifies vehicle details for the given reg number from car details page with expected output data.
        Args:
            car_details_page: Instance of CarDetailsPage
            reg_number: UK Vehicle registration number
            vehicle_data: expected data from output file
            mismatch_list: list of mismatched UK vehicle reg numbers
            reg_not_found_list: list of UK vehicle reg numbers that are not found in expected data from output file
        Returns:
            True/False
        """
        try:
            reg_number = reg_number.replace(" ", "")

            assert car_details_page.is_element_displayed(car_details_page.input_txt_ENTER_CAR_REGISTRATION, 6), \
                "Unable to enter vehicle registration number"
            car_details_page.clear_and_fill_in_field(car_details_page.input_txt_ENTER_CAR_REGISTRATION, reg_number, 6)

            car_details_page.click(car_details_page.btn_FIND_CAR, 15)
            car_details_page.wait_until_text_to_be_present(car_details_page.btn_FEEDBACK, "Feedback", 15)
            if car_details_page.is_element_displayed(car_details_page.ro_txt_REGISTRATION, 6):
                try:
                    exp_vehicle_reg = vehicle_data["VARIANT_REG"].replace(" ", "").strip()

                    c_logger.info(f"Verifying Vehicle Registration - {exp_vehicle_reg}")
                    assert car_details_page.get_text(car_details_page.ro_txt_REGISTRATION, 6) == exp_vehicle_reg, \
                        f"Data Mismatch found for {exp_vehicle_reg}"
                    exp_make = vehicle_data["MAKE_MODEL"].lower()
                    actual_make = car_details_page.get_text(car_details_page.ro_txt_MANUFACTURER, 6).lower()

                    c_logger.info(f"Verifying Vehicle Make - {exp_vehicle_reg}")
                    assert actual_make in exp_make, f"Data Mismatch found for {exp_make}"

                    c_logger.info(f"Verifying Year - {exp_vehicle_reg}")
                    assert car_details_page.get_text(car_details_page.ro_txt_YEAR, 6) == vehicle_data["YEAR"], \
                        f"Data Mismatch found for {vehicle_data["YEAR"]}"

                except AssertionError as e:
                    c_logger.warning(f"Data mismatch found - str{e}")
                    mismatch_list.append(vehicle_data)
                    return False
                car_details_page.click(car_details_page.btn_CHANGE_VEHICLE, 6)
                car_details_page.wait_until_text_to_be_present(car_details_page.btn_FEEDBACK, "Feedback", 15)
                return True
            else:
                car_details_page.wait_until_text_to_be_present(car_details_page.btn_FEEDBACK, "Feedback", 15)
                if car_details_page.is_element_displayed(car_details_page.ro_txt_VEHICLE_NOT_FOUND, 6):
                    c_logger.info(f"Vehicle registration number not found - {reg_number}")
                    reg_not_found_list.append(reg_number)
                    return False
                return False
        except AssertionError:
            mismatch_list.append(vehicle_data)

    @staticmethod
    def verify_records_with_no_match(car_details_page, reg_not_found_list):
        """
        Verifies records that are not found in expected data from the output file
        Args:
            car_details_page: Instance of CarDetailsPage
            reg_not_found_list: list of UK vehicle reg numbers that are not found in expected data from output file
        Returns:
            False - if AssertionError

        """
        try:
            for reg_number in reg_not_found_list:

                car_details_page.clear_and_fill_in_field(car_details_page.input_txt_ENTER_CAR_REGISTRATION, reg_number,
                                                         6)
                car_details_page.click(car_details_page.btn_FIND_CAR, 15)
                car_details_page.wait_until_text_to_be_present(car_details_page.btn_FEEDBACK, "Feedback", 15)
                if car_details_page.is_element_displayed(car_details_page.ro_txt_REGISTRATION, 6):
                    assert reg_number == car_details_page.get_text(car_details_page.ro_txt_REGISTRATION), \
                       f"Vehicle registration does not match for reg number - {reg_number}"
                else:
                    car_details_page.wait_until_text_to_be_present(car_details_page.btn_FEEDBACK, "Feedback", 15)
                    if car_details_page.is_element_displayed(car_details_page.ro_txt_VEHICLE_NOT_FOUND, 6):
                        c_logger.info(f"Vehicle registration number not found - {reg_number}")

        except AssertionError:
            return False
