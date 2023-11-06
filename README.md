### Code for the Paper:
## *"Theoretical Investigation of Inorganic Particulate Matter: The Case of Water Adsorption on a NaCl Particle Model Studied Using Grand Canonical Monte Carlo Simulations"*

### and the Bachelor's Thesis:
## *"Cluster Analysis on the Results of Molecular Simulation of the Water Adsorption Process on Atmospheric Particulate Models."*
### Research Traineeship - BSc in Chemical Science and Technology [L-27] - University of Milano-Bicocca.


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Paper][paper-shield]][paper-url]
[![Thesis][thesis-shield]][thesis-url]

This is the code for the cluster and data analysis of the paper "[Theoretical Investigation of Inorganic Particulate Matter: The Case of Water Adsorption on a NaCl Particle Model Studied Using Grand Canonical Monte Carlo Simulations](https://www.mdpi.com/2304-6740/11/11/421)" ([F. Rizza](https://scholar.google.com/citations?user=yJfbN8AAAAAJ&hl=en&oi=sra), [A. Rovaletti](https://scholar.google.com/citations?user=F4g_VMYAAAAJ&hl=en&oi=sra), G. Carbone, T. Miyake, [C. Greco](https://scholar.google.com/citations?user=C9pWqXAAAAAJ&hl=en&oi=sra), U. Cosentino), published on the international, peer-reviews and open access [Inorganics](https://www.mdpi.com/journal/inorganics/about) journal by [MDPI](https://www.mdpi.com/), and my Bachelor's Thesis: "[Cluster Analysis on the Results of Molecular Simulation of the Water Adsorption Process on Atmospheric Particulate Models.](https://github.com/giocoal/cluster-analysis-on-computational-chemistry-simulations-water-adsorption-on-atmosperic-particulate/blob/main/thesis%20manuscript%20and%20presentation%20slides/Thesis.pdf)"

<p align="center">
<img src="images/ComputationalChemistry.png" width="100%" />
<em>Schematic representation of cluster analysis and data analysis steps.</em>
</p>

My research internship activity was part of a research project concerning the study, by means of computational simulations, of the adsorption process of water on model surfaces of sodium chloride (NaCl) atmospheric particulate matter of marine origin. <br>
To gain a molecular-level understanding of the adsorption process of water vapor on the NaCl surface, Monte Carlo simulations performed in the Grand Canonical ensemble were carried out, considering the water adsorption at different water pressures on a NaCl(001) surface. <br>

During the research internship at the Computational Physical Chemistry Laboratory at the University of Milano-Bicocca, under the supervision of Professor Claudio Greco and Professor Ugo Cosentino, I worked on my Bachelor's Thesis project. <br>
I analyzed 3-D molecular mechanics computational simulations of the water adsorption process on atmospheric particulate matter, leveraging unsupervised machine learning (DBSCAN) for water clusters detection. <br>
Specifically, my work involved the development of a script in Python language (NumPy, pandas, scikit-learn), capable of performing an automated (frame-by-frame) data analysis of the configurations (atomic coordinates of water molecules) generated during each simulation, conducted at a specific water pressure value. <br>
Mainly, the script performs a cluster analysis (DBSCAN) of the configurations, with the purpose of studying the aggregation-type phenomena involving the water molecules adsorbed on the surface, the identified clusters are then classified into "islands" or "layers" according to their size, and their different properties are studied. <br>
The results of my study are collected in my Bachelor's thesis: "[Cluster Analysis on the Results of Molecular Simulation of the Water Adsorption Process on Atmospheric Particulate Models.](https://github.com/giocoal/cluster-analysis-on-computational-chemistry-simulations-water-adsorption-on-atmosperic-particulate/blob/main/thesis%20manuscript%20and%20presentation%20slides/Thesis.pdf)" <br>

Furthermore, during the course of the year 2023, I subsequently contributed, in the context of a voluntary collaboration with the corresponding authors' research groups, to the development of a paper entitled: "[Theoretical Investigation of Inorganic Particulate Matter: The Case of Water Adsorption on a NaCl Particle Model Studied Using Grand Canonical Monte Carlo Simulations](https://www.mdpi.com/2304-6740/11/11/421)" ([F. Rizza](https://scholar.google.com/citations?user=yJfbN8AAAAAJ&hl=en&oi=sra), [A. Rovaletti](https://scholar.google.com/citations?user=F4g_VMYAAAAJ&hl=en&oi=sra), G. Carbone, T. Miyake, [C. Greco](https://scholar.google.com/citations?user=C9pWqXAAAAAJ&hl=en&oi=sra), U. Cosentino), published on the international, peer-reviews and open access [Inorganics](https://www.mdpi.com/journal/inorganics/about) journal by [MDPI](https://www.mdpi.com/). <br>
In particular, I was involved in the investigation, formal analysis and data curation phases.

# Citation

If you find the paper or the source code useful to your projects, please cite the following bibtex:
<pre>
@Article{inorganics11110421,
    AUTHOR = {Rizza, Fabio and Rovaletti, Anna and Carbone, Giorgio and Miyake, Toshiko and Greco, Claudio and Cosentino, Ugo},
    TITLE = {Theoretical Investigation of Inorganic Particulate Matter: The Case of Water Adsorption on a NaCl Particle Model Studied Using Grand Canonical Monte Carlo Simulations},
    JOURNAL = {Inorganics},
    VOLUME = {11},
    YEAR = {2023},
    NUMBER = {11},
    ARTICLE-NUMBER = {421},
    URL = {https://www.mdpi.com/2304-6740/11/11/421},
    ISSN = {2304-6740},
    DOI = {10.3390/inorganics11110421}
}
</pre>

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
[thesis-shield]: https://img.shields.io/badge/Read%20Thesis%20-grey?style=for-the-badge
[thesis-url]: https://github.com/giocoal/cluster-analysis-on-computational-chemistry-simulations-water-adsorption-on-atmosperic-particulate/blob/main/thesis%20manuscript%20and%20presentation%20slides/Thesis.pdf
[paper-shield]: https://img.shields.io/badge/Read%20Paper%20-grey?style=for-the-badge
[paper-url]: https://www.mdpi.com/2304-6740/11/11/421
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
