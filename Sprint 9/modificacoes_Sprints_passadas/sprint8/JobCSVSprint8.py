import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# path s3 Raw
raw_s3_path = "s3://data-lake-do-nycolas/Raw/Local/CSV/Movies/2024/06/29/"

# Especificando o esquema
schema = StructType([
    StructField("id", StringType(), True),
    StructField("tituloPrincipal", StringType(), True), 
    StructField("tituloOriginal", StringType(), True),
    StructField("anoLancamento", IntegerType(), True),
    StructField("tempoMinutos", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notaMedia", StringType(), True),
    StructField("numeroVotos", IntegerType(), True),
    StructField("generoArtista", StringType(), True),
    StructField("personagem", StringType(), True),
    StructField("nomeArtista", StringType(), True),
    StructField("anoNascimento", IntegerType(), True),
    StructField("anoFalecimento", IntegerType(), True),
    StructField("profissao", StringType(), True),
    StructField("titulosMaisConhecidos", StringType(), True)
])

df = spark.read.option("header", "false") \
               .option("delimiter", "|") \
               .schema(schema) \
               .csv(raw_s3_path)

df = df.rdd.zipWithIndex().filter(lambda x: x[1] > 0).map(lambda x: x[0]).toDF(schema=schema)

dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

# path s3 trusted
refined_s3_path = "s3://data-lake-do-nycolas/Trusted/Local/"

# Salvando o DynamicFrame
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={"path": refined_s3_path},
    format="parquet"
)

job.commit()
