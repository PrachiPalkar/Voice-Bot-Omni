import requests
from bs4 import BeautifulSoup
import assist
import webbrowser
import aiml

k = aiml.Kernel()
k.bootstrap(learnFiles="corona.aiml")

class covid():
	def __init__(self):
		self.total = 'Not Available'
		self.deaths = 'Not Available'
		self.recovered = 'Not Available'
		self.totalIndia = 'Not Available'
		self.deathsIndia = 'Not Available'
		self.recoveredIndia = 'Not Available'

	def covidUpdate(self,text):
		URL = 'https://www.worldometers.info/coronavirus/'
		result = requests.get(URL)
		src = result.content
		soup = BeautifulSoup(src, 'html.parser')

		temp = []
		divs = soup.find_all('div', class_='maincounter-number')
		for div in divs:
			temp.append(div.text.strip())
		self.total, self.deaths, self.recovered = temp[0], temp[1], temp[2]
		if "covid" in text:
			print("Omni: Total covid cases in the world: "+temp[0])
			assist.speak("Total covid cases in the world are"+temp[0])
		if "death" in text:
			print("Omni: Total covid death cases in the world: "+temp[1])
			assist.speak("Total covid death cases in the world are"+temp[1])
		if "recover" in text:
			print("Omni: Total covid recovered cases in the world: "+temp[2])
			assist.speak("Total covid recovered cases in the world are"+temp[2])

	def covidUpdateIndia(self,text):
		URL = 'https://www.worldometers.info/coronavirus/country/india/'
		result = requests.get(URL)
		src = result.content
		soup = BeautifulSoup(src, 'html.parser')

		temp = []
		divs = soup.find_all('div', class_='maincounter-number')
		for div in divs:
			temp.append(div.text.strip())
		self.totalIndia, self.deathsIndia, self.recoveredIndia = temp[0], temp[1], temp[2]
		if "covid" in text:
			print("Omni: Total covid cases in India: "+temp[0])
			assist.speak("Total covid cases in India are"+temp[0])
		if "death" in text:
			print("Omni: Total covid death cases in India: "+temp[1])
			assist.speak("Total covid death cases in India are"+temp[1])
		if "recover" in text:
			print("Omni: Total covid recovered cases in India: "+temp[2])
			assist.speak("Total covid recovered cases in India are"+temp[2])

def symptoms():
		print( "Omni: Following are the symptoms of COVID-19:\n" 
				'1. Fever\n',
			    '2. Coughing\n',
				'3. Shortness of breath\n',
				'4. Trouble breathing\n',
				'5. Fatigue\n',
				'6. Chills, sometimes with shaking\n',
				'7. Body aches\n',
				'8. Headache\n',
				'9. Sore throat\n',
				'10. Loss of smell or taste\n',
				'11. Nausea\n',
				'12. Diarrhea\n')
		assist.speak( "Following are the symptoms of COVID-19:" 
				'1. Fever'
			    '2. Coughing'
				'3. Shortness of breath'
				'4. Trouble breathing'
				'5. Fatigue'
				'6. Chills, sometimes with shaking'
				'7. Body aches'
				'8. Headache'
				'9. Sore throat'
				'10. Loss of smell or taste'
				'11. Nausea'
				'12. Diarrhea')

def prevention():
		print("Omni: Following are the things to be taken care of:\n" 
						'1. Clean your hands often. Use soap and water, or an alcohol-based hand rub.\n',
						'2. Maintain a safe distance from anyone who is coughing or sneezing.\n',
						'3. Wear a mask when physical distancing is not possible.\n',
						'4. Don’t touch your eyes, nose or mouth.\n',
						'5. Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze.\n',
						'6. Stay home if you feel unwell.\n',
						'7. If you have a fever, cough and difficulty breathing, seek medical attention.\n')
		assist.speak("Following are the things to be taken care of:" 
						'1. Clean your hands often. Use soap and water, or an alcohol-based hand rub.'
						'2. Maintain a safe distance from anyone who is coughing or sneezing.'
						'3. Wear a mask when physical distancing is not possible.'
						'4. Don’t touch your eyes, nose or mouth.'
						'5. Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze.'
						'6. Stay home if you feel unwell.'
						'7. If you have a fever, cough and difficulty breathing, seek medical attention.')

def cowin():
    url = "https://www.cowin.gov.in/"
    webbrowser.get().open(url)
    print("Omni: Opening COWIN registration link")
    assist.speak("Opening COWIN registration link" )

def main():
	obj = covid()
	while True:
		print("Listening..")
		text=assist.get_audio()
		
		if "world" in text:
			obj.covidUpdate(text)
		elif "India" in text:	
			obj.covidUpdateIndia(text)
		elif "symptom" in text:
			symptoms()
		elif "prevention" in text:
			prevention()
		elif "cowin" in text or "vaccine" in text or "register" in text:
			cowin()
		elif "thank" in text:
			print("Omni: Anytime! I would love to help you more.")
			assist.speak("Anytime! I would love to help you more.")
		elif "bye" in text:
			print("Omni: I hope I assisted you well. Hope to talk to you soon, Bye!") 
			assist.speak("I hope I assisted you well. Hope to talk to you soon, Bye!")
			exit()                                                        
		else:
			response = k.respond(text)
			print("Omni:  "+response)
			assist.speak(response)

if __name__=='__main__':
	main() 