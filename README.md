# lambda-utilize-layer-example

This is a sample SAM template for a lambda which utilizes a lambda layer. For an example of how to deploy a lambda layer, see [https://github.com/mcbanderson/lambda-layer-example](https://github.com/mcbanderson/lambda-layer-example)

The following is an overview of what is provided in this repository.

```bash
.
├── README.md                   <-- This README file
├── src                         <-- Source code for our lambda function
│   ├── __init__.py
│   ├── app.py                  <-- Lambda function code
│   ├── requirements.txt        <-- Lambda function requirements
├── template.yaml               <-- SAM Template
└── tests                       <-- Unit tests
    └── unit
        ├── __init__.py
        └── test_handler.py
```

## Requirements

* AWS CLI already configured
* SAM CLI installed
* [Python 3 installed](https://www.python.org/downloads/)

## Setup

### Including Your Layer

If you created an SSM Parameter when creating your Lambda Layer, then you can use it to easily include the latest version of your Lambda Layer in your Lambda:

```yaml
Parameters:
    MyLayerLatestVersion:
        Type: 'AWS::SSM::Parameter::Value<String>'
        Default: '/Layers/MyLayer/Latest'
Resources:
    MyFunction:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: src/
            Layers:
                - !Ref MyLayerLatestVersion
            ...
```

Be sure that the default value of your parameter (in this case `/Layers/MyLayer/Latest`) matches whatever you named your SSM Parameter.

### Packaging and Deploying

Before we can package and deploy our Lambda, we need an `S3 bucket` where we can upload our packaged Lambda function - If you don't have an S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://<BUCKET_NAME>
```

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket <BUCKET_NAME>
```

Next, the following command will create a Cloudformation Stack and deploy your Lambda function.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name <STACK_NAME> \
    --capabilities CAPABILITY_IAM
```

And that's it! Once your Lambda is deployed, it will be able to access the Lambda Layer you created and import any Python packages and modules that it provides.

## Cleanup

In order to delete our Lambda, you need to delete the CloudFormation stack that was created. To do so you can use the following AWS CLI Command:

```bash
aws cloudformation delete-stack --stack-name <STACK_NAME>
```
