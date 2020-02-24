import os
import re
import time
from copy import deepcopy
from datetime import datetime
import speech_recognition as sr
import moviepy.editor as mp

from LogEntry import LogEntry
from LogFile import LogFile
from pydub import AudioSegment


class VideoLogFile(LogFile):

    def __init__(self):
        super(VideoLogFile, self).__init__()

    def readLogFile(self):
        clip = mp.VideoFileClip(self.filename)
        clip.audio.write_audiofile("audio.mp3")
        audio = AudioSegment.from_wav("audio.mp3")
        segments = audio.dice(60)
        for segment in segments:
            segment.export('temp.wav', format="wav")
            recognizer = sr.Recognizer()
            with sr.AudioFile("temp.wav") as source:
                audio = recognizer.record(source)
                self.lines.append(recognizer.recognize_google(audio))
        if len(segments) > 0:
            os.remove("temp.wav")
        os.remove("audio.mp3")

    def cleanseLogFile(self):
        try:
            self.readLogFile()
            return True
        except Exception as e:
            print(e)
            return False

    def validateLogFile(self, eventStartTime, eventEndTime):
        if not self.cleansed:
            return False
        date = datetime.strptime(time.ctime(os.path.getctime(self.filename)), "%a %b %d %H:%M:%S %Y")
        date = date.strftime("%m/%d/%Y %H:%M %p")
        if date < eventStartTime or date > eventEndTime:
            self.invalidLine = "Whole File"
            self.invalidLineNumber = -1
            self.errorMessage = "Invalid date."
            return False
        return True

    def ingestLogFile(self, creator, eventType):
        if self.validated:
            logEntries = list()
            date = datetime.strptime(time.ctime(os.path.getctime(self.filename)), "%a %b %d %H:%M:%S %Y")
            date = date.strftime("%m/%d/%Y %H:%M %p")
            for line in self.lines:
                logEntry = LogEntry()
                logEntry.date = date
                logEntry.description = line
                logEntry.creator = creator
                logEntry.eventType = eventType
                logEntry.artifact = self.filename
                self.logEntries.append(logEntry)
            self.ingested = True
            return logEntries
        return None

