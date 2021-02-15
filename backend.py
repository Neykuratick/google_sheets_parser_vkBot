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

        if classNumber == 1:
            text += '[09:00 - 10:30]:\n'

        elif classNumber == 2:
            text += '[10:40 - 12:10]:\n'

        elif classNumber == 3:
            text += '[12:40 - 14:10]:\n'

        elif classNumber == 4:
            text += '[14:20 - 15:50]:\n'

        elif classNumber == 5:
            text += '[16:00 - 17:30]:\n'

        # if classNumber % 10 <= 2:
        #     text += '[09:00 - 10:30]:\n'
        #
        # elif 2 < classNumber % 10 <= 4:
        #     text += '[10:40 - 12:10]:\n'
        #
        # elif 4 < classNumber % 10 <= 6:
        #     text += '[12:40 - 14:10]:\n'
        #
        # elif 6 < classNumber % 10 <= 8:
        #     text += '[14:20 - 15:50]:\n'
        #
        # elif 8 < classNumber % 10 <= 10:
        #     text += '[16:00 - 17:30]:\n'

        return text

    def scraper(self, weekday, week):
        # print(weekday, week)

        if weekday == 0:
            weekday_name = 'Понедельник'
        if weekday == 1:
            weekday_name = 'Вторник'
        if weekday == 2:
            weekday_name = 'Среда'
        if weekday == 3:
            weekday_name = 'Четверг'
        if weekday == 4:
            weekday_name = 'Пятница'
        if weekday == 5:
            weekday_name = 'Суббота'
        if weekday == 6:
            weekday_name = 'Воскресенье'

        text = f'[{weekday_name}]\n\n'

        firstclass = weekday * 10
        lastclass = firstclass + 11

        if week % 2 != 0:
            firstclass_const = 1
            range_const = 2
        else:
            firstclass_const = 2
            range_const = 2

        try:
            # print(f'firstclass - {firstclass}\nfirstclass_const - {firstclass_const}\nlastclass - {lastclass}\nrange_const - {range_const}')
            class_index = 0 # порядковый номер пары
            for subject in range(firstclass + firstclass_const, lastclass, range_const):
                # ch.readCol works by adding 11 to the subject. Subject = 1 is A12 in the spreadsheet.
                # print(f"subject - {subject}, spreadsheet row - {subject + 11}")
                class_index += 1
                text += self.addTime(class_index)
                text += ch.readCol()['values'][19][subject]
                try:
                    text += '\nСсылка:'
                    text += getLink(subject)
                except:
                    pass
                text += '\n\n'
        except:
            pass

        # if weekday < 3 or week % 2 == 0:  # just normal scraping
        #     try:
        #         # print(f'firstclass - {firstclass}\nfirstclass_const - {firstclass_const}\nlastclass - {lastclass}\nrange_const - {range_const}')
        #         class_index = 0 # порядковый номер пары
        #         for subject in range(firstclass + firstclass_const, lastclass, range_const):
        #             # print(subject)
        #             class_index += 1
        #             text += self.addTime(class_index)
        #             text += ch.readCol()['values'][19][subject]
        #             try:
        #                 text += '\nСсылка:'
        #                 text += getLink(subject)
        #             except:
        #                 pass
        #             text += '\n\n'
        #     except:
        #         pass
        #
        # elif weekday == 3 and week % 2 != 0:  # adds maths classes in case if they're not in there
        #     try:
        #         for subject in range(firstclass + firstclass_const, lastclass, range_const):
        #             text += self.addTime(subject)
        #             text += ch.readCol()['values'][19][subject]
        #             try:
        #                 text += getLink(subject)
        #             except:
        #                 pass
        #             text += '\n\n'
        #     except:
        #         pass
        #
        #     text += '' # [НЕ ТОЧНО!!] 10:40 - 12:10 Пара Программирования
        #
        # elif weekday == 4 and week % 2 != 0:  # adds programming classes in case if they're not in there
        #     try:
        #         for subject in range(firstclass + firstclass_const, lastclass, range_const):
        #             text += self.addTime(subject)
        #             text += ch.readCol()['values'][19][subject]
        #             try:
        #                 text += getLink(subject)
        #             except:
        #                 pass
        #             text += '\n\n'
        #     except:
        #         pass
        #
        #     text += ''

        return text

    def AllForToday(self):
        weekday = datetime.datetime.today().weekday()
        week = datetime.date.today().isocalendar()[1]
        if weekday == 4 or weekday == 5:  # if tomorrow is saturday or sunday
            return "Сёдня адыхаем"

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