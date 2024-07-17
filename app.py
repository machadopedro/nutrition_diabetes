import streamlit as st
import pandas as pd 
import time

df = pd.read_csv('nutrition_table.csv')
# df = df[['Categoria', 'Alimento (100 g)', 'Carboidratos (g)', 'Proteínas (g)',
#        'Gorduras (g)', 'Índice Glicêmico', 'Calorias (kcal)']]

st.title("Calculo de Refeição")


peso = st.number_input(label="Peso")

fator_correcao = st.number_input(label="Fator de correção")

event = st.dataframe(df.astype(str), selection_mode="single-row", hide_index=True, on_select="rerun",use_container_width=True,)

meal_df = pd.DataFrame(
            columns=["Alimento", "Quantidade (g)", "Carboidratos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina UI"]
        )
if 'meal_df' not in st.session_state:
    st.session_state.meal_df = meal_df

quantidade = st.number_input(label="Quantidade")

if st.button('Adicionar Alimento'):
    alimento_infos = df.iloc[event.selection.rows]
    new_row = {
        "Alimento": alimento_infos['Alimento (100 g)'],
        "Quantidade (g)": quantidade,
        "Carboidratos (g)": alimento_infos['Carboidratos (g)'] * quantidade/100,
        "Proteínas (g)": alimento_infos['Proteínas (g)'] * quantidade/100,
        "Gorduras (g)": alimento_infos['Gorduras (g)'] * quantidade/100,
        "Calorias (kcal)": alimento_infos['Calorias (kcal)'] * quantidade/100,
        "Insulina UI": peso * (alimento_infos['Carboidratos (g)']/10 + alimento_infos['Proteínas (g)']/50 + alimento_infos['Gorduras (g)']/100) * fator_correcao/70 * quantidade/100
    }
    st.session_state.meal_df = pd.concat([st.session_state.meal_df, pd.DataFrame(new_row)], ignore_index=True)
    final_df = st.session_state.meal_df.copy()
    soma = [{
        "Alimento": 'SOMA',
        "Quantidade (g)": sum(final_df['Quantidade (g)']),
        "Carboidratos (g)": sum(final_df['Carboidratos (g)']),
        "Proteínas (g)": sum(final_df['Proteínas (g)']),
        "Gorduras (g)": sum(final_df['Gorduras (g)']),
        "Calorias (kcal)": sum(final_df['Calorias (kcal)']),
        "Insulina UI": sum(final_df['Insulina UI'])
    }]
    final_df = pd.concat([final_df, pd.DataFrame(soma)], ignore_index=True)
    st.dataframe(final_df, hide_index=True, use_container_width=True )

    if st.button('Nova Refeição'):
        meal_df = pd.DataFrame(
                columns=["Alimento", "Quantidade (g)", "Carboidratos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina UI"]
            )
        st.session_state.meal_df = meal_df

