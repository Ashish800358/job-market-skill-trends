from abc import ABC, abstractmethod
from typing import List, Dict
import csv
import os
from datetime import datetime

Job = Dict[str, str]

class BaseScraper(ABC):
    @abstractmethod
    def search(self, role: str, location: str, limit: int = 100) -> List[Job]:
        raise NotImplementedError

    @staticmethod
    def save_csv(rows: List[Job], out_path: str) -> None:
        if not rows:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["title","company","location","url","description"]
                )
                writer.writeheader()
            return
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["title","company","location","url","description"]
            )
            writer.writeheader()
            for r in rows:
                writer.writerow(r)

    @staticmethod
    def default_output_path() -> str:
        os.makedirs("data/raw", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"data/raw/jobs_{timestamp}.csv"
