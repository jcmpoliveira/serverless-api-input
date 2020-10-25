import json
import pytest

from src import app


@pytest.fixture()
def apigw_event_no_replace():

    return {
        "body": '{ "input": "hello world"}',
    }

@pytest.fixture()
def apigw_event_replace():

    return {
        "body": '{ "input": "Hello Google"}',
    }

@pytest.fixture()
def apigw_event_replace_multiple():

    return {
        "body": '{ "input": "Hello Googlee Amazon!"}',
    }

@pytest.fixture()
def apigw_error():

    return {
        "body": 'hello world',
    }


def test_no_change(apigw_event_no_replace, mocker):

    ret = app.lambda_handler(apigw_event_no_replace, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "output" in ret["body"]
    assert data["output"] == "hello world"


def test_input_change(apigw_event_replace, mocker):

    ret = app.lambda_handler(apigw_event_replace, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "output" in ret["body"]
    assert data["output"] == "Hello Google©"

def test_input_change_multiple(apigw_event_replace_multiple, mocker):

    ret = app.lambda_handler(apigw_event_replace_multiple, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "output" in ret["body"]
    assert data["output"] == "Hello Googlee Amazon©!"


def test_error(apigw_error, mocker):

    ret = app.lambda_handler(apigw_error, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 400
    assert not "output" in ret["body"]
    assert data == "Error processing input"