# Kaixiong Ye's script for generating QQ and manhattan plots from XWAS output

args    <- commandArgs(trailingOnly=TRUE)
if(is.na(args[2])){
        stop("Usage:Rscript *.R <input of p values><output basename>\n")
}
 library(qqman)
gwasfile <- args[1];
outbase  <- args[2];
manfile  <- paste(outbase, ".man.pdf", sep="")
qqfile   <- paste(outbase, ".qq.pdf", sep="")
gwasResults<-read.table(gwasfile <- args[1], header=T)
pdf(manfile, h=3, w=7)
par(mar=c(4.1,4.1,1.1,1.1))
manhattan(gwasResults, suggestiveline = F, genomewideline = F, bty="n")
dev.off()
pmax <- max(-log10(gwasResults$P)) + 1
pdf(qqfile, h=3,w=3)
par(mar=c(4.1,4.1,1.1,1.1))
qq(gwasResults$P, main = "", bty="n", xlim=c(0, pmax), ylim=c(0,pmax))
dev.off()
