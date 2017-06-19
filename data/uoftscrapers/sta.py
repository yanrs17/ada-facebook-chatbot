import json

with open('QandAs.json', 'r') as f:
	json_data = json.load(f)
count_len = len(json_data)
print ("Total pair of Q and A is " + str(count_len))

count_Q_words = 0
for item in json_data:
	count_Q_words += len(item['question'].split(' '))
print ("Total word count in all questions is " + str(count_Q_words))

count_A_words = 0
for item in json_data:
	count_A_words += len(item['answer'].split(' '))
print ("Total word count in all answers is " + str(count_A_words))

avg_len_question = count_Q_words // count_len
print("Average length of a question is " + str(avg_len_question))

avg_len_answer = count_A_words // count_len
print("Average length of an answer is " + str(avg_len_answer))

# Total pair of Q and A is 8509
# Total word count in all questions is 61374
# Total word count in all answers is 103867
# Average length of a question is 7
# Average length of an answer is 12
