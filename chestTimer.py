import PySimpleGUI as sg
from time import time

#TODO
# cancels person when timer has been reached
# add project to GITHUB
# player timer changes colour depending on which clock is ticking
# clean up code
# ability to change starting timer
# allow you to change indivudal players times
 
def create_window(players, addition_time):
    sg.theme('black')

    layout = [
        [
            sg.Button('update',key='-UPDATE-'), 
            sg.Combo(['1', '2', '3', '4'], default_value='2', key='-PLAYERS-')
        ],
        [sg.Text('', font = 'Young 50', key = '-TIME-')],
        [
            sg.Button('Start', button_color = ('#FFFFFF','#FF0000'), border_width = 0, key = '-STARTSTOP-'),
            sg.Button('Next' , button_color = ('#FFFFFF','#FF0000'), border_width = 0, key = '-NEXT-')
        ],
        [sg.Column([[]], key = '-LAPS-')]
    ]
    for i in range(players):
        test = f'-player{i}-'
        layout.append([sg.Text(f'{addition_time}', font = 'Young 50', key= test)])
    return sg.Window(
        'Stopwatch',
        layout,
        element_justification = 'center',
        size = (300,500))

class Player():
    def __init__(self, players = 2) -> None:
        self.players = players
        self.player_turn = 0
        self.addition_time = [0]*self.players
        self.allowance_timer = [360] * self.players
        self.start_time = 0
        
    
    def start(self):
        self.start_time = time()

    def update_clocks(self):
        self.elapsed_time = round(time() - self.start_time,1)
        self.player_time = round(
            self.allowance_timer[self.player_turn] - self.elapsed_time - self.addition_time[self.player_turn],
            1
            )

    def next_player(self):
        self.addition_time[self.player_turn] += self.elapsed_time
        self.player_turn += 1
        self.start_time = time()
        if self.player_turn >= self.players:
            self.player_turn = 0
    
    def current_player_time(self):
        return round(
            self.allowance_timer[self.player_turn] - self.addition_time[self.player_turn],
            1
        )



player = Player()
window = create_window(player.players, player.current_player_time())

active = False

while True:
    event, values = window.read(timeout = 10)
    if event in (sg.WIN_CLOSED, '-CLOSE-'):
        break

    if event == '-STARTSTOP-': 
        if active:
            # from active to stop
            active = False
            window['-STARTSTOP-'].update('Reset')
        else:
            # from stop to reset
            if player.start_time > 0:
                #TODO BROKEN - solution: re create class again
                window.close()
                player = Player()
                window = create_window(player.players, player.current_player_time())
            # from start to active 
            else:
                player.start()
                active = True
                window['-STARTSTOP-'].update('Stop')

    if active:
        player.update_clocks()
        window['-TIME-'].update(player.elapsed_time)
        window[f'-player{player.player_turn}-'].update(player.player_time)

        if event == '-NEXT-':
            player.next_player()



    if event == '-UPDATE-':
        #TODO clock to reset when update is pressed
        print('updating to more players', values)
        player_count = int(values['-PLAYERS-'])

        player = Player(player_count)
        window.close()
        window = create_window(player_count, player.current_player_time())
        
window.close()

if __name__ == '__main__':
    #TODO updating if statment
    pass