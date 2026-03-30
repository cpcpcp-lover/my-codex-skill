#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

STEP_ALIASES = {
    "step1": "analyze",
    "step2": "cutout",
    "step3": "fusion",
    "step4": "assets",
    "step5": "typography",
}


def load_local_env() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    for name in (".env.local", ".env"):
        path = repo_root / name
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def read_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str, payload: Dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def env(name: str, default: str = "") -> str:
    value = os.environ.get(name, default)
    return value.strip() if isinstance(value, str) else default


def resolve_endpoint(step_name: str) -> str:
    specific = env(f"DOUBAO_{step_name.upper()}_ENDPOINT")
    if specific:
        return specific
    generic = env("DOUBAO_RUNTIME_ENDPOINT")
    if generic:
        return generic
    base = env("DOUBAO_BASE_URL")
    if not base:
        return ""
    return base.rstrip("/") + "/runtime/" + step_name


def build_prompt(step_name: str, payload: Dict[str, Any]) -> str:
    task_id = payload.get("task_id", "")
    if step_name == "analyze":
        return (
            f"Task {task_id}: analyze the main image and return Blueprint JSON with "
            "theme, palette, style, material_elements, composition, lighting, and negative_constraints."
        )
    if step_name == "cutout":
        return (
            f"Task {task_id}: isolate the main subject, stage it on white, then return a transparent PNG result "
            "and cutout quality status."
        )
    if step_name == "fusion":
        return f"Task {task_id}: create one 4K hero artwork from Blueprint, optional subject cutout, and B-F materials."
    if step_name == "assets":
        return f"Task {task_id}: generate exactly three transparent supporting assets matching the hero artwork style."
    if step_name == "typography":
        return f"Task {task_id}: generate one transparent artistic typography output from the hero artwork and text input."
    return f"Task {task_id}: execute {step_name}."


def normalize_result(step_name: str, provider_response: Dict[str, Any]) -> Dict[str, Any]:
    artifact_urls: List[str] = []
    if isinstance(provider_response.get("artifact_urls"), list):
        artifact_urls = provider_response.get("artifact_urls", [])
    elif isinstance(provider_response.get("images"), list):
        artifact_urls = provider_response.get("images", [])

    structured_output = provider_response.get("structured_output")
    if structured_output is None:
        structured_output = provider_response

    return {
        "success": bool(provider_response.get("success", True)),
        "step": step_name,
        "artifact_urls": artifact_urls,
        "structured_output": structured_output,
        "error_code": provider_response.get("error_code", ""),
        "error_message": provider_response.get("error_message", ""),
    }


def post_json(url: str, payload: Dict[str, Any], timeout_secs: int) -> Dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {env('DOUBAO_API_KEY')}",
    }
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout_secs) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        text = response.read().decode(charset)
        return json.loads(text) if text else {}


def main() -> int:
    load_local_env()
    parser = argparse.ArgumentParser(description="Run a local Doubao-backed bridge for OpenClaw art pipeline skills.")
    parser.add_argument("step", choices=["step1", "step2", "step3", "step4", "step5", "analyze", "cutout", "fusion", "assets", "typography"])
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--dry-run", action="store_true", help="Write the provider request payload without sending it.")
    args = parser.parse_args()

    step_name = STEP_ALIASES.get(args.step, args.step)
    input_payload = read_json(args.input_json)
    request_payload = {
        "task_id": input_payload.get("task_id", ""),
        "step": step_name,
        "prompt": build_prompt(step_name, input_payload),
        "input": input_payload,
        "models": {
            "vision": env("DOUBAO_VISION_MODEL"),
            "image": env("DOUBAO_IMAGE_MODEL"),
        },
    }

    if args.dry_run:
        write_json(args.output_json, {
            "success": True,
            "step": step_name,
            "artifact_urls": [],
            "structured_output": {
                "mode": "dry_run",
                "endpoint": resolve_endpoint(step_name),
                "provider_request": request_payload,
            },
            "error_code": "",
            "error_message": "",
        })
        return 0

    api_key = env("DOUBAO_API_KEY")
    endpoint = resolve_endpoint(step_name)
    if not api_key:
        write_json(args.output_json, {
            "success": False,
            "step": step_name,
            "artifact_urls": [],
            "structured_output": {},
            "error_code": "CONFIG_MISSING_API_KEY",
            "error_message": "Set DOUBAO_API_KEY in .env.local or the local environment before running the bridge.",
        })
        return 1
    if not endpoint:
        write_json(args.output_json, {
            "success": False,
            "step": step_name,
            "artifact_urls": [],
            "structured_output": {},
            "error_code": "CONFIG_MISSING_ENDPOINT",
            "error_message": "Set DOUBAO_RUNTIME_ENDPOINT or a step-specific DOUBAO_*_ENDPOINT before running the bridge.",
        })
        return 1

    timeout_secs = int(env("DOUBAO_TIMEOUT_SECS", "120"))
    try:
        provider_response = post_json(endpoint, request_payload, timeout_secs)
        result = normalize_result(step_name, provider_response)
        write_json(args.output_json, result)
        return 0 if result.get("success") else 1
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        write_json(args.output_json, {
            "success": False,
            "step": step_name,
            "artifact_urls": [],
            "structured_output": {},
            "error_code": f"HTTP_{exc.code}",
            "error_message": message,
        })
        return 1
    except Exception as exc:
        write_json(args.output_json, {
            "success": False,
            "step": step_name,
            "artifact_urls": [],
            "structured_output": {},
            "error_code": "BRIDGE_RUNTIME_ERROR",
            "error_message": str(exc),
        })
        return 1


if __name__ == "__main__":
    sys.exit(main())
