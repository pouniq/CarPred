data <- read.csv("~/Desktop/CarPred/Data/CSV/final.csv")
price <- data$price
price1 <- price/1000000 # برای راحتی کار که داده ها مقدارشان خیلی بزرگ نباشد تمامی قیمت ها را بر یک میلیون تقسیم میکنیم 
plot (price1 , ylab="* 1000000 kon")
qqnorm(price1)
shapiro.test(price1) # پر واضح است که داده های مربوط به قیمت ماشین از توزیع نرمال پیروی نمیکنند
mileage <- data$mileage
mileage1<- mileage / 1000 #تمام داده های مربوط به کارکرد خود هارا برای راحتی تقسیم بر هزار میکنیم
plot(mileage1)
plot (price1 , mileage1 , xlab="* 1000000 kon", ylab="* 1000 kon")
plot(price,mileage,main="Asli va Bedoone taaqir") # هیچگونه رابطه خطی بین کارکرد ماشین و قیمت ماشین دیده نمیشود !!
qqnorm(mileage1)
shapiro.test(mileage1)# داده های مربوط به کارکرد هم از توزیع نرمال پیروی نمیکنند
date <- data$date
date1<- as.character(date)
table(date1)
lst <- list(price=price1,mileage=mileage1,date=date)
dframe<- as.data.frame(lst)
plot(dframe)
price2 <- log(price1)
lst <- list(price=price2,mileage=mileage1,date=date)
dframe<- as.data.frame(lst)
plot(dframe)
#رابطه بین متغیر قیمت و سال تولید خودرو خطی شد ! با بالا بودن سال تولید خودرو قیمت خودرو نیز افزایش می یابد ولی متغیر کارکرد ماشین هنوز درست نشده
mileage2<- log(mileage1)
lst <- list(price=price2,mileage=mileage2,date=date)
dframe<- as.data.frame(lst)
plot(dframe)
mileage3 <- (mileage1)^2
lst <- list(price=price2,mileage=mileage3,date=date)
dframe<- as.data.frame(lst)
plot(dframe)
#این جا ما هم توان دوم و هم لگ متغیر کارکرد رو رسم کردیم تا ببینیم کدوم میتونه بهتر باشه ؟!

reg<- lm(price ~ . ,data=dframe)
summary(reg)
# اماره F میگه حداقل یکی از ضرایب معنی دار است و وقتی سراغ ازمون t میریم میبنیم متغیر date با مقدار p-value خیلی کم معنی دار شده است اما متغیر mileage لزومی نداره در مدل باشه !!

lst <- list(price=price2,mileage=mileage3,date=date)
dframe<- as.data.frame(lst)
reg1 <- lm(price~ . , data=dframe)
summary(reg1)
anova(reg1)
# کمی بدتر شد پس نتیجه میگیریم که توان دوم mileage بدتر از لگ mileage است ، پس با همون لگ کار میکنیم
