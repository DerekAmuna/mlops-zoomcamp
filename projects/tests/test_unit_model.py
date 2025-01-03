#! /usr/bin/env python3
import base64
import json
from unittest.mock import Mock

from model import (KinesisCallback, ModelService, base64_decode,
                   create_kinesis_client, get_model_location)


def get_sample_wine_data():
    return {
        "fixed_acidity": 7.4,
        "volatile_acidity": 0.7,
        "citric_acid": 0.0,
        "residual_sugar": 1.9,
        "chlorides": 0.076,
        "free_sulfur_dioxide": 11.0,
        "total_sulfur_dioxide": 34.0,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4,
    }


def get_sample_wine_event():
    return {"wine": get_sample_wine_data(), "wine_id": "123"}


def get_mock_model():
    model = Mock()
    model.predict.return_value = [5]  # Mock prediction value
    return model


def test_base64_decode():
    wine_event = {"wine_id": "123", "wine": {"fixed_acidity": 7.4}}
    encoded = base64.b64encode(json.dumps(wine_event).encode("utf-8"))
    decoded = base64_decode(encoded)
    assert decoded == wine_event


def test_get_model_location():
    location = get_model_location("run-123")
    assert location.startswith("s3://wine-model/1/run-123")


def test_model_service_prepare_features():
    model_service = ModelService(model=Mock())
    sample_data = get_sample_wine_data()
    features = model_service.prepare_features(sample_data)

    assert len(features) == 11
    assert features["fixed acidity"] == sample_data["fixed_acidity"]
    assert features["alcohol"] == sample_data["alcohol"]


def test_model_service_predict():
    model = get_mock_model()
    model_service = ModelService(model=model)
    features = {"fixed_acidity": 7.4, "alcohol": 9.4}
    prediction = model_service.predict(features)

    assert isinstance(prediction, int)
    assert prediction == 5
    model.predict.assert_called_once()


def test_model_service_lambda_handler():
    model = get_mock_model()
    sample_event = get_sample_wine_event()

    encoded_data = base64.b64encode(json.dumps(sample_event).encode("utf-8")).decode(
        "utf-8"
    )
    print(encoded_data)
    event = {"Records": [{"kinesis": {"data": encoded_data}}]}

    callback_mock = Mock()
    model_service = ModelService(
        model=model, model_version="test-version", callbacks=[callback_mock]
    )

    result = model_service.lambda_handler(event)

    assert "predictions" in result
    assert len(result["predictions"]) == 1
    prediction = result["predictions"][0]
    assert prediction["model"] == "wine_quality_prediction_model"
    assert prediction["version"] == "test-version"
    assert "wine_quality" in prediction["prediction"]
    callback_mock.assert_called_once()


def test_kinesis_callback():
    mock_kinesis = Mock()
    callback = KinesisCallback(mock_kinesis, "test-stream")

    prediction_event = {"prediction": {"wine_id": "123", "wine_quality": 5}}

    callback.put_record(prediction_event)

    mock_kinesis.put_record.assert_called_once_with(
        StreamName="test-stream", Data=json.dumps(prediction_event), PartitionKey="123"
    )


def test_create_kinesis_client():
    client = create_kinesis_client()
    assert client is not None
    assert hasattr(client, "put_record")
