import sys
import json
import requests

def send_log(api_key, log_message, tags):

	url = "https://http-intake.logs.datadoghq.com/api/v2/logs"
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"DD-API-KEY": api_key
	}

	payload = {
		"ddsource": "apex",
		"ddtags": tags,
		"message": log_message
	}

	response = requests.post(url, headers=headers, data=json.dumps(payload))

def main():

	json_file = sys.argv[1]
	environment = sys.argv[2]
	DATADOG_API_KEY = sys.argv[3]

	with open(json_file, 'r') as file:
		results = json.load(file)
		
	summary = results['result']['summary']
	test_results = results['result']['tests']
	test_coverage = results['result']['coverage']['coverage']

	# Send summary result
	send_log(DATADOG_API_KEY, summary, 'apexTestSummary,'+ environment)

	# Send test results
	for test in test_results:
		send_log(DATADOG_API_KEY, test, 'apexTestResults,STAGEFULL')

	# Send test coverage
	for coverage in test_coverage:
		send_log(DATADOG_API_KEY, coverage, 'apexTestCoverage,STAGEFULL')

if __name__ == "__main__":
	main()