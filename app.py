import streamlit as st

# Konfiguracja
st.set_page_config(page_title="Kalkulator WAKOL", layout="centered")

st.title("🏗️ System WAKOL")
st.write("Kalkulator materiałowy dla ogrzewania bruzdowanego.")

# WPROWADZANIE DANYCH
metraz = st.number_input("Wpisz metraż (m2):", min_value=1.0, value=100.0)

stan = st.radio(
    "Czy rurki są już zaszpachlowane?",
    ["NIE - rurki na wierzchu", "TAK - bruzdy pełne"]
)

# OBLICZENIA (Wymuszone wartości)
grunt_n = 0.075
siatka_n = 1.0
z635_n = 7.5

# Sprawdzamy wybór użytkownika
if "NIE" in stan:
    z645_n = 4.5  # 2.5 bruzdy + 2.0 siatka
    opis_stanu = "Pełna technologia"
else:
    z645_n = 2.0  # Tylko siatka
    opis_stanu = "Proces uproszczony"

# Wyniki końcowe
total_grunt = metraz * grunt_n
total_siatka = metraz * siatka_n
total_z645 = metraz * z645_n
total_d3060 = total_z645 / 3.6
total_z635 = metraz * z635_n

# WYŚWIETLANIE (Używamy kolumn, aby wyniki nie były puste)
st.divider()
st.subheader(f"Wyniki dla {metraz} m²")

# Wyświetlamy wyniki w formie czytelnych kart
c1, c2 = st.columns(2)
with c1:
    st.metric("D 3004 (Grunt)", f"{total_grunt:.2f} kg")
    st.metric("AR 150 (Siatka)", f"{total_siatka:.0f} m2")
    st.metric("D 3060 (Plastyfikator)", f"{total_d3060:.2f} kg")

with c2:
    st.metric("Z 645 (Masa)", f"{total_z645:.2f} kg")
    st.write(f"({total_z645/25:.1f} worków)")
    st.metric("Z 635 (Wylewka)", f"{total_z635:.2f} kg")
    st.write(f"({total_z635/25:.1f} worków)")

st.success(f"Status: {opis_stanu}")
