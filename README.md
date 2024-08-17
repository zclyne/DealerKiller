# DealerKiller

DealerKiller is an automatic price-negotiation bot based on LLM. It reads emails from auto dealers in your mailbox, generate a response via LLM and sends the notification in real-time to the configured IM.

## Getting Started

### Running

This project uses `poetry` for package management, to run the project:

```shell
poetry run python main.py
```

### Testing
To run tests on the project:
```shell
poetry run pytest
```

## Mail

The `mail` component currently only supports gmail. Source code is based on [simplemail](https://github.com/jeremyephron/simplegmail/tree/master) with necessary modifications to better work with `DealerKiller`.

## LLM

The `llm` component adopts the OpenAI API and currently supports locally-running models with ollama.

## IM

The `im` component currently only supports Discord.