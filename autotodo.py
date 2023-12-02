from macnotesapp import NotesApp
from datetime import date, timedelta
import re

def title(day: date):
      return    day.month.__str__() + \
            "-" + day.day.__str__() + \
            "-" + day.year.__str__()

def remove_dones(old_body):
    indexes = [m.start() for m in re.finditer("✅", old_body)]
    rend = []
    lend = []
    new_body = ""
    index_len = len(indexes)

    if index_len == 0:
        new_body = old_body
    else:
        for i in range(index_len):

            index = indexes[i]
            while True:
                if old_body[index:index+2] == "\n" :
                    rend.append(index+2) # we delete the \n 
                    break
                elif old_body[index] == "<":
                    rend.append(index) # we don't delete the <
                    break
                index += 1

            index = indexes[i]
            while True:
                if old_body[index:index+2] == "\n":
                    lend.append(index) # we keep any  \n on the left side
                    break
                elif old_body[index] == ">":
                    lend.append(index) # again keeping >
                    break
                index -= 1

        assert(len(rend) == len(lend) == index_len)

        for i in range(index_len):
            new_body += old_body[:lend[i]] + old_body[rend[i]:]
    
    return new_body

today = date.today()
yesterday = today - timedelta(days = 1)
yesterday_title = title(yesterday)
today_title = title(today)

# generate our notes object and look for yesterday's note
notesapp = NotesApp()
note = notesapp.notes(name = [yesterday_title])

# remove all done lines from the note
new_body = remove_dones(note[0].body)

# formatting issues TODO: fix this
new_body = new_body[65:]

# make todays note
account = notesapp.account("iCloud")
account.make_note(
    today_title, new_body.replace(yesterday_title,""), folder="TODOLIST"
)
