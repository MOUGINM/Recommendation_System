# **Système de Recommandation de Films**

## **Description**
Ce projet est une application Streamlit qui utilise un système de recommandation basé sur la similarité de films. Les données sont prétraitées et nettoyées pour permettre une recherche efficace par **titre** ou **mots-clés**, avec des recommandations adaptées.

---

## **Fonctionnalités**
1. Recherchez des films similaires par **titre** (insensible à la casse).
2. Recherchez des films similaires à partir de **mots-clés**.
3. Affichez les genres, mots-clés et résumés des films recommandés.
4. Redirection dynamique vers des plateformes populaires :
   - **Google**
   - **JustWatch**
   - **IMDb**

---

## **Structure du Projet**
- **`recomandation_clean_data.ipynb`** : Notebook Python pour nettoyer et préparer les données (dataset).
- **`streamlit_app.py`** : Application Streamlit principale qui utilise les données nettoyées pour fournir des recommandations interactives.
- **`clean_data.csv`** : Dataset nettoyé utilisé par l'application.

---

## **Installation**

### **1. Cloner le dépôt**
```bash
git clone https://github.com/MOUGINM/Recommendation_System
cd Recommendation_System
```

### **2. Installer les dépendances**
Assurez-vous d'avoir Python 3.x et installez les bibliothèques nécessaires 

---

## **Utilisation**

### **1. Utilisation dans un NoteBook**
Si vous souhaitez l'utiliser dans le notebook `recomandation_clean_data.ipynb`.

### **2. Lancer l'application Streamlit**
```bash
streamlit run streamlit_app.py
```

Une fois démarré, ouvrez votre navigateur grace au lien générer par Streamlit dans le terminal pour interagir avec l'application.

---

## **Aperçu**
1. **Interface Principale :**
   - Entrez un titre de film ou des mots-clés pour obtenir des recommandations.
2. **Résultats :**
   - Affichage des films similaires avec genres, mots-clés, résumé et boutons pour rechercher sur Google, JustWatch, ou IMDb.

---


## **Crédits**
- Développement : [Mougin Mehdi]
