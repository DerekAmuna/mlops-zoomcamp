# pylint: disable=duplicate-code

import os
import json
import requests
from deepdiff import DeepDiff

with open("event.json", "rt", encoding="utf-8") as f_in:
    event = json.load(f_in)


url = os.getenv("LOCAL_STACK_TEST_URL", "http://localhost:8080/2015-03-31/functions/function/invocations")
actual_response = requests.post(url, json=event, timeout=100).json()
print("actual response:")

print(json.dumps(actual_response, indent=2))

expected_response = {
    "predictions": [
        {
            "model": "wine_quality_prediction_model",  # added s for failure testing
            "version": "1542fc238fef40ddae60538ed932c35b",
            "prediction": {
                "wine_quality": 5,
                "wine_id": 123,
            },
        }
    ]
}


diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f"diff={diff}")

assert "type_changes" not in diff
assert "values_changed" not in diff