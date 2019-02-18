import calendar

from datetime import date

from core.commands import CommandBase


class CurrentCalendarCommand(CommandBase):

    def __init__(self, commands):
        super(CurrentCalendarCommand, self).__init__(commands, CommandBase.TYPE_DIRECT, "calendar")

    def help(self, config, event):
        return "The current calendar."

    def work(self, config, event):
        response = "<@{}> I assume this year:\n```{}```.".format(event["user"],
                                                                 calendar.TextCalendar().formatyear(date.today().year))
        return response
