# Analia Cabello Cano

# Linear regression analysis

# Year vs temp during growing season

grow_ssn_data <- read.csv("my_data_frames/growing_season_data.csv")
grow_ssn_data <- data.frame(grow_ssn_data)
#grow_ssn_data$Year <- as.factor(grow_ssn_data$Year)

model <- lm(temp ~ Year, data=grow_ssn_data)
summary(model)

par(mfrow = c(2, 2))
plot(model)


par(mfrow = c(1, 1))
plot(grow_ssn_data$Year, grow_ssn_data$temp, xlab="Year",ylab="Temperature in growing season /ºC", main = "Year vs temperature in growing season")
abline(model, col = "red")



grow_ssn_data$Year <- as.factor(grow_ssn_data$Year)

model2 <- lm(temp ~ Year, data=grow_ssn_data)
anova(model2)

par(mfrow = c(1, 1))
plot(grow_ssn_data$Year, grow_ssn_data$temp, xlab="Year",ylab="Temperature in growing season /ºC", main = "Year vs temperature in growing season")