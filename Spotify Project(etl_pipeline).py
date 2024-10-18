import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node album
album_node1728974500347 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://project-spotify-data-set/staging/albums.csv"], "recurse": True}, transformation_ctx="album_node1728974500347")

# Script generated for node artist
artist_node1728974499299 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://project-spotify-data-set/staging/artists.csv"], "recurse": True}, transformation_ctx="artist_node1728974499299")

# Script generated for node track
track_node1728974501397 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://project-spotify-data-set/staging/track.csv"], "recurse": True}, transformation_ctx="track_node1728974501397")

# Script generated for node Join(albums&artists)
Joinalbumsartists_node1728974508263 = Join.apply(frame1=album_node1728974500347, frame2=artist_node1728974499299, keys1=["artist_id"], keys2=["id"], transformation_ctx="Joinalbumsartists_node1728974508263")

# Script generated for node Join(join1&track)
Joinjoin1track_node1728974509412 = Join.apply(frame1=Joinalbumsartists_node1728974508263, frame2=track_node1728974501397, keys1=["track_id"], keys2=["track_id"], transformation_ctx="Joinjoin1track_node1728974509412")

# Script generated for node Drop Fields
DropFields_node1728974516272 = DropFields.apply(frame=Joinjoin1track_node1728974509412, paths=["id", "`.track_id`"], transformation_ctx="DropFields_node1728974516272")

# Script generated for node Destination
Destination_node1728974523290 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1728974516272, connection_type="s3", format="glueparquet", connection_options={"path": "s3://project-spotify-data-set/datawarehouse/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="Destination_node1728974523290")

job.commit()