# Load verbs cvs as a dataframe and plot a linear and logaritmic plot of relative freq

verbs=read.csv('/Users/rbarbera/Developer/freq-verbs/freq-verbs/verbs-freq.csv',sep=';', header=TRUE)
x = verbs[['frequency']]
x.dec.lin=sort(x,decreasing=TRUE)
x.dec.log=log(x.dec.lin)
x.dec.log.norm = 1.0-x.dec.log/min(x.dec.log)
x.dec.log.norm = x.dec.log.norm/sum(x.dec.log.norm)

png('/Users/rbarbera/Developer/freq-verbs/freq-verb-linear.png',width=600,height=400)
plot(x.dec.lin,
	main="Verbs's use frequency (Invoke IT data)",
	xlab='Verb index',
	ylab='Relative frequency',
	type='n')
grid()
lines(x.dec.lin,col='red')
dev.off()

png('/Users/rbarbera/Developer/freq-verbs/freq-verb-log.png',width=600,height=400)
plot(x.dec.log.norm,
	main="Verbs's use frequency (Invoke IT data)",
	xlab='Verb index',
	ylab='Log(relative frequency) normalized',
	type='n')
grid()
lines(x.dec.log.norm,col='red')
dev.off()

png('/Users/rbarbera/Developer/freq-verbs/hist-log.png',width=600,height=400)
hist(x.dec.log.norm,
	main="Number of verbs vs Frequency (log-norm)",
	xlab="freq (normalized sum(freq)=1)",
	ylab="number of verbs")
dev.off()
	
png('/Users/rbarbera/Developer/freq-verbs/hist-idx.png',width=600,height=400)
hist(seq(length(x.dec.log.norm)),
	main="Number of verbs selected by index",
	xlab="index",
	ylab="number of verbs")
dev.off()
