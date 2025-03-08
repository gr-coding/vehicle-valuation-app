## Vehicle Valuation App is an Automation test suite to verify UK vehicle details by searching using vehicle registration number in car valuation website.

# pre-requisites
    Requires Python 3.8 or later. 
    create virtual environment:
    virtualenv venv

# Install dependencies:
    venv\Scripts\activate
     pip install -r requirements.txt

# Running tests:
    Check your browser version, Download and unpack chrome driver in project root directory
    -E - environment, Allowed value: prod
    -B - browser, Allowed values: chrome, firefox
    pytest -B "chrome" -E "prod" -k "test_car_details_by_reg"

# Reports
    HTML report and assets will be generated after every run and can be found in reports folder (project root directory)
