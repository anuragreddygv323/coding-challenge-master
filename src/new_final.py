UniCountertags=list()
def main():
    import os
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    print file_dir
    input_file = file_dir + r'/tweet_input/tweets.txt'
    print input_file
    output_file = file_dir + r'/tweet_output/output.txt'
    print output_file
    Avg_degree_total(input_file,output_file)

class Tweetlvlscore(object):
		def __init__(self, time,tags):

			self.time = time
			self.tags = tags
			self.length=len(tags)
			self.new_tags=[]
			global UniCountertags 
			self.new_tags = list(set(tags)-set(UniCountertags))
			if self.length != 1:
				UniCountertags = UniCountertags+self.new_tags
			self.newtags_length=len(self.new_tags)
					
	  
		def Tweetscore(self):
			self.scores=(self.length-1)*(self.newtags_length)+(self.newtags_length)*(self.length-self.newtags_length)   
			return (self.scores)
	
def Avg_degree_total(input_file,output_file):
	twitter_input = open(input_file,"r")
	f = open(output_file, 'w')
	f.close()
	import pandas as pd
	from datetime import datetime
	from datetime import timedelta
	import simplejson
	Tweettime = list()
	Tweet_hashs = list()
	def inputfile(twitter_input):
		for line in twitter_input:        
			single_tweet = simplejson.loads(line)
			if 'created_at'in single_tweet:            
				if(len(single_tweet["entities"]['hashtags'])>0):
					tags=[]
					time_stamp = single_tweet['created_at']                
					hash_tags = single_tweet["entities"]['hashtags']
					Tweettime.append(time_stamp)
					for i in range(len(hash_tags)):
						tags.append(hash_tags[i]["text"])
					Tweet_hashs.append(tags) 
					
		return (Tweettime,Tweet_hashs)
	Tweetdata=pd.DataFrame(columns=('Time_stamp','Hashtags'))
	Tweetdata.Time_stamp,Tweetdata.Hashtags=inputfile(twitter_input)
	Tweetdata.Time_stamp=pd.to_datetime(Tweetdata.Time_stamp)
	Tweetdata=Tweetdata.sort_values('Time_stamp')
	Tweetdata.index = range(0,Tweetdata.shape[0])
	def Averagescore(score_value):
		return((score_value)/float(len(UniCountertags)))
	def write_file(score_value):
         with open(output_file,'a') as f:
             f.write("{0:.2f}\n".format((score_value)))
	   
	Paverage_score = list()
	dataroll = pd.DataFrame(columns=('Time_stamp','Hashtags'))
	score_value = 0
	for j in range(Tweetdata.shape[0]):
		Latest_tweet_time=Tweetdata.Time_stamp[j]
		start_tweet_time = Latest_tweet_time - timedelta(seconds=60)
		dataroll = dataroll.append(Tweetdata.loc[j])
		fil_dataroll= dataroll[(dataroll['Time_stamp']>start_tweet_time) & (dataroll['Time_stamp']<=Latest_tweet_time)]
		if((dataroll.shape[0]-fil_dataroll.shape[0])>0):
		   UniCountertags[:] = []
		   score_value=0
		   dataroll = fil_dataroll
		fil_dataroll.index = range(0,fil_dataroll.shape[0])
		for i in range(fil_dataroll.shape[0]):
			a=Tweetlvlscore(fil_dataroll.Time_stamp[i],fil_dataroll.Hashtags[i])
			score_value = a.Tweetscore() + score_value
		
		if (len(UniCountertags) == 0):
			write_file(round(Paverage_score,2))  
		else:
			Paverage_score = Averagescore(score_value)
			write_file(round(Paverage_score,2))

if __name__ == '__main__':
    main()