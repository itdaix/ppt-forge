#!/usr/bin/env python3
"""Gemini API helper (team edition) — same CLI as the Muse connector helper,
but the API key comes from the GEMINI_API_KEY environment variable.

Setup: get a key at https://aistudio.google.com/apikey , then
  export GEMINI_API_KEY=<your key>

Commands:
  models                                   list available models (key check)
  ask --prompt TEXT [--model MODEL]        one generateContent call, prints text
  ask --prompt-file PATH [--model MODEL]   same, prompt read from a UTF-8 file
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://generativelanguage.googleapis.com"
DEFAULT_MODEL = "gemini-3-flash-preview"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def call(method, path, body=None):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        print("ERROR: GEMINI_API_KEY is not set. Get a key at "
              "https://aistudio.google.com/apikey and export GEMINI_API_KEY=<key>.",
              file=sys.stderr)
        sys.exit(2)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("x-goog-api-key", key)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            payload = {"error": {"message": f"HTTP {e.code} with unreadable body"}}
        return e.code, payload


def cmd_models(_args):
    status, payload = call("GET", "/v1beta/models")
    if status != 200:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1
    names = [m.get("name", "") for m in payload.get("models", [])]
    print(f"HTTP 200, {len(names)} models")
    for n in names:
        print(" ", n)
    return 0


def cmd_ask(args):
    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as f:
            prompt = f.read()
    else:
        prompt = args.prompt
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4},
    }
    status, payload = call("POST", f"/v1beta/models/{args.model}:generateContent", body)
    if status != 200:
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    texts = []
    for cand in payload.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "text" in part:
                texts.append(part["text"])
    print("\n".join(texts))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Gemini API helper (GEMINI_API_KEY)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("models")
    p_ask = sub.add_parser("ask")
    g = p_ask.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    p_ask.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()
    if args.cmd == "models":
        return cmd_models(args)
    return cmd_ask(args)


if __name__ == "__main__":
    sys.exit(main())
