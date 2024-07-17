import streamlit as st
import pandas as pd 
import time

df = pd.read_csv('nutrition_table.csv')
# df = df[['Categoria', 'Alimento (100 g)', 'Carboidratos (g)', 'Proteínas (g)',
#        'Gorduras (g)', 'Índice Glicêmico', 'Calorias (kcal)']]

st.title("Calculo de Refeição")
if 'clicked' not in st.session_state:
        st.session_state.clicked = False
def click_button():
    st.session_state.clicked = True
peso = st.sidebar.number_input(label="Peso do paciente", value=70, key="peso")

fator_correcao = st.sidebar.number_input(label="Fator de correção", value=1.0, step=0.1, key="fator_correcao")

st.selectbox("Busque alimento", df["Alimento (100 g)"], index=None, key="alimento_escolhido")

quantidade = st.number_input(label="Quantidade (g)", value=100, key="quantidade")

if 'refeicao' not in st.session_state:
    refeicao = pd.DataFrame(
            columns=["Alimento", "Quantidade (g)", "Carboidratos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina UI"]
        )
    st.session_state.refeicao = refeicao

final_df = pd.DataFrame(
            columns=["Alimento", "Quantidade (g)", "Carboidratos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina UI"]
        )
if st.button('Adicionar Alimento'):
    st.session_state.clicked = False
    if st.session_state.quantidade <= 0:
        st.warning("Quantidade deve ser maior que 0", icon="⚠️")
    if st.session_state.alimento_escolhido is None:
        st.warning(f"Escolha um alimento", icon="⚠️")
    else:
        alimento_infos = df[df["Alimento (100 g)"] == st.session_state.alimento_escolhido]
        new_row = {
            "Alimento": alimento_infos['Alimento (100 g)'],
            "Quantidade (g)": st.session_state.quantidade,
            "Carboidratos (g)": alimento_infos['Carboidratos (g)'] * st.session_state.quantidade/100,
            "Proteínas (g)": alimento_infos['Proteínas (g)'] * st.session_state.quantidade/100,
            "Gorduras (g)": alimento_infos['Gorduras (g)'] * st.session_state.quantidade/100,
            "Calorias (kcal)": alimento_infos['Calorias (kcal)'] * st.session_state.quantidade/100,
            "Insulina UI": peso * (alimento_infos['Carboidratos (g)']/10 + alimento_infos['Proteínas (g)']/50 + alimento_infos['Gorduras (g)']/100) * fator_correcao/70 * st.session_state.quantidade/100
        }
        st.session_state.refeicao = pd.concat([st.session_state.refeicao, pd.DataFrame(new_row)], ignore_index=True)
        final_df = st.session_state.refeicao.copy()
        soma = [{
            "Alimento": 'Total',
            "Quantidade (g)": sum(final_df['Quantidade (g)']),
            "Carboidratos (g)": sum(final_df['Carboidratos (g)']),
            "Proteínas (g)": sum(final_df['Proteínas (g)']),
            "Gorduras (g)": sum(final_df['Gorduras (g)']),
            "Calorias (kcal)": sum(final_df['Calorias (kcal)']),
            "Insulina UI": sum(final_df['Insulina UI'])
        }]
        final_df = pd.concat([final_df, pd.DataFrame(soma)], ignore_index=True)
st.subheader("Refeição")
st.dataframe(final_df, hide_index=True, use_container_width=True, on_select="ignore")



if len(final_df) > 0:
    st.button('Nova refeição', on_click=click_button)

if st.session_state.clicked:
    refeicao = pd.DataFrame(
            columns=["Alimento", "Quantidade (g)", "Carboidratos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina UI"]
        )
    st.session_state.refeicao = refeicao
# text_search = st.text_input("Busque alimentos", value="")
# alimento_processed = df["Alimento (100 g)"].str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8').str.lower()
# m1 = alimento_processed.str.contains(str.lower(text_search))
# df_search = df[m1]

# N_cards_per_row = 3
# if text_search:

#     for n_row, row in df_search.reset_index().iterrows():
#         i = n_row%N_cards_per_row
#         if i==0:
#             st.write("---")
#             cols = st.columns(N_cards_per_row, gap="large")
#         # draw the card
#         with cols[n_row%N_cards_per_row]:
#             st.caption(f"{row['Categoria'].strip()} ")
#             st.markdown(f"**{row['Alimento (100 g)'].strip()}**")
#             st.markdown(f"*{row['Calorias (kcal)']}*")
#             # st.markdown(f"**{row['Video']}**")



st.header("Tabela Nutricional")
event = st.dataframe(df.astype(str), selection_mode="single-row", hide_index=True, on_select="rerun",use_container_width=True,)

# meal_df = pd.DataFrame(
#             columns=["Alimento", "Quantidade (g)", "Carboidratos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina UI"]
#         )
# if 'meal_df' not in st.session_state:
#     st.session_state.meal_df = meal_df



# if st.button('Adicionar Alimento'):
#     alimento_infos = df.iloc[event.selection.rows]
#     new_row = {
#         "Alimento": alimento_infos['Alimento (100 g)'],
#         "Quantidade (g)": quantidade,
#         "Carboidratos (g)": alimento_infos['Carboidratos (g)'] * quantidade/100,
#         "Proteínas (g)": alimento_infos['Proteínas (g)'] * quantidade/100,
#         "Gorduras (g)": alimento_infos['Gorduras (g)'] * quantidade/100,
#         "Calorias (kcal)": alimento_infos['Calorias (kcal)'] * quantidade/100,
#         "Insulina UI": peso * (alimento_infos['Carboidratos (g)']/10 + alimento_infos['Proteínas (g)']/50 + alimento_infos['Gorduras (g)']/100) * fator_correcao/70 * quantidade/100
#     }
#     st.session_state.meal_df = pd.concat([st.session_state.meal_df, pd.DataFrame(new_row)], ignore_index=True)
#     final_df = st.session_state.meal_df.copy()
#     soma = [{
#         "Alimento": 'SOMA',
#         "Quantidade (g)": sum(final_df['Quantidade (g)']),
#         "Carboidratos (g)": sum(final_df['Carboidratos (g)']),
#         "Proteínas (g)": sum(final_df['Proteínas (g)']),
#         "Gorduras (g)": sum(final_df['Gorduras (g)']),
#         "Calorias (kcal)": sum(final_df['Calorias (kcal)']),
#         "Insulina UI": sum(final_df['Insulina UI'])
#     }]
#     final_df = pd.concat([final_df, pd.DataFrame(soma)], ignore_index=True)
#     st.dataframe(final_df, hide_index=True, use_container_width=True )

#     if st.button('Nova Refeição'):
#         meal_df = pd.DataFrame(
#                 columns=["Alimento", "Quantidade (g)", "Carboidratos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina UI"]
#             )
#         st.session_state.meal_df = meal_df

