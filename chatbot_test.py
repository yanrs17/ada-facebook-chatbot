from chatbot.chatbotmanager import ChatbotManager 

if __name__ == '__main__':
	ChatbotManager()
	question = "How r u buddy"
	answer = ChatbotManager.callBot(question)
	print(answer+" lololol")