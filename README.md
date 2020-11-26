# serverless-api-input

## Usage



```bash
curl --request POST 'https://<api-gw-endpoint>/v1/replace' \
     --header "Content-Type: application/json" \
     --data '{"input": "This is the string you want to input."}'
```

## Endpoint details

**Endpoint:** https://<api-gw-endpoint>/v1/replace

**Method:** POST

**Data format:** JSON encoded request body

| Parameter  | Description  | Format       |
| ---------- | ------------ | ------------ |
| input      | Input message  |     String |



**Response Body:** JSON encoded response

| Parameter  | Description  | Format       |
| ---------- | ------------ | ------------ |
| ouput      | Output message  |     String |


**Status Code:**

| Status     | Description  | 
| ---------- | ------------ | 
| 200        | Success      |
| 400        | Error        |


## Solution

This solution consists on the following resources:

- Lambda function - a lambda function that receives a string as an input and returns the same string with certain words replaced
- API Gateway resource - an API gateway endpoint to expose the lambda with a POST method available
- S3 Bucket - an S3 Bucket configured as a static website, hosting a simple frontend to interact with the API


## Content

This project contains source code and supporting files for a serverless application. It includes the following files and folders.

- src - Code for the application's Lambda function.
- template.yaml - Cloudformation template that defines all the resources deployed
- tests - Unit tests for the application code. 
- website - The html file for the frontend to be stored in an S3 bucket
- .github/workflows - CI/CD to build and deploy the solution



## Deployment

### Dependencies

To depoy this solution, the following is required:

* AWS account with the required permissions
* S3 bucket to store artifacts
* AWS credentials configured in your local machine

And the follwoing dependencies:

* [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3](https://www.python.org/downloads/)
* [Pytest ](https://docs.pytest.org/en/stable/getting-started.html)
* [Docker](https://hub.docker.com/search/?type=edition&offering=community)


### Deploy template


```bash
sam build
sam package --output-template-file package.yaml --s3-bucket <ARTIFACTS_BUCKET_NAME> --s3-prefix serverless-api-input
sam deploy --template-file package.yaml --stack-name serverless-api-input --s3-bucket <ARTIFACTS_BUCKET_NAME> --s3-prefix serverless-api-input --capabilities CAPABILITY_IAM --no-fail-on-empty-changeset
```

### Update index.html with API Gateway endpoint and upload to S3

```bash
API_ENDPOINT=(`aws cloudformation describe-stacks --stack-name serverless-api-input --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text`)
sed -i "s|REPLACE_API_ENDPOINT_HERE|$API_ENDPOINT|g" website/index.html
aws s3 cp --acl public-read website/index.html s3://serverless-api-website-jo-bucket/
```

## Unit tests

Tests are defined in the `tests` folder in this project. You need [pytest](https://docs.pytest.org/en/latest/) to run unit tests.

```bash
python -m pytest tests/ -v
```

## Cleanup

To delete the application, use the AWS CLI.

```bash
aws cloudformation delete-stack --stack-name serverless-api-input
```

