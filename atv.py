import sys, getopt
from pyspark.sql import SparkSession

if __name__ == "__main__":
	spark = SparkSession.builder.appName("Tabelas").getOrCreate()
	opts, args = getopt.getopt(sys.argv[1:], "a:t:")
	arquivo, tabela = "",""
	for opt, arg in opts:
		if opt == "-a":
			arquivo = arg
		elif opt == "-t":
			tabela == arg
	df = spark.read.load(arquivo)
	df.write.format("jdbc").option("url","jdbc:postgresql://localhost:5432/tabela").option("dbtable",tabela).option("user","postgres").option("password","123456").option("driver","org.postgresql.Driver").save()
	spark.stop()
	
	
