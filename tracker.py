import calendar
import datetime
import pprint

import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sg.theme("DarkBrown2")

layout = [[sg.Canvas(key='-GRAPH-')],
          [sg.T("Balance: "), sg.T(key='-DIF-')],
          [sg.T("Enter amount spent"), sg.I(key="-AMT-", do_not_clear=True)],
          [sg.T("Add memo"), sg.I(key="-MEMO-")],
          [sg.Radio("Expense", "Radio", key="-EXP-"), sg.Radio("Income", "Radio", key="-INC-")],
          [sg.I(key="-DATE-"),
           sg.CalendarButton("Date", close_when_date_chosen=True, target="-DATE-", no_titlebar=False)],
          [sg.Submit(), sg.B("Expense"), sg.B("Income"), sg.Cancel()]]

headings = ["Date", "Memo", "Amount"]
cal_dates = {}
days = []
exp_txn = []
inc_txn = []
tot_exp, tot_inc = 0, 0
date = datetime.datetime.today()
month = date.month

# initializing calendar
for i in range(1, 13):
    days_in_month = calendar.monthrange(date.year, i)[1]
    cal_dates[i] = [0 for j in range(1, days_in_month + 1)]


def expenses():
    exp_layout = [[sg.Table(values=exp_txn, headings=headings, max_col_width=50, auto_size_columns=True,
                            display_row_numbers=True, justification='center', num_rows=10, key='-TABLE-', row_height=35,
                            tooltip='Expenses Table')],
                  [sg.T("Total: " + str(tot_exp))]]
    exp_win = sg.Window("Expenses", exp_layout, modal=True)
    while True:
        e, v = exp_win.read()
        if e == sg.WINDOW_CLOSED:
            break
    exp_win.close()


def income():
    inc_layout = [[sg.Table(values=inc_txn, headings=headings, max_col_width=50, auto_size_columns=True,
                            display_row_numbers=True, justification='center', num_rows=10, key='-TABLE-', row_height=35,
                            tooltip='Income Table')],
                  [sg.T("Total: " + str(tot_inc))]]
    inc_win = sg.Window("Income", inc_layout, modal=True)
    while True:
        e, v = inc_win.read()
        if e == sg.WINDOW_CLOSED:
            break
    inc_win.close()


def txn_per_day(txn_date, amt):
    txn_day = cal_dates[txn_date.month]
    txn_day[txn_date.day - 1] += amt
    pprint.pprint(cal_dates)
    print(cal_dates[txn_date.month])


def update_figure(txn_month):
    idx = txn_month if txn_month != month else month
    days_in_txn_month = calendar.monthrange(date.year, txn_month)[1]
    day_txn = [j for j in range(1, days_in_txn_month + 1)]
    global figure_agg, fig, ax, figure_canvas_agg
    if figure_agg:
        figure_canvas_agg.get_tk_widget().forget()
        plt.clf()
        figure_agg = False
        fig = plt.figure()
        ax = fig.add_subplot(111)
        figure_canvas_agg = FigureCanvasTkAgg(fig, window['-GRAPH-'].TKCanvas)
    ax.plot(day_txn, cal_dates[idx], "k-o")
    ax.set_title("Expense vs Day")
    ax.set_xlabel('days')
    ax.set_ylabel('expense')
    ax.grid()
    figure_agg = True
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()


window = sg.Window("Tracker2", layout, finalize=True)
figure_agg = False

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("Expense vs Day")
ax.set_xlabel('days')
ax.set_ylabel('expense')
figure_canvas_agg = FigureCanvasTkAgg(fig, window['-GRAPH-'].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

while True:
    event, values = window.read()
    txn_date = datetime.datetime.strptime(values["-DATE-"], '%Y-%m-%d %H:%M:%S')
    if event in (sg.WINDOW_CLOSED, "Cancel"):
        break
    elif event == "Submit":
        txn_type = "expense" if values["-EXP-"] else "income"
        txn = [values["-DATE-"], values["-MEMO-"], values["-AMT-"]]
        if txn_type == "expense":
            exp_txn.append(txn)
            tot_exp += int(values['-AMT-'])
            txn_per_day(txn_date, int(values['-AMT-']))
        else:
            inc_txn.append(txn)
            tot_inc += int(values['-AMT-'])
        sg.popup("Your transaction updated Successfully!!")
        window['-DIF-'].update(tot_inc - tot_exp)
        window['-AMT-'].update('')
        window['-DATE-'].update('')
        update_figure(txn_date.month)
    elif event == "Expense":
        expenses()
    elif event == "Income":
        income()


window.close()
