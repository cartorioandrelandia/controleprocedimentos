import streamlit as st
from datetime import date
from supabase import create_client, Client

# 1) Conexão Supabase (crie projeto e pegue URL e KEY)
SUPABASE_URL  = st.secrets["SUPABASE_URL"]
SUPABASE_KEY  = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📋 Controle de Procedimentos")

# 2) Formulário
with st.form("form_procedimento", clear_on_submit=False):
    num_tombo        = st.text_input("Número Tombo")
    tipo_proc        = st.text_input("Tipo de Procedimento")
    data_autuacao    = st.date_input("Data da Autuação", date.today())
    data_portaria    = st.date_input("Data da Portaria / Despacho")
    num_processo     = st.text_input("Nº Processo")
    num_pcnet        = st.text_input("Nº Pcnet")
    cidade           = st.text_input("Cidade")
    tipificacao      = st.text_input("Tipificação")
    data_prazo       = st.date_input("Data do Prazo")
    prazo_em_dias    = st.number_input("Prazo em Dias", min_value=0, value=0)

    reds_text         = st.text_area("Nº Reds (vírgula)", help="Ex: 123, 456, 789")
    inv_text          = st.text_area("Investigados (vírgula)")
    vit_text          = st.text_area("Vítimas (vírgula)")

    submitted = st.form_submit_button("💾 Salvar Procedimento")
    if submitted:
        # 3) Insere no Supabase tabela "procedimentos"
        proc = supabase.table("procedimentos").insert({
            "numero_tombo":      num_tombo,
            "tipo_procedimento": tipo_proc,
            "data_autuacao":     data_autuacao.isoformat(),
            "data_portaria":     data_portaria.isoformat(),
            "num_processo":      num_processo,
            "num_pcnet":         num_pcnet,
            "cidade":            cidade,
            "tipificacao":       tipificacao,
            "data_prazo":        data_prazo.isoformat(),
            "prazo_em_dias":     int(prazo_em_dias),
        }).execute().data[0]

        proc_id = proc["id"]

        # 4) Helper para multi-valor
        def create_multi(text, table_name, col_name):
            for val in [v.strip() for v in text.split(",") if v.strip()]:
                supabase.table(table_name).insert({
                    col_name: val,
                    "procedimento_id": proc_id
                }).execute()

        create_multi(reds_text,        "reds",         "numero_red")
        create_multi(inv_text,         "investigados", "nome")
        create_multi(vit_text,         "vitimas",      "nome")

        st.success("✅ Procedimento salvo com sucesso!")
