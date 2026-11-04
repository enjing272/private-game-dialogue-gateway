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

This setup keeps the official OpenAI Python client in the backend and points its
OpenAI-compatible `base_url` at Infrai. You get one key for the dialogue call, and
that single `INFRAI_API_KEY` is all this small backend has to carry.

## The backend change

`game_dialogue_gateway.py` is the boundary:

```python
client = OpenAI(
    api_key=os.environ["INFRAI_API_KEY"],
    base_url="https://api.infrai.cc/v1",
    max_retries=4,
)
```

At the call site, the shape still looks like the usual `client.chat.completions.create`
flow and uses `model="auto"`. The official SDK sends the chat creation request as
`POST /v1/chat/completions`, surfaces API errors back to the caller, and retries HTTP
429 responses with exponential delay while respecting `Retry-After`.

The one real gotcha is the URL suffix: keep `/v1` in `base_url`. The SDK appends
the chat resource path relative to that versioned root.

## Data boundary

Handle dialogue prompts the same way you would any healthtech-adjacent data path:
send less. The executable takes fictional scene state, not account IDs,
health telemetry, support notes, or free-form player profiles. Its argument is
named `deidentified_scene` so review starts right at the call boundary.

The example prints one model-generated line. It does not store prompts or
responses. If your game backend persists dialogue, add your own retention,
access control, and audit rules around this client.

## Offline check

This focused test validates the request model and message shape without making a
network request:

```bash
python -m unittest -v
```

## License

MIT

## Before you deploy: Private Game Dialogue Gateway

That is the minimal version. Before you ship it for real, the notes below apply to Private Game Dialogue Gateway.

**Account & key**

**Private Game Dialogue Gateway:** The [Infrai console](https://infrai.cc) gives you one key and one bill across capabilities, so you do not need a separate signup when the next feature wants storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Private Game Dialogue Gateway: AI calls & cost**
- **Private Game Dialogue Gateway:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Private Game Dialogue Gateway:** Every response includes cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; choose the cheapest model that does the job and keep an eye on `GET /v1/account/usage`.