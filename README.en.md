# Multi-Agent AI Research Workflow

[中文](README.md) · English

A portable framework for research collaboration: start with a problem and an initial idea, investigate prior work, co-design methods and experiments, implement and analyze them, write the paper and figures, and seek an independent review of substantive issues. Researchers lead scientific judgment and key experimental design; agents support literature search, implementation, execution, analysis, and testable improvements.

**This repository provides role instructions, workflows, and optional templates. It is not an implemented autonomous execution platform, and it does not aim at fully autonomous research.** It is a human-in-the-loop framework: researchers take part in and confirm key decisions (see "Human in the loop" in the [shared conventions](agents/README.md)), and agents proceed within the confirmed scope. Use the roles in a multi-agent tool or apply them sequentially with one agent. The framework is not tied to a model, orchestrator, discipline, publication venue, or compute environment.

## Quick start

1. Give the mentor your idea, code, results, or manuscript and describe what you want to resolve. The [guided intake](docs/mentor-guided-intake.md) identifies your starting point and asks one to three questions per round, limited to what the next step needs. Agents investigate unfamiliar literature, baselines, and environments; a completed questionnaire is not required.
2. The [idea description guide](docs/idea-guideline.md) and optional [short template](templates/idea.md) can help, and you can start without a method. The mentor gradually collects existing materials and answers in one [research note](templates/research-note.md). For lasting preferences, optionally copy [`profiles/user.example.md`](profiles/user.example.md) to local `profiles/user.md`; work can begin without it, and the local file is ignored by Git.
3. Give the main agent [`agents/README.md`](agents/README.md), [`agents/mentor.md`](agents/mentor.md), the local profile, and the research note. All roles also load the [RSI conventions](docs/rsi.md) and applicable local improvement records. Load other role instructions with their companion files (see the loading table in [`agents/README.md`](agents/README.md)) as needed. Sequential use works without a multi-agent orchestrator.
4. Start where the project needs help. A new idea often starts with `literature + method`; existing code or results can go to `code + analysis`. Use `writing` for the manuscript and the `reviewer` entry point to assign independent writing and domain experts for final review.

A starting task to adapt:

> Read the shared principles and mentor instructions, reusing this project's materials. I want to resolve: … . Identify my starting point and guide me through the minimum information needed next, asking one to three questions per round. Help investigate unfamiliar technical details and offer evidence-backed options. Proceed when enough is known, continue independent work while waiting, and keep agreements and open questions in one research note.

For experiments, the [feedback and evidence guide](docs/experiment-loop.md) connects existing execution tools and distinguishes engineering failures, valid negative results, and insufficient evidence. An optional Python standard-library [evidence checker](scripts/check_evidence.py) checks files, metric sources, and declared numbers. It does not run experiments or certify scientific validity.

## Seven responsibilities

| Role | Main responsibility |
|---|---|
| [`literature`](agents/literature.md) | Find existing solutions, baselines, transferable mechanisms, and counterevidence; record sources |
| [`method`](agents/method.md) | Co-design methods and key experiments with the researcher; assess feasibility and weaknesses |
| [`code`](agents/code.md) | Implement and run baselines, methods, and ablations; preserve configurations, logs, and reproduction instructions |
| [`analysis`](agents/analysis.md) | Verify results, diagnose failures, and propose further comparisons with the method role |
| [`writing`](agents/paper-writer.md) | Read comparable papers closely; write and create research figures from actual evidence |
| [`reviewer`](agents/manuscript-reviewer.md) | Two independent experts assess academic language, field-specific writing conventions, and substantive research issues |
| [`mentor`](agents/mentor.md) | Guide users through the information needed next; coordinate direction, priorities, and collaboration |

These are responsibilities, not seven required persistent processes. Review contains a [writing expert, `review-writing`](agents/writing-reviewer.md), who checks grammar, word choice, terminology, and academic expression, and a [domain expert, `review-domain`](agents/domain-reviewer.md), who reads comparable papers from leading journals and conferences to assess argument, structure, experiments, and figures, as well as research validity. Both remain independent of the manuscript authoring role and produce separate reports for the mentor to consolidate. `reviewer` is a dispatch entry point, not a third reviewer. Other roles may be combined or supplemented with temporary specialists.

## Principles

- **Learn from evidence.** Study how others solve problems and write papers. Check mechanisms and novelty claims against original papers, official implementations, and meaningful comparisons.
- **Keep researchers involved in design.** Researchers choose problems, hypotheses, key experiments, and major tradeoffs. Agents actively identify weaknesses, feasibility limits, and alternative explanations.
- **Let experiments and writing inform each other.** Enter at any point supported by the available materials; there are no mandatory stage gates.
- **Make results traceable.** Connect major claims to actual code, configurations, data descriptions, run outputs, and analysis. Preserve negative results too.
- **Let every role improve its own work.** Agents use user requirements, feedback, and actual outcomes to revise strategies and role instructions, including how they diagnose and verify improvements. Check changes against real materials, keep unverified strategies provisional, and preserve a way to revert. [RSI](docs/rsi.md) is applied as needed, with no extra permanent role or per-step approval process.
- **Use two independent review perspectives.** Writing and domain experts may review in parallel; consolidation prioritizes issues that affect research validity. Domain experts search beyond the author's references and support comparisons of writing conventions with actual source passages.

## Documentation

- [Mentor guided intake](docs/mentor-guided-intake.md) · [Idea description guide](docs/idea-guideline.md) · [Architecture and collaboration](docs/architecture.md) · [Lightweight workflow](docs/workflows.md) · [Task coordination](docs/operating-model.md)
- [Experiment feedback and evidence](docs/experiment-loop.md) · [Runnable synthetic evidence example](examples/evidence-demo/README.md)
- [Literature, writing, and review](docs/literature-and-writing.md) · [Search sources by field](docs/literature-sources.md) · [Personalization](docs/personalization.md) · [RSI for all roles](docs/rsi.md)
- [Framework-owned skills](skills/README.md) · [Research paper writing](skills/research-paper-writing/SKILL.md) · [Source learning notes](skills/research-paper-writing/references/source-notes.md)
- [Optional templates](templates/README.md) · [Examples](examples/README.md)
- [Comparison with AutoResearch projects](docs/prior-art.md) · [Lessons and limits of The AI Scientist](docs/ai-scientist-lessons.md) · [Lessons from nnU-Net's research design](docs/nnunet-lessons.md)
- [Lessons from real use (2026-10)](docs/lessons-2026-10.md) · [Changelog](CHANGELOG.md)

The linked role instructions and detailed documentation are currently in Chinese. Local `profiles/user.md` and project research materials stay outside version control by default (`.gitignore` also excludes `studies/` and `docs/reference/`, which you can create for local projects and reference material). Keep private data, credentials, unlicensed paper copies, and raw source caches out of the public repository.
