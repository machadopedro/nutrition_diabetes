import streamlit as st
import pandas as pd 
import time

st.set_page_config(layout="wide")
df = pd.read_csv('nutrition_table.csv')

st.title("Calculo de Refeição")
def nova_refeicao():
    if 'refeicao_lista' not in st.session_state:
        st.session_state.refeicao_lista = []
    st.session_state.refeicao_lista.append(st.session_state.refeicao)
    if 'refeicao_summary_lista' not in st.session_state:
        st.session_state.refeicao_summary_lista = []
    total_refeicao = st.session_state.refeicao[st.session_state.refeicao['Alimento'] == 'Total']
    refeicao_summary = {
        'Horário': time.strftime("%H:%M"),
        'Quantidade (g)': total_refeicao['Quantidade (g)'].values[0],
        'Carboidratos líquidos (g)': total_refeicao['Carboidratos líquidos (g)'].values[0],
        'Proteínas (g)': total_refeicao['Proteínas (g)'].values[0],
        'Gorduras (g)': total_refeicao['Gorduras (g)'].values[0],
        'Calorias (kcal)': total_refeicao['Calorias (kcal)'].values[0],
        'Insulina (UI)': total_refeicao['Insulina (UI)'].values[0]
    }
    st.session_state.refeicao_summary_lista.append(refeicao_summary)
    refeicao = pd.DataFrame(
            columns=["Alimento", "Quantidade (g)", "Carboidratos líquidos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina (UI)"]
        )
    st.session_state.refeicao = refeicao

def remove_refeicao():
    st.session_state.refeicao_summary_lista.pop(st.session_state.check_meal['selection']['rows'][0])
    st.session_state.refeicao_lista.pop(st.session_state.check_meal['selection']['rows'][0])

def update_refeicao():
    st.session_state.refeicao['Insulina (UI)'] = st.session_state.peso * (st.session_state.refeicao['Carboidratos líquidos (g)']/10 + st.session_state.refeicao['Proteínas (g)']/50 + st.session_state.refeicao['Gorduras (g)']/100) * st.session_state.fator_correcao/70 * st.session_state.quantidade/100
peso = st.sidebar.number_input(label="Peso do paciente", value=70, key="peso", on_change=update_refeicao)

fator_correcao = st.sidebar.number_input(label="Fator de correção", value=1.0, step=0.1, key="fator_correcao", on_change=update_refeicao)

st.selectbox("Busque alimento", df["Alimento (100 g)"], index=None, key="alimento_escolhido")

st.number_input(label="Quantidade (g)", value=100, step=10, key="quantidade")

if 'refeicao' not in st.session_state:
    refeicao = pd.DataFrame(
            columns=["Alimento", "Quantidade (g)", "Carboidratos líquidos (g)", "Proteínas (g)", "Gorduras (g)", "Calorias (kcal)", "Insulina (UI)"]
        )
    st.session_state.refeicao = refeicao

if st.button('Adicionar Alimento'):
    if st.session_state.quantidade <= 0:
        st.warning("Quantidade deve ser maior que 0", icon="⚠️")
    if st.session_state.alimento_escolhido is None:
        st.warning(f"Escolha um alimento", icon="⚠️")
    else:
        alimento_infos = df[df["Alimento (100 g)"] == st.session_state.alimento_escolhido]
        new_row = {
            "Alimento": alimento_infos['Alimento (100 g)'],
            "Quantidade (g)": st.session_state.quantidade,
            "Carboidratos líquidos (g)": alimento_infos['Carboidratos líquidos (g)'] * st.session_state.quantidade/100,
            "Proteínas (g)": alimento_infos['Proteínas (g)'] * st.session_state.quantidade/100,
            "Gorduras (g)": alimento_infos['Gorduras (g)'] * st.session_state.quantidade/100,
            "Calorias (kcal)": alimento_infos['Calorias (kcal)'] * st.session_state.quantidade/100,
            "Insulina (UI)": st.session_state.peso * (alimento_infos['Carboidratos líquidos (g)']/10 + alimento_infos['Proteínas (g)']/50 + alimento_infos['Gorduras (g)']/100) * st.session_state.fator_correcao/70 * st.session_state.quantidade/100
        }
        # Remove the 'Total' row if it exists
        if 'Total' in st.session_state.refeicao['Alimento'].values:
            st.session_state.refeicao = st.session_state.refeicao[st.session_state.refeicao['Alimento'] != 'Total']

        if len(st.session_state.refeicao) > 0 and new_row["Alimento"].values[0] in st.session_state.refeicao["Alimento"].values:
            matching_index = st.session_state.refeicao[st.session_state.refeicao["Alimento"] == new_row["Alimento"].values[0]].index[0]

            # Update the values using the matching index
            st.session_state.refeicao.loc[matching_index, "Quantidade (g)"] += st.session_state.quantidade
            st.session_state.refeicao.loc[matching_index, "Carboidratos líquidos (g)"] += new_row["Carboidratos líquidos (g)"].values[0]  # Access the value directly
            st.session_state.refeicao.loc[matching_index, "Proteínas (g)"] += new_row["Proteínas (g)"].values[0]
            st.session_state.refeicao.loc[matching_index, "Gorduras (g)"] += new_row["Gorduras (g)"].values[0]
            st.session_state.refeicao.loc[matching_index, "Calorias (kcal)"] += new_row["Calorias (kcal)"].values[0]
            st.session_state.refeicao.loc[matching_index, "Insulina (UI)"] += new_row["Insulina (UI)"].values[0]
        else:
            st.session_state.refeicao = pd.concat([st.session_state.refeicao, pd.DataFrame(new_row)], ignore_index=True)

        soma = [{
            "Alimento": "Total",
            "Quantidade (g)": sum(st.session_state.refeicao['Quantidade (g)']),
            "Carboidratos líquidos (g)": sum(st.session_state.refeicao['Carboidratos líquidos (g)']),
            "Proteínas (g)": sum(st.session_state.refeicao['Proteínas (g)']),
            "Gorduras (g)": sum(st.session_state.refeicao['Gorduras (g)']),
            "Calorias (kcal)": sum(st.session_state.refeicao['Calorias (kcal)']),
            "Insulina (UI)": sum(st.session_state.refeicao['Insulina (UI)'])
        }]
        # st.session_state.refeicao.loc['Total']= st.session_state.refeicao.sum(numeric_only=True, axis=0)
        st.session_state.refeicao = pd.concat([st.session_state.refeicao, pd.DataFrame(soma)], ignore_index=True)
        # st.data_editor(st.session_state.refeicao)
st.subheader("Refeição")

def update():
    alimento_editado_index = list(st.session_state.editor['edited_rows'].keys())[0]
    alimento_nome = st.session_state.refeicao.iloc[alimento_editado_index, 0]  # Get the food name from the edited row
    alimento_infos = df[df["Alimento (100 g)"] == alimento_nome]  # Compare against the food name
    quantidade = st.session_state.editor['edited_rows'][alimento_editado_index]["Quantidade (g)"]
    st.session_state.refeicao.loc[alimento_editado_index, "Carboidratos líquidos (g)"] = alimento_infos['Carboidratos líquidos (g)'].values[0] * quantidade/100
    st.session_state.refeicao.loc[alimento_editado_index, "Proteínas (g)"] = alimento_infos['Proteínas (g)'].values[0] * quantidade/100
    st.session_state.refeicao.loc[alimento_editado_index, "Gorduras (g)"] = alimento_infos['Gorduras (g)'].values[0] * quantidade/100
    st.session_state.refeicao.loc[alimento_editado_index, "Calorias (kcal)"] = alimento_infos['Calorias (kcal)'].values[0] * quantidade/100
    st.session_state.refeicao.loc[alimento_editado_index, "Insulina (UI)"] = st.session_state.peso * (alimento_infos['Carboidratos líquidos (g)'].values[0]/10 + alimento_infos['Proteínas (g)'].values[0]/50 + alimento_infos['Gorduras (g)'].values[0]/100) * st.session_state.fator_correcao/70 * quantidade/100
    st.session_state.refeicao.loc[alimento_editado_index, "Quantidade (g)"] = quantidade
    # Remove the 'Total' row if it exists
    if 'Total' in st.session_state.refeicao['Alimento'].values:
        st.session_state.refeicao = st.session_state.refeicao[st.session_state.refeicao['Alimento'] != 'Total']
    soma = [{
            "Alimento": 'Total',
            "Quantidade (g)": sum(st.session_state.refeicao['Quantidade (g)']),
            "Carboidratos líquidos (g)": sum(st.session_state.refeicao['Carboidratos líquidos (g)']),
            "Proteínas (g)": sum(st.session_state.refeicao['Proteínas (g)']),
            "Gorduras (g)": sum(st.session_state.refeicao['Gorduras (g)']),
            "Calorias (kcal)": sum(st.session_state.refeicao['Calorias (kcal)']),
            "Insulina (UI)": sum(st.session_state.refeicao['Insulina (UI)'])
        }]
        # st.session_state.refeicao.loc['Total']= st.session_state.refeicao.sum(numeric_only=True, axis=0)
    st.session_state.refeicao = pd.concat([st.session_state.refeicao, pd.DataFrame(soma)], ignore_index=True)
columns = list(st.session_state.refeicao.columns)
columns.remove('Quantidade (g)')

st.data_editor(st.session_state.refeicao, hide_index=True, key='editor', on_change=update, use_container_width=True, disabled=set(columns))

if len(st.session_state.refeicao) > 0:
    st.button('Nova refeição', on_click=nova_refeicao)


if ('refeicao_summary_lista' in st.session_state) and len(st.session_state.refeicao_summary_lista) > 0:
    st.subheader("Historico de refeições")
    check_meal = st.dataframe(pd.DataFrame(st.session_state.refeicao_summary_lista), key='check_meal', hide_index=True, use_container_width=True, selection_mode='single-row', on_select='rerun')

    if len(check_meal['selection']['rows']) > 0:
        st.markdown("**Detalhes**")
        st.dataframe(pd.DataFrame(st.session_state.refeicao_lista[check_meal['selection']['rows'][0]]), hide_index=True, use_container_width=True)
        st.button("Remover", type="primary", on_click=remove_refeicao)
        

st.header("Tabela Nutricional")
event = st.dataframe(df.astype(str), hide_index=True, use_container_width=True,)
