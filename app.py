import streamlit as st

# Konfiguracja wizualna
st.set_page_config(page_title="Kalkulator WAKOL", page_icon="🔥", layout="centered")

# Stylizacja dla lepszej widoczności na telefonie
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 System WAKOL")
st.subheader("Kalkulator do Ogrzewania Bruzdowanego")

# Sekcja wprowadzania danych
with st.container():
    st.write("### Parametry Inwestycji")
    metraz = st.number_input("Metraż powierzchni ($m^2$):", min_value=1.0, value=100.0, step=1.0)
    
    stan = st.selectbox(
        "Czy rurki są już zaszpachlowane?",
        options=["NIE - rurki na wierzchu", "TAK - rurki zaszpachlowane"]
    )

# --- LOGIKA TECHNOLOGICZNA ---
grunt_n = 0.075
siatka_n = 1.0
z635_n = 7.5

if "NIE" in stan:
    z645_n = 4.5  # 2.5 (bruzdy) + 2.0 (zatopienie siatki)
    opis = "PEŁNA TECHNOLOGIA (Bruzdy + Siatka + Wylewka)"
else:
    z645_n = 2.0  # Tylko zatopienie siatki
    opis = "ZBROJENIE I WYGŁADZENIE (Siatka + Wylewka)"

z645_total = metraz * z645_n
d3060_total = z645_total / 3.6

# --- WYŚWIETLANIE WYNIKÓW ---
st.divider()
st.info(f"📋 **Zestawienie dla: {metraz} $m^2$**\n\nStatus: {opis}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Grunt D 3004", f"{metraz * grunt_n:.2f} kg")
    st.metric("Siatka AR 150", f"{metraz * siatka_n:.0f} m²")
    st.metric("Plastyfikator D 3060", f"{d3060_total:.2f} kg")

with col2:
    st.metric("Masa Z 645", f"{z645_total:.2f} kg")
    st.caption(f"Potrzeba: {z645_total/25:.1f} worków")
    st.metric("Wylewka Z 635", f"{metraz * z635_n:.2f} kg")
    st.caption(f"Potrzeba: {(metraz * z635_n)/25:.1f} worków")

st.divider()
st.success(f"💡 **Pamiętaj:** Mieszaj masę Z 645 z plastyfikatorem D 3060 w proporcji **1:3.6**.")
