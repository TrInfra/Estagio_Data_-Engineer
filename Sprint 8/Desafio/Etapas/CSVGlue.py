import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

csv_path = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

df_movies = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": [csv_path],
        "recurse": True,
    },
    format="csv",
    format_options={
        "withHeader": True,
        "separator": ","
    }
).toDF()

dynamic_df_movies = DynamicFrame.fromDF(df_movies, glueContext, "dynamic_df_movies")

glueContext.write_dynamic_frame.from_options(
    frame=dynamic_df_movies,
    connection_type="s3",
    connection_options={
        "path": target_path,
    },
    format="parquet",
    format_options={"compression": "SNAPPY"},
    transformation_ctx="write_movies_data"
)

job.commit()