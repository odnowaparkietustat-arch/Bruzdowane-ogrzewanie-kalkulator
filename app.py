import streamlit as st
from datetime import date

st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="centered")

st.title("🛠️ System Doradztwa Technicznego")
st.subheader("Wywiad Techniczny i Protokół WAKOL")

# --- MODUŁ WYWIADU ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    inwestycja = st.text_input("Nazwa inwestycji / Obiekt", "Budynek mieszkalny")
    miejscowosc = st.text_input("Miejscowość", "Huta Dłutowska")
with col_in2:
    adres = st.text_input("Ulica i nr", "Pabianicka 15")
    data_ogledzin = st.date_input("Data oględzin", date.today())

st.divider()

# Q1 - Rodzaj podłoża
substrate = st.selectbox("1. Rodzaj podłoża", ["Cementowy", "Anhydrytowy", "OSB", "Płytki ceramiczne", "Inny"])

# Q2 - Ogrzewanie
st.write("2. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Wybierz:", ["TAK", "NIE"], index=1, label_visibility="collapsed")
heating_type = ""
if heating_exists == "TAK":
    heating_type = st.selectbox("Rodzaj ogrzewania:", ["Wodne klasyczne", "Bruzdowane", "Suche", "Elektryczne"])

# Q3-Q5 - Parametry mechaniczne
needs_levelling = st.radio("3. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1)
thickness = st.number_input("Grubość masy (mm)", 0) if needs_levelling == "TAK" else 0

cracks = st.radio("4. Czy są spękania/dylatacje?", ["TAK", "NIE"], index=1)
cracks_meters = st.number_input("Ilość metrów bieżących (mb)", 0.0) if cracks == "TAK" else 0

holes = st.radio("5. Czy są ubytki?", ["TAK", "NIE"], index=1)

# Q6-Q9 - Pomiary
moisture = st.number_input("6. Poziom wilgoci jastrychu (CM %)", 0.0, format="%.1f")
st.write("7. Wytrzymałość jastrychu")
strength = st.select_slider("Poziom:", options=[1, 2, 3, 4, 5], value=3, 
    format_func=lambda x: {1:"B. słaby", 2:"Słaby", 3:"Umiark. słaby", 4:"Umiark. mocny", 5:"Mocny"}[x])

ventilation = st.radio("8. Wentylacja:", ["Grawitacyjna", "Mechaniczna"])
temp = st.number_input("9. Temperatura powietrza (°C)", 20)
humidity = st.number_input("9. Wilgotność powietrza (%)", 50)

submit = st.button("GENERUJ PROTOKÓŁ OGLĘDZIN")

# --- GENEROWANIE PROTOKOŁU ---
if submit:
    st.divider()
    
    # Nagłówek wizualny
    st.markdown(f"### PROTOKÓŁ Z OGLĘDZIN INWESTYCJI")
    st.markdown(f"**Dotyczy:** {inwestycja}, ul. {adres}, {miejscowosc}")
    
    # Treść protokołu wzorowana na PDF
    protokol_text = f"""
    **Loba-Wakol Polska Sp. z o.o.** ul. Sławęcińska 16, Macierzysz, 05-850 Ożarów Mazowiecki  
    Data: {data_ogledzin.strftime('%d.%m.%Y')} | Autor: Ekspert WAKOL  
    
    ---
    **I. Oględziny i badania**
    
    **a) Oględziny optyczne:** Podłoże stanowi jastrych {substrate.lower()}. {"Wykryto instalację ogrzewania podłogowego (" + heating_type + ")." if heating_exists == "TAK" else "Brak instalacji ogrzewania podłogowego."} 
    {"Podłoże wymaga wyrównania masą samorozlewną." if needs_levelling == "TAK" else ""}
    {"Stwierdzono spękania klawiszujące w ilości " + str(cracks_meters) + " mb." if cracks == "TAK" else ""}
    
    **b) Badanie wytrzymałości:** Próba rysikiem: {"Pozytywna" if strength >= 4 else "Dostateczna" if strength == 3 else "Negatywna"}.
    
    **c) Badanie wilgotności podłoża:** Wynik pomiaru: **{moisture}% CM**.  
    Status: {"POZYTYWNY" if (moisture <= 1.8 and heating_exists == "NIE") or (moisture <= 1.5 and heating_exists == "TAK") else "NEGATYWNY (Wymagana bariera)"}
    
    **d) Warunki otoczenia:** Temperatura: {temp}°C | Wilgotność: {humidity}% | Wentylacja: {ventilation}
    
    ---
    **II. Zalecenia techniczne**
    
    Biorąc pod uwagę wyniki badań, zaleca się:
    
    **1. Przygotowanie podłoża:** * Szlifowanie podłoża w celu usunięcia mleczka cementowego i otwarcia porów. Dokładne odkurzenie.
    """
    
    # Dynamiczne zalecenia produktowe
    if cracks == "TAK":
        protokol_text += "\n    * **Naprawa spękań:** Zastosować żywicę laną **WAKOL PS 205** oraz klamry stalowe."
    
    if (substrate == "Cementowy" and moisture > 1.8) or (heating_exists == "TAK" and moisture > 1.5):
        protokol_text += "\n    * **Bariera odcinająca:** Obowiązkowo 2 warstwy **WAKOL PU 280**."
    else:
        protokol_text += "\n    * **Gruntowanie:** Zastosować **WAKOL D 3004**."

    if needs_levelling == "TAK":
        protokol_text += f"\n    * **Wyrównanie:** Masa szpachlowa **WAKOL Z 615** (grubość {thickness} mm)."

    protokol_text += """
    
    **2. Klejenie:** * Do montażu okładziny użyć kleju silanowego **WAKOL MS 230** lub **WAKOL MS 260**.
    
    ---
    **Podstawa zaleceń:** Stosowanie produktów WAKOL w podanej kolejności zgodnie z kartami technicznymi i normami rzemiosła.
    """
    
    st.info(protokol_text)
    
    # Przycisk do pobrania (opcjonalnie jako tekst)
    st.download_button("Pobierz tekst protokołu", protokol_text, file_name=f"Protokol_{miejscowosc}.txt")
