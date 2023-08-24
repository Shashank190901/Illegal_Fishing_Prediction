# Illegal Fishing

## Predicting and Understanding Illegal Fishing project

### Project description

The aim of this project was to create a prediction model for illegal fishing using machine learning algorithms and focused on transshipment unauthorised encounters, and also to apply statistical analysis and general research to understand better the behavior of illegal fishing activity. In addition to it, throughout the project, another goal was added: create a list of countries behaving similarly when it comes to illegal fishing, in order to blacklist countries misbehaving in the field. 

### Questions and Hypotheses

The main question of the project was "Can we predict illegal fishing?" - based on transshipment data, which is one type of illegal fishing. Splitting the questions and hypptheses in three main fields:

1) Predicting illegal fishing:
- Which algorithm can be used to predict illegal fishing?
- Is transshipment data enough to see an illegal fishing trend?
- Can I predict illegal fishing accuratly and how?
- Do I have relevant features to predict if the activity is likely to be illegal or not?

2) Understanding illegal fishing:
- Which countries are misbehaving the most when it comes to illegal fishing?
- Does the data I got meet the media coverage on the topic?
- Is there a trend on the type of boat, illegal fishing, Illegal, Unreported and Unregulated fishing (IUU) and country flags?
- Is there any possible regression to understand better the relationships in the illegal fishing data?

3) Blacklist:
- Are there countries behaving similarly when it comes to illegal fishing that should be avoided when buying fish?
- Can the model make sense with the data limitations I have?
- Which countries should be avoided the most?
- Which algorithm can be used to group their behaviour?


### Datasets

The data used for the project can be found in the data folder. For this project, two main sources were used and an additional source to match ISO3 country to the country name:

1)  fisshing_vessels.csv, taken from https://globalfishingwatch.org/data-download/datasets/public-fishing-vessels-v1 with the active fishing vessels from 2012 to 2016

2) transshipment.csv, taken from https://globalfishingwatch.org/data-download/datasets/public-miller-frontiers-marine-science-2018 - it contains potential illegal fishing encounters looking into transshipment unauthorised activities, from 2012 to 2016

3) IUU.csv, taken from http://www.iuufishingindex.net/ranking with the IUU ranking

4) Country_ISO.csv, taken from https://satvasolutions.com/download-list-of-countries-in-format-iso-3166-1-alpha-3-and-sql-and-csv-file/, with the Iso3 matching the country for the merge

### Data organisation and wrangling

The data wrangling can be found in the data_wrangling folder. 

1) fishing_vessels_clean.ipynb - data cleaning of the dataset with the fishing vessels and adding the ISO file to get the country names. Some changes were made thinking of the merging needed afterwards regarding the transshipment data.

2) transshipment_clean.ipynb - data cleaning of the transshipment activity dataset, including extracting the location from coordinates 

### Data analysis

The data analysis can be found in the data_analysis folder.

1) analysis_prediction_model.ipynb - it contains the merge between transshipment Maritime Mobile Service Identity (MMSI) vessels and not. After the merge, a binary column representing illegal fishing activity or not was added (taking into consideration the transshipment activity). The MMSI is a unique classifier and once a MMSI was caught in illegal activity, it was considered as illegal by the model. Therefore, 1 represents illegal fishing, 0 represents no illegal activity (at least associated to transshipment). The relevant features were selected for the model and different algorithms were trained. Ultimately, the Ramdom Forest machine learning algorithm gave the best prediction base. After reaching a good result, the model was still improved adding bins - the finally accuracy reached around 80%. 

2) analysis_regression_illegal_focus.ipynb - it contains a deeper analysis focus on the illegal fishing itself. Different binning techniques, linear regressions etc were made to understand the connection between different features as boat characteristics, encounter location, time, season, country flag etc and the IUU ranking or number of transshipment encounters. Matplotlib was used several times to understand the data better and a case study about China came from the analysis.

3) blacklist_analysis.ipynb - Nearest neighbours machine learning algorithm was applied to create a list of countries behaving similarly; the focus was china but it is dynamic depending on the goal

### Results

The results were positive and relevant. Namely:

1) Illegal vs legal prediction: 80% accurary with random forest algorithm by binning and/or creating binary variables for the country flag, length, tonnage and engine power, IUU index, gear type.

2) The illegal fishing analysis brought up countries that have been associated to illegal fishing in the media and the techniques they use the most. It was very interesting to have the data corroborating what the media have been showing about illegal fishing and countries misbehaving. It also added relevant information as the usual characteristics of the boats for each countries, as well types of fishing gear, hot location spots for transshipment activities, etc which is also associated to the overfishing they have been targeting.

3) A blacklist model which gave Peru, Taiwan and Russia with similar activity to China - which makes sense looking at the plotting, data and news.

### Problems

Although the results were quite acceptable and the amount of data as well, there was not enough transshipment encounter data to have a huge scale for the project although there are millions of data about fishing vessels everyday. Despite that, the main issue was to get a proper regression when it comes to illegal fishing - although some interesting results came out.

### Repository organisation

1) README.md file explaining the project
2) gitignore
3) data folder with all csv files, described under dataset
4) data_analysis folder with the models and statistical analysis, described under data analysis
5) data_wrangling folder with the data cleaning needed, described under data organisation and wrangling
6) tableau, with the link to the tableau 
7) tableau_csv_files with the csv files exported from the data_analysis in order to use in tableau


### Workflow

The workflow is describe in Trello: https://trello.com/b/UlEIgpNJ/illegalfishing

### Project links

Repository: https://github.com/Brunadiasmiguel/illegal_fishing
Google slides presentation: https://docs.google.com/presentation/d/1TC5UYdqZXm_IEAc2d5dfq6P2hPx8DJGFIRMdcg-sAbE/edit?usp=sharing
Tableau: https://public.tableau.com/profile/bruna8094#!/vizhome/illegal_fishing/Illegal_fishing_story


### Research links

Information on the threats of illegal fishing: https://www.worldwildlife.org/threats/illegal-fishing
https://worldoceanreview.com/en/wor-2/fisheries/illegal-fishing/
https://ec.europa.eu/fisheries/sites/fisheries/files/docs/publications/2019-tackling-iuu-fishing_en.pdf

Understanding transshipment: https://www.frontiersin.org/articles/10.3389/fmars.2018.00240/full

UN 14 goal: life underwater https://www.un.org/sustainabledevelopment/wp-content/uploads/2020/07/E_infographics_14.pdf

IUU official info: http://www.iuufishingindex.net/ranking

Fish stock levels info: http://www.fao.org/state-of-fisheries-aquaculture
http://www.fao.org/iuu-fishing/en/

News: https://www.theguardian.com/world/2020/sep/25/chinese-fishing-peru-us-beijing-row
https://www.theguardian.com/environment/2020/jul/27/chinese-fishing-vessels-galapagos-islands#img-1
https://www.inkstonenews.com/business/chinas-squid-fishing-threatening-its-neighbors-and-world/article/2151229

