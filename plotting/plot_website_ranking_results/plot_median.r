#data <- read.csv(file="ads_1.csv", header=TRUE, sep=",")
args = commandArgs(trailingOnly=TRUE)
data <- read.csv(file=args[1], header=TRUE, sep=",",check.names=FALSE)
pdf(args[2])
par(mar=c(4, 11, 4, 4)) # Resize the margin to fit the y axis labels
#barplot(as.numeric(data[1,]), main="Precision at K", horiz=TRUE, names.arg=colnames(data), las=1, font.lab=1, font.main=1, family='serif', border=NA)
#xx <- barplot(as.numeric(data[1,]), main="Median", horiz=TRUE, names.arg=colnames(data), las=1, font.lab=1, font.main=1, family='serif', xlim=c(0,100)) #font.lab and font.main defines font size
mm <- max(data)
s <- 1.5
xx <- barplot(as.numeric(data[1,]), xlab="Median", main=args[3], horiz=TRUE, names.arg=colnames(data), las=1, font.lab=1, font.main=1, family='serif', xlim=c(0, mm*1.1), cex.names=s, cex.axis=s, cex.lab=2.5, cex.main=2.5, cex.sub=s) #font.lab and font.main defines font size

text(y = xx-0.3, x = as.numeric(data[1,]) + 0.055*mm, label = as.numeric(data[1,]), pos = 3, cex = s, family="serif") # show text on top of each bar

dev.off()
