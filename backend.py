import datetime
from ConnectSheet import ConnectSheet
from getLink import getLink

ch = ConnectSheet()
week = datetime.date.today().isocalendar()[1]


class Backend:

    def __init__(self):
        self.text = ''

    def whatLine(self):
        week = datetime.date.today().isocalendar()[1]

        if week % 2:
            return 'под чертой'
        else:
            return 'над чертой'

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
        return text

    def scraper(self, weekday, week, dayTimedelta=0):
        # future is how many days to add to the date

        if weekday == 0:
            weekday_name = 'Понедельник'
        elif weekday == 1:
            weekday_name = 'Вторник'
        elif weekday == 2:
            weekday_name = 'Среда'
        elif weekday == 3:
            weekday_name = 'Четверг'
        elif weekday == 4:
            weekday_name = 'Пятница'
        elif weekday == 5:
            weekday_name = 'Суббота'
        elif weekday == 6:
            weekday_name = 'Воскресенье'

        if week % 2:
            line = 'под чертой'
        else:
            line = 'над чертой'

        firstclass = weekday * 10
        lastclass = firstclass + 11

        if week % 2 != 0:
            firstclass_const = 1
            range_const = 2
        else:
            firstclass_const = 2
            range_const = 2

        text = f'({weekday_name}, {line}, неделя номер №{week}, {datetime.date.today() + datetime.timedelta(days=dayTimedelta)})\n\n'

        try:
            # print(f'firstclass - {firstclass}\nfirstclass_const - {firstclass_const}\nlastclass - {lastclass}\nrange_const - {range_const}')
            class_index = 0  # порядковый номер пары
            for subject in range(firstclass + firstclass_const, lastclass, range_const):
                # text += '\n------------------\n'
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
                text += '\n------------------\n\n'
        except:
            pass

        return text

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

    def AllForToday(self):
        weekday = datetime.datetime.today().weekday()
        week = datetime.date.today().isocalendar()[1]
        if weekday > 4:  # if tomorrow is saturday or sunday
            return "Сёдня адыхаем"

        return self.scraper(weekday, week)

    def byDay(self, weekday):
        week = datetime.date.today().isocalendar()[1]

        dayTimedelta = abs(datetime.datetime.today().weekday() - weekday)
        return self.scraper(weekday, week, dayTimedelta)

    def tomorrowClasses(self):
        weekday = datetime.datetime.today().weekday() + 1
        week = datetime.date.today().isocalendar()[1]
        if weekday > 4:  # if tomorrow is saturday or sunday
            return "Завтра адыхаем"

        if weekday > 6:
            weekday = 0

        dayTimedelta = abs(datetime.datetime.today().weekday() - weekday)
        return self.scraper(weekday, week, dayTimedelta)

    def byDayNext(self, weekday):  # by next week
        week = datetime.date.today().isocalendar()[1]
        week += 1

        dayTimedelta = abs(datetime.datetime.today().weekday() - weekday) + 7
        return self.scraper(weekday, week, dayTimedelta)
