setwd(normalizePath(dirname(R.utils::commandArgs(asValues=TRUE)$"f")))
source('../findNSourceUtils.R')

test.glm2binregression.golden <- function(H2Oserver) {
	
#Import data: 
Log.info("Importing CUSE data...") 
cuseH2O<- h2o.uploadFile.FV(H2Oserver, locate("../../smalldata/cuseexpanded.csv"), key="cuseH2O")
cuseR<- read.csv(locate("smalldata/cuseexpanded.csv"), header=T)

Log.info("Test H2O treatment of FACTORS AS PREDICTORS")
Log.info("Run matching models in R and H2O")
fitH2O<- h2o.glm.FV(y="UsingBinom", x=c("Age", "Ed", "Wantsmore"), data=cuseH2O, family="binomial", lambda=0, alpha=0, nfolds=0)
fitR<- glm(UsingBinom ~ AgeA + AgeC + AgeD + LowEd + MoreYes, family=binomial, data=cuseR)


Log.info("Print model statistics for R and H2O... \n")
Log.info(paste("H2O Deviance  : ", fitH2O@model$deviance,      "\t\t", "R Deviance   : ", fitR$deviance))
Log.info(paste("H2O Null Dev  : ", fitH2O@model$null.deviance, "\t\t", "R Null Dev   : ", fitR$null.deviance))
Log.info(paste("H2O residul df: ", fitH2O@model$df.residual,    "\t\t\t\t", "R residual df: ", fitR$df.residual))
Log.info(paste("H2O null df   : ", fitH2O@model$df.null,       "\t\t\t\t", "R null df    : ", fitR$df.null))
Log.info(paste("H2O aic       : ", fitH2O@model$aic,           "\t\t", "R aic        : ", fitR$aic))

Log.info("Compare model statistics in R to model statistics in H2O")
expect_equal(fitH2O@model$null.deviance, fitR$null.deviance, tolerance = 0.01)
expect_equal(fitH2O@model$deviance, fitR$deviance, tolerance = 0.01)
expect_equal(fitH2O@model$df.residual, fitR$df.residual, tolerance = 0.01)
expect_equal(fitH2O@model$df.null, fitR$df.null, tolerance = 0.01)
expect_equal(fitH2O@model$aic, fitR$aic, tolerance = 0.01)

testEnd()
}

doTest("GLM Test: Golden GLM2 - Factors as predictors", test.glm2binregression.golden)

