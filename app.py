import streamlit as st
import pandas as pd

import streamlit as st
from itertools import cycle
import requests

# caching.clear_cache()

# @st.experimental_memo(suppress_st_warning=True)
st.subheader('Card game')
st.write('please click restart button and refresh the link when starting new game')


@st.cache_resource  # @st.singleton
def initioal_deck(number_cards, deckid, player):
    cardurl = f'https://deckofcardsapi.com/api/deck/{deckid}/draw/?count={number_cards}'
    deckurl_card = requests.get(cardurl).json()
    images = []
    values = []
    v = player
    for i in deckurl_card['cards']:
        imag = i["image"]
        val = i["value"]
        try:
            val = int(val)
        except:
            val = i["value"]
        images.append(imag)
        values.append(val)

    return images, values


def initioal_deck_(number_cards):
    cardurl = f'https://deckofcardsapi.com/api/deck/{deckid}/draw/?count={number_cards}'
    deckurl_card = requests.get(cardurl).json()
    images = []
    values = []
    for i in deckurl_card['cards']:
        imag = i["image"]
        val = i["value"]
        try:
            val = int(val)
        except:
            val = i["value"]
        images.append(imag)
        values.append(val)

    return images, values


def calculate_hand_value(hand):
    value = 0
    has_ace = False

    for card in hand:
        rank = str(card)

        if rank.isdigit():
            value += int(rank)
        elif rank in ['JACK', 'QUEEN', 'KING']:
            value += 10
        elif rank == 'ACE':
            has_ace = True
            value += 11

    if has_ace and value > 21:
        value -= 10

    return value


@st.cache_resource
def new_game(name):
    deckurl_ = requests.get(
        "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json(
        )
    deckid = deckurl_['deck_id']
    return deckid


ask_number_of_people = st.number_input('How many people are going to play?', 2)
name_of_players = []

with st.form("annotation_form"):
    for player in range(ask_number_of_people):
        name = st.text_input(f'Name of player {player+1}', key=player)
        name_of_players.append(name)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Confirmed")

name_of_players[:] = [x for x in name_of_players if x]

if len(name_of_players) > 0:

    deckid = new_game(name_of_players)

    players = []
    plapyers_im = []

    players_index_img_ = []

    for i in name_of_players:
        image, values = initioal_deck(2, deckid, i)
        players.append(values)
        plapyers_im.append(image)

    # st.write(name_of_players)

    for count, i in enumerate(name_of_players):
        st.subheader(i + " " + 'hand')
        st.image(plapyers_im[count], use_column_width=False, width=100)

    # st.image(players_index_img_, use_column_width=False, width=100)
    if 'disable' not in st.session_state:
        st.session_state.disable = False

    if 'disable_stand' not in st.session_state:
        st.session_state.disable_stand = False

    if 'load_state' not in st.session_state:
        st.session_state.load_state = False

    select_button_ = st.selectbox(f'select', name_of_players)
    st.session_state.disable = False
    st.session_state.disable_stand = False
    select_button_ = name_of_players.index(select_button_)

    if 'count' not in st.session_state:
        st.session_state['count'] = 0

    import pandas as pd

    if st.button('hit', disabled=st.session_state.disable_stand
                 ) or st.session_state.load_state:

        image, card = initioal_deck_(1)

        players_index = players[select_button_] + card
        players_index_img = plapyers_im[select_button_] + image
        players_index_img_.append(image)

        name = name_of_players[select_button_]
        name_imag = name_of_players[select_button_] + '_1'

        if name_imag not in st.session_state:
            st.session_state[name_imag] = []

        if name not in st.session_state:
            st.session_state[name] = []

        t = st.session_state[name] + players_index
        t_image = st.session_state[name_imag] + players_index_img

        st.session_state[name] = list(set(t))
        st.session_state[name_imag] = list(set(t_image))

        # # st.experimental_rerun()
        # st.write(st.session_state[name])
        # st.write(card)

        st.image(st.session_state[name_imag],
                 use_column_width=False,
                 width=100)

    if st.button('stand') or st.session_state.load_state:

        # st.session_state.load_state = False
        # st.session_state.disable_stand = False
        st.session_state.disable_stand = True

        name = name_of_players[select_button_]
        name_ = name + '_'

        if name not in st.session_state:
            st.session_state[name] = []

        if len(st.session_state[name]) == 0:
            st.session_state[name] = players[select_button_]
        else:
            pass
            # st.write(st.session_state[name])

            if name_ not in st.session_state:
                st.session_state[name_] = calculate_hand_value(
                    st.session_state[name])

            st.subheader(calculate_hand_value(st.session_state[name]))

        df = pd.DataFrame()

        df['players_name'] = [name]
        df['cards_link'] = [st.session_state[name]]
        df['score'] = [calculate_hand_value(st.session_state[name])]
        df.to_csv(f'df_{name}.csv', index=False)

    if st.button('see the winner'):

        import glob

        get_all_csv = glob.glob('*.csv')

        df = pd.DataFrame()
        for file in get_all_csv:
            data = pd.read_csv(file)
            df = pd.concat([df, data], axis=0)

        df_ = df[df['score'] <= 21]

        try:
            das = df_.sort_values(by=['score'], ascending=False).dropna()
            df = df.sort_values(by=['score'], ascending=False).dropna()

            st.write(df[['players_name', 'score']])
            winner = list(das['players_name'])[0]
            st.subheader(f'{winner} :  is the winner')

        except:
            st.subheader(f'all loseed')

    def clear_state():
        for i in name_of_players:
            st.session_state[i] = []
        return

    if st.button('restart_game',
                 on_click=clear_state) or st.session_state.load_state:
        # st.session_state.load_state = True
        import os
        import glob
        for file in glob.glob("*.csv"):
            os.remove(file)

else:
    st.write('Enter the players name')
