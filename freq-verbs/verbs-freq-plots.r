# Load verbs cvs as a dataframe and plot a linear and logaritmic plot of relative freq

verbs=read.csv('/Users/rbarbera/Developer/freq-verbs/freq-verbs/verbs-freq.csv',sep=';', header=TRUE)
x = verbs[['frequency']]
x.dec.lin=sort(x,decreasing=TRUE)
x.dec.log=log(x.dec.lin)
x.dec.log.norm = 1.0-x.dec.log/min(x.dec.log)

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
