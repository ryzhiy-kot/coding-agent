from .agents.setup import create_root_agent


def main() -> None:
    print("Coding agent ready. Use create_root_agent() or create_financial_analyst_agent().")


__all__ = ["create_root_agent", "main"]
