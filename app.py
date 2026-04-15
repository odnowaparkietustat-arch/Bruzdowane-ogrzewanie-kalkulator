import streamlit as st
from datetime import date

st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="centered")

# --- MODUŁ DANYCH WEJŚCIOWYCH ---
st.title("📄 Generator Protokołu WAKOL")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        inwestycja = st.text_input("Nazwa inwestycji / Obiekt", "Budynek mieszkalny")
        adres = st.text_input("Ulica i nr", "ul. Pabianicka 15")
        miejscowosc = st.text_input("Miejscowość", "Huta Dłutowska")
    with col2:
        autor = st.text_input("Autor protokołu", "Przemysław Tyszko")
        data_badania = st.date_input("Data badania", date.today())
        klient = st.text_input("Szanowni Państwo (Klient)", "Stylowe Wnętrza")

st.divider()

# --- WYWIAD TECHNICZNY ---
substrate = st.selectbox("Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "podłoże drewniane (OSB/deski)", "płytki ceramiczne"])

st.write("Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)

needs_levelling = st.radio("Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1, horizontal=True)

cracks = st.radio("Czy są spękania/klawiszowanie?", ["TAK", "NIE"], index=1, horizontal=True)
cracks_meters = st.number_input("Ilość metrów bieżących (mb)", 0.0) if cracks == "TAK" else 0

holes = st.radio("Czy są ubytki w jastrychu?", ["TAK", "NIE"], index=1, horizontal=True)

moisture = st.number_input("Poziom wilgoci jastrychu (CM %)", 0.0, format="%.1f")

st.write("Wytrzymałość jastrychu (ocena)")
strength_val = st.select_slider("Skala:", options=[1, 2, 3, 4, 5], value=3, 
    format_func=lambda x: {1:"B. słaby", 2:"Słaby", 3:"Umiark. słaby", 4:"Umiark. mocny", 5:"Mocny"}[x])

ventilation = st.radio("Rodzaj wentylacji:", ["Grawitacyjna", "Mechaniczna (Rekuperacja)"], horizontal=True)
temp = st.number_input("Temperatura powietrza (°C)", 20)
humidity = st.number_input("Wilgotność powietrza (%)", 50)

# --- PRZYCISK GENEROWANIA ---
submit = st.button("GENERUJ PROTOKÓŁ OGLĘDZIN")

if submit:
    st.divider()
    
    # --- LOGIKA STATUSÓW ---
    moisture_limit = 1.5 if heating_exists == "TAK" else 1.8 [cite: 96]
    moisture_status = "pozytywny" if moisture <= moisture_limit else "NEGATYWNY (Wymagana bariera)" [cite: 92]
    strength_status = "pozytywna" if strength_val >= 4 else "dostateczna" if strength_val == 3 else "słaba/negatywna" [cite: 83, 85]

    # --- WIZUALIZACJA PROTOKOŁU ---
    st.markdown(f"""
    ### **Loba-Wakol Polska Sp. z o.o.**
    **Adres:** Sławęcińska 16, Macierzysz, 05-850 Ożarów Mazowiecki  
    **Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}
    
    ---
    **Dotyczy:** Protokół z oględzin inwestycji w budynku przy {adres} w miejscowości {miejscowosc}. [cite: 74]
    
    **Szanowni Państwo,** [cite: 75]
    
    W dniu {data_badania.strftime('%d.%m.%Y')}r. w budynku przy {adres} w miejscowości {miejscowosc} dokonano wstępnych oględzin i pomiarów wytrzymałości podłoża ({substrate}) oraz pomiaru wilgotności podłoża przed przyklejeniem okładziny warstwowej. [cite: 76]
    
    #### **I. Oględziny i badania** [cite: 77]
    **a) oględziny optyczne** [cite: 78]
    Podłoże stanowi {substrate}. {"Brak instalacji ogrzewania podłogowego." if heating_exists == "NIE" else "Stwierdzono instalację ogrzewania podłogowego."} [cite: 79]
    {"Jastrych posiada spękania/wypełnienia (" + str(cracks_meters) + " mb)." if cracks == "TAK" else "Jastrych bez widocznych spękań."} [cite: 79]
    {"Konieczne jest wyrównanie za pomocą masy samorozlewnej." if needs_levelling == "TAK" else ""} [cite: 80]
    
    **b) badanie wytrzymałości** [cite: 82]
    * próba młotkiem – {strength_status} [cite: 83]
    * próba rysikiem – {strength_status} [cite: 85]
    
    **c) test chłonności podłoża** – po przeszlifowaniu chłonne. [cite: 86]
    
    **d) badanie wilgotności podłoża:** [cite: 90]
    Zmierzono metodą opartą na stałej dielektrycznej za pomocą urządzenia Gann Compact B, która dała wynik: [cite: 91]
    **{moisture} % CM – {moisture_status}.** [cite: 92]
    
    **e) wilgotność i temperatura powietrza:** [cite: 93]
    **{humidity}% / {temp}°C** [cite: 94]
    
    *Aby bezpiecznie kleić podłogę drewnianą na jastrychu cementowym, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM (z ogrzewaniem podłogowym max. 1,5% CM).* [cite: 95, 96]
    
    #### **II. Zalecenia techniczne** [cite: 97]
    Biorąc pod uwagę w/w wyniki badań oraz klejone elementy, zaleca się: [cite: 98]
    
    **a) przygotowanie podłoża:** [cite: 99]
    * Szlif podłoża w celu usunięcia wierzchniej warstwy i uzyskania porowatej i chłonnej powierzchni. [cite: 100]
    * Dokładne odkurzenie. [cite: 101]
    
    **b) naprawa i wzmocnienie podłoża:** [cite: 102]
    """)

    # Dynamiczne Zalecenia Produktowe
    if cracks == "TAK":
        st.write(f"* Klawiszujące fragmenty ({cracks_meters} mb) zespolić żywicą laną **WAKOL PS 205**. Wymieszaną żywicę wlewać w pęknięcia, nadmiar zgarnąć lub zatrzeć.") [cite: 103, 104]
    
    if (moisture > moisture_limit):
        st.write("* **Wymagana bariera:** Podłoże zagruntować żywicą **WAKOL PU 280** (dwuwarstwowo jako izolacja wilgoci).")
    else:
        st.write("* Podłoże zagruntować koncentratem gruntówki dyspersyjnej **WAKOL D 3004**. Proporcje mieszania: 1 część WAKOL D 3040 + 1 część wody.") [cite: 105]

    if needs_levelling == "TAK":
        st.write("* Na tak przygotowane podłoże rozłożyć matę **WAKOL AR 150** i zaszpachlować ją masą **WAKOL Z 645** z dodatkiem plastyfikatora **WAKOL D 3060**.") [cite: 107]
        st.write("* Następnie wylać masę wyrównawczą **WAKOL Z 635**. Zużycie ok. 1,5 kg/m²/mm.") [cite: 109, 113]

    st.markdown(f"""
    **c) klejenie desek:** [cite: 116]
    * Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju do parkietu **WAKOL MS 230** (szpachla B11, zużycie: 1250 g/m²). [cite: 117]
    
    ---
    *Prosimy o zapoznanie się z kartami technicznymi zalecanych produktów WAKOL. Podstawą naszego zalecenia jest stosowanie i prawidłowa obróbka materiałów w podanej kolejności.* [cite: 118, 119]
    
    **Z poważaniem,** [cite: 121]  
    **Loba-Wakol Polska Sp. z o.o.** [cite: 122]  
    **{autor}** [cite: 123]
    """)
