#!/usr/bin/env python3
import os, keyboard, requests as req
from tkinter import *

CREDITS = """\
---------------------------
█▀ ░ █░█░█ ░ █▀
▄█ ▄ ▀▄▀▄▀ ▄ ▄█
Smart Waste Sorter
---------------------------
CREDITS
---------------------------
Programming - SD
Programming - CZ
Graphic Design - EY
Database compilation - MX
---------------------------
"""

MUNICIPALITY = open("location.txt", 'r').read()


window = Tk()
window.title("S.W.S")
window.geometry("800x800")
#window.attributes('-fullscreen', True)

def format_disposal(query):
    #Formats the results from the Database file
    return query.replace("C", "Compost").replace("R", "Recycling").replace("G", "Garbage").replace("S", "Special Disposal")


def search_results(query):
    i = 0
    municipality_id = 0
    results = ""
    query = query.lower().replace(query[0], query[0].upper()).split(' ')[0]
    waste = open("./sws-database.csv", encoding = "utf-8")
    waste.readline()
    for line in waste:     
        items = line.split(',')
        #i == 0 checks to see if it's the first readable line in the database which contains the "legend" (I.E the labels for what collumn means what)
        if i == 0:
            #Should've just used municipality_id = items.index(MUNICIPALITY) or something
            for item in items:
                municipality_id += 1
                if item == MUNICIPALITY:
                    break
        i += 1
        if query in items[0]:
            results += f"{items[0]} | {format_disposal(items[municipality_id - 1])}"
    return results

def results_window(results, query):
    rwin = Tk()
    rwin.geometry("800x400")
    rwin.title(f"{query} - S.W.S Results")
    scroll_bar = Scrollbar(rwin)
    scroll_bar.pack(side = RIGHT, fill = Y)
    Label(rwin, text = "| Item | Disposal | Icon |").pack()
    
    if not results:
        Label(rwin, text = f"*No results found for \"{query}\"*").place(x = 300, y = 200)
    
    symbols_list = Listbox(rwin, width = 10, height = 300, yscrollcommand = scroll_bar.set)
    result_list = Listbox(rwin, width = 70, height = 300, yscrollcommand = scroll_bar.set)
    result_array = results.split('\n')
    for result in result_array:
        disposal = result.split("|")[1].strip()
        #Some regex to format garbage to the garbage sign
        symbol = ("🚮" if disposal == "Garbage" else ("♻️" if disposal == "Recycling" else ("🍎" if disposal == "Compost" else "❗")))
        symbols_list.insert(END, symbol)
        result_list.insert(END, result)
        #Needed to make a separate scrollbar for the symbols

    result_list.pack()
    symbols_list.place(x = 680, y = 20)



def main_menu():
    search = ""
    background = PhotoImage(file='background.png')
    bg_label = Label(window, image=background)
    bg_label.pack()
    bg_label.place(x = 0, y = 0)
    def search():
        search = search_bar.get('1.0', 'end').strip()
        results = search_results(search).strip()
        results_window(results, search)
    
    def key_search(placeholder):
        #1 arg is needed for keyboard.on_press to work
        search = search_bar.get('1.0', 'end').strip()
        if not search:
            return
        #Deletes the last search results so that they don't overla[p]
        last_results = window.winfo_children()[len(window.winfo_children()) - 1]
        if "label" in str(last_results): 
            last_results.destroy()
        results = search_results(search).strip()
        results_text = Label(window, text = results)
        results_text.place(x = 150, y = 420)

    keyboard.on_press(key_search, suppress=False)
    
    text = Label(window, text = "S.W.S - Smart Waste Sorter")
    search_bar = Text(
        window,
        height = 1,
        width = 60,
    )

    search_button = Button(
        window,
        text = "Search",
        command = search
    )

    search_button.place(x = 650, y = 100)
    search_bar.place(x = 150, y = 100)

    text.pack()

    municipality_button = Button(
        window,
        text = "Configure Municipality",
        command = municipality_window
    )

    credits_button = Button(
        window,
        text = "Credits",
        command = credits
    )

    info_button = Button(
        window,
        text = "Manual",
        command = man
    )

    municipality_button.place(x = 625, y = 0)

    credits_button.place(x = 0, y = 770)

    info_button.place(x = 724, y = 770)
    window.mainloop()

def credits():
    credits_window = Tk()
    credits_window.title("S.W.S - CREDITS")
    credits_window.geometry("400x400")
    Label(credits_window, text = CREDITS).place(x = 100, y = 100)

def man():
    #open new window with manual
    return

def municipality_window():
    mwin = Tk()
    mwin.title("Municipality Configuration")
    mwin.geometry("150x300")

    def find_location():
        #TBD
        lwin = Tk()
        lwin.title("Find My Municipality")
        lwin.geometry("600x400")
        res = req.get(f"http://ip-api.com/json/?fields=proxy,lat,lon,city").json()
        Label(lwin, text = f"""\
City: {res['city']}
Latitude: {res['lat']}
Longitude: {res['lon']}

Municipality Map of Ontario:
https://geohub.lio.gov.on.ca/datasets/11be9127e6ae43c4850793a3a2ee943c/explore
""").pack()

    def muncipality_input():
        def get_text():
            raw_input = text_input.get('1.0', 'end').strip()
            municipality_input = raw_input.split(" ")[0].lower()
            municipality = municipality_input.replace(municipality_input[0], municipality_input[0].upper(), 1)
            location_file = open('./location.txt', 'w')
            location_file.truncate(0)
            location_file.write(municipality)
            Label(lwin, text = "Municipality changed.\nPlease restart S.W.S for your changes to take effect*").pack()
        lwin = Tk()
        lwin.title("Input Municipality")
        lwin.geometry("400x400")
        Label(lwin, text = f"Current municipality -> {MUNICIPALITY}").pack()
        text_input = Text(
            lwin,
            height = 1,
            width = 60,
        )
        Label(lwin, text = "Input Municipality").pack()
        input_button = Button(
            lwin,
            text = "Submit Text",
            command = get_text
        )
        input_button.pack()
        text_input.pack()
    location_button = Button(
        mwin,
        text = "Find Municipality",
        command = find_location
    )

    manual_input_button = Button(
        mwin,
        text = "Input Municipality",
        command = muncipality_input
    )

    manual_input_button.place(x = 0, y = 50)

    location_button.place(x = 0, y = 0)

main_menu()