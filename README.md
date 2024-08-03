# DealerKiller

DealerKiller is an automatic price-negotiation bot based on LLM. It reads emails from auto dealers in your mailbox, generate a response via LLM and sends the notification in real-time to the configured IM.

## Getting Started

This project uses `poetry` for package management, to run the project:

```shell
poetry run python main.py
```

## Mail

The `mail` components currently only supports gmail. Source code is based on [simplemail](https://github.com/jeremyephron/simplegmail/tree/master) with necessary modifications to better work with `DealerKiller`.