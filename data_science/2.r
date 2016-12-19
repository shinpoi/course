# encode = UTF8

##############################
#  linear regression

print("linear regression:")

x <- 0:50
y <- 7*x+13

f <- lsfit(x,y)
plot(x, y, main='Linear Regression')
abline(f)

print("Press Enter to non-linear regression")
scan("")

##############################
#  non-linear regression

x <- 0:50
y <- 3*x + 2*x^2 + x^3

plot(x, y, main='Nonlinear Regression')

f1 <- lm(y~x)
lines(x, predict(f1))

f2 <- lm(y~x+I(x^2))
lines(x, predict(f2), col='red')

f3 <- lm(y~x+I(x^2)+I(x^3))
lines(x, predict(f3), col='blue')
