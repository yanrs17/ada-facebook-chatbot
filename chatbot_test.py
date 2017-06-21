from chatbot.chatbotmanager import ChatbotManager 

if __name__ == '__main__':
	ChatbotManager()
	question = "do u like me"
	answer = ChatbotManager.callBot(question)
	print(answer+" lololol\n")
	question2 = "really"
	answer = ChatbotManager.callBot(question2)
	print(answer+" lololol")