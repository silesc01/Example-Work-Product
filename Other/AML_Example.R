pacman::p_load(dplyr, plyr, tidyr, stringr, splitstackshape, gsheet, purrr,lubridate, readxl, forecast, tibble, sqldf, ggplot2, caret, mlbench)
wd <- c("C:/Users/siles/C:/Users/siles/Desktop/DSKTOP/JOB/TekPartners")
AML_Example <- read.csv("C:/Users/siles/Desktop/DSKTOP/JOB/TekPartners/AML_Example.csv", header=T, sep=",", stringsAsFactors = FALSE)

#######-Is having an invalid email address a good predictor of a fraudulent payment?-######
View(AML_Example)
names(AML_Example)
str(AML_Example)
summary(AML_Example$Valid_Email)
summary(AML_Example$Valid_PMT)

tab_AML <- table(AML_Example$Valid_Email, AML_Example$Valid_PMT)
print(tab_AML)

prop.table(tab_AML)
prop.table(tab_AML, 1)

plot(tab_AML, xlab = "Valid_Email", ylab = "Valid_PMT", col = "red")

#Candidate Model 1 - Linear Regression
model <- lm(formula = Valid_PMT ~ Valid_Email, data = AML_Example)
summary(model)
plot(model)

#Candidate Model 2 - Logistic Regression
gmodel <- glm(formula = Valid_PMT ~ Valid_Email, data = AML_Example, family = binomial)
summary(gmodel)
plot(gmodel)

ggplot(data = AML_Example, aes(x = Valid_PMT, y = Valid_Email)) + 
    geom_jitter(width = 0, height = 0.025, alpha = 0.5) +
    geom_smooth(method = 'glm', se = TRUE)

#Candidate Model KNN - K Nearest Neighbors
library(class)

######Candidate Model KNN 1 
train_labels1 <- train1$Valid_Email == 'Invalid'
train_labels2 <- train2$Valid_Email == 'Invalid'
train_labels3 <- train3$Valid_Email == 'Invalid'

train1 <- AML_Example[1:186, ] 
test1 <- AML_Example[187:746, ]
pred1 <- knn(train = train1[,c(5,6)], test = test1[,c(5,6)], cl = train_labels1, k = 1)
table(pred1, test1$Valid_PMT)

######Candidate Model KNN 2
train2 <- AML_Example[1:372, ]   
test2 <- AML_Example[373:746, ]
pred2 <- knn(train = train2[,c(5,6)], test = test2[,c(5,6)], cl = train_labels2, k = 1)
table(pred2, test2$Valid_PMT)

######Candidate Model KNN 3
train3 <- AML_Example[1:466, ]   
test3 <- AML_Example[467:746, ]
pred3 <- knn(train = train3[,c(5,6)], test = test3[,c(5,6)], cl = train_labels3, k = 1)
table(pred3, test3$Valid_PMT)

#####Calculate Peformance of each Candidate model 
accuracy <- function(x){sum(diag(x)/(sum(rowSums(x)))) * 100}
accuracy(table(pred1,test1$Valid_PMT))
accuracy(table(pred2,test2$Valid_PMT))
accuracy(table(pred3,test3$Valid_PMT))

#####As pred3 is the Champion, validate on holdout sample to determine if it should be put into production
validate = AML_Example[747:932,]
PredModel <- knn(train = train3[,c(5,6)], test = validate[,c(5,6)], cl = train_labels3, k = 1)
accuracy(table(PredModel,validate$Valid_PMT))
