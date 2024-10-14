import sys
import json
import urllib.request
import urllib.parse

def send_log(api_key, log_message, tags, environment, log_status):

	url = "https://http-intake.logs.datadoghq.com/api/v2/logs"
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"DD-API-KEY": api_key
	}

	payload = {
		"ddsource":"Salesforce",
		"service":"Riskplatform",
		"enviroment": environment,
		"ddtags": tags,
		"message": log_message,
		"level": log_status
	}

	req = urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode('utf-8'), method='POST')
	response = urllib.request.urlopen(req)

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
	if summary['outcome'] == 'Failed':
		send_log(DATADOG_API_KEY, summary, 'apexTestSummary', environment, "WARN")
	else:
		send_log(DATADOG_API_KEY, summary, 'apexTestSummary', environment, "INFO")

	# Send test results
	for test in test_results:
		if test['Outcome'] == 'Fail':
			send_log(DATADOG_API_KEY, test, 'apexTestResults', environment, "WARN")
		else:
			send_log(DATADOG_API_KEY, test, 'apexTestResults', environment, "INFO")

	# Send test coverage
	for coverage in test_coverage:
		if coverage['coveredPercent'] < 75:
			send_log(DATADOG_API_KEY, coverage, 'apexTestCoverage', environment, "WARN")
		else:
			send_log(DATADOG_API_KEY, coverage, 'apexTestCoverage', environment, "INFO")

if __name__ == "__main__":
	main()