# Databricks notebook source
# MAGIC %md 
# MAGIC You may find this series of notebooks at https://github.com/databricks-industry-solutions/ocr-phi-masking. For more information about this solution accelerator, visit https://www.databricks.com/solutions/accelerators/automated-phi-removal.

# COMMAND ----------

# MAGIC %md
# MAGIC # PHI de-identification 
# MAGIC Under the Health Insurance Portability and Accountability Act (HIPAA) minimum necessary standard, HIPAA-covered entities (such as health systems and insurers) are required to make reasonable efforts to ensure that access to Protected Health Information (PHI) is limited to the minimum necessary information to accomplish the intended purpose of particular use, disclosure, or request.
# MAGIC 
# MAGIC In this solution accelerator we show how to use databricks lakehouse platform and John Snow Lab's SparkOCR and NLP for Health Care pre-trained models to:
# MAGIC 
# MAGIC 1. Store clinical notes in pdf format in deltalake
# MAGIC 2. Use [SparkOCR](https://nlp.johnsnowlabs.com/docs/en/ocr) to improve image quality and extract text from pdfs
# MAGIC 3. Use [SparkNLP pre-trained models](https://nlp.johnsnowlabs.com/2020/08/04/deidentify_large_en.html) for phi extraction and de-identification
# MAGIC 
# MAGIC 
# MAGIC <img src="https://hls-eng-data-public.s3.amazonaws.com/img/phi-deid-ra.png" width=65%>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Notebooks
# MAGIC <img src="https://hls-eng-data-public.s3.amazonaws.com/img/phi-deid-dataflow.png" width=30%>
# MAGIC 
# MAGIC  1. `pdf-ocr`: This notebook imports pdf files containing oncology reports and uses sparkOCR for image processing and text extraction. Resulting entities and text are stored in delta
# MAGIC  2. `phi-deidentification`: In this notebook we use pre-trained models to extract phi and mask extracted phi. Resulting obfuscated clinical notes are stored in delta for downstream analysis. 
# MAGIC  3. `config`: Utility notebook for setting up the environment

# COMMAND ----------

slides_html="""

<iframe src="https://docs.google.com/presentation/d/1yR3oBKg8vvwKjvj4WWezf5ygJweo8rWuklD7IF4uVX0/embed?start=true&loop=true&delayms=4000" frameborder="0" width="900" height="560" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
"""
displayHTML(slides_html)

# COMMAND ----------

# MAGIC %md
# MAGIC ## License
# MAGIC Copyright / License info of the notebook. Copyright [2021] the Notebook Authors.  The source in this notebook is provided subject to the [Apache 2.0 License](https://spdx.org/licenses/Apache-2.0.html).  All included or referenced third party libraries are subject to the licenses set forth below.
# MAGIC 
# MAGIC |Library Name|Library License|Library License URL|Library Source URL| 
# MAGIC | :-: | :-:| :-: | :-:|
# MAGIC |Pandas |BSD 3-Clause License| https://github.com/pandas-dev/pandas/blob/master/LICENSE | https://github.com/pandas-dev/pandas|
# MAGIC |Numpy |BSD 3-Clause License| https://github.com/numpy/numpy/blob/main/LICENSE.txt | https://github.com/numpy/numpy|
# MAGIC |Apache Spark |Apache License 2.0| https://github.com/apache/spark/blob/master/LICENSE | https://github.com/apache/spark/tree/master/python/pyspark|
# MAGIC |Spark NLP |Apache-2.0 License| https://github.com/JohnSnowLabs/spark-nlp/blob/master/LICENSE | https://github.com/JohnSnowLabs/spark-nlp|
# MAGIC |MatPlotLib | | https://github.com/matplotlib/matplotlib/blob/master/LICENSE/LICENSE | https://github.com/matplotlib/matplotlib|
# MAGIC |Pillow (PIL) | HPND License| https://github.com/python-pillow/Pillow/blob/master/LICENSE | https://github.com/python-pillow/Pillow/|
# MAGIC |Spark NLP for Healthcare|[Proprietary license - John Snow Labs Inc.](https://www.johnsnowlabs.com/spark-nlp-health/) |NA|NA|
# MAGIC |Spark OCR |[Proprietary license - John Snow Labs Inc.](https://nlp.johnsnowlabs.com/docs/en/ocr) |NA|NA|
# MAGIC 
# MAGIC |Author|
# MAGIC |-|
# MAGIC |Databricks Inc.|
# MAGIC |John Snow Labs Inc.|

# COMMAND ----------

# MAGIC %md
# MAGIC ## Disclaimers
# MAGIC Databricks Inc. (“Databricks”) does not dispense medical, diagnosis, or treatment advice. This Solution Accelerator (“tool”) is for informational purposes only and may not be used as a substitute for professional medical advice, treatment, or diagnosis. This tool may not be used within Databricks to process Protected Health Information (“PHI”) as defined in the Health Insurance Portability and Accountability Act of 1996, unless you have executed with Databricks a contract that allows for processing PHI, an accompanying Business Associate Agreement (BAA), and are running this notebook within a HIPAA Account.  Please note that if you run this notebook within Azure Databricks, your contract with Microsoft applies.
