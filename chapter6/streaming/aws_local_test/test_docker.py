# pylint: disable=duplicate-code

import os
import json

import requests
from deepdiff import DeepDiff

with open("event.json", "rt", encoding="utf-8") as f_in:
    event = json.load(f_in)


url = os.getenv("LOCAL_STACK_TEST_URL",)
actual_response = requests.post(url, json=event, timeout=10).json()
print("actual response:")

print(json.dumps(actual_response, indent=2))

expected_response = {
    "predictions": [
        {
            "model": "ride_duration_prediction_model",  # added s for failure testing
            "version": os.getenv("RUN_ID"),
            "prediction": {
                "ride_duration": 20.970334029909353,
                "ride_id": 4594435555302002,
            },
        }
    ]
}


diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f"diff={diff}")

assert "type_changes" not in diff
assert "values_changed" not in diff
