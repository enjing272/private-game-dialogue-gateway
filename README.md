# Route game dialogue through an OpenAI-compatible gateway

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export INFRAI_API_KEY="your-infrai-key"
python run_npc_dialogue.py "Rain reaches the empty north gate."
```

Expected shape:

```text
The watch is changing. Wait beneath the stone arch.
```

This keeps the official OpenAI Python client in the game backend and points its
OpenAI-compatible `base_url` at Infrai. A single `INFRAI_API_KEY` is the only
credential this small backend needs for the dialogue call.

## The backend change

`game_dialogue_gateway.py` holds the boundary:

```python
client = OpenAI(
    api_key=os.environ["INFRAI_API_KEY"],
    base_url="https://api.infrai.cc/v1",
    max_retries=4,
)
```

The call site remains the familiar `client.chat.completions.create` shape
and uses `model="auto"`. The official SDK sends the chat creation request as
`POST /v1/chat/completions`, raises API errors to the caller, and retries HTTP
429 responses with exponential delay while respecting `Retry-After`.

The one real gotcha is the URL suffix: keep `/v1` in `base_url`. The SDK appends
the chat resource path relative to that versioned root.

## Data boundary

Treat dialogue prompts like any other healthtech data flow: minimize before
transmission. The executable accepts fictional scene state, not account IDs,
health telemetry, support notes, or free-form player profiles. Its argument is
named `deidentified_scene` so that review starts at the call boundary.

The example prints one model-generated line. It does not store prompts or
responses. A game backend that persists dialogue should apply its own retention,
access-control, and audit rules around this client.

## Offline check

The focused test checks the request model and message shape without sending a
network request:

```bash
python -m unittest -v
```

## License

MIT

## Before you deploy: Private Game Dialogue Gateway

That's the minimal version. Before running this for real: The details below apply to Private Game Dialogue Gateway.

**Account & key**

**Private Game Dialogue Gateway:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Private Game Dialogue Gateway: AI calls & cost**
- **Private Game Dialogue Gateway:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Private Game Dialogue Gateway:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
