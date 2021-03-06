#data <- read.csv(file="ads_1.csv", header=TRUE, sep=",")
#library("RColorBrewer")
args = commandArgs(trailingOnly=TRUE)
data <- read.csv(file=args[1], header=TRUE, sep=",",check.names=FALSE)
pdf(args[2]) # output file name
par(mar=c(4, 8, 4, 4)) # Resize the margin to fit the y axis labels
s <- 1.5
#xx <- barplot(as.numeric(data[1,]), main=args[4], names.arg=colnames(data), las=1, font.lab=1, font.main=1, family='serif', legend=args[3], xlim=c(0,100), args.legend = list(x ="topleft"), xlab="Precision at k (%)")
xx <- barplot(as.numeric(data[1,]), main=args[4], names.arg=colnames(data), las=1, font.lab=1, font.main=1, family='serif', legend=args[3], ylim=c(0,100), args.legend = list(x ="topleft"), ylab="Precision at k (%)", xlab="Number of seeds", cex.names=s, cex.axis=s, cex.lab=2.5, cex.main=2.5, cex.sub=s)
#xx <- barplot(as.matrix(data),col=brewer.pal(n = 3, name = "RdBu"),  main="Precision at K", horiz=TRUE, names.arg=colnames(data), las=1, font.lab=1, font.main=1, family='serif', xlim=c(0,100)) #font.lab and font.main defines font size
#xx <- barplot(as.matrix(data),col=c("grey","#F7F7F7"),  main="Precision at K", horiz=TRUE, names.arg=colnames(data), las=1, font.lab=1, font.main=1, family='serif', xlim=c(0,100), legend=c("k=10", "k=12"), args.legend = list(x ="bottomright")) #font.lab and font.main defines font size
#xx <- barplot(as.numeric(data[1,]), main="Precision at K", horiz=TRUE, names.arg=colnames(data), las=1, font.lab=1, font.main=1, family='serif', xlim=c(0,100)) #font.lab and font.main defines font size

mm <- max(data)
text(x = xx, y = as.numeric(data[1,]), label = as.numeric(data[1,]), pos = 3, cex = s, family="serif") # show text on top of each bar

dev.off()
