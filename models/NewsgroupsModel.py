import contextlib
import os
from typing import Any
import joblib
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sklearn.pipeline import Pipeline


class PredictionInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    category: str


memory = joblib.Memory(location="cache.joblib")

@memory.cache(ignore=["model"])
def predict(model: Pipeline, text: str) -> int:
    prediction = model.predict([text])
    return prediction[0]

class NewsgroupsModel:
    model: Pipeline = None
    targets: list[str] = None

    def load_model(self) -> None:
        """Loads the model"""
        model_file = os.path.join(os.path.dirname(__file__), "newsgroups_model.joblib")
        loaded_model: tuple[Pipeline, list[str]] = joblib.load(model_file)
        model, targets = loaded_model
        self.model = model
        self.targets = targets

    async def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model or not self.targets:
            raise RuntimeError("Model is not loaded")
        prediction = predict(self.model, input.text)
        category = self.targets[prediction]
        return PredictionOutput(category=category)


newgroups_model = NewsgroupsModel()