# Skill 1.2.3 lab: Resilient model access

Call a model through in-Region, geographic and global inference profiles, then add adaptive retries, a fallback model and a Step Functions circuit breaker.

- **Time:** about 40 minutes
- **Cost:** under US$0.20
- **Region:** us-west-2
- **Needs:** AWS CloudShell or Python 3.10+ with `boto3`; Amazon Nova 2 Lite and Nova Micro through inference profiles

## Files

| File | What it is |
| --- | --- |
| `profiles.py` | Calls Nova 2 Lite by bare model ID, US profile and global profile |
| `fallback.py` | Adaptive retries plus a fallback model on retryable errors only (`SIMULATE = True` fakes a throttle) |
| `circuit-breaker-statemachine.json` | Step Functions definition with retry, backoff and a fallback branch (deploying it is optional) |

## Run it

```bash
python profiles.py
python fallback.py
```

Expected: the bare model ID fails and both profiles succeed; `fallback.py` reports the simulated throttle and answers from Nova Micro.

Full walkthrough: the Medium post **AIP-C01 Skill 1.2.3: Resilient Model Access**.
