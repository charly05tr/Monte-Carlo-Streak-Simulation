"""
Interfaz web (Streamlit) para la simulación Monte Carlo de rachas.

Ejecutar con:  streamlit run app.py
"""

import altair as alt
import pandas as pd
import streamlit as st

from simulacion import simulacion_monte_carlo_continuo, valor_esperado_teorico

st.set_page_config(page_title="Monte Carlo: rachas de caras", layout="wide")
st.title("Simulación Monte Carlo: rachas de caras")
st.caption("¿Cuántos lanzamientos de moneda hacen falta para obtener N caras seguidas?")

with st.sidebar:
    st.header("Parámetros")
    largo_racha = st.slider("Caras seguidas (N)", min_value=1, max_value=16, value=12)
    num_simulaciones = st.number_input(
        "Número de simulaciones", min_value=1, max_value=100_000, value=2_000, step=500
    )
    usar_semilla = st.checkbox("Usar semilla fija (reproducible)")
    semilla = st.number_input("Semilla", value=42, step=1) if usar_semilla else None
    st.info(f"Valor teórico esperado: **{valor_esperado_teorico(largo_racha):,}** lanzamientos")
    ejecutar = st.button("Ejecutar simulación", type="primary", use_container_width=True)

if ejecutar:
    barra = st.progress(0.0, text="Simulando...")
    resultado = simulacion_monte_carlo_continuo(
        num_simulaciones=int(num_simulaciones),
        largo_racha=largo_racha,
        semilla=int(semilla) if semilla is not None else None,
        al_progresar=lambda hechas, total: barra.progress(
            hechas / total, text=f"Simulando... {hechas:,}/{total:,}"
        ),
    )
    barra.empty()
    st.session_state["resultado"] = resultado

resultado = st.session_state.get("resultado")

if resultado is None:
    st.write("Configurá los parámetros y presioná **Ejecutar simulación**.")
    st.stop()

error = (resultado.promedio - resultado.teorico) / resultado.teorico * 100

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Promedio simulado", f"{resultado.promedio:,.2f}", f"{error:+.2f}% vs teórico", delta_color="off")
c2.metric("Valor teórico", f"{resultado.teorico:,}")
c3.metric("Mediana", f"{resultado.mediana:,.0f}")
c4.metric("Mínimo", f"{resultado.minimo:,}")
c5.metric("Máximo", f"{resultado.maximo:,}")

df = pd.DataFrame(
    {
        "simulacion": range(1, len(resultado.lanzamientos) + 1),
        "lanzamientos": resultado.lanzamientos,
        "promedio_acumulado": resultado.promedios_acumulados(),
    }
)
linea_teorica = alt.Chart(pd.DataFrame({"teorico": [resultado.teorico]})).mark_rule(
    color="red", strokeDash=[6, 4]
)

col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Distribución de lanzamientos necesarios")
    histograma = (
        alt.Chart(df)
        .mark_bar(opacity=0.8)
        .encode(
            x=alt.X("lanzamientos:Q", bin=alt.Bin(maxbins=50), title="Lanzamientos"),
            y=alt.Y("count():Q", title="Frecuencia"),
            tooltip=[alt.Tooltip("count():Q", title="Frecuencia")],
        )
    )
    st.altair_chart(histograma + linea_teorica.encode(x="teorico:Q"), use_container_width=True)

with col_der:
    st.subheader("Convergencia del promedio")
    convergencia = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("simulacion:Q", title="Simulación"),
            y=alt.Y("promedio_acumulado:Q", title="Promedio acumulado"),
            tooltip=["simulacion", alt.Tooltip("promedio_acumulado:Q", format=",.2f")],
        )
    )
    st.altair_chart(convergencia + linea_teorica.encode(y="teorico:Q"), use_container_width=True)

st.caption("La línea roja punteada marca el valor teórico 2^(N+1) − 2.")

with st.expander("Ver datos crudos"):
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("Descargar CSV", df.to_csv(index=False), "resultados.csv", "text/csv")
