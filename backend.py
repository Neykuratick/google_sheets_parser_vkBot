import datetime
from ConnectSheet import ConnectSheet
from getLink import getLink

ch = ConnectSheet()
week = datetime.date.today().isocalendar()[1]


class Backend:

    def __init__(self):
        self.text = 'h'

    def addTime(self, classNumber):
        text = ''

        if classNumber % 10 <= 2:
            text += '[09:00 - 10:30]:\n'

        elif 2 < classNumber % 10 <= 4:
            text += '[10:40 - 12:10]:\n'

        elif 4 < classNumber % 10 <= 6:
            text += '[12:40 - 14:10]:\n'

        elif 6 < classNumber % 10 <= 8:
            text += '[14:20 - 15:50]:\n'

        elif 8 < classNumber % 10 <= 10:
            text += '[16:00 - 17:30]:\n'

        return text

    def scraper(self, weekday, week):
        text = ''

        firstclass = weekday * 10
        lastclass = firstclass + 10

        if week % 2 == 0:
            firstclass_const = 1
            range_const = 2
        else:
            firstclass_const = 2
            range_const = 2

        if weekday < 3 or week % 2 == 0:  # just normal scraping
            try:
                for subject in range(firstclass + firstclass_const, lastclass, range_const):
                    text += self.addTime(subject)
                    text += ch.readCol()['values'][19][subject]
                    try:
                        text += '\nСсылка:'
                        text += getLink(subject)
                    except:
                        pass
                    text += '\n\n'
            except:
                pass

        elif weekday == 3 and week % 2 != 0:  # adds maths classes in case if they're not in there
            try:
                for subject in range(firstclass + firstclass_const, lastclass, range_const):
                    text += self.addTime(subject)
                    text += ch.readCol()['values'][19][subject]
                    try:
                        text += getLink(subject)
                    except:
                        pass
                    text += '\n\n'
            except:
                pass

            text += '[НЕ ТОЧНО!!] Пара матана\n\n'
            text += '[НЕ ТОЧНО!!] Пара матана\n\n'
            text += '[НЕ ТОЧНО!!] Пара матана\n\n'

        elif weekday == 4 and week % 2 != 0:  # adds programming classes in case if they're not in there
            try:
                for subject in range(firstclass + firstclass_const, lastclass, range_const):
                    text += self.addTime(subject)
                    text += ch.readCol()['values'][19][subject]
                    try:
                        text += getLink(subject)
                    except:
                        pass
                    text += '\n\n'
            except:
                pass

            text += '[НЕ ТОЧНО!!] 10:40 - 12:10 Пара Программирования\n\n'

        return text

    def AllForToday(self):
        weekday = datetime.datetime.today().weekday()
        week = datetime.date.today().isocalendar()[1]

        return self.scraper(weekday, week)

    def byDay(self, day):
        weekday = day
        week = datetime.date.today().isocalendar()[1]

        return self.scraper(weekday, week)

    def tomorrowClasses(self):
        weekday = datetime.datetime.today().weekday()
        week = datetime.date.today().isocalendar()[1]
        if weekday == 4 or weekday == 5:  # if tomorrow is saturday or sunday
            return "Завтра адыхаем"
        else:
            weekday += 1

        if weekday > 4:
            weekday = 0
            week += 1

        return self.scraper(weekday, week)

    def byDayNext(self, day):  # by next week
        weekday = day
        week = datetime.date.today().isocalendar()[1]
        week += 1

        return self.scraper(weekday, week)
