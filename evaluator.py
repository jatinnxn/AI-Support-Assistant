from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass
class EvaluationResult:
    test_name: str
    passed: bool
    score: float
    message: str


class Evaluator:

    @staticmethod
    def evaluate(
        test_name: str,
        prediction: Dict[str, Any],
        validator: Callable[[Dict[str, Any]], bool],
    ) -> EvaluationResult:

        try:
            passed = validator(prediction)

            return EvaluationResult(
                test_name=test_name,
                passed=passed,
                score=1.0 if passed else 0.0,
                message="PASS" if passed else "FAIL",
            )

        except Exception as e:

            return EvaluationResult(
                test_name=test_name,
                passed=False,
                score=0.0,
                message=str(e),
            )