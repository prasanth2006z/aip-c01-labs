# Skill 1.3.2 lab: A multimodal pipeline (audio and images)

Turn a customer voicemail and a photographed returns form into the same structured JSON, using Amazon Polly (to create test audio), Amazon Transcribe and Amazon Nova 2 Lite on Bedrock.

- **Time:** about 40 minutes
- **Cost:** under US$0.05
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; permission for Polly, Transcribe, S3 and `bedrock:InvokeModel`; Amazon Nova 2 Lite through the US inference profile; an S3 bucket in us-west-2

## Files

| File | What it is |
| --- | --- |
| `multimodal_pipeline.py` | The lab: `audio` step (Polly → S3 → Transcribe → Nova 2 Lite) and `image` step (form image → Nova 2 Lite) |
| `returns-form.png` | A photographed returns form for the image step |

## Run it

```bash
pip install boto3
export LAB_BUCKET=your-bucket-name
python multimodal_pipeline.py audio
python multimodal_pipeline.py image
```

Both steps print a return request as JSON with `order_id`, `item`, `reason` and `customer_wants`.

## Clean up

Delete the `aip-lab/` objects (voicemail and transcript) from your bucket.
