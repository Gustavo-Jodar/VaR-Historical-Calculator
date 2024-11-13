import requests
import os

# Define API URL and CSV file path for testing
BASE_URL = "http://localhost:5000"
TEST_FOLDER = "tests/"

# data = {'confidence_level': 0.95}
def test(url, file, data, expected_response, expected_code):
    response = requests.post(url, files=file, data=data)
    assert response.status_code == expected_code, f"Expected {expected_code}, got {response.status_code}"
    assert expected_response in str(response.json()), "Response JSON did not contain expected key"


def test_trade_var():
    """Test the /trade/var endpoint with a CSV file and confidence level."""
    url = f"{BASE_URL}/trade/var"
    data = {'confidence_level': 0.95}

    print("-- Testing trade/var")

    # Test corrected calculation 1
    print("test corrected calculation 1")
    with open(TEST_FOLDER + 'singletrade.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Calculated Value at Risk", 201)

    # Test corrected calculation 2
    print("test corrected calculation 2")
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Calculated Value at Risk", 201)

    # Test confidence level exceeds 1
    print("test confidence level 3")
    data = {'confidence_level': 1.01}
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, 'Confidence level must be greater than 0 and smaller than 1.', 400)

    # Test confidence level of 0
    print("test confidence level 4")
    data = {'confidence_level': 0}
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Confidence level must be greater than 0 and smaller than 1.", 400)

    # Test corrupted file
    print("test corrupted file 5")
    data = {'confidence_level': 0.95}
    with open(TEST_FOLDER + 'corrupted_file.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Input file not accepted, please review the accepted format.", 400)

    print("Test /trade/var passed.")


def test_portfolio_var():
    """Test the /portfolio/var endpoint with a CSV file and confidence level."""
    url = f"{BASE_URL}/portfolio/var"
    data = {'confidence_level': 0.95}

    print("-- Testing portfolio/var")

    # Test corrected calculation 1
    print("test corrected calculation 1")
    with open(TEST_FOLDER + 'Portfolio 1 - PL.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Calculated Value at Risk", 201)

    # Test corrected calculation 2
    print("test corrected calculation 2")
    with open(TEST_FOLDER + 'singletrade.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Calculated Value at Risk", 201)


    # Test corrected calculation 3
    print("test corrected calculation 3")
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Calculated Value at Risk", 201)


    # Test confidence level exceeds 1
    print("test confidence level 4")
    data = {'confidence_level': 1.01}
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, 'Confidence level must be greater than 0 and smaller than 1.', 400)

    # Test confidence level of 0
    print("test confidence level 5")
    data = {'confidence_level': 0}
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Confidence level must be greater than 0 and smaller than 1.", 400)

    # Test corrupted file
    print("test corrupted file 6")
    data = {'confidence_level': 0.95}
    with open(TEST_FOLDER + 'corrupted_file.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Input file not accepted, please review the accepted format.", 400)

    print("-- Test /portfolio/var passed.")


def test_portfolio_var_per_trade():
    """Test the /portfolio/varPerTrade endpoint with a CSV file and confidence level."""
    url = f"{BASE_URL}/portfolio/varPerTrade"
    data = {'confidence_level': 0.95}

    print("-- Testing portfolio/varPerTrade")

    # Test corrected calculation 1
    print("test corrected calculation 1")
    with open(TEST_FOLDER + 'Portfolio 1 - PL.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "trade_id", 201)

    # Test corrected calculation 2
    print("test corrected calculation 2")
    with open(TEST_FOLDER + 'singletrade.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "trade_id", 201)


    # Test corrected calculation 3
    print("test corrected calculation 3")
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "trade_id", 201)


    # Test confidence level exceeds 1
    print("test confidence level 4")
    data = {'confidence_level': 1.01}
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, 'Confidence level must be greater than 0 and smaller than 1.', 400)

    # Test confidence level of 0
    print("test confidence level 5")
    data = {'confidence_level': 0}
    with open(TEST_FOLDER + '1_10.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Confidence level must be greater than 0 and smaller than 1.", 400)

    # Test corrupted file
    print("test corrupted file 6")
    data = {'confidence_level': 0.95}
    with open(TEST_FOLDER + 'corrupted_file.csv', 'rb') as file:
        files = {'file': file}
        test(url, files, data, "Input file not accepted, please review the accepted format.", 400)

    print("-- Test /portfolio/varPerTrade passed.")


def run_tests():
    try:
        test_trade_var()
        test_portfolio_var()
        test_portfolio_var_per_trade()
        print("All tests passed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")
    
if __name__ == "__main__":
    run_tests()
