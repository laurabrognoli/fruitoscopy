cat("\014")
# load the required libraries
library(pls)
#putsd in the right directory
setwd("~/Desktop/Grapes/")
#read teh csv file with grapes data
grapestmp <- read.csv("~/Desktop/Grapes/grapes_data/grapes.csv", header=FALSE)
#read the white reference ____ divide all te spectra by the white reference
ref <- read.csv("~/Desktop/Grapes/grapes_data/white_ref_corr.dat", header=FALSE)
#normalize
grapes <- grapestmp/ref[,1]
#transpose the matrix
grapes <- t(grapes)
#separate data and read the labels
labelsspectra <- read.delim("~/Desktop/Grapes/grapes_data/labelsspectra.txt",stringsAsFactors = FALSE)
#unites the colums
grapes <- cbind(grapes,labelsspectra)
#just create a subset of the original database
averaged <- grapes[1:18,]

for(j in 1:18){
  averaged[j,1:3280] <- 1/3*(grapes[(j-1)*3+1,1:3280]+grapes[(j-1)*3+2,1:3280]+grapes[(j-1)*3+2,1:3280])
  averaged[j,3281:3283] <- grapes[(j-1)*3+1,3281:3283]
  averaged[j,3284] <- "average"
}

#BLACK A
#read file chemo use 2 grape
chemo <- read.delim("~/Desktop/Grapes/grapes_data/chemo.csv",stringsAsFactors = FALSE)
#skip grape b(quite random-change later)
skipped <- "a"
#select only the averag data except for the one excludede before and add grape label
mydata <- averaged[averaged$grape!=skipped,c(1:3280,"color","group","grape")]
chemo$grape <- mydata$grape
#conbine the data(chemo of the average data)
combined <- merge(mydata,chemo,sort=FALSE)
#extract the numerical column of the average
spectracols <- 1:3280+3


#choose justtthe black
mycolor <- "black"
#look which are the most correlated columns with the brix
selected_cols <- c()
k <- 0
for(j in spectracols){
  z <- abs(cor(combined[combined$color==mycolor,j],combined[combined$color==mycolor,"brix"]))
  if(z>0.90){
    k <- k+1
    selected_cols[k] <- j
    #print(c(j,z))
  } 
}
#transform the pixel in wavelenghts


print("###################################################################")
wavelengths <- 234.14+0.27*selected_cols
print(wavelengths)
print("specific black a")
aaa <- as.matrix(combined[combined$color==mycolor,selected_cols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds

print("black a general")
aaa <- as.matrix(combined[combined$color==mycolor,spectracols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds



print("both color general a")
aaa <- as.matrix(combined[,spectracols])
zzz <- data.frame(I(aaa),var=combined[,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
a <- result$fitted.values[,1,2]
#R-squared
R2(result)
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds




#BLACK B
#read file chemo use 2 grape
chemo <- read.delim("~/Desktop/Grapes/grapes_data/chemo.csv",stringsAsFactors = FALSE)
#skip grape b(quite random-change later)
skipped <- "b"
#select only the averag data except for the one excludede before and add grape label
mydata <- averaged[averaged$grape!=skipped,c(1:3280,"color","group","grape")]
chemo$grape <- mydata$grape
#conbine the data(chemo of the average data)
combined <- merge(mydata,chemo,sort=FALSE)
#extract the numerical column of the average
spectracols <- 1:3280+3


#choose justtthe black
mycolor <- "black"
#look which are the most correlated columns with the brix
selected_cols <- c()
k <- 0
for(j in spectracols){
  z <- abs(cor(combined[combined$color==mycolor,j],combined[combined$color==mycolor,"brix"]))
  if(z>0.90){
    k <- k+1
    selected_cols[k] <- j
    #print(c(j,z))
  } 
}
#transform the pixel in wavelenghts
print("###################################################################")
wavelengths <- 234.14+0.27*selected_cols
print(wavelengths)
print("specific black b")
aaa <- as.matrix(combined[combined$color==mycolor,selected_cols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds

print("black b general")
aaa <- as.matrix(combined[combined$color==mycolor,spectracols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds



print("both color general b")
aaa <- as.matrix(combined[,spectracols])
zzz <- data.frame(I(aaa),var=combined[,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
a <- result$fitted.values[,1,2]
#R-squared
R2(result)
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds


#BLACK C
#read file chemo use 2 grape
chemo <- read.delim("~/Desktop/Grapes/grapes_data/chemo.csv",stringsAsFactors = FALSE)
#skip grape b(quite random-change later)
skipped <- "c"
#select only the averag data except for the one excludede before and add grape label
mydata <- averaged[averaged$grape!=skipped,c(1:3280,"color","group","grape")]
chemo$grape <- mydata$grape
#conbine the data(chemo of the average data)
combined <- merge(mydata,chemo,sort=FALSE)
#extract the numerical column of the average
spectracols <- 1:3280+3


#choose justtthe black
mycolor <- "black"
#look which are the most correlated columns with the brix
selected_cols <- c()
k <- 0
for(j in spectracols){
  z <- abs(cor(combined[combined$color==mycolor,j],combined[combined$color==mycolor,"brix"]))
  if(z>0.90){
    k <- k+1
    selected_cols[k] <- j
    #print(c(j,z))
  } 
}
#transform the pixel in wavelenghts
print("###################################################################")
wavelengths <- 234.14+0.27*selected_cols
print(wavelengths)
print("specific black c")
aaa <- as.matrix(combined[combined$color==mycolor,selected_cols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds

print("black c general")
aaa <- as.matrix(combined[combined$color==mycolor,spectracols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds



print("both color general c")
aaa <- as.matrix(combined[,spectracols])
zzz <- data.frame(I(aaa),var=combined[,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
a <- result$fitted.values[,1,2]
#R-squared
R2(result)
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds



#WHITE A
#read file chemo use 2 grape
chemo <- read.delim("~/Desktop/Grapes/grapes_data/chemo.csv",stringsAsFactors = FALSE)
#skip grape b(quite random-change later)
skipped <- "a"
#select only the averag data except for the one excludede before and add grape label
mydata <- averaged[averaged$grape!=skipped,c(1:3280,"color","group","grape")]
chemo$grape <- mydata$grape
#conbine the data(chemo of the average data)
combined <- merge(mydata,chemo,sort=FALSE)
#extract the numerical column of the average
spectracols <- 1:3280+3


#choose justtthe black
mycolor <- "white"
#look which are the most correlated columns with the brix
selected_cols <- c()
k <- 0
for(j in spectracols){
  z <- abs(cor(combined[combined$color==mycolor,j],combined[combined$color==mycolor,"brix"]))
  if(z>0.90){
    k <- k+1
    selected_cols[k] <- j
    #print(c(j,z))
  } 
}
#transform the pixel in wavelenghts
print("###################################################################")
wavelengths <- 234.14+0.27*selected_cols
print(wavelengths)
print("specific white a")
aaa <- as.matrix(combined[combined$color==mycolor,selected_cols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds

print("white a general")
aaa <- as.matrix(combined[combined$color==mycolor,spectracols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds



print("both color general a")
aaa <- as.matrix(combined[,spectracols])
zzz <- data.frame(I(aaa),var=combined[,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
a <- result$fitted.values[,1,2]
#R-squared
R2(result)
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds






#WHITE B
#read file chemo use 2 grape
chemo <- read.delim("~/Desktop/Grapes/grapes_data/chemo.csv",stringsAsFactors = FALSE)
#skip grape b(quite random-change later)
skipped <- "b"
#select only the averag data except for the one excludede before and add grape label
mydata <- averaged[averaged$grape!=skipped,c(1:3280,"color","group","grape")]
chemo$grape <- mydata$grape
#conbine the data(chemo of the average data)
combined <- merge(mydata,chemo,sort=FALSE)
#extract the numerical column of the average
spectracols <- 1:3280+3


#choose justtthe black
mycolor <- "white"
#look which are the most correlated columns with the brix
selected_cols <- c()
k <- 0
for(j in spectracols){
  z <- abs(cor(combined[combined$color==mycolor,j],combined[combined$color==mycolor,"brix"]))
  if(z>0.90){
    k <- k+1
    selected_cols[k] <- j
    #print(c(j,z))
  } 
}
#transform the pixel in wavelenghts
print("###################################################################")
wavelengths <- 234.14+0.27*selected_cols
print(wavelengths)
print(wavelengths)
print("specific white b")
aaa <- as.matrix(combined[combined$color==mycolor,selected_cols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds

print("white b general")
aaa <- as.matrix(combined[combined$color==mycolor,spectracols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds



print("both color general b")
aaa <- as.matrix(combined[,spectracols])
zzz <- data.frame(I(aaa),var=combined[,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
a <- result$fitted.values[,1,2]
#R-squared
R2(result)
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds




#WHITE C
#read file chemo use 2 grape
chemo <- read.delim("~/Desktop/Grapes/grapes_data/chemo.csv",stringsAsFactors = FALSE)
#skip grape b(quite random-change later)
skipped <- "c"
#select only the averag data except for the one excludede before and add grape label
mydata <- averaged[averaged$grape!=skipped,c(1:3280,"color","group","grape")]
chemo$grape <- mydata$grape
#conbine the data(chemo of the average data)
combined <- merge(mydata,chemo,sort=FALSE)
#extract the numerical column of the average
spectracols <- 1:3280+3


#choose justtthe black
mycolor <- "white"
#look which are the most correlated columns with the brix
selected_cols <- c()
k <- 0
for(j in spectracols){
  z <- abs(cor(combined[combined$color==mycolor,j],combined[combined$color==mycolor,"brix"]))
  if(z>0.90){
    k <- k+1
    selected_cols[k] <- j
    #print(c(j,z))
  } 
}
#transform the pixel in wavelenghts
print("###################################################################")
wavelengths <- 234.14+0.27*selected_cols
print(wavelengths)
print("specific white c")
aaa <- as.matrix(combined[combined$color==mycolor,selected_cols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds

print("white c general")
aaa <- as.matrix(combined[combined$color==mycolor,spectracols])
zzz <- data.frame(I(aaa),var=combined[combined$color==mycolor,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
#R-squared
R2(result)
a <- result$fitted.values[,1,2]
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds



print("both color general c")
aaa <- as.matrix(combined[,spectracols])
zzz <- data.frame(I(aaa),var=combined[,"brix"])
result <- plsr(var~aaa,data=zzz,ncomp=2,validation="none")
a <- result$fitted.values[,1,2]
#R-squared
R2(result)
b <- zzz$var
preds <- cbind(pred=a,true=b)
preds

library(lattice)

all_wavelengths <- 234.14+0.27*spectracols

xyplot(c(0,1.6)~c(200,1200),
       main="",
       xlab=list(label="Wavelenght (nm)",cex=1.3),
       ylab=list(label="(Normalized) Intensity",cex=1.3),
       scales=list(
         x=list(at=seq(200,1200,200),cex=1.3),
         y=list(at=seq(0,1.5,0.25),cex=1.3)
         ),
       panel=function(...){
         llines(all_wavelengths,combined[1,spectracols],col="black",type="l",lwd=3)
         llines(all_wavelengths,ref[,1],col="blue",type="l",lwd=1)
         llines(all_wavelengths,grapes[1,1:3280],col="red",type="l",lwd=1,lty=2)
       }
       ) 

pp <- png("file1.png", width=800, height=800)
xyplot(c(0,1.6)~c(200,1200),
       main="",
       xlab=list(label="Wavelenght (nm)",cex=1.3),
       ylab=list(label="(Normalized) Intensity",cex=1.3),
       scales=list(
         x=list(at=seq(200,1200,200),cex=1.3),
         y=list(at=seq(0,1.5,0.25),cex=1.3)
       ),
       panel=function(...){
         # panel.xyplot(...)
         panel.xyplot(all_wavelengths,combined[1,spectracols],col="black",type="l",lwd=3)
         panel.xyplot(all_wavelengths,combined[2,spectracols],col="black",type="l",lwd=3)
         panel.xyplot(all_wavelengths,combined[3,spectracols],col="blue",type="l",lwd=3)
         panel.xyplot(all_wavelengths,combined[4,spectracols],col="blue",type="l",lwd=3)
         panel.xyplot(all_wavelengths,combined[5,spectracols],col="red",type="l",lwd=3)
         panel.xyplot(all_wavelengths,combined[6,spectracols],col="red",type="l",lwd=3)
         panel.xyplot(all_wavelengths,combined[7,spectracols],col="black",type="l",lwd=3)
        panel.xyplot(all_wavelengths,combined[8,spectracols],col="black",type="l",lwd=3)
        panel.xyplot(all_wavelengths,combined[9,spectracols],col="black",type="l",lwd=3)
      panel.xyplot(all_wavelengths,combined[10,spectracols],col="purple",type="l",lwd=3)
  panel.xyplot(all_wavelengths,combined[11,spectracols],col="black",type="l",lwd=3)
    panel.xyplot(all_wavelengths,combined[12,spectracols],col="pink",type="l",lwd=3)
         # llines(all_wavelengths,combined[1,spectracols],col="black",type="l",lwd=3)
         # llines(all_wavelengths,combined[2,spectracols],col="black",type="l",lwd=3)
         # llines(all_wavelengths,combined[3,spectracols],col="blue",type="l",lwd=3)
         # llines(all_wavelengths,combined[4,spectracols],col="blue",type="l",lwd=3)
         # llines(all_wavelengths,combined[5,spectracols],col="red",type="l",lwd=3)
         # llines(all_wavelengths,combined[6,spectracols],col="red",type="l",lwd=3)
         #panel.xyplot(all_wavelengths,combined[6,spectracols],col="red",type="l",lwd=3)
         # llines(all_wavelengths,combined[7,spectracols],col="yellow",type="l",lwd=3)
         # llines(all_wavelengths,combined[8,spectracols],col="yellowk",type="l",lwd=3)
       # llines(all_wavelengths,combined[9,selected_cols],col="purple",type="l",lwd=3)
       # llines(all_wavelengths,combined[10,selected_cols],col="purple",type="l",lwd=3)
       # llines(all_wavelengths,combined[11,selected_cols],col="pink",type="l",lwd=3)
       # llines(all_wavelengths,combined[12,selected_cols],col="pink",type="l",lwd=3)
       }
) 
dev.off()
