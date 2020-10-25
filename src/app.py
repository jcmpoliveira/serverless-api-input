import json
import re


def lambda_handler(event, context):
    print(event)

    try:

        body = event.get("body")
        message = json.loads(body).get("input")
        replace = ["Oracle", "Google", "Microsoft", "Amazon", "Deloitte"]

        for word in replace:
            message = re.sub(r"\b" + word + r"\b", word+"©", message)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "output": message,
            }),
        }

    except:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps("Error processing input"),
        }
