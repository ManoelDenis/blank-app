
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
from io import StringIO

# Autenticação com Google Sheets via st.secrets
def conectar_google_sheets(nome_planilha):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Converte AttrDict para dict antes de serializar
    cred_dict = dict(st.secrets["google_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(nome_planilha).sheet1
    return sheet

# Perguntas do formulário
def formulario():
    st.title("Avaliação da Disciplina – Resistência dos Materiais I")
    st.write("**Objetivo:** Avaliar a percepção dos(as) estudantes sobre a disciplina, visando melhorias.")

    respostas = {}

    def pergunta(titulo, questao, opcoes):
        st.markdown(f"### {titulo}")
        respostas[titulo] = st.radio(questao, opcoes, horizontal=True)
        respostas[f"{titulo} - Comentário"] = st.text_input("Comentário (opcional):", key=titulo)

    pergunta("1. Organização", "Como você avalia a organização da disciplina?", ["Excelente", "Boa", "Regular", "Ruim", "Péssima"])
    pergunta("2. Clareza", "Como você avalia a clareza das explicações?", ["Muito clara", "Clara", "Razoável", "Pouco clara", "Confusa"])
    pergunta("3. Materiais", "Como avalia os materiais (slides, exercícios etc.)?", ["Muito úteis", "Úteis", "Pouco úteis", "Inúteis", "Não utilizei"])
    pergunta("4. Teoria e prática", "A disciplina relacionou bem teoria e prática?", ["Sim, totalmente", "Parcialmente", "Pouco", "Não"])
    pergunta("5. Participação", "Você se sentiu estimulado(a) a participar?", ["Sempre", "Na maioria das vezes", "Às vezes", "Raramente", "Nunca"])
    pergunta("6. Dificuldade", "Como avalia o nível de dificuldade?", ["Muito difícil", "Difícil", "Moderado", "Fácil", "Muito fácil"])
    pergunta("7. Aprendizado", "Você aprendeu os conteúdos essenciais?", ["Sim, bastante", "O necessário", "Pouco", "Não aprendi"])
    pergunta("8. Avaliações", "Como avalia os instrumentos de avaliação?", ["Justos e coerentes", "Um pouco difíceis", "Mal elaborados", "Não opino"])
    pergunta("9. Professor(a)", "Como avalia a didática e disponibilidade do(a) professor(a)?", ["Excelente", "Boa", "Regular", "Ruim", "Péssima"])

    st.markdown("### 10. Comentários Finais")
    respostas["10. Comentários Finais"] = st.text_area("Sugestões, críticas ou elogios (opcional):")

    if st.button("Enviar respostas"):
        try:
            sheet = conectar_google_sheets("Avaliacao_RMI")
            data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + list(respostas.values())
            sheet.append_row(data)
            st.success("Respostas enviadas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")

# Rodar o app
if __name__ == "__main__":
    formulario()
