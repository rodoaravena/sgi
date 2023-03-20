from apps.activity.models import Session
from datetime import datetime, timedelta

def getSessionsBetweenTimestamps(gte, lte):
    if gte is None or lte is None:
        sessions = Session.objects.all().order_by('pc', 'start').prefetch_related('pc')
    else:
        if gte > lte:
            return None
        sessions = Session.objects.filter(start__gte=gte, start__lte=lte).order_by('pc', 'start').prefetch_related('pc')
    return sessions

def getTimestamp(dt):
    return int(datetime.timestamp(dt)) * 1000

def getStartOfDay(dt):
    return datetime(dt.year, dt.month, dt.day)

def getTodayTimestamps():
    now = datetime.now()
    today = getStartOfDay(now)
    return (getTimestamp(today), getTimestamp(now))

def getThisWeekTimestamps():
    now = datetime.now()
    today = getStartOfDay(now)
    startOfWeek = today - timedelta(days=today.weekday())
    return (getTimestamp(startOfWeek), getTimestamp(now))

def getThisMonthTimestamps():
    now = datetime.now()
    today = getStartOfDay(now)
    startOfMonth = today.replace(day=1)
    return (getTimestamp(startOfMonth), getTimestamp(now))

def getThisYearTimestamps():
    now = datetime.now()
    today = getStartOfDay(now)
    startOfYear = today.replace(day=1, month=1)
    return (getTimestamp(startOfYear), getTimestamp(now))

def getSessionsByOption(option):
    if option == 'today':
        timestamps = getTodayTimestamps()
    elif option == 'week':
        timestamps = getThisWeekTimestamps()
    elif option == 'month':
        timestamps = getThisMonthTimestamps()
    elif option == 'year':
        timestamps = getThisYearTimestamps()
    else:
        return None
    gte, lte = timestamps
    return getSessionsBetweenTimestamps(gte, lte)


def formatSessions(sessions):
    for s in sessions:
        if (s.end is not None):
            td = timedelta(milliseconds=s.end - s.start)
            s.time = str(td).split('.')[0]
            s.end = datetime.fromtimestamp(s.end / 1000).strftime("%d/%m/%Y - %H:%M:%S")
        else:            
            s.time = '-'
            s.end = 'Activo'
        s.start = datetime.fromtimestamp(s.start / 1000).strftime("%d/%m/%Y - %H:%M:%S")
    return sessions

def sessionsToJson(sessions):
    def sessionToJson(session):
        s = {}
        s['pc'] = session.pc.name
        s['start'] = session.start
        s['end'] = session.end
        s['time'] = session.time
        return s        

    return list(map(sessionToJson, sessions))

