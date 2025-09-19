import streamlit as st
import random
import os

st.set_page_config(page_title="Blackjack 🃏", page_icon="🃏", layout="centered")

if 'deck' not in st.session_state:
    suits = ['♠', '♥', '♦', '♣']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    st.session_state.deck = [(v, s) for s in suits for v in values]
    random.shuffle(st.session_state.deck)
    st.session_state.dinero = 1000
    st.session_state.bet = 0
    st.session_state.apuesta_minima = 50
    st.session_state.player_cards = []
    st.session_state.dealer_cards = []
    st.session_state.player_stopped = False
    st.session_state.game_over = False

def card_value(card):
    v, _ = card
    if v in ['J', 'Q', 'K']:
        return 10
    elif v == 'A':
        return 11
    else:
        return int(v)

def calculate_score(cards):
    score = sum(card_value(c) for c in cards)
    aces = sum(1 for c in cards if c[0] == 'A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def get_card_image_filename(card):
    value, suit = card
    suit_map = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}
    return f"cards/{value}{suit_map[suit]}.png"

def reset_game():
    suits = ['♠', '♥', '♦', '♣']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    st.session_state.deck = [(v, s) for s in suits for v in values]
    random.shuffle(st.session_state.deck)
    st.session_state.player_cards = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_cards = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.player_stopped = False
    st.session_state.game_over = False

st.title("🎰 Blackjack Game 🎰")
st.write(f"💰 Dinero disponible: **${st.session_state.dinero}**")
st.write(f"💵 Apuesta mínima: **${st.session_state.apuesta_minima}**")

if st.session_state.bet == 0:
    apuesta = st.number_input("¿Cuánto deseas apostar?", min_value=st.session_state.apuesta_minima, max_value=st.session_state.dinero, step=10)
    if st.button("Comenzar partida"):
        st.session_state.bet = apuesta
        st.session_state.dinero -= apuesta
        reset_game()
        st.rerun()

if st.session_state.bet > 0:
    st.subheader("🧍 Tus cartas:")
    cols = st.columns(len(st.session_state.player_cards))
    for i, card in enumerate(st.session_state.player_cards):
        cols[i].image(get_card_image_filename(card), width=100)
    player_score = calculate_score(st.session_state.player_cards)
    st.write(f"🎯 Puntuación del jugador: **{player_score}**")

    st.subheader("🤖 Cartas del dealer:")
    dealer_score = calculate_score(st.session_state.dealer_cards)
    if st.session_state.player_stopped or st.session_state.game_over:
        dealer_cols = st.columns(len(st.session_state.dealer_cards))
        for i, card in enumerate(st.session_state.dealer_cards):
            dealer_cols[i].image(get_card_image_filename(card), width=100)
        st.write(f"🎯 Puntuación del dealer: **{dealer_score}**")
    else:
        st.image(get_card_image_filename(st.session_state.dealer_cards[0]), width=100)
        st.image("cards/back.png", width=100) if os.path.exists("cards/back.png") else st.write("❓")

    if not st.session_state.game_over and not st.session_state.player_stopped:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🃏 Pedir carta"):
                nueva = st.session_state.deck.pop()
                st.session_state.player_cards.append(nueva)
                if calculate_score(st.session_state.player_cards) > 21:
                    st.session_state.game_over = True
                st.rerun()
        with col2:
            if st.button("✋ Plantarse"):
                st.session_state.player_stopped = True
                while calculate_score(st.session_state.dealer_cards) < 17:
                    st.session_state.dealer_cards.append(st.session_state.deck.pop())
                st.session_state.game_over = True
                st.rerun()

    if st.session_state.game_over:
        st.subheader("🎲 Resultado")
        player_score = calculate_score(st.session_state.player_cards)
        dealer_score = calculate_score(st.session_state.dealer_cards)

        if player_score > 21:
            st.error("💥 Te pasaste de 21. ¡Pierdes!")
        elif dealer_score > 21:
            st.success("🎉 El dealer se pasó. ¡Ganas!")
            st.session_state.dinero += st.session_state.bet * 2
        elif player_score > dealer_score:
            st.success("🏆 Tienes mejor puntuación. ¡Ganas!")
            st.session_state.dinero += st.session_state.bet * 2
        elif dealer_score > player_score:
            st.error("😞 El dealer gana con mejor puntuación.")
        else:
            st.warning("😐 Empate... pero el dealer gana en empate.")

        st.write(f"💰 Dinero actual: **${st.session_state.dinero}**")

        if st.session_state.dinero <= 0:
            st.error("😈 Has perdido todo tu dinero, espero que te hayas divertido 😈")

        if st.button("🔄 Jugar de nuevo"):
            st.session_state.bet = 0
            reset_game()

            st.rerun()
