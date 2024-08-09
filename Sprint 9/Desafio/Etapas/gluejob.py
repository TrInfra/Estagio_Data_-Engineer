import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col, explode, concat_ws, split, lit, udf, monotonically_increasing_id, array_contains
from pyspark.sql.types import ArrayType, IntegerType
from pyspark.sql import functions as F
from pyspark.sql.window import Window

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# paths
tmdb_path = "s3://data-lake-do-nycolas/Trusted/TMDB/dt=2024/08/05/"
imdb_path = "s3://data-lake-do-nycolas/Trusted/Local/"

# Reading TMDB
print("log: Reading data from TMDB")
tmdb_data = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [tmdb_path]},
    format="parquet"
).toDF()
print("log: TMDB data read successfully")

# Reading IMDB
print("log: reading IMDB data")
imdb_data = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [imdb_path]},
    format="parquet"
).toDF()
print("log: IMDB data read successfully")

# remove duplicates IMDB
print("log: removing duplicates from IMDB")
imdb_data = imdb_data.dropDuplicates(["id", "tituloPrincipal", "tituloOriginal", "anoLancamento", "genero", "notaMedia", "numeroVotos"])
print("log: duplicates removed from IMDB")

# Renaming and filtering IMDB columns
print("log: renaming IMDB columns")
imdb_data = imdb_data.withColumnRenamed("id", "imdb_id") \
                     .withColumnRenamed("tituloPrincipal", "title") \
                     .withColumnRenamed("tituloOriginal", "original_title") \
                     .withColumnRenamed("anoLancamento", "release_year") \
                     .withColumnRenamed("genero", "genres") \
                     .withColumnRenamed("notaMedia", "vote_average") \
                     .withColumnRenamed("numeroVotos", "vote_count")
print("log: successfully renamed columns.")

# Transforming and filtering IMDB genres
print("log: transforming IMDB genres")
imdb_data = imdb_data.withColumn("genres", split(col("genres"), ",")) \
                     .withColumn("popularity", lit(0).cast("double"))
print("log: IMDB genres transformed")

print("log: filtering IMDB data for Action and Adventure genres")
imdb_data = imdb_data.filter(
    (array_contains(col("genres"), "Action")) | (array_contains(col("genres"), "Adventure"))
)
print("log: filtered IMDB data successfully")

# Creating a dictionary to map TMDB genres
genres_tmdb = [
    {"id": 28, "name": "Action"},
    {"id": 12, "name": "Adventure"},
    {"id": 16, "name": "Animation"},
    {"id": 35, "name": "Comedy"},
    {"id": 80, "name": "Crime"},
    {"id": 99, "name": "Documentary"},
    {"id": 18, "name": "Drama"},
    {"id": 10751, "name": "Family"},
    {"id": 14, "name": "Fantasy"},
    {"id": 36, "name": "History"},
    {"id": 27, "name": "Horror"},
    {"id": 10402, "name": "Music"},
    {"id": 9648, "name": "Mystery"},
    {"id": 10749, "name": "Romance"},
    {"id": 878, "name": "Science Fiction"},
    {"id": 10770, "name": "TV Movie"},
    {"id": 53, "name": "Thriller"},
    {"id": 10752, "name": "War"},
    {"id": 37, "name": "Western"}
]
print("log: creating DataFrame for TMDB genres")
genre_df_tmdb = spark.createDataFrame(genres_tmdb)
print("log: TMDB Genres DataFrame created")

# mapping names to IDs
genre_mapping = {row['name']: row['id'] for row in genres_tmdb}

# map the genres
def map_genres(genres):
    return [genre_mapping[genre] for genre in genres if genre in genre_mapping]

# Registering the function as UDF
map_genres_udf = udf(map_genres, ArrayType(IntegerType()))

print("log: applying UDF to map IMDB genres")
imdb_data = imdb_data.withColumn("genre_ids", map_genres_udf(col("genres")))
print("log: IMDB genres successfully mapped")

print("log: extracting information from the TMDB release_date column")
tmdb_data = tmdb_data.withColumn("year", col("release_date").substr(1, 4).cast("int")) \
                     .withColumn("decade", (col("year") / 10).cast("int") * 10) \
                     .withColumn("id_time", col("year"))
print("log: information extracted successfully")

print("log: creating the dimension of time")
dimensao_tempo_tmdb = tmdb_data.select("year", "decade").distinct()
imdb_tempo = imdb_data.select("release_year") \
                      .withColumnRenamed("release_year", "year") \
                      .withColumn("decade", (col("year") / 10).cast("int") * 10)
print("log: uniting dimensions of time")
dimensao_tempo = dimensao_tempo_tmdb.union(imdb_tempo).distinct()
dimensao_tempo = dimensao_tempo.withColumn("id_time", col("year"))
dimensao_tempo_df = DynamicFrame.fromDF(dimensao_tempo, glueContext, "dim_time_df")

print("log: saving the time dimension to S3")
glueContext.write_dynamic_frame.from_options(
    frame=dimensao_tempo_df,
    connection_type="s3",
    connection_options={"path": "s3://data-lake-do-nycolas/Refined/db_refined/dim_time/"},
    format="parquet"
)
print("log: time dimension saved successfully")

print("log: expanding TMDB genre_ids")
tmdb_data = tmdb_data.withColumn("genre_id", explode(col("genre_ids")))

print("log: creating the fact table")
fato_mov = tmdb_data.select("imdb_id", "popularity", "vote_average", "vote_count", "id_time", "genre_id") \
                    .dropDuplicates(["imdb_id", "genre_id"]) \
                    .withColumn("id", monotonically_increasing_id().cast("int"))  

fato_mov_df = DynamicFrame.fromDF(fato_mov, glueContext, "fato_movie_df")

print("log: saving the fact table to S3")
glueContext.write_dynamic_frame.from_options(
    frame=fato_mov_df,
    connection_type="s3",
    connection_options={"path": "s3://data-lake-do-nycolas/Refined/db_refined/fato_movie/"},
    format="parquet"
)
print("log: fact table saved successfully")

print("log: creating the gender dimension")
# For TMDB, adding the genus name
genre_data_tmdb = tmdb_data.select(explode(col("genre_ids")).alias("genre_id")).distinct()
genre_data_tmdb = genre_data_tmdb.join(genre_df_tmdb, genre_data_tmdb["genre_id"] == genre_df_tmdb["id"], "inner") \
                                 .select(genre_data_tmdb["genre_id"], genre_df_tmdb["name"])
# For IMDB, adding the genre name
genre_data_imdb = imdb_data.select(explode(col("genre_ids")).alias("genre_id")).distinct()
genre_data_imdb = genre_data_imdb.join(genre_df_tmdb, genre_data_imdb["genre_id"] == genre_df_tmdb["id"], "inner") \
                                 .select(genre_data_imdb["genre_id"], genre_df_tmdb["name"])

# Uniting gender dimensions
dimensao_genero = genre_data_tmdb.union(genre_data_imdb).distinct()
dimensao_genero_df = DynamicFrame.fromDF(dimensao_genero, glueContext, "dim_genre_df")

print("log: saving the gender dimension in S3")
glueContext.write_dynamic_frame.from_options(
    frame=dimensao_genero_df,
    connection_type="s3",
    connection_options={"path": "s3://data-lake-do-nycolas/Refined/db_refined/dim_genre/"},
    format="parquet"
)
print("log: gender dimension saved successfully")

print("log: creating the movie dimension")
windowSpec = Window.orderBy("imdb_id")

dimensao_filme = imdb_data.select("imdb_id", "original_title", "title").distinct() \
                          .withColumn("id_movie", F.row_number().over(windowSpec) - 1)

dimensao_filme_df = DynamicFrame.fromDF(dimensao_filme, glueContext, "dim_movie_df")

print("Log: saving the movie dimension in S3")
glueContext.write_dynamic_frame.from_options(
    frame=dimensao_filme_df,
    connection_type="s3",
    connection_options={"path": "s3://data-lake-do-nycolas/Refined/db_refined/dim_movie/"},
    format="parquet"
)
print("Log: movie Dim saves successfully")

job.commit()