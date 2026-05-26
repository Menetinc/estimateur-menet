import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. Configuration de la page
st.set_page_config(page_title="Ménet Inc. - Estimateur officiel", page_icon="🏢", layout="centered")

# --- STYLE CSS UNIFIÉ (FOND BLANC, BLEU ROYAL, NETTOYAGE DES INSTRUCTIONS) ---
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        .tab-button-active {
            display: flex; align-items: center; justify-content: center;
            width: 100%; height: 42px; background-color: #007bff; color: white !important;
            border: 1px solid #007bff; border-radius: 8px; font-weight: bold; font-family: sans-serif;
            box-shadow: 0 4px 6px rgba(0, 123, 255, 0.2);
        }
        /* Supprime définitivement la mention grise sous tous les champs des formulaires */
        div[data-testid="stForm"] [data-testid="InputInstructions"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE PRINCIPALE ---
st.markdown("<h2 style='text-align: center; color: #007bff; font-family: sans-serif; margin-bottom:0;'>MÉNET INC.</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6c757d; font-size: 1rem; margin-bottom: 25px;'>Solutions professionnelles d'entretien commercial et d'assemblage</p>", unsafe_allow_html=True)

# --- CONFIGURATION DU SYSTEME DE COURRIEL SÉCURISÉ ---
def envoyer_courriel_nettoyage(nom, courriel, tel, superficie, frequence, heures, prix, 
                              bureaux, toilettes, vestiaires, lavage, conferences, halls, 
                              escaliers, etages, cafeteria, gym, formation, lounge, allaitement, dechets, ascenseur, note_client):
    serveur_smtp = "smtp.hostinger.com"
    port_smtp = 465  
    expediteur = "contact@menet.ca"
    mot_de_passe = st.secrets["MOT_DE_PASSE_SMTP"]
    destinataire = "contact@menet.ca"

    message = MIMEMultipart()
    message["From"] = expediteur
    message["To"] = destinataire
    message["Subject"] = f"🚨 DEVIS NETTOYAGE COMMERCIAL - {nom}"

    corps = f"""
    Bonjour Omar,
    Une simulation de NETTOYAGE COMMERCIAL vient d'être effectuée.

    👥 CLIENT : {nom} | Courriel : {courriel} | Tél : {tel}
    📝 NOTE CLIENT : {note_client if note_client.strip() else "Aucune"}

    📐 CONFIGURATION :
    - Superficie : {superficie:,} pi² | Fréquence : {frequence}

    🔢 INVENTAIRE :
    - Bureaux : {bureaux} | Toilettes : {toilettes} | Vestiaires : {vestiaires}
    - Lavage mains : {lavage} | Conférences : {conferences} | Halls : {halls}
    - Escaliers : {escaliers} cage(s) sur {etages} étage(s)
    - Options : Cafétéria({cafeteria}), Gym({gym}), Formation({formation}), Lounge({lounge}), Allaitement({allaitement}), Déchets({dechets}), Ascenseur({ascenseur})

    🧠 OPÉRATIONS (SECRET) :
    - Temps requis : {heures:.2f} h / jour (Marge 20% incluse)
    - Tarif : 42.00 $ / h
    💰 PRIX MENSUEL SUGGÉRÉ : {prix:,.2f} $ CAD / mois (Plus taxes)
    """
    message.attach(MIMEText(corps, "plain", "utf-8"))
    try:
        server = smtplib.SMTP_SSL(serveur_smtp, port_smtp)
        server.login(expediteur, mot_de_passe)
        server.sendmail(expediteur, destinataire, message.as_string())
        server.close()
        return True
    except:
        return False

def envoyer_courriel_montage(nom, courriel, tel, type_montage, détails_meubles, prix_estimé, note_client, temps_total_h=0, cout_mo=0, frais_dep=0):
    serveur_smtp = "smtp.hostinger.com"
    port_smtp = 465  
    expediteur = "contact@menet.ca"
    mot_de_passe = st.secrets["MOT_DE_PASSE_SMTP"]
    destinataire = "contact@menet.ca"

    message = MIMEMultipart()
    message["From"] = expediteur
    message["To"] = destinataire
    message["Subject"] = f"🚨 DEVIS MONTAGE DE MEUBLES ({type_montage.upper()}) - {nom}"

    if type_montage == "Commercial":
        heures_texte = f"- Main-d'œuvre estimée : {temps_total_h:.2f} heures\n- Coût main-d'œuvre ({temps_total_h:.2f} h x 55$) : {cout_mo:.2f} $\n- Frais de déplacement fixe : {frais_dep:.2f} $"
    else:
        heures_texte = f"- Facturation : Prix fixes résidentiels\n- Note : Minimum de déplacement de 60$ appliqué si inférieur."

    corps = f"""
    Bonjour Omar,
    Une simulation de MONTAGE DE MEUBLES vient d'être effectuée.

    👥 CLIENT : {nom} | Courriel : {courriel} | Tél : {tel}
    📝 NOTE CLIENT : {note_client if note_client.strip() else "Aucune"}
    🛠️ TYPE DE MONTAGE : {type_montage}

    📦 INVENTAIRE DES MEUBLES :
    {détails_meubles}
    
    🧠 ANALYSE ET TARIFICATION (SECRET) :
    {heures_texte}

    💰 PRIX TOTAL SUGGÉRÉ : {prix_estimé:,.2f} $ CAD (Plus taxes)
    """
    message.attach(MIMEText(corps, "plain", "utf-8"))
    try:
        server = smtplib.SMTP_SSL(serveur_smtp, port_smtp)
        server.login(expediteur, mot_de_passe)
        server.sendmail(expediteur, destinataire, message.as_string())
        server.close()
        return True
    except:
        return False


# --- LOGIQUE DE SÉLECTION DES ONGLETS PRINCIPAUX ---
if "choix_service" not in st.session_state:
    st.session_state.choix_service = "nettoyage"

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.session_state.choix_service == "nettoyage":
        st.markdown('<div class="tab-button-active">🧹 Nettoyage Commercial</div>', unsafe_allow_html=True)
    else:
        if st.button("🧹 Nettoyage Commercial", use_container_width=True, key="btn_nettoie_tab"):
            st.session_state.choix_service = "nettoyage"
            st.rerun()
with col_btn2:
    if st.session_state.choix_service == "montage":
        st.markdown('<div class="tab-button-active">🔨 Montage de Meubles</div>', unsafe_allow_html=True)
    else:
        if st.button("🔨 Montage de Meubles", use_container_width=True, key="btn_montage_tab"):
            st.session_state.choix_service = "montage"
            st.rerun()

st.write("---")


# --- VUE 1 : FORMULAIRE NETTOYAGE COMMERCIAL ---
if st.session_state.choix_service == "nettoyage":
    st.markdown("<h3 style='color: #007bff; margin-top:0;'>🧹 Demande de Nettoyage Commercial</h3>", unsafe_allow_html=True)
    st.info("💡 Conseil : Laissez à 0 pour les zones inexistantes ou non incluses.")
    
    with st.form("form_nettoyage_complet"):
        st.markdown("#### 📐 Dimensions et Fréquence")
        c_dim1, c_dim2 = st.columns(2)
        with c_dim1:
            # Remis à 0 par défaut
            superficie = st.number_input("Superficie totale (en pieds carrés) :", min_value=0, value=0, step=100)
        with c_dim2:
            frequence_label = st.selectbox("Fréquence du nettoyage :", ["Hebdomadaire (1 jour / semaine)", "Bihebdomadaire (2 jours / semaine)", "3 jours / semaine", "4 jours / semaine", "5 jours / semaine", "6 jours / semaine", "7 jours / semaine (7/7)"])

        st.markdown("#### 🔢 Nombre de zones et d'équipements")
        cz1, cz2, cz3 = st.columns(3)
        with cz1:
            # Remis à 0 par défaut
            nb_bureaux = st.number_input("1. Nombre de bureaux :", min_value=0, value=0, step=1)
            nb_lavage = st.number_input("4. Stations lavage mains :", min_value=0, value=0, step=1)
        with cz2:
            # Remis à 0 par défaut
            nb_toilettes = st.number_input("2. Toilettes communes :", min_value=0, value=0, step=1)
            nb_conferences = st.number_input("5. Salles de conférence :", min_value=0, value=0, step=1)
        with cz3:
            nb_vestiaires = st.number_input("3. Vestiaires et douches :", min_value=0, value=0, step=1)
            nb_halls = st.number_input("6. Halls et réceptions :", min_value=0, value=0, step=1)

        st.write("7. Escaliers :")
        ce1, ce2 = st.columns(2)
        with ce1: nb_escaliers = st.number_input("Nombre de cages d'escalier", min_value=0, value=0, step=1)
        with ce2: nb_etages_escalier = st.number_input("Total d'étages à couvrir", min_value=0, value=0, step=1)

        st.markdown("#### 🎯 Autres zones spécifiques présentes")
        cp1, cp2, cp3, cp4 = st.columns(4)
        with cp1:
            has_cafeteria = st.pills("Cafétéria ou coin repas :", ["Non", "Oui"], default="Non", key="p_cafet")
            has_allaitement = st.pills("Salle allaitement :", ["Non", "Oui"], default="Non", key="p_allait")
        with cp2:
            has_gym = st.pills("Salle de gym :", ["Non", "Oui"], default="Non", key="p_gym")
            has_dechets = st.pills("Local tri / déchets :", ["Non", "Oui"], default="Non", key="p_dechets")
        with cp3:
            has_formation = st.pills("Salles de formation :", ["Non", "Oui"], default="Non", key="p_form")
            has_ascenseur = st.pills("Présence d'ascenseur(s) :", ["Non", "Oui"], default="Non", key="p_asc")
        with cp4:
            has_lounge = st.pills("Zone détente (Lounge) :", ["Non", "Oui"], default="Non", key="p_lounge")

        commentaire_client = st.text_area("Spécificités ou zones non mentionnées :", placeholder="Ex: Grand vitrage...", max_chars=300)

        st.markdown("#### 📧 Coordonnées")
        cco1, cco2, cco3 = st.columns(3)
        with cco1: nom_client = st.text_input("Nom complet / Entreprise :", key="input_nom_net")
        with cco2: courriel_client = st.text_input("Adresse courriel :", key="input_mail_net")
        with cco3: tel_client = st.text_input("Numéro de téléphone :", key="input_tel_net")

        soumettre_nettoyage = st.form_submit_button("🚀 Transmettre ma demande Nettoyage", use_container_width=True, type="primary")

    # Moteur de calculs opérationnels
    jours_par_semaine = 1
    if "Bihebdomadaire" in frequence_label: jours_par_semaine = 2
    elif "3 jours" in frequence_label: jours_par_semaine = 3
    elif "4 jours" in frequence_label: jours_par_semaine = 4
    elif "5 jours" in frequence_label: jours_par_semaine = 5
    elif "6 jours" in frequence_label: jours_par_semaine = 6
    elif "7 jours" in frequence_label: jours_par_semaine = 7

    minutes_base = (superficie / 3500) * 60
    minutes_elements = (nb_bureaux * 2) + (nb_toilettes * 15) + (nb_vestiaires * 20) + (nb_lavage * 5) + (nb_conferences * 10) + (nb_halls * 15) + (nb_escaliers * nb_etages_escalier * 10)
    minutes_options = sum([20 if has_cafeteria == "Oui" else 0, 20 if has_gym == "Oui" else 0, 15 if has_formation == "Oui" else 0, 10 if has_lounge == "Oui" else 0, 10 if has_allaitement == "Oui" else 0, 10 if has_dechets == "Oui" else 0, 5 if has_ascenseur == "Oui" else 0])

    heures_par_jour = ((minutes_base + minutes_elements + minutes_options) * 1.20) / 60
    visites_par_mois = jours_par_semaine * 4.33
    prix_mensuel_secret = (heures_par_jour * visites_par_mois) * 42

    if soumettre_nettoyage:
        # Calcule si le client a laissé tout le questionnaire vide
        total_zones = nb_bureaux + nb_lavage + nb_toilettes + nb_conferences + nb_vestiaires + nb_halls + nb_escaliers
        
        if not nom_client or not courriel_client or not tel_client:
            st.error("❌ Veuillez remplir vos coordonnées.")
        elif superficie == 0 and total_zones == 0:
            st.error("❌ Veuillez sélectionner au moins 1 zone ou entrer une superficie.")
        else:
            with st.spinner("Transmission..."):
                succes = envoyer_courriel_nettoyage(nom_client, courriel_client, tel_client, superficie, frequence_label, heures_par_jour, prix_mensuel_secret, nb_bureaux, nb_toilettes, nb_vestiaires, nb_lavage, nb_conferences, nb_halls, nb_escaliers, nb_etages_escalier, has_cafeteria, has_gym, has_formation, has_lounge, has_allaitement, has_dechets, has_ascenseur, commentaire_client)
            if succes: st.success("🏢 **Demande transmise avec succès !** Notre équipe étudie vos données et vous contactera sous peu.")
            else: st.error("⚠️ Erreur SMTP.")

    st.write("---")
    if st.checkbox("🔑 Panneau secret (Directeur des opérations)", key="sec_net"):
        st.write("### 🧠 Analyse Interne du Nettoyage")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⏱️ TEMPS REQUIS / VISITE", f"{heures_par_jour:.2f} heures")
            st.metric("📅 FRÉQUENCE MENSUELLE", f"{visites_par_mois:.1f} visites / mois")
        with col2:
            st.metric("💰 TAUX HORAIRE APPLIQUÉ", "42.00 $ / h")
            st.metric("📊 FACTURATION MENSUELLE", f"{prix_mensuel_secret:,.2f} $ / mois")


# --- VUE 2 : FORMULAIRE MONTAGE DE MEUBLES ---
elif st.session_state.choix_service == "montage":
    st.markdown("<h3 style='color: #007bff; margin-top:0;'>🔨 Demande de Montage de Meubles</h3>", unsafe_allow_html=True)
    
    type_secteur = st.pills("Quel est le type de projet ?", ["Commercial (Bureaux, Commerces)", "Résidentiel (Maison, Appartement)"], default="Commercial (Bureaux, Commerces)", key="p_secteur")

    détails_meubles = ""
    prix_total = 0.0
    temps_total_main_doeuvre = 0.0
    cout_main_doeuvre = 0.0
    frais_deplacement = 0.0

    with st.form("form_montage_complet"):
        if type_secteur == "Commercial (Bureaux, Commerces)":
            st.markdown("#### 🏢 Mobilier Commercial")
            st.info("💡 Sélectionnez les quantités requises pour votre projet afin de générer votre estimation.")
            
            cm1, cm2 = st.columns(2)
            with cm1:
                q_bureau_std = st.number_input("Bureau de travail standard :", min_value=0, value=0, step=1)
                q_table_conf = st.number_input("Table de conférence ou de réunion :", min_value=0, value=0, step=1)
                q_armoire_cl = st.number_input("Classeur ou Armoire de rangement :", min_value=0, value=0, step=1)
            with cm2:
                q_bureau_dir = st.number_input("Bureau de direction / Mobilier exécutif :", min_value=0, value=0, step=1)
                q_chaise_bur = st.number_input("Chaise de bureau / Fauteuil ergonomique :", min_value=0, value=0, step=1)
                q_comptoir = st.number_input("Comptoir d'accueil / Mobilier de réception :", min_value=0, value=0, step=1)
            
            min_totale = (q_bureau_std * 45 * 1) + (q_bureau_dir * 60 * 2) + (q_table_conf * 90 * 2) + (q_chaise_bur * 15 * 1) + (q_armoire_cl * 45 * 2) + (q_comptoir * 120 * 2)
            temps_total_main_doeuvre = min_totale / 60
            cout_main_doeuvre = temps_total_main_doeuvre * 55.0
            if min_totale > 0: frais_deplacement = 70.0
            prix_total = cout_main_doeuvre + frais_deplacement
            
            if q_bureau_std > 0: détails_meubles += f"- {q_bureau_std}x Bureau standard\n"
            if q_bureau_dir > 0: détails_meubles += f"- {q_bureau_dir}x Bureau de direction\n"
            if q_table_conf > 0: détails_meubles += f"- {q_table_conf}x Table de conférence\n"
            if q_chaise_bur > 0: détails_meubles += f"- {q_chaise_bur}x Chaise de bureau\n"
            if q_armoire_cl > 0: détails_meubles += f"- {q_armoire_cl}x Classeur / Armoire\n"
            if q_comptoir > 0: détails_meubles += f"- {q_comptoir}x Comptoir d'accueil\n"
        else:
            st.markdown("#### 🏠 Mobilier Résidentiel")
            st.info("💡 Tarifs forfaitaires transparents par meuble. Déplacement minimum de 60 $ requis.")
            
            cr1, cr2 = st.columns(2)
            with cr1:
                q_lit = st.number_input("Lit complet / Base de lit :", min_value=0, value=0, step=1)
                st.write("") 
                q_pax = st.number_input("Armoire de garde-robe (style PAX) :", min_value=0, value=0, step=1)
                st.write("")
                q_meuble_tv = st.number_input("Meuble de télévision / Unité murale :", min_value=0, value=0, step=1)
            with cr2:
                q_commode = st.number_input("Commode / Bureau à tiroirs :", min_value=0, value=0, step=1)
                st.write("")
                q_table_res = st.number_input("Table à manger et chaises :", min_value=0, value=0, step=1)
                st.write("")
                q_sofa = st.number_input("Sofa / Divan sectionnel :", min_value=0, value=0, step=1)
            
            calcul_fixe = (q_lit * 50) + (q_commode * 60) + (q_pax * 80) + (q_table_res * 45) + (q_meuble_tv * 50) + (q_sofa * 30)
            if calcul_fixe > 0 and calcul_fixe < 60.0: prix_total = 60.0
            else: prix_total = float(calcul_fixe)
                
            if q_lit > 0: détails_meubles += f"- {q_lit}x Lit / Base de lit\n"
            if q_commode > 0: détails_meubles += f"- {q_commode}x Commode à tiroirs\n"
            if q_pax > 0: détails_meubles += f"- {q_pax}x Armoire PAX\n"
            if q_table_res > 0: détails_meubles += f"- {q_table_res}x Table à manger\n"
            if q_meuble_tv > 0: détails_meubles += f"- {q_meuble_tv}x Meuble TV\n"
            if q_sofa > 0: détails_meubles += f"- {q_sofa}x Sofa / Sectionnel\n"

        st.markdown("#### 📝 Précisions particulières")
        commentaire_montage = st.text_area("Indiquez la marque des meubles ou des contraintes d'accès :", placeholder="Ex: Modèle IKEA PAX...")

        st.markdown("#### 📧 Coordonnées")
        cco_m1, cco_m2, cco_m3 = st.columns(3)
        with cco_m1: nom_client = st.text_input("Nom complet / Entreprise :", key="input_nom_mon")
        with cco_m2: courriel_client = st.text_input("Adresse courriel :", key="input_mail_mon")
        with cco_m3: tel_client = st.text_input("Numéro de téléphone :", key="input_tel_mon")

        soumettre_montage = st.form_submit_button("🚀 Transmettre ma demande Montage", use_container_width=True, type="primary")

    if soumettre_montage:
        if not nom_client or not courriel_client or not tel_client:
            st.error("❌ Veuillez remplir vos coordonnées.")
        elif détails_meubles == "":
            st.error("❌ Veuillez sélectionner au moins 1 meuble.")
        else:
            type_label = "Commercial" if "Commercial" in type_secteur else "Résidentiel"
            with st.spinner("Transmission..."):
                succes = envoyer_courriel_montage(nom_client, courriel_client, tel_client, type_label, détails_meubles, prix_total, commentaire_montage, temps_total_main_doeuvre, cout_main_doeuvre, frais_deplacement)
            if succes: st.success("🏢 **Demande transmise avec succès !** Notre équipe étudie vos données et vous contactera sous peu.")
            else: st.error("⚠️ Erreur SMTP.")

    st.write("---")
    
    # 1. On affiche UNIQUEMENT la zone de texte pour le mot de passe
    code_admin = st.text_input("🔑 Zone réservée (Administration)", type="password")
    
    # 2. Les calculs s'activent UNIQUEMENT si le mot de passe est exactement le bon
    # (Remplace 'NettoyageQuebec2026' par ton vrai mot de passe)
    if code_admin == 'NettoyageQuebec2026':
        st.success("Accès Directeur des opérations validé")
        st.write("### 🧠 Analyse Interne du Montage")
        
        if "Commercial" in type_secteur:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("⏱️ TEMPS DE MAIN-D'ŒUVRE", f"{temps_total_main_doeuvre:.2f} heures")
                st.metric("💰 COÛT HORAIRE (55$/h)", f"{cout_main_doeuvre:,.2f} $")
            with col2:
                st.metric("🚚 FRAIS DÉPLACEMENT", f"{frais_deplacement:.2f} $")
                st.metric("📊 FACTURE CLIENT TOTAL", f"{prix_total:,.2f} $")
        else:
            st.markdown(f"- **Régime :** Tarification Forfaitaire Résidentielle")
            if prix_total == 60.0 and calcul_fixe < 60.0:
                st.info("ℹ️ Note : Le montant a été haussé au minimum de déplacement résidentiel de 60.00 $.")
            st.markdown(f"- **PRIX TOTAL ESTIMÉ :** **`{prix_total:,.2f} $ CAD`** *(plus taxes)*")
