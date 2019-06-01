args = commandArgs(trailingOnly=TRUE)
data = read.csv(file=args[1], header=TRUE, sep=",",check.names=FALSE)
pdf(args[2])
#names.arg = data[0,], # x-axis labels
#col = colors, # colors
#fill = sequential[6:1], # 6:1 reorders so legend order matches graph
par(mar=c(5, 11, 4, 4)) # Resize the margin to fit the y axis labels
s <- 1.8
xx = barplot(as.matrix(data),
	horiz=TRUE,
	xlab = "Coverage (%)", 
    xlim = c(0,100), 
    family = "serif", las=1, font.lab=2,
    col = c("light grey", "white"),
    cex.names=s, cex.axis=s, cex.lab=s, cex.main=s, cex.sub=s)

#legend = c("Complement", "Intersection"),
#legend("topright", c("Complement", "Intersection"), cex=s, pch=s, pt.cex=s, fill = c("light grey", "white"))
legend("topright", c("Complement", "Intersection"), cex=s, pt.cex=s, fill = c("light grey", "white"))

text(y = xx-0.3, x = as.numeric(data[1,]) + as.numeric(data[2,]) + 10, label = as.numeric(data[1,]) + as.numeric(data[2,]), pos = 3, cex = s, family="serif") # show text on top of each bar
