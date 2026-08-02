data <- read.csv("~/Desktop/CarPred/Data/CSV/final.csv")
price <- data$price
price1 <- price/1000000 # برای راحتی کار که داده ها مقدارشان خیلی بزرگ نباشد تمامی قیمت ها را بر یک میلیون تقسیم میکنیم 
plot (price1 , ylab="* 1000000 kon")
qqnorm(price1)
shapiro.test(price1) # پر واضح است که داده های مربوط به قیمت ماشین از توزیع نرمال پیروی نمیکنند
boxplot(price1) #برای چولگی داده های قیمت
mileage <- data$mileage
mileage1<- mileage / 1000 #تمام داده های مربوط به کارکرد خود هارا برای راحتی تقسیم بر هزار میکنیم
plot(mileage1)
plot (price1 , mileage1 , xlab="* 1000000 kon", ylab="* 1000 kon")
plot(price,mileage,main="Asli va Bedoone taaqir") # هیچگونه رابطه خطی بین کارکرد ماشین و قیمت ماشین دیده نمیشود !!
qqnorm(mileage1)
qqline(mileage1)
shapiro.test(mileage1)# داده های مربوط به کارکرد هم از توزیع نرمال پیروی نمیکنند
boxplot(mileage1) # بررسی جولگی داده های کارکرد
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

# محاسبه ماتریس همبستگی برای متغیر های قیمت، کارکرد و سال تولید 

lst <- list(price=price1,mileage=mileage1,date=date)
dframe<- as.data.frame(lst)
cor(dframe)

#محاسبه ماتریس همبستگی متغیر های قیمت، کارکرد و سال تولید وقتی با لگ متغیر های قیمت و کارکرد رفتیم جلو ، که به نسبت همبستگی از حالت قبل کمتر شد!

lst <- list(price=price2,mileage=mileage2,date=date)
dframe<- as.data.frame(lst)
cor(dframe)