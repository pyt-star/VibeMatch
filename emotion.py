from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr


recognizer = sr.Recognizer()
sentiment_obj = SentimentIntensityAnalyzer()

recognizer.pause_threshold = 2.0
recognizer.dynamic_energy_threshold = True

with sr.Microphone() as source:
    print("Calibrating background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=2)

    print("Speak now (take your time)...")
    
    recorded_audio = recognizer.listen(source,timeout=5, phrase_time_limit=15  )

    print("Done recording.\n")

try:
    
    print("Recognizing...")
    text = recognizer.recognize_google(recorded_audio, language="en-US")
    
    print("You said:", text)

   
    print("\nAnalyzing sentiment...")
    sentiment = sentiment_obj.polarity_scores(text)

    print("\nSentiment Scores:")
    print(sentiment)

    if sentiment['compound'] >= 0.05:
        print("Overall Sentiment: Positive")
    elif sentiment['compound'] <= -0.05:
        print("Overall Sentiment: Negative")
    else:
        print("Overall Sentiment: Neutral")

except sr.WaitTimeoutError:
    print("You didn't start speaking in time.")
except sr.UnknownValueError:
    print("Could not understand audio clearly.")
except Exception as ex:
    print("Error:", ex)