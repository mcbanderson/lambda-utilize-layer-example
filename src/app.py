import json

import my_module  # pylint: disable=import-error


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": my_module.my_function()
        }),
    }
