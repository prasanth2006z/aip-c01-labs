import boto3
from botocore.exceptions import ClientError

br = boto3.client("bedrock-runtime", region_name="us-west-2")
msg = [{"role": "user", "content": [{"text": "Name one AWS Region."}]}]

for model_id in ["amazon.nova-2-lite-v1:0",          # bare model ID, in-Region
                 "us.amazon.nova-2-lite-v1:0",       # geographic profile
                 "global.amazon.nova-2-lite-v1:0"]:  # global profile
    try:
        r = br.converse(modelId=model_id, messages=msg)
        print(f"OK   {model_id}: {r['metrics']['latencyMs']} ms")
    except ClientError as e:
        print(f"FAIL {model_id}: {e.response['Error']['Code']}")
