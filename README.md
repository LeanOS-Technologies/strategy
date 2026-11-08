# Strategy

**A business needs a definition, AI or not. Definitions give clarity and set the path. This group of four specialist workers helps you build yours with your own AI, by asking the right things in the right AI space.**

Ask AI for a strategy and it returns a first plausible answer, settling choices you may not have known needed deciding. Understanding what works and what doesn't takes time, and it starts from a clear account of what you are building: what the business is, whom it serves, why they choose it, how it earns and what it does next.

These workers put those professional questions and their relationships in front of your AI. They ask for what they are missing, develop connected choices and bring them to you. You decide, and when a decision changes, the documents built on it are flagged.

Free under the MIT licence. The whole group, with nothing held back.

## The workers

| Worker | Develops |
| --- | --- |
| `venture-strategist` | The venture definition, objectives, bets and focus, and the strategy review |
| `market-strategist` | Segments, target segments and opportunities |
| `positioning-strategist` | Differentiation, the frame and the category |
| `business-model-designer` | The revenue model, offers and prices |

[AGENTS.md](AGENTS.md) is the group's entry point: its state, members, must-agree rules and routing. Each worker's skills are in its own folder, at `{worker}/.claude/skills/{skill}/SKILL.md`, and its `AGENTS.md` routes a request to them. Contracts and checks are in `.group/`.

## Start

You need an AI agent and Python 3.11 or later. Add the group to your venture's repository at `workers/strategy`, where its commands expect it:

```
git clone https://github.com/LeanOS-Technologies/strategy.git workers/strategy
```

Then, from your repository root, ask your agent:

> Read workers/strategy/AGENTS.md. Establish the initial direction for my venture "my-venture". Here is what I know: ...

Bring your purpose, customers and offer, however rough. The workers ask for the rest.

Their documents are written as candidates under `venture/my-venture/strategy/candidate/`. Nothing becomes current until you accept it. You can also start smaller: ask one worker for one document, such as your venture definition.

To check the documents:

```
python3 workers/strategy/.group/tools/check.py venture/my-venture/strategy
```

## Licence

MIT. Use it, study it, change it and share it. Your strategy documents are yours. See [LICENSE](LICENSE).

Built by [LeanOS](https://www.leanos.tech), which builds systems operating with AI.
