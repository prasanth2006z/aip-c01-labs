import json, urllib.request, boto3

bedrock = boto3.client("bedrock-runtime")
CONFIG_URL = ("http://localhost:2772/applications/genai-lab"
              "/environments/prod/configurations/model-settings")

def get_config():
    with urllib.request.urlopen(CONFIG_URL) as r:
        return json.loads(r.read())

def lambda_handler(event, context):
    cfg = get_config()
    resp = bedrock.converse(
        modelId=cfg["model_id"],
        messages=[{"role": "user",
                   "content": [{"text": event.get("question", "What is RAG in one sentence?")}]}],
        inferenceConfig={"maxTokens": cfg["max_tokens"],
                         "temperature": cfg.get("temperature", 0.5)},
    )
    return {
        "model_used": cfg["model_id"],
        "answer": resp["output"]["message"]["content"][0]["text"],
        "input_tokens": resp["usage"]["inputTokens"],
        "output_tokens": resp["usage"]["outputTokens"],
    }
