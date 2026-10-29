"""Lab: Skill 1.3.2 - a small multimodal pipeline (audio and image) on AWS.

  python multimodal_pipeline.py audio   # Polly -> S3 -> Transcribe -> Nova 2 Lite -> JSON
  python multimodal_pipeline.py image   # returns-form.png -> Nova 2 Lite -> JSON

Set LAB_BUCKET to an S3 bucket in us-west-2 before running the audio step.
"""
import json, os, sys, time
from pathlib import Path
import boto3

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-2-lite-v1:0"
BUCKET = os.environ.get("LAB_BUCKET", "")
AUDIO_KEY = "aip-lab/voicemail.mp3"
TRANSCRIPT_KEY = "aip-lab/voicemail-transcript.json"

VOICEMAIL = ("Hi, this is Sam calling about order A-4471. The cordless drill I bought last week "
             "arrived with a cracked battery cover. I'd like a replacement rather than a refund, please.")

INSTRUCTION = ("Extract the return request as JSON with exactly these keys: "
               "order_id, item, reason, customer_wants (refund or replacement, or null if not stated). "
               "Reply with the JSON only.")

bedrock = boto3.client("bedrock-runtime", region_name=REGION)


def ask_model(content_blocks):
    r = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": content_blocks}],
        inferenceConfig={"maxTokens": 300, "temperature": 0},
    )
    text = r["output"]["message"]["content"][0]["text"].strip()
    if text.startswith("```"):                      # tolerate a ```json fenced reply
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


def audio_step():
    if not BUCKET:
        sys.exit("Set LAB_BUCKET to an S3 bucket in us-west-2 first.")
    s3 = boto3.client("s3", region_name=REGION)
    polly = boto3.client("polly", region_name=REGION)
    transcribe = boto3.client("transcribe", region_name=REGION)

    # 1. Create audio to work with
    speech = polly.synthesize_speech(Text=VOICEMAIL, OutputFormat="mp3", VoiceId="Joanna")
    s3.put_object(Bucket=BUCKET, Key=AUDIO_KEY, Body=speech["AudioStream"].read())
    print(f"1. Voicemail uploaded to s3://{BUCKET}/{AUDIO_KEY}")

    # 2. Transcribe it (asynchronous job)
    job_name = f"aip-lab-voicemail-{int(time.time())}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": f"s3://{BUCKET}/{AUDIO_KEY}"},
        MediaFormat="mp3",
        LanguageCode="en-US",
        OutputBucketName=BUCKET,
        OutputKey=TRANSCRIPT_KEY,
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)["TranscriptionJob"]["TranscriptionJobStatus"]
        if status in ("COMPLETED", "FAILED"):
            break
        print("   transcribing...")
        time.sleep(5)
    if status == "FAILED":
        sys.exit("Transcription failed; check the job in the Transcribe console.")
    result = json.loads(s3.get_object(Bucket=BUCKET, Key=TRANSCRIPT_KEY)["Body"].read())
    transcript = result["results"]["transcripts"][0]["transcript"]
    print(f"2. Transcript: {transcript}")

    # 3. Transcript -> structured request
    print("3. Structured request:")
    print(json.dumps(ask_model([{"text": f"{INSTRUCTION}\n\nTranscript:\n{transcript}"}]), indent=2))


def image_step():
    image_bytes = (Path(__file__).parent / "returns-form.png").read_bytes()
    print("4. From the form image:")
    print(json.dumps(ask_model([
        {"image": {"format": "png", "source": {"bytes": image_bytes}}},
        {"text": INSTRUCTION},
    ]), indent=2))


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "audio":
        audio_step()
    elif step == "image":
        image_step()
    else:
        sys.exit("Usage: python multimodal_pipeline.py audio|image")
