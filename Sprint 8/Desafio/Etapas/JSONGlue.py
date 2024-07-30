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

# paths dos diretorios do meu bucket(Job parameters)
base_path =args['S3_INPUT_PATH'] 
target_path=args['S3_TARGET_PATH']

df_tmdb = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": [base_path + "Acao/", base_path + "Aventura/"],
        "recurse": True,
    },
    format="json"
).toDF()

# Remove duplicatas com base no ID
df_tmdb = df_tmdb.dropDuplicates(["id"])

# Buscando apenas as colunas que vou precisar para o desafio final
df_tmdb = df_tmdb.select(
    col("id"),
    col("genre_ids"),
    col("original_title"),
    col("popularity"),
    col("release_date"),
    col("title"),
    col("vote_average"),
    col("vote_count")
)

dynamic_df_tmdb = DynamicFrame.fromDF(df_tmdb, glueContext, "dynamic_df_tmdb")

glueContext.write_dynamic_frame.from_options(
    frame=dynamic_df_tmdb,
    connection_type="s3",
    connection_options={
        "path": target_path,
    },
    format="parquet",
    format_options={"compression": "SNAPPY"},
    transformation_ctx="write_data"
)

job.commit()
