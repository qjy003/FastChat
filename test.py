# Import the `test` function from the `src.base.utils` module.
from src.base.utils import test

# This script is designed to send batch requests to a specified URL using test case data.
# Parameters for the `test` function are as follows:
# - url: The URL to which requests will be sent.
# - test_json_file: The path to the JSON file containing the test case data.
# - test_case_keys: A list of specific keys for the test cases that should be sent.
# - test_case_prefixs: A list of prefixes to filter which test cases should be sent based on their keys.
# - batch_size: The number of requests to send asynchronously in each batch. A larger batch size can increase speed.
# - result_path: the folder path of the request results to be saved.
# Dictionary data result:
#
# Test case name: {
# description: "Description of the error in the test case",
# data: { # Structure of the request data
# ....
# }
# }

if __name__ == '__main__':
    # Execute the `test` function with specified parameters.
    # Replace the empty strings and lists with the appropriate values for your use case.
    test(url='http://127.0.0.1:18868/chat',
         test_json_file='data/json/test.json',
         test_case_keys=["http联通性测试"],
         test_case_prefixs=[],
         result_path='data/result',
         batch_size=10)
