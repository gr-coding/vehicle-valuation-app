import csv
import re


from utils.custom_log import CustomLog

c_logger = CustomLog.log_gen()


class FileHelper:

    @staticmethod
    def extract_uk_vehicle_reg_num(input_file):
        """
        Extracts UK vehicle registration numbers from data from input file
        Args:
              input_file: Text file with UK Vehicle registration numbers
        Returns:
            UK Vehicle reg number list
        """

        file_data = FileHelper._read_file(input_file)

        uk_reg_pattern = r'\b[A-Z]{2}\d{2} [A-Z]{3}\b|\b[A-Z]{2}\d{2}[A-Z]{3}\b'
        uk_vehicle_reg_data = re.findall(uk_reg_pattern, file_data)

        if uk_vehicle_reg_data:
            unique_reg_data = set(uk_vehicle_reg_data)
            return unique_reg_data
        else:
            c_logger.info(f"UK Vehicle Registration number(s) not found in file. please check")
            return False

    @staticmethod
    def _read_file(input_file):
        """
        Reads the given file and returns file data
        Args:
            input_file: given file
        Returns:
            contents of the file
        Raises:
            FileNotFoundError
        """
        try:
            with open(input_file, 'r') as file:
                file_data = file.read()
                return file_data
        except FileNotFoundError as e:
            raise e

    @staticmethod
    def read_csv_file(input_file, file_keys=None):
        """ Reads and returns file data in a list
        Args:
            input_file:file with row of records in csv format
            file_keys: required csv file headers
        Returns:
            file_data: list of records in the csv file
        Raises:
            OSError
        """

        try:
            with open(input_file) as csv_file:
                file_data = csv.DictReader(csv_file)
                if file_keys:
                    if not (all(x in file_data.fieldnames for x in file_keys)):
                        c_logger.info("Invalid file - missing required file headers")
                        return False
                return list(file_data)
        except OSError as e:
            raise e
