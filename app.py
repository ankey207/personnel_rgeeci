import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Personnels RGEE-CI",layout="wide", initial_sidebar_state="auto", page_icon="logo_rgeeci.jpg")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def show_photo_agent(path):
    try:
        file_ = open(f"photos/{path}.jpg", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        return data_url
    except:
        file_ = open(f"identite.jpg", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        return data_url



def show_logo(path):
    file_ = open(f"{path}", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    return data_url

path_logo_ins ="ins_logo.jpg"
path_logo_rgeeci = "logo_rgeeci.jpg"


# Charger les données depuis le fichier Excel
@st.cache_data
def load_data():
    df = pd.read_excel('agents.xlsx', dtype={'matricule': str})
    return df

data = load_data()

# Obtenir les paramètres de l'URL
query_params = st.query_params

# Obtenir le matricule depuis les paramètres de l'URL
matricule = query_params.get("matricule", [None])

if matricule:
    try:
        student_info = data[data['matricule'] == matricule]
        if not student_info.empty:
            nom = student_info['name'].values[0]
            prenoms = student_info['last_name'].values[0]
            sexe = student_info['sexe'].values[0]
            contact = student_info['contact1'].values[0]
            zone_travail = student_info['Zone de travail'].values[0]
            photo_path = f"photos/{student_info['matricule'].values[0]}.jpg"  # Assuming photo filenames match matricule

            code = f'''
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Carte Agent Recenseur</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background: linear-gradient(to right, #f0e6d1, #e2f0e6);
                    }}
                    .card {{
                        width: 500px;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
                        text-align: center;
                        background: linear-gradient(to right, #f0e6d1, #e2f0e6);
                    }}
                    .header, .footer {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .header img, .footer img {{
                        width: 100px;
                    }}
                    .title {{
                        font-size: 14px;
                        font-weight: bold;
                        margin: 10px 0;
                    }}
                    .subtitle {{
                        font-size: 12px;
                        color: #333;
                    }}
                    .photo {{
                        margin: 20px 0;
                    }}
                    .photo img {{
                        width: 150px;
                        height: 200px;
                        object-fit: cover;
                        border-radius: 4px;
                    }}
                    .agent-info {{
                        font-size: 16px;
                        font-weight: bold;
                        color: green;
                    }}
                    .agent-name {{
                        font-size: 20px;
                        color: orange;
                        font-weight: bold;
                    }}
                    .agent-matricule {{
                        font-size: 16px;
                        color: orange;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="header">
                        <img src="data:image/png;base64,{show_logo(path_logo_ins)}" alt="Logo Institut National de la Statistique">
                        <img src="data:image/png;base64,{show_logo(path_logo_rgeeci)}" alt="Logo RGEECI">
                    </div>
                    <div class="title">RÉPUBLIQUE DE CÔTE D'IVOIRE</div>
                    <div class="subtitle">MINISTÈRE DE L'ÉCONOMIE, DU PLAN ET DU DÉVELOPPEMENT</div>
                    <div class="title">INSTITUT NATIONAL DE LA STATISTIQUE</div>
                    <h2 class="title">RECENSEMENT GÉNÉRAL DES ENTREPRISES ET ETABLISSEMENTS DE CÔTE D'IVOIRE 2024</h2>
                    <div class="photo">
                        <img src="data:image/png;base64,{show_photo_agent(matricule)}" alt="Photo Agent">
                    </div>
                    <div class="agent-info">AGENT RECENSEUR</div>
                    <div class="agent-name">{nom} {prenoms}</div>
                    <div class="agent-matricule">{matricule}</div>
                    <div class="agent-matricule">{contact}</div>
                    <div class="agent-matricule">{zone_travail}</div>

                </div>
            </body>
            </html>
            '''
            st.html(code)
        else:
            st.error("Matricule non trouvé.")
    except ValueError:
        st.error("Matricule invalide.")
else:
    st.write("Veuillez fournir un matricule dans l'URL.")
