# Swiss Data Intelligence

## Abstract

## 1. Introduction
### 1.1 Context and Motivation

Switzerland provides a broad range of official public data covering demographic, socioeconomic, geographic and housing-related topics. A central point of access is opendata.swiss, the Swiss public administration's portal for Open Government Data (OGD), which provides a centralised catalogue of datasets published by the Confederation, cantons, communes and other public organisations. The portal facilitates the discovery and reuse of government data for different analytical and public purposes (opendata.swiss, n.d.).

The availability of public data creates opportunities for combining information from different statistical domains to investigate regional patterns. However, data availability alone does not directly provide an analytical view of a specific problem. Answering questions involving several statistical dimensions requires the identification of suitable datasets, the harmonisation of geographic and temporal information, the integration of different data structures, and the application of appropriate analytical methods. This project uses this process as the basis for developing a reproducible data and machine-learning workflow based on official Swiss data.

Home ownership was selected as the initial use case for this work. The Federal Statistical Office (FSO) publishes official statistics on the Swiss building and housing stock and on housing conditions, including information that enables the analysis of home ownership at cantonal level (Federal Statistical Office, n.d.). This provides a suitable regional case study because home ownership can be compared across Swiss cantons and combined with official information describing their demographic and household structures. Rather than analysing the housing indicator in isolation, this project investigates whether these characteristics can contribute to explaining and predicting differences in home-ownership rates across cantons.

This use case forms the first implemented component of Swiss Data Intelligence, conceived as a modular approach for transforming Swiss public data into reproducible analytical outputs. Within the scope of this work, the emphasis is deliberately placed on data integration, exploratory analysis, machine learning and interactive visualisation. The broader concept could later be extended to additional datasets and analytical capabilities, while the present implementation provides a concrete and evaluable proof of concept.

### 1.2 Problem Statement

Official Swiss statistics provide information on housing, population and household characteristics through different datasets. While these sources can be analysed independently, investigating relationships across statistical domains requires them to be transformed into a common analytical structure. In the context of this project, this involves combining housing, demographic and household information at a consistent geographic and temporal level.

The analytical problem addressed in this work is whether demographic and household characteristics contain sufficient information to explain and predict variation in home-ownership rates across Swiss cantons. This is not only a modelling problem. It also requires the construction of a consistent dataset from multiple official sources, the selection of meaningful features, and an evaluation strategy that reflects the geographic and temporal structure of the data.

Based on this problem, the main research question is:

**To what extent can demographic characteristics and household structure explain and predict differences in home-ownership rates across Swiss cantons?**

The question is investigated using canton-year observations covering the period from 2019 to 2024. Particular attention is given to distinguishing between two different generalisation settings: predicting observations from cantons not used for model training and predicting a later year for cantons already represented in the historical data. This distinction is important for assessing what type of predictive capability the resulting models actually demonstrate.

### 1.3 Objectives

The main objective of this work is to develop and evaluate a reproducible machine-learning workflow that integrates official Swiss public data to investigate variation in home-ownership rates across cantons. The project combines data engineering, exploratory analysis, predictive modelling and interactive visualisation within a single end-to-end use case.

To achieve this objective, the work focuses on integrating three main statistical domains published by the Federal Statistical Office: home ownership, household composition and population demographics. The resulting analytical dataset uses the canton-year as its unit of observation and covers all 26 Swiss cantons from 2019 to 2024. Demographic and household characteristics are then used as predictors of the cantonal home-ownership rate.

The modelling component compares a simple baseline with linear and tree-based regression approaches. Model performance is evaluated using error and goodness-of-fit metrics, with particular attention to the distinction between geographic generalisation to unseen cantons and temporal generalisation to a later year. The analysis also considers feature importance and canton-level prediction errors to support interpretation of model behaviour.

In addition to the analytical workflow, the project delivers a functional prototype of Swiss Data Intelligence implemented as an interactive Streamlit application. The application integrates the processed data, geographic information and the final machine-learning model to enable the exploration of cantonal demographic, household and home-ownership patterns and to demonstrate how the analytical results can be made accessible through an interactive interface.

### 1.4 Scope

The scope of this work is intentionally limited to a focused proof of concept based on official Swiss public data. The implemented use case covers home ownership, household composition and population demographics at canton-year level for all 26 Swiss cantons between 2019 and 2024.

The work focuses on data integration, exploratory analysis, feature engineering, supervised regression, model evaluation and interactive visualisation. It does not attempt to establish causal relationships between the selected characteristics and home ownership, nor does it aim to provide long-term forecasts or a production-scale data platform.

Capabilities considered within the broader Swiss Data Intelligence concept, including natural-language querying, retrieval-augmented generation, automated ingestion of additional public datasets, real-time processing and production MLOps infrastructure, remain outside the implemented scope and are considered possible directions for future development.

### 1.5 Report Structure

The remainder of this report is structured as follows. Chapter 2 presents the relevant background and related work on Swiss public data, home ownership and the application of machine learning to regional and socioeconomic data. Chapter 3 describes the data sources, data preparation process, exploratory analysis, feature engineering, modelling approaches and validation strategy. Chapter 4 presents the exploratory and modelling results, including the evaluation of geographic and temporal generalisation and the analysis of model behaviour and errors. Chapter 5 describes the design and implementation of the Swiss Data Intelligence prototype. Finally, Chapter 6 discusses the results and limitations of the work, provides a critical reflection on the implemented approach and presents the main conclusions and possible directions for future development.

## 2. Background and Related Work
### 2.1 Swiss Public Data

Switzerland provides a wide range of official statistics on population, households, housing and regional characteristics. These data are published by the Federal Statistical Office (FSO) and other federal institutions and are also made available through the Swiss Open Government Data ecosystem. Combining information from these different areas creates opportunities to explore socioeconomic differences across Swiss regions.

Home ownership is one of the areas where these regional differences are particularly visible. The Swiss Federal Office for Housing defines the home-ownership rate as the share of owner-occupied dwellings among all permanently occupied dwellings. At national level, around 36% of permanently occupied dwellings are owner-occupied. The rate increased between 1970 and 2015 and has slightly declined in more recent years (Federal Office for Housing [BWO], 2025).

The national rate, however, hides considerable differences between cantons. Official FSO statistics also show differences according to household composition. For example, home ownership is more common among couple households than among single-person households (Federal Statistical Office [FSO], 2021). These differences make it useful to analyse home ownership together with demographic and household characteristics rather than as an isolated housing indicator.

Previous research shows that home ownership is related to a combination of demographic, household, economic and policy factors. Bourassa et al. (2015), reviewing international evidence on homeownership, identify household age and household structure among the relevant demographic dimensions, while also highlighting the role of income, wealth, borrowing constraints and housing policies. Recent Swiss research provides further evidence of this broader context. Bolliger et al. (2025), using Swiss administrative tax records, find heterogeneous effects in transitions to home ownership according to characteristics such as age, income and wealth. Related Swiss research has also examined demographic and household characteristics in relation to residential space consumption (Delbiaggio et al., 2018).

Based on this context, this project focuses on differences in home-ownership rates across Swiss cantons between 2019 and 2024. It combines official statistics on home ownership, household composition and population demographics at canton-year level. The objective is not to establish causal relationships, but to evaluate whether these characteristics provide useful information for explaining and predicting the regional differences observed in home ownership.

### 2.2 Machine Learning Context

Machine-learning methods provide a way to investigate relationships between multiple characteristics and a socioeconomic outcome without assuming that these relationships are necessarily linear. This is relevant for regional data, where demographic, household and geographic characteristics can interact in ways that may not be fully represented by a simple linear model.

The data used in this project are tabular, with each observation described by a set of demographic and household features. For this type of data, tree-based models provide an important alternative to linear approaches because they can represent non-linear relationships and interactions between variables. Large-scale benchmarking by Grinsztajn et al. (2022) shows that tree-based models remain strong performers on typical tabular datasets. Based on this context, the modelling strategy in this project compares a linear approach with two tree-based ensemble methods, Random Forest and Gradient Boosting. The objective is not to identify a universally superior algorithm, but to compare models with different levels of flexibility on the same data.

An additional challenge comes from the structure of regional data. The analytical dataset used in this project contains repeated observations for the same 26 cantons between 2019 and 2024. Observations belonging to the same canton should therefore not automatically be treated as independent geographic units. Roberts et al. (2017) show that standard random cross-validation can be inappropriate when data contain spatial, temporal or hierarchical dependencies, because observations in training and validation sets may be more closely related than observations encountered in the intended prediction scenario.

This issue is also discussed specifically in the context of geospatial machine learning. Wang et al. (2023) show that random cross-validation can produce overly optimistic estimates when the validation data do not adequately represent the locations where predictions will eventually be made. They propose a spatial cross-validation method that explicitly considers geographic and feature-space differences between training and validation data. Although the present work does not implement spatial cross-validation in this strict sense, the same general concern is relevant when evaluating whether a model can generalise to cantons that were not used during training.

For this reason, model evaluation in this project distinguishes between geographic and temporal generalisation. Geographic generalisation is evaluated by keeping complete cantons separated between training and validation, while temporal generalisation is evaluated by training on earlier years and testing on a later year for already observed cantons. These two settings answer different questions and provide a more informative assessment of model performance than a single random train-test split. The exact validation procedure and evaluation metrics are described in Section 3.5.

### 2.3 Related Work

Previous research on home ownership shows that regional differences can be studied by combining demographic, household, economic and housing-related information. International research has identified characteristics such as age and household structure as relevant dimensions for explaining differences in home-ownership rates, while also highlighting the importance of economic conditions, borrowing constraints and housing policies (Bourassa et al., 2015). In Switzerland, recent studies have also used detailed socioeconomic information to investigate housing-related questions, including transitions to home ownership and residential space consumption (Bolliger et al., 2025; Delbiaggio et al., 2018).

The present work takes a different but complementary approach. Instead of modelling individual household tenure decisions, it integrates recent official public datasets at canton-year level and applies machine-learning methods to investigate regional variation in home-ownership rates. The contribution therefore lies not only in the predictive analysis, but also in the construction of a reproducible workflow that connects data ingestion, preparation, exploratory analysis, modelling, evaluation and interactive visualisation.

Making analytical results accessible is also part of the broader Swiss Data Intelligence concept. In the implemented prototype, this is addressed through an interactive application that allows users to explore cantonal indicators, geographic patterns and model outputs without directly working with the underlying datasets or Python code. More advanced approaches can reduce this technical barrier further. For example, Brunner and Stockinger (2021) propose ValueNet, a natural-language-to-SQL system designed to translate user questions into database queries while incorporating information from the underlying database.

Natural-language querying was considered as a possible extension of Swiss Data Intelligence but is not part of the implemented MVP. The current work instead focuses on establishing the underlying analytical workflow and exposing its results through a structured interactive interface. Natural-language access, the integration of additional public datasets and other intelligent data-access mechanisms are therefore considered possible directions for future development.

<!-- TODO: Integrate Delbiaggio & Wanzenried cantonal homeownership study if full text becomes available. -->

## 3. Data
### 3.1 Data Sources
### 3.2 Dataset Selection
### 3.3 Data Ingestion
### 3.4 Data Preparation and Integration
### 3.5 Data Quality and Limitations

## 4. Methodology
### 4.1 Analytical Problem
### 4.2 Exploratory Data Analysis
### 4.3 Feature Engineering
### 4.4 Baseline
### 4.5 Machine Learning Models
### 4.6 Evaluation Strategy

## 5. Results and Discussion
### 5.1 Exploratory Findings
### 5.2 Model Performance
### 5.3 Model Interpretation
### 5.4 Discussion and Limitations

## 6. Conclusions
### 6.1 Main Findings
### 6.2 Future Work

## References

opendata.swiss. (n.d.). About us. https://opendata.swiss/en/about

Federal Statistical Office. (n.d.). Buildings. https://www.bfs.admin.ch/bfs/en/home/statistics/construction-housing/



## Appendix

## AI / Tools Disclosure