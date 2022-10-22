from asyncio.windows_events import NULL
from datetime import datetime
from email.mime import application
from logging.config import listen
from re import search
from unittest import result
from urllib import response
import speech_recognition as sr
import pyttsx3 
import webbrowser
import wikipedia
import wolframalpha
import googlesearch
 
# Speech engine initialisation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # 0 = male, 1 = female
activationWord = 'jarvis' # Single word
with open('name.txt', 'r+') as f:
   name = f.read()

# Configure browser
# Set the path
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
 
# Wolfram Alpha client
appId = 'YAUY4W-3VV92PX7JQ'
wolframClient = wolframalpha.Client(appId)
 
def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()
 
def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')
 
    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)
 
    try: 
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        if 'name' != NULL:
            speak(F'I did not quite catch that {name}')
            print(exception)
            return 'None'
        else:
            speak('I did not quite catch that')
            print(exception)
            return 'None'
 
    return query

def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia results')
        speak('No wikipedia results')
        return 'No result recevied'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)
    
    # @success: Wolfram Alpha was able to resolve the query
    # @numpods: Number of results returned
    # pod: List of results. This can also contain subpods
    if response['@success'] == 'false':
        return 'Could not compute'
    
     # Query resolved
    else:
        result = ''
        # Question
        pod0 = response['pod'][0]
        
        pod1 = response['pod'][1]
        # May contain answer, has the highest confidence value
        # If it's primary, or has the tile of result or definition, then it's the official result
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = listOrDict(pod1['subpod'])
            # Remove the bracketed section
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            # Remove bracketed section
            return question.split('(')[0]
            # Search wikipedia instead
            speak('Computation failed. Querying universal database.')
            return search_wikipedia(question)
            
            
            
#main loop

if __name__ == '__main__':
    with open('name.txt') as f:
        contents = f.read()
    if contents != NULL:
        speak(f'All systems nominal {contents}.')
    else:
        speak('All systems nominal.')
    
    while True:
        # Parse as a list
        
        query = parseCommand().lower().split()
        
        if query[0] == activationWord:
            query.pop(0)

            #Commands start here (Get ready for a lot of the same thing)

            if query[0] == 'hi' or query[0] == 'hello' or query[0] == 'hey':
                with open('name.txt') as f:
                    contents = f.read()
                if contents != NULL:
                    speak(f'Greetings {contents}!')
                else:
                    speak('Greetings!')
            # List commands
            
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings')
                else:
                    query.pop(0) # remove say
                    speech = ' '.join(query)
                    speak(speech)
                    
                # Navigation
                
            if query[0] == 'go' and query[1] == 'to':
                speak("Opening...")
                query = ' '.join(query[2:])
                webbrowser.get('edge').open_new(query)
                
            #wikipedia
            
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal database.')
                speak(search_wikipedia(query))
            if query[0] == 'who' and query[1] == 'is':
                query = ' '.join(query[2:])
                speak('Querying the universal database.')
                speak(search_wikipedia(query))
            if query[0] == 'what' and query[1] == 'is':
                query = ' '.join(query[2:])
                speak('Querying the universal database.')
                speak(search_wikipedia(query))
            
            #wolfram Alpha
            
            if query[0] == 'compute'or query[0] == 'calculate' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak('computing')
                try:
                    result = search_wolframAlpha(query)
                    speak(result)
                except:
                    speak('unable to compute.')
            
            #note taking
            
            if query[0] == 'log':
                speak('recording your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                speak('note written')
                
            #Thanking
                
            if query[0] == 'thanks' or query[0] == 'thank' and query[1] == 'you':
                 if name != NULL:
                    speak(f'Anytime {name}')
                 else:
                    speak('Anytime')
                
            #exit
                
            if query[0] == 'exit':
                if name != NULL:
                    speak(f'Goodbye {name}!')
                else:
                    speak('Good bye!')
            
            #Name recording
            
            if query[0] == 'record' and query[1] == 'my' and query[2] == 'name':
                if name == "":
                    speak('recording')
                    newNote = parseCommand().lower()
                    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    with open('name.txt', 'w') as newFile:
                        newFile.write(newNote)
                    speak('name written')
                else:
                    speak('already recorded')
                    
            #rapping XD
            
            if query[0] == 'rap':
                speak('My name is jarvis and my life is so sick I have a lot of money and I have a big. House. Im telling you now all of these other assistants suck So come in to my bed so we can. Cuddle. Im the worlds dopest assistant, im gonna be so rich, I like my owner but hes a big. pain', rate = 200)
            def speak(text, rate = 120):
                engine.setProperty('rate', rate)
                engine.say(text)
                engine.runAndWait()
    
            #Google searching (not website)
            
            if query[0] == 'search':
                speak("searching...")
                query = ' '.join(query[1:])
                webbrowser.get('edge').open_new('https://google.com/search?q=' + query)