# Multi-Agent AI Research Workflow

[中文](README.md) · English

A portable framework for research collaboration: start with a problem and an initial idea, investigate prior work, co-design methods and experiments, implement and analyze them, write the paper and figures, and seek an independent review of substantive issues. Researchers lead scientific judgment and key experimental design; agents support literature search, implementation, execution, analysis, and testable improvements.

**This repository provides roles, skills, workflows, and optional templates for human-in-the-loop research.** Researchers participate in consequential scientific decisions; agents reuse existing materials, decisions, and authorization to complete work within scope. See the [shared conventions](agents/README.md) for execution boundaries. This is not an already running autonomous platform and is not tied to a model, orchestrator, discipline, or compute environment.

Move lengthy retrieval, comparison, and analysis to the background within the explicitly confirmed scope. Keep the main conversation responsive, share verified findings promptly, and focus each exchange on one research decision. See "Real-time communication and background work" in the [shared conventions](agents/README.md), including how to handle clients without background or interruption support.

## Quick start

1. Give the mentor your idea, code, results, or manuscript and describe what you want to resolve. The [guided intake](docs/mentor-guided-intake.md) identifies your starting point and asks one to three questions per round, limited to what the next step needs. Agents investigate unfamiliar literature, baselines, and environments; a completed questionnaire is not required.
2. The [idea description guide](docs/idea-guideline.md) and optional [short template](templates/idea.md) can help, and you can start without a method. The mentor gradually collects existing materials and answers in one [research note](templates/research-note.md). For lasting preferences, optionally copy [`profiles/user.example.md`](profiles/user.example.md) to local `profiles/user.md`; work can begin without it, and the local file is ignored by Git.
3. For cross-role work, load the [research workflow entry](skills/ai-research-workflow/SKILL.md) and [shared conventions](agents/README.md). For a focused task, choose its primary skill from the [role skill index](skills/README.md). Load only relevant materials and private preferences. Sequential execution is possible when subagents are unavailable; disclose any independence limitations.
4. Start where the project needs help. A new idea often starts with `literature + method`; existing code or results can go to `code + analysis`. Use `writing` for the manuscript and the `reviewer` entry point to assign independent writing and domain experts for final review.

A starting task to adapt:

> Reuse this project's existing materials and select roles and skills for the current problem. I want to resolve: … . Ask only for information that changes the next step, reuse existing decisions and authorization, and continue independent work. Bring evidence and options to consequential scientific or resource choices. Deliver actual artifacts, verification status, and important gaps without expanding a local task into a full workflow.

For experiments, the [feedback and evidence guide](docs/experiment-loop.md) connects existing execution tools and distinguishes engineering failures, valid negative results, and insufficient evidence. An optional Python standard-library [evidence checker](scripts/check_evidence.py) checks files, metric sources, and declared numbers. It does not run experiments or certify scientific validity.

## Research and editing responsibilities

| Role | Main responsibility |
|---|---|
| [`literature`](agents/literature.md) | Find existing solutions, baselines, transferable mechanisms, and counterevidence; record sources |
| [`method`](agents/method.md) | Co-design methods and key experiments with the researcher; assess feasibility and weaknesses |
| [`code`](agents/code.md) | Implement and run baselines, methods, and ablations; preserve configurations, logs, and reproduction instructions |
| [`analysis`](agents/analysis.md) | Verify results, diagnose failures, and propose further comparisons with the method role |
| [`writing`](agents/paper-writer.md) | Read comparable papers closely; write and create research figures from actual evidence |
| [`reviewer`](agents/manuscript-reviewer.md) | Two independent experts assess academic language, field-specific writing conventions, and substantive research issues |
| [`mentor`](agents/mentor.md) | Guide users through the information needed next; coordinate direction, priorities, and collaboration |
| [`review-redundancy`](agents/redundancy-reviewer.md) | Apply deletion tests to identify unnecessary content and simplify it while preserving meaning |

These are responsibilities, not required persistent processes. Review contains a [writing expert, `review-writing`](agents/writing-reviewer.md), who checks grammar, word choice, terminology, and academic expression, and a [domain expert, `review-domain`](agents/domain-reviewer.md), who reads comparable papers from leading journals and conferences to assess argument, structure, experiments, and figures, as well as research validity. Both remain independent of the manuscript authoring role and produce separate reports for the mentor to consolidate. `reviewer` is a dispatch entry point, not a third reviewer. Other roles may be combined or supplemented with temporary specialists.

The [redundancy reviewer, `review-redundancy`](agents/redundancy-reviewer.md), checks conversation, prose, documentation, and code across roles. Detection is the default mode and lists only actionable items as “original → suggestion (one-sentence reason).” Simplification mode returns the complete revised text. When there is no clear issue, its only reply is “未发现明确的可删冗余”.

## Principles

- **Learn from evidence.** Study how others solve problems and write papers. Check mechanisms and novelty claims against original papers, official implementations, and meaningful comparisons.
- **Keep researchers involved in consequential decisions.** Researchers participate in scientific direction, key protocols, and substantive claims. Continue concrete work within existing authorization; additional resources or external disclosure require the applicable authorization.
- **Let experiments and writing inform each other.** Enter at any point supported by the available materials; there are no mandatory stage gates.
- **Make results traceable.** Connect major claims to actual code, configurations, data descriptions, run outputs, and analysis. Preserve negative results too.
- **Let every role improve its work.** Use actual failures and explicit feedback within the task, retain verification, applicability, and a way to revert, and keep unverified strategies provisional. Better work strategies do not establish method validity. See [RSI](docs/rsi.md).
- **Use two independent review perspectives.** Writing and domain experts may review in parallel; consolidation prioritizes issues that affect research validity. Domain experts search beyond the author's references and support comparisons of writing conventions with actual source passages.

## Documentation

- [Mentor guided intake](docs/mentor-guided-intake.md) · [Idea description guide](docs/idea-guideline.md) · [Architecture and collaboration](docs/architecture.md) · [Lightweight workflow](docs/workflows.md) · [Task coordination](docs/operating-model.md)
- [Experiment feedback and evidence](docs/experiment-loop.md) · [Runnable synthetic evidence example](examples/evidence-demo/README.md)
- [Literature, writing, and review](docs/literature-and-writing.md) · [Search sources by field](docs/literature-sources.md) · [Personalization](docs/personalization.md) · [RSI for all roles](docs/rsi.md)
- [Skills for ten research roles](skills/README.md) · [Workflow entry](skills/ai-research-workflow/SKILL.md) · [Research paper writing](skills/research-paper-writing/SKILL.md) · [Readable and maintainable code](skills/readable-code-engineer/SKILL.md)
- [Optional templates](templates/README.md) · [Examples](examples/README.md)
- [Comparison with AutoResearch projects](docs/prior-art.md) · [Lessons and limits of The AI Scientist](docs/ai-scientist-lessons.md) · [Lessons from nnU-Net's research design](docs/nnunet-lessons.md)
- [Lessons from real use (2026-10)](docs/lessons-2026-10.md) · [Changelog](CHANGELOG.md)

The linked role instructions and detailed documentation are currently in Chinese. Local `profiles/user.md` and project research materials stay outside version control by default (`.gitignore` also excludes `studies/` and `docs/reference/`, which you can create for local projects and reference material). Keep private data, credentials, unlicensed paper copies, and raw source caches out of the public repository.
