# ANALISI DEI RISULTATI DI SIMULAZIONI MOLECOLARI DEL PROCESSO DI ADSORBIMENTO DI ACQUA SU MODELLI DI PARTICOLATO ATMOSFERICO
## Tirocinio curricolare - Laurea in Scienze e Tecnologie Chimiche [L-27]

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

La mia attività di tirocinio si inseriva in un progetto di ricerca riguardante lo studio, mediante simulazioni computazionali Monte Carlo Gran Canonico, del processo di adsorbimento di acqua su superfici modello di particolato atmosferico di origine marina (NaCl).
Il mio lavoro ha visto lo sviluppo di uno script in Python (NumPy, pandas, scikit-learn), in grado effettuare una data analysis automatizzata (frame by frame) delle configurazioni (coordinate atomiche delle molecole d'acqua) generate durante ogni simulazione, condotta ad uno specifico valore di pressione di H2O.
Principalmente lo script esegue una cluster analysis (DBSCAN) delle configurazioni, con lo scopo di studiare i fenomeni di tipo aggregativo che coinvolgono le molecole d’acqua adsorbite sulla superficie, i cluster individuati sono poi classificati in “isole” o “strati” in funzione della dimensione, e sono ne sono state studiate le diverse proprietà.
I risultati dell'analisi sono rappresentati dallo script sfruttando tabelle e visualizzazioni (Matplotlib, pyplot e seaborn).

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/giocoal/Cluster_analysis_Visualization_Computational_Chemistry.svg?style=for-the-badge
[contributors-url]: https://github.com/giocoal/Cluster_analysis_Visualization_Computational_Chemistry/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/giocoal/Cluster_analysis_Visualization_Computational_Chemistry.svg?style=for-the-badge
[forks-url]: https://github.com/giocoal/Cluster_analysis_Visualization_Computational_Chemistry/network/members
[stars-shield]: https://img.shields.io/github/stars/giocoal/Cluster_analysis_Visualization_Computational_Chemistry.svg?style=for-the-badge
[stars-url]: https://github.com/giocoal/Cluster_analysis_Visualization_Computational_Chemistry/stargazers
[issues-shield]: https://img.shields.io/github/issues/giocoal/Cluster_analysis_Visualization_Computational_Chemistry.svg?style=for-the-badge
[issues-url]: https://github.com/giocoal/Cluster_analysis_Visualization_Computational_Chemistry/issues
[license-shield]: https://img.shields.io/github/license/giocoal/Cluster_analysis_Visualization_Computational_Chemistry.svg?style=for-the-badge
[license-url]: https://github.com/giocoal/Cluster_analysis_Visualization_Computational_Chemistry/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/giorgio-carbone-63154219b/
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
