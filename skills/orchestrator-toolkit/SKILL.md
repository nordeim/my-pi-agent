---
name: orchestrator-toolkit
description: Pure-Python orchestration toolkit for task management, complexity analysis, decomposition, persistence, and recovery. Use when breaking down complex projects, tracking progress, or building lightweight orchestration systems.
---

# Orchestrator Toolkit Skill

A pure-Python orchestration toolkit built from patterns extracted from the OpenCode Industrial Orchestrator. Provides task management, complexity analysis, decomposition, persistence, and recovery capabilities.

## Description

The Orchestrator Toolkit is a lightweight, zero-dependency Python library for managing complex workflows. It extracts the most valuable patterns from the industrial-strength OpenCode Industrial Orchestrator and packages them into an easy-to-use toolkit suitable for single-agent or small-team orchestration needs.

## Capabilities

- **Task Management**: Hierarchical tasks with state machines, dependencies, and progress tracking
- **Complexity Analysis**: Heuristic-based task complexity scoring and capability inference
- **Task Decomposition**: Template-based automatic breakdown with 6 templates
- **Persistence**: JSON-based storage for lightweight task persistence
- **Recovery & Health**: Checkpointing, health scoring, and failure recovery mechanisms

## When to Use

Use this skill when you need to:
- Break down complex projects into manageable tasks
- Analyze task complexity and estimate effort
- Track progress and dependencies in workflows
- Persist task state to disk without a database
- Implement retry mechanisms and health monitoring
- Build lightweight orchestration systems

## Quick Start

```python
from orchestrator.tasks.entity import TaskEntity, TaskPriority, TaskComplexity
from orchestrator.tasks.complexity import ComplexityAnalyzer
from orchestrator.tasks.decomposition import TaskDecompositionService
from orchestrator.tasks.templates import TemplateRegistry
from orchestrator.storage.json_store import JsonStore

# Create a task
task = TaskEntity(
    title="Build Web Application",
    description="Create a full-stack web app with authentication",
    priority=TaskPriority.HIGH
)

# Analyze complexity
analyzer = ComplexityAnalyzer()
complexity = analyzer.analyze(task)
print(f"Complexity: {complexity.score:.2f} ({complexity.level.name})")
# Output: Complexity: 0.75 (MODERATE)

# Decompose into subtasks
decomposer = TaskDecompositionService()
print(decomposer.available_templates())
# Output: ['microservice', 'crud', 'ui_component', 'security', 'api', 'refactor']

result = decomposer.decompose(task)
subtasks = task.children

# Persist to storage
store = JsonStore("./tasks.json")
store.save(task)
```

## Templates

| Template | Subtasks | Use Case |
|----------|----------|----------|
| `microservice` | 8 | "Build user authentication microservice" |
| `crud` | 8 | "Create product management CRUD" |
| `ui_component` | 7 | "Build user profile page component" |
| `security` | 7 | "Implement OAuth2 authentication" |
| `api` | 6 | "Create REST API for user management" |
| `refactor` | 6 | "Refactor authentication module" |

## State Machine

Task lifecycle uses a validated state machine:

```
States: pending → ready → in_progress → completed/failed/cancelled
        ↑                    ↓
        └── blocked ←────────┘
        └── paused ←─────────┘

Terminal states: completed, failed, cancelled
```

Valid transitions:
- `pending` → `ready`, `in_progress`, `cancelled`
- `ready` → `in_progress`, `cancelled`
- `in_progress` → `completed`, `failed`, `blocked`, `paused`
- `blocked` → `in_progress`, `cancelled`
- `paused` → `in_progress`, `cancelled`

## Components

### Domain Layer (`domain/`)
- `states.py` — Generic StateMachine with validated transitions
- `events.py` — Domain events (TaskCreated, TaskDecomposed, etc.)
- `exceptions.py` — Domain-specific error types

### Tasks Layer (`tasks/`)
- `entity.py` — TaskEntity with hierarchy, DAG dependencies, PERT estimates
- `complexity.py` — ComplexityAnalyzer (keyword/capability detection)
- `decomposition.py` — TaskDecompositionService with TemplateRegistry integration
- `templates.py` — 6 pre-built templates for common patterns

### Recovery Layer (`recovery/`)
- `checkpoint.py` — CheckpointMixin for state serialization
- `health.py` — HealthScorer for task vitality assessment

### Storage Layer (`storage/`)
- `json_store.py` — JSON persistence with UUID string keys

## Configuration

No external configuration required. All components work out-of-the-box.

```python
# Custom storage path
store = JsonStore("/path/to/my/tasks.json")

# Custom complexity thresholds
analyzer = ComplexityAnalyzer()
```

## Testing

Run the comprehensive test suite:

```bash
cd /home/pete/.openclaw/workspace
source /opt/venv/bin/activate
PYTHONPATH=/home/pete/.openclaw/workspace python3 -m pytest orchestrator/tests/ -v
# 119 tests passing
```

## Examples

Located in `orchestrator/examples/`:

```bash
cd /home/pete/.openclaw/workspace
PYTHONPATH=/home/pete/.openclaw/workspace python3 orchestrator/examples/decompose_task.py
PYTHONPATH=/home/pete/.openclaw/workspace python3 orchestrator/examples/state_machine_demo.py
PYTHONPATH=/home/pete/.openclaw/workspace python3 orchestrator/examples/basic_usage.py
```

## Design Philosophy

- **Pure Python**: Zero external dependencies beyond standard library
- **Event-Driven**: Domain events for decoupled communication
- **Type Hints**: Full type hinting for IDE support
- **Tested**: 119 tests covering all functionality
- **Extensible**: Clean interfaces for customization

## Patterns Extracted from OpenCode Industrial Orchestrator

1. **State Machine Validation** — 8-state task machine + 12-state session machine
2. **Checkpoint-Based Recovery** — State serialization for failure recovery
3. **Health Scoring** — Multi-factor health assessment algorithm
4. **Task Decomposition with DAGs** — Hierarchical breakdown using dependency graphs
5. **PERT Estimation** — Three-point estimation with confidence weighting
6. **Event Collection** — Domain event emission for audit trails
7. **History Tracking** — Task lifecycle tracking for analytics
8. **TemplateRegistry** — Pluggable template system for decomposition patterns

## Complexity Levels

| Level | Hours Range | Description |
|-------|-------------|-------------|
| TRIVIAL | < 0.25h | Quick fixes, typo corrections |
| SIMPLE | 0.25-1h | Single function, minor feature |
| MODERATE | 1-4h | Component, API endpoint |
| COMPLEX | 4-8h | Service, feature module |
| EXPERT | 8+h | System, distributed architecture |

## Limitations

- Designed for single-agent or small-team use
- No built-in distributed consensus (use external coordination for multi-node)
- JSON storage not suitable for high-concurrency scenarios
- Complexity analysis is heuristic-based, not ML-trained

## Dependencies

- Python 3.8+
- No external dependencies (uses only standard library)

## Performance

- Task creation: <1ms
- Complexity analysis: ~2ms
- Task decomposition: ~5-10ms (depends on template)
- JSON storage: ~1-5ms per operation

## File Locations

```
/home/pete/.openclaw/workspace/orchestrator/
├── domain/           # States, events, exceptions
├── tasks/            # Entity, complexity, decomposition, templates
├── recovery/         # Checkpoint, health
├── storage/          # JSON store
├── examples/         # Usage demos
└── tests/            # 119 tests
```
