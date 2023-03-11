import os
from playsound import playsound
from events import Events
from src.SetTimeOut import SetTimeOut
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult

class Timer:
    alarms: list[bool] = []
    integers: list[str] = [
        "zéro", "une", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
        "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf",
        "vingt", "vingt et une", "vingt-deux", "vingt-trois", "vingt-quatre", "vingt-cinq", "vingt-six", "vingt-sept", "vingt-huit", "vingt-neuf",
        "trente", "trente et une", "trente-deux", "trente-trois", "trente-quatre", "trente-cinq", "trente-six", "trente-sept", "trente-huit", "trente-neuf",
        "quarante", "quarante et une", "quarante-deux", "quarante-trois", "quarante-quatre", "quarante-cinq", "quarante-six", "quarante-sept", "quarante-huit", "quarante-neuf",
        "cinquante", "cinquante et une", "cinquante-deux", "cinquante-trois", "cinquante-quatre", "cinquante-cinq", "cinquante-six", "cinquante-sept", "cinquante-huit", "cinquante-neuf",
        "soixante"
    ]

    def __init__(self, processor: Processor, tts, events: Events):
        self.tts = tts
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("timer.minutes", self.timerMinutes)
        processor.addAction("timer.stop", self.timerStop)
    
    def timerRing(self, args: list[any]):
        alarmPath: str = os.path.join(os.path.dirname(__file__), "mp3", "alarm.mp3")
        while(self.alarms[args[0]] == False):
            playsound(alarmPath)
    
    def timerStop(self, intent: Intent, result: ProcessorResult):
        for index, alarm in enumerate(self.alarms):
            self.alarms[index] = True

    def timerMinutes(self, intent: Intent, result: ProcessorResult):
        minutesString: str = intent.variables['minutes']
        if minutesString in self.integers:
            minutesInt: int = self.integers.index(minutesString)

            index: int = -1
            for loopIndex, alarm in enumerate(self.alarms):
                if self.alarms[loopIndex] == True:
                    index = loopIndex
            if index < 0:
                index = len(self.alarms)
                self.alarms.append(False)

            SetTimeOut(self.timerRing, minutesInt * 60 * 1000, [index])

            intent.variables["minutes"] = intent.variables['minutes']
            self.tts(intent.answer())






        