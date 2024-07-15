import sys
import pyspark.sql.functions as f
from pyspark.sql import SparkSession
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, max as spark_max, sum as spark_sum

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

try:
    df = glueContext.create_dynamic_frame.from_options(
        connection_type="s3",
        connection_options={"paths": [source_file]},
        format="csv",
        format_options={"withHeader": True}
    )
    
    df.printSchema()
    
    df_spark = df.toDF()
    
    df_upper = df_spark.select(f.upper(f.col('nome')).alias('nome'), 'ano', 'sexo', 'total')
    
    print("Total de linhas:", df_spark.count())
    
    df_grouped = df_spark.groupBy("ano", "sexo").count().orderBy("ano", ascending=False)
    df_grouped.show()
    
    df_female = df_spark.filter(col("sexo") == 'F')
    df_female_max = df_female.groupBy("ano").agg(spark_max("total").alias("max_total")).orderBy("max_total", ascending=False).first()
    print("Nome feminino com mais registros:", df_female_max)
    
    df_male = df_spark.filter(col("sexo") == 'M')
    df_male_max = df_male.groupBy("ano").agg(spark_max("total").alias("max_total")).orderBy("max_total", ascending=False).first()
    print("Nome masculino com mais registros:", df_male_max)
    
    df_yearly = df_spark.groupBy("ano").agg(spark_sum("total").alias("sum_total")).orderBy("ano").limit(10)
    df_yearly.show()
    
    df_upper.write.partitionBy("sexo", "ano").json(target_path)
    
    print("sucesso!")
except Exception as e:
    print("Ocorreu um erro:", e)
    
job.commit()
