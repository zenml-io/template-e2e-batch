# {% include 'license_header' %}


import json
import os
from typing import Type

from zenml.enums import ArtifactType
from zenml.io import fileio
from zenml.materializers.base_materializer import BaseMaterializer

from artifacts import ModelMetadata


class ModelMetadataMaterializer(BaseMaterializer):
    ASSOCIATED_TYPES = (ModelMetadata,)
    ASSOCIATED_ARTIFACT_TYPE = ArtifactType.STATISTICS

    def load(self, data_type: Type[ModelMetadata]) -> ModelMetadata:
        """Read from artifact store.

        Args:
            data_type: What type the artifact data should be loaded as.

        Raises:
            ValueError: on deserialization issue

        Returns:
            Read artifact.
        """
        super().load(data_type)

        ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
        import sklearn.ensemble
        import sklearn.linear_model
        import sklearn.tree

        modules = [sklearn.ensemble, sklearn.linear_model, sklearn.tree]

        with fileio.open(os.path.join(self.uri, "data.json"), "r") as f:
            data = json.loads(f.read())
        class_name = data["class"]
        cls = None
        for module in modules:
            if cls := getattr(module, class_name, None):
                break
        if cls is None:
            raise ValueError(
                f"Cannot deserialize `{class_name}` using {self.__class__.__name__}. "
                f"Only classes from modules {[m.__name__ for m in modules]} "
                "are supported"
            )
        data["class"] = cls
        ### YOUR CODE ENDS HERE ###

        return data

    def save(self, data: ModelMetadata) -> None:
        """Write to artifact store.

        Args:
            data: The data of the artifact to save.
        """
        super().save(data)

        ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
        # Dump the model metadata directly into the artifact store as a YAML file
        with fileio.open(os.path.join(self.uri, "data.json"), "w") as f:
            data["class"] = data["class"].__name__
            f.write(json.dumps(data))
        ### YOUR CODE ENDS HERE ###
