from dataclasses import dataclass, asdict
from django.db import models
from typing import List, Optional
from pathlib import Path
from core.json_storage import load_json, save_json


class Company(models.Model):
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200, null=True, blank=True)  # Champ optionnel
    def __str__(self):
        return self.name

    @staticmethod
    def all_companies(base_dir: Optional[Path] = None) -> List["Company"]:
        """
        Charge toutes les entreprises depuis companies.json.
        """
        data = load_json("companies.json", base_dir=base_dir)
        return [Company(**item) for item in data]

    @staticmethod
    def save_all(companies: List["Company"], base_dir: Optional[Path] = None) -> None:
        """
        Sauvegarde toutes les entreprises dans companies.json.
        """
        save_json("companies.json", [asdict(c) for c in companies], base_dir=base_dir)


