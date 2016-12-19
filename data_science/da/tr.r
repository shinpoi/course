# install.packages("kernlab")
# library(kernlab)

detail = FALSE

# train with 1100 samples
train <- read.table("train_data_1100.txt", header = T)
test <- read.table("test_data.txt", header = T)

linsvm <- ksvm(x = class ~., data=train, type="C-svc", kernel = "vanilladot")
kersvm <- ksvm(x = class ~., data=train, type="C-svc", kernel = "rbfdot")

lin_predict <- predict(linsvm, test)
ker_predict <- predict(kersvm, test)

result_lin_1100 <- table(lin_predict, test$class)
result_ker_1100 <- table(ker_predict, test$class)

# train with 5500 samples
train <- read.table("train_data_5500.txt", header = T)

linsvm <- ksvm(x = class ~., data=train, type="C-svc", kernel = "vanilladot")
kersvm <- ksvm(x = class ~., data=train, type="C-svc", kernel = "rbfdot")

lin_predict <- predict(linsvm, test)
ker_predict <- predict(kersvm, test)

result_lin_5500 <- table(lin_predict, test$class)
result_ker_5500 <- table(ker_predict, test$class)

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
cat("\n ######## Result of 1100 Samples ########## \n")
evaluate(result_lin_1100, "LinearSvm", detail)
evaluate(result_ker_1100, "KernelSvm", detail)

cat("\n ######## Result of 5500 Samples ########## \n")
evaluate(result_lin_5500, "LinearSvm", detail)
evaluate(result_ker_5500, "KernelSvm", detail)

