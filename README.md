# ANALISI DEI RISULTATI DI SIMULAZIONI MOLECOLARI DEL PROCESSO DI ADSORBIMENTO DI ACQUA SU MODELLI DI PARTICOLATO ATMOSFERICO
## Tirocinio curricolare - Laurea in Scienze e Tecnologie Chimiche [L-27]

La mia attività di tirocinio si inseriva in un progetto di ricerca riguardante lo studio, mediante simulazioni computazionali Monte Carlo Gran Canonico, del processo di adsorbimento di acqua su superfici modello di particolato atmosferico di origine marina (NaCl).
Il mio lavoro ha visto lo sviluppo di uno script in Python (NumPy, pandas, scikit-learn), in grado effettuare una data analysis automatizzata (frame by frame) delle configurazioni (coordinate atomiche delle molecole d'acqua) generate durante ogni simulazione, condotta ad uno specifico valore di pressione di H2O.
Principalmente lo script esegue una cluster analysis (DBSCAN) delle configurazioni, con lo scopo di studiare i fenomeni di tipo aggregativo che coinvolgono le molecole d’acqua adsorbite sulla superficie, i cluster individuati sono poi classificati in “isole” o “strati” in funzione della dimensione, e sono ne sono state studiate le diverse proprietà.
I risultati dell'analisi sono rappresentati dallo script sfruttando tabelle e visualizzazioni (Matplotlib, pyplot e seaborn)
