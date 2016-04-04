unique_tags=[]
class Calculate_score(object):
		
		""" 
		Attributes:
			name: A string representing the customer's name.
			balance: A float tracking the current balance of the customer's account.
		"""

		def __init__(self, time,tags):
			
			
			self.time = time
			
			self.tags = tags
			self.length=len(tags)
			self.new_tags=[]
			global unique_tags 
			self.new_tags = list(set(tags)-set(unique_tags))
			if self.length != 1:
				unique_tags = unique_tags+self.new_tags
			self.newtags_length=len(self.new_tags)
					
	  
		def score(self):
			self.scores=(self.length-1)*(self.newtags_length)+(self.newtags_length)*(self.length-self.newtags_length)   
			return (self.scores)
	
def avg_deg(input_file,output_file):
	import simplejson,os
	import pandas as pd      
	twitter_input = open(input_file,"r")
	f = open(output_file, 'w')
	f.close()
	
	total_time = []
	total_hash = []
	def inputfile(twitter_input):
		for line in twitter_input:        
			single_tweet = simplejson.loads(line)
			if 'created_at'in single_tweet:            
				if(len(single_tweet["entities"]['hashtags'])>0):
					tags=[]
					time_stamp = single_tweet['created_at']                
					hash_tags = single_tweet["entities"]['hashtags']
					total_time.append(time_stamp)
					for i in range(len(hash_tags)):
						tags.append(hash_tags[i]["text"])
					total_hash.append(tags) 
					
		return (total_time,total_hash)
	data=pd.DataFrame(columns=('Time_stamp','Hashtags'))
	data.Time_stamp,data.Hashtags=inputfile(twitter_input)
	data.Time_stamp=pd.to_datetime(data.Time_stamp)
	data=data.sort_values('Time_stamp')
	data.index = range(0,data.shape[0])
	def avg_score(score_val):
		return((score_val)/float(len(unique_tags)))
	def write_file(score_val):
         with open(output_file,'a') as f:
             f.write("{0:.2f}\n".format((score_val)))
			 
	prev_avg_score = []
	#unique_tags = []
	from datetime import timedelta
	temp1 = pd.DataFrame(columns=('Time_stamp','Hashtags'))
	score_val = 0
	for j in range(data.shape[0]):
		#print j
		End_tag=data.Time_stamp[j]
		Start = End_tag - timedelta(seconds=60)
		temp1 = temp1.append(data.loc[j])
		temp2= temp1[(temp1['Time_stamp']>Start) & (temp1['Time_stamp']<=End_tag)]
		if((temp1.shape[0]-temp2.shape[0])>0):
		   unique_tags[:] = []
		   score_val=0
		   temp1 = temp2
		temp2.index = range(0,temp2.shape[0])
		

		
		for i in range(temp2.shape[0]):
			a=Calculate_score(temp2.Time_stamp[i],temp2.Hashtags[i])
			score_val = a.score() + score_val
		
		if (len(unique_tags) == 0):
			#print prev_avg_score
			#print 'success'
			write_file(round(prev_avg_score,2))  
		else:
			#print avg_score(score_val) 
			prev_avg_score = avg_score(score_val)
			#print 'nsuccess'
			write_file(round(prev_avg_score,2))

if __name__ == '__main__':
    import os
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    print file_dir
    input_file = file_dir + r'/tweet_input/tweets.txt'
    print input_file
    output_file = file_dir + r'/tweet_output/output.txt'
    print output_file
    avg_deg(input_file,output_file)
