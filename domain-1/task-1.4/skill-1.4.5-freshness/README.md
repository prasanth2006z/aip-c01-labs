# Skill 1.4.5 lab: Keep the vector store fresh

Change and delete documents in the knowledge base from the [Skill 1.4.2 lab](../skill-1.4.2-metadata), detect what's stale before syncing, run an incremental sync and read its statistics. Then automate it with a Lambda function triggered by S3 events and a nightly schedule.

- **Time:** about 30 minutes
- **Cost:** a few cents
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; the `aip-lab-kb` knowledge base and `LAB_BUCKET` from the Skill 1.4.2 lab

## Files

| File | What it is |
| --- | --- |
| `docs-v2/returns-policy-2026.txt` | The April update of the 2026 returns policy (hedge trimmers: 21 days) |
| `freshness.py` | Lab steps: ask, change, detect, sync |
| `sync_on_change.py` | Lambda handler that starts a sync on S3 changes or on a schedule |

## Part 1: Incremental sync by hand

```bash
pip install boto3
export LAB_BUCKET=your-bucket-name KB_ID=XXXXXXXXXX DS_ID=XXXXXXXXXX
python freshness.py ask      # 14 days, from the current 2026 policy
python freshness.py change   # update the 2026 policy, delete the 2025 one
python freshness.py detect   # STALE and ORPHANED documents, before any sync
python freshness.py sync     # only the changed and deleted documents are processed
python freshness.py ask      # 21 days; the 2025 policy is gone
```

In the sync statistics, look for `numberOfModifiedDocumentsIndexed: 1` and `numberOfDocumentsDeleted: 1`: the sync scans everything but re-embeds only what changed.

## Part 2: Automate it (console)

1. **Lambda:** create a Python function `kb-sync` from `sync_on_change.py` (handler `sync_on_change.handler`). Set `KB_ID` and `DS_ID`. Give its role `bedrock:StartIngestionJob` on the knowledge base.
2. **S3 trigger:** bucket → Properties → Event notifications → create one for **All object create events** and **All object removal events**, prefix `kb-docs/`, destination `kb-sync`.
3. **Schedule:** EventBridge Scheduler → Create schedule → cron `0 2 * * ? *` (02:00 daily) → target Lambda `kb-sync`.
4. Test: upload any `.txt` file under `kb-docs/`, then check the function's logs and the data source's sync history.

Only one sync can run per data source at a time. The function logs and skips a trigger that arrives during a sync; the nightly schedule catches anything skipped. For changes that must appear within seconds, push them with a custom data source (see the [Skill 1.4.4 lab](../skill-1.4.4-connectors)).

## Clean up

See the clean-up list in [the task README](../README.md); it removes everything Task 1.4 created.
