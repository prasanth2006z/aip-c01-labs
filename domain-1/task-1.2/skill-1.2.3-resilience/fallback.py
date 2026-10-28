import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

PRIMARY  = "us.amazon.nova-2-lite-v1:0"
FALLBACK = "us.amazon.nova-micro-v1:0"
RETRYABLE = {"ThrottlingException", "ServiceUnavailableException",
             "ModelNotReadyException", "ModelTimeoutException",
             "InternalServerException"}
SIMULATE = True   # set False to call the primary for real

br = boto3.client("bedrock-runtime", region_name="us-west-2",
                  config=Config(retries={"max_attempts": 3, "mode": "adaptive"}))

def call(model_id, text):
    if SIMULATE and model_id == PRIMARY:
        raise ClientError({"Error": {"Code": "ThrottlingException",
                                     "Message": "simulated"}}, "Converse")
    r = br.converse(modelId=model_id,
                    messages=[{"role": "user", "content": [{"text": text}]}],
                    inferenceConfig={"maxTokens": 200})
    return r["output"]["message"]["content"][0]["text"]

def resilient_answer(text):
    try:
        return PRIMARY, call(PRIMARY, text)
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code not in RETRYABLE:
            raise          # a bad request won't succeed on another model
        print(f"primary failed with {code}; using fallback")
        return FALLBACK, call(FALLBACK, text)

print(resilient_answer("Give one tip for reducing LLM latency."))
