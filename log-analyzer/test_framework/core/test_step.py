from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional, List, Dict, Any


class StepStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    PASSED = auto()
    FAILED = auto()
    SKIPPED = auto()
    WARNING = auto()


@dataclass
class TestStep:
    name: str
    description: str = ""
    status: StepStatus = StepStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    substeps: List['TestStep'] = field(default_factory=list)
    error: Optional[Exception] = None
    screenshot_path: Optional[str] = None

    def start(self):
        self.status = StepStatus.RUNNING
        self.start_time = datetime.now()
        return self

    def end(self, status: StepStatus = StepStatus.PASSED, error: Optional[Exception] = None):
        self.status = status
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.error = error
        return self

    def add_substep(self, step: 'TestStep'):
        self.substeps.append(step)
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status.name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "metadata": self.metadata,
            "substeps": [s.to_dict() for s in self.substeps],
            "error": str(self.error) if self.error else None,
            "screenshot": self.screenshot_path
        }


class StepBuilder:
    def __init__(self, parent_step: Optional[TestStep] = None):
        self._current_step = TestStep("Unnamed Step")
        self._parent_step = parent_step

    def name(self, name: str) -> 'StepBuilder':
        self._current_step.name = name
        return self

    def description(self, description: str) -> 'StepBuilder':
        self._current_step.description = description
        return self

    def metadata(self, key: str, value: Any) -> 'StepBuilder':
        self._current_step.metadata[key] = value
        return self

    def with_screenshot(self, path: str) -> 'StepBuilder':
        self._current_step.screenshot_path = path
        return self

    def build(self) -> TestStep:
        if self._parent_step:
            self._parent_step.add_substep(self._current_step)
        return self._current_step


def step(name: Optional[str] = None, description: str = ""):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get the test case instance (self)
            self = args[0]

            # Create step name if not provided
            step_name = name or func.__name__.replace('_', ' ').title()

            # Create and start the step
            step = (TestStep(step_name, description)
                    .start()
                    .metadata("location", f"{func.__module__}.{func.__qualname__}"))

            # Add to test case's steps
            if hasattr(self, 'add_step'):
                self.add_step(step)

            try:
                result = func(*args, **kwargs)
                step.end(StepStatus.PASSED)
                return result
            except AssertionError as e:
                step.end(StepStatus.FAILED, e)
                raise
            except Exception as e:
                step.end(StepStatus.ERROR, e)
                raise
            finally:
                if hasattr(self, 'record_step'):
                    self.record_step(step)

        wrapper.is_step = True
        return wrapper

    return decorator


class StepRecorder:
    def __init__(self):
        self.steps: List[TestStep] = []
        self._current_step: Optional[TestStep] = None

    def begin_step(self, name: str, description: str = "") -> TestStep:
        step = TestStep(name, description).start()
        if self._current_step:
            self._current_step.add_substep(step)
        else:
            self.steps.append(step)
        self._current_step = step
        return step

    def end_current_step(self, status: StepStatus = StepStatus.PASSED,
                         error: Optional[Exception] = None):
        if self._current_step:
            self._current_step.end(status, error)
            self._current_step = None

    def add_step_metadata(self, key: str, value: Any):
        if self._current_step:
            self._current_step.metadata[key] = value

    def capture_screenshot(self, path: str):
        if self._current_step:
            self._current_step.screenshot_path = path

    def get_step_hierarchy(self) -> List[Dict[str, Any]]:
        return [step.to_dict() for step in self.steps]