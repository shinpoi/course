# install.packages("e1071")

library(e1071)

detail = FALSE

# train with 1100 samples
test <- read.table("test_data_1000.txt", header = T)

train <- read.table("train_data_550.txt", header = T)
t_550 <- naiveBayes(train[,-197], train[,197])

train <- read.table("train_data_1100.txt", header = T)
t_1100 <- naiveBayes(train[,-197], train[,197])

train <- read.table("train_data_5500.txt", header = T)
t_5500 <- naiveBayes(train[,-197], train[,197])

re_550 <- table(predict(t_550,test), test[,197])
re_1100 <- table(predict(t_1100,test), test[,197])
re_5500 <- table(predict(t_5500,test), test[,197])

# Evaluate function
evaluate <- function(result, name, detail=FALSE){
	cat("\n\n", "### result of", name, " ###\n\n")
	if (detail){
	print(result)
	}

	# Accuracy:
	n <- 0
	for(i in 1:10){
		n <- n+result[i,][i]
	}

	accuracy <- n/sum(result)
	cat("\n", "accuracy=", accuracy, "\n\n")
	 
	# Precision:
	# Pr.init
	precision <- c(1:10)
	for(i in 1:10)(precision[i] <- 0)
	
	# Pr.calculate
	for(i in 1:10){
		row <- result[i,]
		num <- sum(row)
		right <- row[i]
		precision[i] <- right/num
	}
	
	# Pr.show
	for(i in 1:10){
	    if (detail){
	    cat("precision[", i-1, "]=", precision[i], "\n")
	    }
	}

	cat("\n")
	# Recall:
	# Re.init
	recall <- c(1:10)
	for(i in 1:10)(recall[i] <- 0)
	
	# Re.calculate
	for(i in 1:10){
		col <- result[,i]
		num <- sum(col)
		right <- col[i]
		recall[i] <- right/num
	}

	# Re.show
	for(i in 1:10){
	    if (detail){
	    cat("recall[", i-1, "]=", recall[i], "\n")
	    }
	}

	# F­-Measure:
	cat("\n")
	fmeasure <- c(1:10)
	for(i in 1:10){
		fmeasure[i] <- (2*precision[i]*recall[i])/(precision[i]+recall[i])
		if (detail){
		cat("F­-Measure[", i-1, "]=", fmeasure[i], "\n")
		}
	}
	cat("\n Average of F­-Measure:", sum(fmeasure)/10)
	cat("\n\n————————————————————————————————————\n\n")
}

# Show Result
evaluate(re_550, "550 Samples", detail)
evaluate(re_1100, "1100 Samples", detail)
evaluate(re_5500, "5500 Samples", detail)

