import os
import subprocess

import pytest
from pyspark.sql import SparkSession

os.environ["SPARK_TESTING"] = "1"


def _has_java_runtime() -> bool:
	try:
		result = subprocess.run(
			["java", "-version"],
			capture_output=True,
			text=True,
			check=False,
		)
		return result.returncode == 0
	except FileNotFoundError:
		return False


@pytest.fixture(scope="session")
def spark_session():
	if not _has_java_runtime():
		pytest.skip("Java runtime is not available for PySpark tests")

	spark = (
		SparkSession.builder.master("local[*]")
		.appName("ny-rides-tests")
		.config("spark.ui.enabled", "false")
		.config("spark.sql.shuffle.partitions", "1")
		.getOrCreate()
	)

	yield spark

	spark.stop()
