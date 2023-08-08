#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.


import os
import pathlib
import shutil
import subprocess
import sys
from typing import Optional

import pytest
from copier import Worker
from zenml.client import Client
from zenml.enums import ExecutionStatus

TEMPLATE_DIRECTORY = str(
    pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent, "template")
)


def generate_and_run_project(
    tmp_path_factory: pytest.TempPathFactory,
    open_source_license: Optional[str] = "apache",
    auto_format: bool = True,
    pipeline_name: str = "e2e_pipeline_pytest",
    hyperparameters_tuning: bool = True,
    metric_compare_promotion: bool = True,
    data_quality_checks: bool = True,
):
    """Generate and run the starter project with different options."""

    answers = {
        "project_name": "Pytest Templated Project",
        "version": "0.0.1",
        "open_source_license": str(open_source_license).lower(),
        "auto_format": auto_format,
        "pipeline_name": pipeline_name,
        "hyperparameters_tuning": hyperparameters_tuning,
        "metric_compare_promotion": metric_compare_promotion,
        "data_quality_checks": data_quality_checks,
    }
    if open_source_license:
        answers["email"] = "pytest@zenml.io"
        answers["full_name"] = "Pytest"

    # generate the template in a temp path
    current_dir = os.getcwd()
    dst_path = tmp_path_factory.mktemp("pytest-template")
    print("TEMPLATE_DIR:", TEMPLATE_DIRECTORY)
    print("dst_path:", dst_path)
    print("current_dir:", current_dir)
    os.chdir(str(dst_path))
    with Worker(
        src_path=TEMPLATE_DIRECTORY,
        dst_path=str(dst_path),
        data=answers,
        unsafe=True,
    ) as worker:
        worker.run_copy()

    # run the project
    call = [sys.executable, "run.py"]

    try:
        subprocess.check_call(
            call,
            cwd=str(dst_path),
            env=os.environ.copy(),
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to run project generated with parameters: {answers}"
        ) from e

    # check the pipeline run is successful
    for pipeline_suffix in ["_training", "_batch_inference"]:
        pipeline = Client().get_pipeline(pipeline_name + pipeline_suffix)
        assert pipeline
        runs = pipeline.runs
        assert len(runs) == 1
        assert runs[0].status == ExecutionStatus.COMPLETED

        # clean up
        Client().delete_pipeline(pipeline_name + pipeline_suffix)

    os.chdir(current_dir)
    shutil.rmtree(dst_path)


@pytest.mark.parametrize("open_source_license", ["mit", None], ids=["oss", "css"])
def test_generate_license(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
    open_source_license: Optional[str],
):
    """Test generating licenses."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        open_source_license=open_source_license,
    )


def test_no_auto_format(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
):
    """Test turning off code auto-format."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        auto_format=False,
    )


def test_custom_pipeline_name(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
):
    """Test using custom pipeline name."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        pipeline_name="custom_pipeline_name",
    )

def test_no_hp_tuning(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
):
    """Test turning off hyperparameter tuning."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        hyperparameters_tuning=False
    )

def test_latest_promotion(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
):
    """Test using latest promotion."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        metric_compare_promotion=False
    )

def test_no_data_quality_checks(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
):
    """Test skipping Data Quality checks."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory, 
        data_quality_checks=False,
    )
