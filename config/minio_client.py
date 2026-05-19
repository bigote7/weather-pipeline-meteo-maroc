from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from config.settings import (
    MINIO_ACCESS_KEY,
    MINIO_BUCKET,
    MINIO_ENDPOINT,
    MINIO_SECRET_KEY,
    PROJECT_ROOT,
)

LOCAL_DATA_DIR = PROJECT_ROOT / "data" / MINIO_BUCKET
USE_LOCAL_FALLBACK = os.getenv("USE_LOCAL_STORAGE", "auto")  # auto | true | false


def _use_local() -> bool:
    if USE_LOCAL_FALLBACK == "true":
        return True
    if USE_LOCAL_FALLBACK == "false":
        return False
    try:
        import boto3
        from botocore.client import Config

        client = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )
        client.list_buckets()
        return False
    except Exception:
        return True


def _local_path(key: str) -> Path:
    return LOCAL_DATA_DIR / key.replace("/", os.sep)


def get_s3_client():
    import boto3
    from botocore.client import Config

    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


def ensure_bucket(client=None) -> None:
    if _use_local():
        LOCAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
        print("[Storage] Mode local:", LOCAL_DATA_DIR)
        return
    client = client or get_s3_client()
    buckets = [b["Name"] for b in client.list_buckets().get("Buckets", [])]
    if MINIO_BUCKET not in buckets:
        client.create_bucket(Bucket=MINIO_BUCKET)


def put_json(key: str, data: Any, client=None) -> None:
    if _use_local():
        path = _local_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return
    client = client or get_s3_client()
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    client.put_object(
        Bucket=MINIO_BUCKET,
        Key=key,
        Body=body,
        ContentType="application/json",
    )


def get_json(key: str, client=None) -> Any:
    if _use_local():
        path = _local_path(key)
        return json.loads(path.read_text(encoding="utf-8"))
    client = client or get_s3_client()
    obj = client.get_object(Bucket=MINIO_BUCKET, Key=key)
    return json.loads(obj["Body"].read().decode("utf-8"))


def list_keys(prefix: str, client=None) -> list[str]:
    if _use_local():
        base = LOCAL_DATA_DIR / prefix.replace("/", os.sep)
        if not base.exists():
            return []
        keys = []
        for p in base.rglob("*.json"):
            rel = p.relative_to(LOCAL_DATA_DIR).as_posix()
            keys.append(rel)
        return keys
    client = client or get_s3_client()
    keys: list[str] = []
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=MINIO_BUCKET, Prefix=prefix):
        for item in page.get("Contents", []):
            keys.append(item["Key"])
    return keys
