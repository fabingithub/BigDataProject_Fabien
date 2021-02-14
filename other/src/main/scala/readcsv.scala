import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession

object readcsv extends App {


  val spark = org.apache.spark.sql.SparkSession.builder
    .master("local")
    .appName("Spark CSV Reader")
    .getOrCreate;

  val df = spark.read
    .option("header", "true") //first line in file has headers
    .option("delimiter",";")
    .csv("file:///H:/Documents/cours/S4 Big Data Management/assignements/projet 2 data cleaning/csv/blak-einstaklingar.csv")
    .persist()
  ;
  df.show(df.count.toInt,false);

}