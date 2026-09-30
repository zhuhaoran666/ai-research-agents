# Multi-Agent AI Research Workflow

[中文](README.md) · English

A portable framework for research collaboration: start with a problem and an initial idea, investigate prior work, co-design methods and experiments, implement and analyze them, write the paper and figures, and seek an independent review of substantive issues. Researchers lead scientific judgment and key experimental design; agents support literature search, implementation, execution, analysis, and testable improvements.

**This repository provides role instructions, workflows, and optional templates. It is not an implemented autonomous execution platform.** Use the roles in a multi-agent tool or apply them sequentially with one agent. The framework is not tied to a model, orchestrator, discipline, publication venue, or compute environment.

## Quick start

1. Copy [`profiles/user.example.md`](profiles/user.example.md) to local `profiles/user.md`. Record only preferences relevant to collaboration; the local file is ignored by Git.
2. Create a research note, optionally using [`templates/research-note.md`](templates/research-note.md). Describe the problem, initial idea, available materials, resource limits, and most important question to test.
3. Give the main agent [`agents/README.md`](agents/README.md), [`agents/mentor.md`](agents/mentor.md), the local profile, and the research note. Load other role instructions as needed. Sequential use works without a multi-agent orchestrator.
4. Start where the project needs help. A new idea often starts with `literature + method`; existing code or results can go to `code + analysis`. Use `writing` for the manuscript and an independent `reviewer` for its final assessment.

A starting task to adapt:

> Read the shared principles, mentor and literature role instructions, and this project's research note. Investigate existing solutions, the closest strong baselines, and their relevant limitations. Identify the evidence that most affects the initial idea and suggest two experiments to design together. State which sources and sections you actually read. Keep proposed work distinct from completed results.

## Seven responsibilities

| Role | Main responsibility |
|---|---|
| [`literature`](agents/literature.md) | Find existing solutions, baselines, transferable mechanisms, and counterevidence; record sources |
| [`method`](agents/method.md) | Co-design methods and key experiments with the researcher; assess feasibility and weaknesses |
| [`code`](agents/code.md) | Implement and run baselines, methods, and ablations; preserve configurations, logs, and reproduction instructions |
| [`analysis`](agents/analysis.md) | Verify results, diagnose failures, and propose further comparisons with the method role |
| [`writing`](agents/paper-writer.md) | Read comparable papers closely; write and create research figures from actual evidence |
| [`reviewer`](agents/manuscript-reviewer.md) | Independently investigate the literature and assess contributions, methods, comparisons, and conclusions |
| [`mentor`](agents/mentor.md) | Coordinate direction, priorities, and collaboration; clarify important intent and maintain preferences |

These are responsibilities, not seven required persistent processes. Keep writing and review separate when independent judgment is needed. Other roles may be combined or supplemented with temporary specialists.

## Principles

- **Learn from evidence.** Study how others solve problems and write papers. Check mechanisms and novelty claims against original papers, official implementations, and meaningful comparisons.
- **Keep researchers involved in design.** Researchers choose problems, hypotheses, key experiments, and major tradeoffs. Agents actively identify weaknesses, feasibility limits, and alternative explanations.
- **Let experiments and writing inform each other.** Enter at any point supported by the available materials; there are no mandatory stage gates.
- **Make results traceable.** Connect major claims to actual code, configurations, data descriptions, run outputs, and analysis. Preserve negative results too.
- **Review substantive issues independently.** Reviewers search beyond the author's references and assess whether the argument holds before addressing wording details.

## Documentation

- [Architecture and collaboration](docs/architecture.md) · [Lightweight workflow](docs/workflows.md) · [Task coordination](docs/operating-model.md)
- [Literature, writing, and review](docs/literature-and-writing.md) · [Personalization](docs/personalization.md)
- [Optional templates](templates/README.md) · [Examples](examples/README.md)
- [Comparison with AutoResearch projects](docs/prior-art.md) · [Lessons from nnU-Net's research design](docs/nnunet-lessons.md)

The linked role instructions and detailed documentation are currently in Chinese. Local `profiles/user.md` and project research materials stay outside version control by default. Keep private data, credentials, unlicensed paper copies, and raw source caches out of the public repository.
