# Swiss Data Intelligence

## Abstract

Swiss public data provide extensive information on demographic, household, and housing characteristics, but combining these sources into a consistent analytical workflow requires substantial data preparation and methodological decisions. This project develops **Swiss Data Intelligence**, an end-to-end machine-learning workflow for investigating differences in home-ownership rates across Swiss cantons using official public data.

Data from the Federal Statistical Office on home ownership, household composition, and population demographics were integrated into a canton-year dataset covering all 26 Swiss cantons from 2019 to 2024. After exploratory analysis and feature engineering, nine demographic and household predictors were used to compare a mean baseline, Linear Regression, Random Forest, and Gradient Boosting. Model evaluation explicitly distinguished between geographic generalisation to previously unseen cantons and temporal generalisation to a new year for already observed cantons.

Gradient Boosting achieved the best performance under canton-grouped cross-validation, with a mean absolute error of 6.05 percentage points and an R² of 0.359, reducing MAE by approximately 19.4% relative to the mean baseline. Temporal evaluation produced substantially stronger results, with an R² of 0.885 for 2024. However, a simple persistence baseline based on the 2023 value achieved an R² of 0.964, demonstrating that much of the apparent temporal predictability is associated with the strong year-to-year stability of canton-level home-ownership rates.

The results show that demographic and household characteristics contain useful predictive information, but explain only part of the geographic variation in Swiss home ownership. The resulting workflow was integrated into an interactive Streamlit MVP, demonstrating a reproducible process from public-data integration and analysis to machine-learning evaluation, geographic visualisation, and interactive exploration.

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

#### 1.5 Report Structure

The remainder of this report is organised as follows. Chapter 2 presents the background and related work, covering Swiss public data, the home-ownership context, machine learning for regional and socioeconomic data, and related approaches to intelligent data interfaces.

Chapter 3 describes the project approach and planning, including the iterative development process and the estimated effort associated with the main project activities.

Chapter 4 presents the data foundation of the project, from dataset discovery and selection to ingestion, preparation, integration, and the construction of the final canton-year analytical dataset.

Chapter 5 describes the methodology used for exploratory analysis, feature engineering, model development, and validation. Particular attention is given to the distinction between geographic and temporal generalisation.

Chapter 6 presents the empirical results, including the main exploratory findings, model performance, geographic and temporal generalisation, and model interpretation and error analysis.

Chapter 7 describes the implementation of the Swiss Data Intelligence MVP and shows how the processed data, geographic information, and machine-learning model were integrated into an interactive Streamlit application.

Finally, Chapter 8 discusses the main findings in relation to the research question, critically examines the limitations of the project, and presents the conclusions and potential directions for future development.

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

For this reason, model evaluation in this project distinguishes between geographic and temporal generalisation. Geographic generalisation is evaluated by keeping complete cantons separated between training and validation, while temporal generalisation is evaluated by training on earlier years and testing on a later year for already observed cantons. These two settings answer different questions and provide a more informative assessment of model performance than a single random train-test split. The exact validation procedure and evaluation metrics are described in Section 5.4.

### 2.3 Related Work

Previous research on home ownership shows that regional differences can be studied by combining demographic, household, economic and housing-related information. International research has identified characteristics such as age and household structure as relevant dimensions for explaining differences in home-ownership rates, while also highlighting the importance of economic conditions, borrowing constraints and housing policies (Bourassa et al., 2015). In Switzerland, recent studies have also used detailed socioeconomic information to investigate housing-related questions, including transitions to home ownership and residential space consumption (Bolliger et al., 2025; Delbiaggio et al., 2018).

The present work takes a different but complementary approach. Instead of modelling individual household tenure decisions, it integrates recent official public datasets at canton-year level and applies machine-learning methods to investigate regional variation in home-ownership rates. The contribution therefore lies not only in the predictive analysis, but also in the construction of a reproducible workflow that connects data ingestion, preparation, exploratory analysis, modelling, evaluation and interactive visualisation.

Making analytical results accessible is also part of the broader Swiss Data Intelligence concept. In the implemented prototype, this is addressed through an interactive application that allows users to explore cantonal indicators, geographic patterns and model outputs without directly working with the underlying datasets or Python code. More advanced approaches can reduce this technical barrier further. For example, Brunner and Stockinger (2021) propose ValueNet, a natural-language-to-SQL system designed to translate user questions into database queries while incorporating information from the underlying database.

Natural-language querying was considered as a possible extension of Swiss Data Intelligence but is not part of the implemented MVP. The current work instead focuses on establishing the underlying analytical workflow and exposing its results through a structured interactive interface. Natural-language access, the integration of additional public datasets and other intelligent data-access mechanisms are therefore considered possible directions for future development.

<!-- TODO: Integrate Delbiaggio & Wanzenried cantonal homeownership study if full text becomes available. -->

# 3. Project Approach and Planning

## 3.1 Project Approach

The project followed an iterative and experiment-driven approach, with the objective of developing a complete analytical workflow from Swiss public data to an interactive machine-learning application. Rather than defining a complex technical architecture from the beginning, the work was progressively refined according to the availability and characteristics of the data and the results obtained during the analysis.

The initial concept of Swiss Data Intelligence was broader than the final implementation. The original idea was to create a modular platform capable of integrating multiple Swiss public datasets and providing intelligent access to them through analytical and potentially natural-language interfaces. However, implementing all of these components within the scope of a CAS transfer project would have introduced considerable technical complexity without necessarily improving the quality of the analytical evaluation.

For this reason, the project was progressively narrowed to a clearly defined minimum viable product. Home ownership was selected as the initial analytical use case, while demographic characteristics and household structure were chosen as the main explanatory dimensions. This provided a sufficiently focused problem for developing and evaluating the complete workflow while maintaining the broader Swiss Data Intelligence concept as a foundation for future extensions.

The development process was organised around successive stages. Public datasets were first discovered and evaluated according to their relevance, geographic granularity, temporal coverage, and compatibility with the intended canton-year analytical structure. The selected datasets were then ingested, harmonised, and integrated into a common analytical dataset. Exploratory analysis was subsequently used to understand the structure of the target and predictors and to guide feature engineering and the validation strategy.

Machine-learning development followed the exploratory analysis rather than being treated as an isolated modelling task. Several models and baselines were evaluated using validation strategies designed around the geographic and temporal structure identified in the data. The results were then analysed not only in terms of predictive performance, but also with respect to model errors, feature importance, and the distinction between geographic and temporal generalisation.

The final stage integrated the processed data, geographic information, and selected machine-learning model into the Swiss Data Intelligence Streamlit application. This created a functional vertical slice of the original concept, connecting public data acquisition and preparation with analysis, modelling, evaluation, and an interactive user interface.

Throughout the project, scope decisions were guided by the principle of completing and validating the end-to-end workflow before introducing additional technical components. Features such as automated data ingestion, model lifecycle management, streaming architectures, feature stores, and an LLM-based interface were therefore considered possible extensions rather than requirements of the MVP. This approach allowed the project to concentrate its available effort on data quality, methodological validity, reproducibility, and critical evaluation of the results.


## 3.2 Project Planning

The project followed an iterative development process rather than a strictly sequential workflow. The main activities progressed from the initial definition of Swiss Data Intelligence through data preparation, analysis, modelling and validation, MVP development, and final documentation. Several activities overlapped or were revisited as new findings emerged.

The development process was structured around six main stages: **Project Definition, Data Foundation, Analysis, Modelling & Evaluation, MVP Development, and Finalisation**. These stages represent the logical progression of the project rather than equal periods of calendar time. This distinction is important because the intensity of the work varied substantially throughout the project.

The first stage focused on defining the project scope, research question, MVP boundaries, and overall technical architecture. The Data Foundation stage then concentrated on identifying suitable Swiss public datasets and developing the ingestion, harmonisation, and integration processes required to construct a consistent canton-year analytical dataset.

Once the data foundation had been established, exploratory data analysis was used to investigate the geographic and temporal structure of home ownership and its relationships with demographic and household characteristics. The results of this analysis informed the subsequent feature-engineering decisions and modelling strategy.

The Modelling & Evaluation stage included the implementation and comparison of the baseline, Linear Regression, Random Forest, and Gradient Boosting models. Validation was treated as a distinct component of the modelling workflow and included canton-grouped cross-validation, temporal holdout evaluation, a persistence baseline, and canton-level error analysis.

The selected model and processed data were subsequently integrated into the Swiss Data Intelligence Streamlit MVP. The final stage concentrated on consolidating the analytical results, scientific literature, technical documentation, figures, and final report.

Some activities, particularly technical documentation, literature review, and project management, were performed iteratively across several stages rather than at a single point in the development process. Table X therefore represents the project as an overlapping development workflow. The horizontal dimension indicates the approximate logical progression of the work rather than calendar time, while the estimated effort is reported separately for each activity.

[INSERT TABLE X: PROJECT DEVELOPMENT GANTT]

**Table X.** Project development progression and estimated effort. Horizontal position represents the approximate logical progression of the project rather than equal periods of calendar time. Continuous and recurring blocks indicate activities that extended across, or were revisited during, different development stages. Source: own elaboration.

The estimated total project effort was approximately **113 hours**. A substantial proportion of this effort was dedicated to data discovery, ingestion, preparation, and integration. In particular, identifying public datasets that were both relevant to the research question and sufficiently compatible in terms of geographic granularity, temporal coverage, and structure required substantial exploratory work before the final analytical dataset could be constructed.

The distribution of effort also reflects the decision to prioritise a complete end-to-end workflow rather than model complexity alone. Model development represented only one component of the project, alongside data engineering, exploratory analysis, validation, interpretation, application development, documentation, and scientific reporting.

                                      PROJECT DEVELOPMENT PROGRESSION
                         ────────────────────────────────────────────────────────►

                                          DATA                    MODELLING &
                             PROJECT      FOUNDATION   ANALYSIS    EVALUATION     MVP      FINALISATION
                             DEFINITION

Activity                     Effort
───────────────────────────────────────────────────────────────────────────────────────────────────────

Project definition,
scope & architecture           5 h       ███████


Environment &
repository setup               5 h       ███████     ██


Data discovery &
dataset selection             20 h       ██          ███████████


Data ingestion                 7 h                   █████████


Data preparation &
integration                   12 h                   █████████   ██


EDA & feature
engineering                   10 h                               █████████


ML modelling                   7 h                                           ███████


Validation &
error analysis                 7 h                                           █████████


Streamlit MVP
development                   12 h                                                        ███████████


Technical documentation
& traceability                 7 h       ██          ██          ██          ██           ██       █████


Literature review &
references                     8 h       ██          ██          ██          ██                    █████


Report preparation
& writing                     10 h                                                                  █████████


Project management,
Git & supporting tasks         3 h       ██          ██          ██          ██           ██       ██

───────────────────────────────────────────────────────────────────────────────────────────────────────
TOTAL ESTIMATED EFFORT        113 h

## 4. Data
### 4.1 Data Discovery and Dataset Selection

The identification and selection of suitable datasets represented an important part of the project. Switzerland provides a large amount of official public data, but identifying sources that could be combined for a specific analytical problem required more than finding individually relevant datasets. Geographic granularity, temporal coverage, variable definitions, data structure and potential join keys also had to be considered.

To support this process, a data inventory was created to document and compare candidate datasets. For each source, information such as provider, thematic domain, access location, geographic and temporal coverage, granularity, potential join keys, expected analytical value and possible role within the MVP was recorded. The inventory was progressively refined as the analytical use case became more clearly defined.

The initial search focused primarily on housing, population, household structure and demographic characteristics. Candidate sources were investigated mainly through the Federal Statistical Office (FSO) and the Swiss Open Government Data ecosystem. Dataset selection was guided by three main criteria: relevance to the research question, compatibility at canton level, and sufficient temporal overlap to construct a consistent analytical period.

Several potentially relevant datasets were evaluated but not included in the final workflow. In some cases, their temporal coverage was incompatible with the common analytical period; in others, the information overlapped with a source already selected or did not provide sufficient additional value for the focused MVP. For example, the *Demographic Balance by Canton* dataset available during the discovery process contained data for 2025, while equivalent observations for the 2019–2024 period could not be identified.

Based on this process, three main statistical datasets were selected: home-ownership rates by canton, private households by household size, and population by canton, sex, marital status and age. A geographic reference dataset was additionally used to harmonise canton identifiers across the different sources. Together, these sources provided the information required to construct a common canton-year analytical dataset covering the period from 2019 to 2024.

Table X summarises the principal datasets considered during the discovery process and their role in the final project.

| Dataset | Domain | Decision | Role / rationale |
|---|---|---|---|
| Home Ownership Rate by Canton | Housing | **Selected** | Provides the home-ownership rate used as the target variable |
| Private Households by Household Size | Households | **Selected** | Provides household-composition information used to derive predictor variables |
| Population by Canton, Sex, Marital Status and Age | Demographics | **Selected** | Provides detailed population information used to derive demographic predictors |
| BFS Geo Canton Lookup | Geographic reference | **Selected** | Used to harmonise geographic identifiers and canton names across sources |
| Occupied Dwellings by Occupancy Status and Canton | Housing | Evaluated, not selected | Relevant to housing tenure, but overlaps with the selected home-ownership outcome and introduces additional occupancy dimensions |
| Demographic Balance by Canton | Demographics | Evaluated, not selected | Available data covered 2025, while equivalent observations for the 2019–2024 analytical period could not be identified during data discovery |
| Permanent and Non-Permanent Resident Population by Canton | Demographics | Evaluated, not selected | Considered as a population source, but the age-detailed population dataset provided the demographic structure required for the analysis |

The resulting selection was intentionally focused. The objective was not to incorporate every potentially relevant socioeconomic variable, but to establish a consistent and interpretable first use case for Swiss Data Intelligence. Other datasets identified during discovery therefore remain potential extensions rather than being considered unsuitable sources.

### 4.2 Data Sources

The final analytical dataset was constructed from three main statistical sources published by the Federal Statistical Office (FSO), complemented by a geographic reference dataset for the harmonisation of canton identifiers. The selected sources cover home ownership, household composition and population demographics. Although some of the original datasets provide a broader temporal range, the analysis was restricted to the common period from 2019 to 2024.

#### 4.2.1 Home Ownership Rate by Canton

The target variable was obtained from the FSO dataset *Home Ownership Rate by Canton*, accessed through the Swiss Open Government Data portal (Federal Statistical Office, n.d.). The dataset provides annual home-ownership rates at cantonal level and includes observations from 2019 onwards.

The home-ownership rate is expressed as a percentage and was used as the dependent variable throughout the analysis. In addition to the cantonal observations, the source contains an aggregate value for Switzerland. This national observation was retained as a descriptive reference where relevant but was not included as an additional geographic unit in the analytical dataset.

#### 4.2.2 Private Households by Household Size

Household composition was obtained from the FSO dataset *Private Households by Institutional Units and Household Size* (Federal Statistical Office, [YEAR]). The source used in this project contains annual observations from 2012 to 2024 and distinguishes households according to the number of persons living in them.

For consistency with the other selected sources, only observations from 2019 to 2024 were retained for the analysis. The dataset provides the basis for describing household structure within each canton, including one-person, two-person and larger households. These data were subsequently transformed into household-size shares for use as explanatory variables.

<!-- TODO REFERENCE: Replace the current Zotero record for the 2012-2023 edition with the exact FSO source/version used for the 2012-2024 dataset. -->

#### 4.2.3 Population by Canton, Sex, Marital Status and Age

Demographic information was obtained from the FSO population statistics through PX-Web (Federal Statistical Office, n.d.). The selected dataset provides population counts by canton together with detailed breakdowns by sex, marital status and individual age.

For this project, the source was used to construct demographic characteristics at canton-year level for the period from 2019 to 2024. The detailed age information was initially preserved rather than imposing predefined age groups during data ingestion. This allowed the demographic structure required for the modelling stage to be derived later in the analytical workflow.

#### 4.2.4 Geographic Reference Data

A geographic reference table provided by the FSO was used to support the consistent identification of the 26 Swiss cantons across the selected statistical sources (Federal Statistical Office, [YEAR]). This was necessary because canton names were not represented identically in all source files, particularly for cantons with multilingual names.

The reference data provided stable geographic identifiers that could be used independently of these naming differences. These identifiers were subsequently used to harmonise the datasets before integration at canton-year level.

<!-- TODO REFERENCE: Verify the exact FSO geographic reference source and Zotero metadata before finalising the Word document. -->

### 4.3 Data Ingestion, Preparation and Integration

The selected data sources differed in structure, level of detail and geographic representation. A reproducible preparation workflow was therefore developed to transform them into a common canton-year structure before integration. Original source files were preserved in the raw-data layer, while cleaning and transformation steps were performed separately. This separation ensured that the original data remained unchanged and that the construction of the analytical dataset could be reproduced from the source files.

#### 4.3.1 Home-Ownership Data

The home-ownership source contained 162 observations covering 27 geographic units and six years from 2019 to 2024. The geographic units consisted of the 26 Swiss cantons and an additional aggregate observation for Switzerland. No missing values were present in the target variable.

Because the unit of analysis was defined as the canton-year, the national aggregate was excluded from the analytical dataset. After this filtering step, the data contained 156 observations representing all 26 cantons across the six-year analytical period. The geographic identifier, year and home-ownership rate were retained for subsequent integration.

#### 4.3.2 Household Data

The household source contained 1,134 observations for the selected 2019-2024 period, covering 27 geographic units and seven household-size categories: one, two, three, four, five, six or more persons, and the total number of private households.

After excluding the national aggregate for Switzerland, 1,092 observations remained. No duplicate combinations of canton, year and household-size category were identified. The data were then reshaped so that each canton-year represented a single observation, resulting in 156 rows.

Household counts were transformed into the total number of private households and six variables representing the share of households in each size category. At this stage, all six household-size categories were preserved rather than combining them into broader groups. This avoided introducing an arbitrary aggregation during data preparation and allowed variable selection to be addressed later during exploratory analysis and feature engineering.

#### 4.3.3 Population Data

The population source contained 3,024 observations and 107 variables. It provided population information by canton, sex, marital status and individual age. To construct a demographic representation consistent with the canton-year unit of analysis, the data were restricted to total sex and total marital-status categories.

The national aggregate for Switzerland and geographic observations not corresponding to one of the 26 cantons were subsequently removed. This resulted in 156 observations covering the complete 2019-2024 canton-year structure.

The source provided 101 individual age variables in addition to total population. These detailed age variables were deliberately preserved during data preparation rather than being immediately aggregated into predefined age groups. This separated source-data preparation from later feature-engineering decisions and retained the demographic detail required for subsequent analysis.

#### 4.3.4 Geographic Harmonisation

The selected sources represented cantons using different geographic conventions, including geographic codes, canton abbreviations and multilingual canton names. A geographic reference table from the FSO was therefore used to establish consistent identifiers for the 26 cantons.

Differences in canton naming were resolved before integration. These included multilingual representations such as Bern/Berne, Fribourg/Freiburg and Valais/Wallis, as well as other naming differences across the source files. After harmonisation, all population observations were successfully assigned to one of the 26 canton identifiers, with no missing geographic codes.

<!-- TODO REFERENCE: Verify the exact FSO geographic reference source and insert the corresponding Zotero citation. -->

#### 4.3.5 Dataset Integration and Validation

After source-specific preparation and geographic harmonisation, the three statistical datasets were integrated using the combination of year and geographic identifier as the common key. One-to-one merge validation was applied to ensure that each source contributed at most one observation to each canton-year combination.

The resulting analytical dataset contained 156 observations and 113 variables, representing all 26 Swiss cantons over the six-year period from 2019 to 2024. Final validation confirmed that each canton-year combination was unique, all expected cantons and years were present, and no missing values were present in either the target variable or the integrated analytical dataset.

The validated dataset was exported as `canton_year_analytical_dataset_2019_2024.csv` and used as the input for the subsequent exploratory analysis and feature-engineering stages.

### 4.4 Final Analytical Dataset

The data preparation and integration process resulted in a complete canton-year analytical dataset covering all 26 Swiss cantons from 2019 to 2024. With six annual observations per canton, the dataset contained 156 observations and 113 variables before subsequent feature engineering and selection.

Each row represented one canton in one year and combined the home-ownership rate with household and demographic information. The dataset therefore contained three main types of analytical information:

- **Target variable:** home-ownership rate at canton-year level.
- **Household characteristics:** total number of private households and the distribution of households across six household-size categories.
- **Demographic characteristics:** total population and detailed population counts by individual age.

The combination of geographic identifier and year uniquely identified every observation. The final validation confirmed complete coverage of the expected 26 cantons and six years, with no duplicated canton-year observations and no missing values in the integrated dataset.

| Characteristic | Final analytical dataset |
|---|---|
| Unit of analysis | Canton-year |
| Geographic coverage | 26 Swiss cantons |
| Temporal coverage | 2019-2024 |
| Years | 6 |
| Observations | 156 |
| Variables | 113 |
| Target | Home-ownership rate |
| Duplicate canton-year observations | 0 |
| Missing values | 0 |

At this stage, the dataset intentionally retained more demographic and household detail than was ultimately required for modelling. Feature construction and selection were performed only after exploratory analysis, allowing these decisions to be based on the observed structure of the data rather than being imposed during data ingestion.

The resulting dataset, `canton_year_analytical_dataset_2019_2024.csv`, provided the common analytical basis for the exploratory analysis and machine-learning workflow described in the following chapters.

## 5. Methodology

### 5.1 Exploratory Data Analysis

Exploratory data analysis (EDA) was performed before feature engineering and model development to understand the structure of the analytical dataset and to identify characteristics that could affect the subsequent modelling strategy. The analysis focused on the target variable, its temporal and geographic variation, and the relationships between home ownership and the available household and demographic characteristics.

The home-ownership rate was first examined through descriptive statistics and its distribution across the complete canton-year dataset. Its evolution over the 2019-2024 period was then analysed at both national and cantonal level. The official Swiss aggregate, which had been excluded from the modelling dataset, was retained at this stage as a descriptive benchmark for comparison with the cantonal observations.

Particular attention was given to distinguishing variation between cantons from variation within the same canton over time. This analysis was important because the dataset contains repeated annual observations for each geographic unit. Comparing these two sources of variation provided an indication of whether the analytical problem was predominantly driven by differences between cantons or by changes over time. This structure was subsequently taken into account when defining the model-validation strategy described in Section 5.4.

Household characteristics were explored using the household-size shares constructed during data preparation. Their distributions and relationships with the home-ownership rate were examined, together with correlations between the household variables themselves. Since the household-size shares represent components of the same total, their compositional structure and resulting dependencies were considered during subsequent feature selection.

The detailed population-by-age variables were also explored to identify a more interpretable representation of demographic structure. Rather than using the complete set of individual-age variables directly in the models, age information was subsequently aggregated into broader demographic groups. Population size was additionally examined as a potential explanatory characteristic.

The EDA therefore served two purposes. First, it provided a descriptive understanding of home-ownership patterns and the structure of the predictor variables. Second, it informed later methodological decisions concerning feature construction, feature selection and model validation. The resulting exploratory findings are presented separately in Section 6.1.

### 5.2 Feature Engineering and Selection

Feature engineering was performed after the exploratory analysis to reduce the dimensionality of the analytical dataset and construct a compact set of interpretable predictors. This was particularly important because the dataset contained only 156 canton-year observations, while the integrated analytical dataset retained detailed household and demographic information.

The feature-engineering process followed two main principles. First, transformations were intended to produce variables that were comparable across cantons of different sizes. Second, feature definitions were not optimised according to model performance or selected solely because of their observed relationship with the target. This was intended to preserve interpretability and reduce the risk of introducing target-driven decisions before model evaluation.

#### 5.2.1 Household Composition

Household structure was represented using the shares of private households belonging to each household-size category. The available categories comprised households with one, two, three, four, five, and six or more persons.

Using relative shares rather than only absolute household counts allowed household composition to be compared across cantons of substantially different sizes. The household shares were also examined during EDA to identify their relationships with the home-ownership rate and the dependencies between the composition variables.

Because the six household-size shares jointly represent a complete composition, they sum to one for each canton-year observation. Including all six shares together with an intercept would therefore introduce perfect linear dependence. The share of households with six or more persons was consequently omitted as the reference category, leaving five household-composition variables in the final feature set.

#### 5.2.2 Demographic Structure

The original population data contained 101 individual age variables. Using all of these variables directly would have resulted in a high-dimensional representation relative to the 156 available observations and would also have introduced substantial redundancy between neighbouring ages.

Exploratory analysis of population shares by individual age showed a structured relationship between age composition and the home-ownership rate. However, selecting individual ages or defining age boundaries according to their observed relationship with the target could introduce target-driven feature engineering and increase the risk of overfitting. The age groups were therefore defined independently of model performance.

The selected groups were aligned with demographic age classifications used by the Federal Statistical Office (FSO). Swiss population statistics distinguish age groups such as 0-19, 20-39, 40-64, 65-79 and 80 years and older (Office fédéral de la statistique, 2024). For the present analysis, the two oldest categories were combined because the objective was to obtain a compact demographic representation suitable for the relatively small analytical dataset. This resulted in four age groups:

- 0-19 years
- 20-39 years
- 40-64 years
- 65 years and older

The resulting boundaries therefore followed an externally interpretable demographic structure rather than being optimised against the home-ownership target. The 65-year threshold is also consistent with the commonly used definition of the older population in international demographic statistics (OECD, [YEAR]).

For each canton-year observation, the population count within each age group was divided by total population to obtain four demographic shares. The resulting shares were validated to ensure that they jointly represented the complete age distribution.

Since the four age-group shares sum to one, including all of them together with an intercept would introduce perfect linear dependence. The 0-19 age group was therefore omitted from the model feature set and retained as the reference category, leaving three demographic-composition variables.

<!-- TODO REFERENCES:
- Add the FSO population/demographic publication supporting the 0-19, 20-39, 40-64, 65-79 and 80+ age classification.
- Add the OECD demographic reference for the definition of population aged 65+ if retained in the final text.
-->

#### 5.2.3 Canton Population Size

Total population was retained as an indicator of canton size. Population differs substantially across Swiss cantons, and the exploratory analysis showed that the raw population variable had a pronounced right-skewed distribution (skewness = 1.90).

To obtain a more compact representation of canton size, total population was therefore log-transformed:

\[
\text{LOG\_TOTAL\_POPULATION} = \ln(1 + \text{TOTAL\_POPULATION})
\]

The transformation substantially reduced the asymmetry of the variable, with skewness decreasing from 1.90 to -0.28. As shown in Figure X, this produced a more symmetric representation while preserving the ordering of canton population sizes.

The transformation does not change the weight assigned to individual canton-year observations. It only changes the numerical representation of the population predictor by compressing large absolute differences between cantons.

[INSERT FIGURE X: population_log_transformation.png]

**Figure X.** Distribution of canton population before and after logarithmic transformation. The dashed line indicates the median. The transformation substantially reduces the right-skewness of the original population variable. Source: own elaboration based on FSO data.

#### 5.2.4 Final Feature Set

The feature-engineering and selection process resulted in nine predictors representing household composition, demographic structure and canton size.

| Feature group | Predictor |
|---|---|
| Household composition | Share of 1-person households |
| Household composition | Share of 2-person households |
| Household composition | Share of 3-person households |
| Household composition | Share of 4-person households |
| Household composition | Share of 5-person households |
| Demographic composition | Population share aged 20-39 |
| Demographic composition | Population share aged 40-64 |
| Demographic composition | Population share aged 65+ |
| Canton size | Log-transformed total population |

The share of households with six or more persons and the population share aged 0-19 were retained conceptually as reference categories but were not included as separate model predictors. Canton, year and geographic identifiers were preserved in the modelling dataset for traceability and validation but were not provided directly to the models as predictive features.

The resulting modelling dataset contained the home-ownership target, nine predictors and three identifier variables for each of the 156 canton-year observations. Integrity checks confirmed complete geographic and temporal coverage, unique canton-year combinations and the absence of missing values before model development.

### 5.3 Machine Learning Models and Baselines

The modelling stage compared a small set of regression approaches with increasing capacity to represent nonlinear relationships. Given the limited size of the modelling dataset (156 canton-year observations), the objective was not to perform an extensive model search, but to evaluate whether the selected demographic and household characteristics contained useful predictive information and whether nonlinear models could capture relationships that a simple linear specification could not.

Four regression approaches were evaluated: a mean-based baseline, Linear Regression, Random Forest, and Gradient Boosting. The same feature set described in Section 5.2 was used throughout the comparison.

#### 5.3.1 Mean-Based Baseline

A `DummyRegressor` with a mean strategy was used as the primary reference model. For each training sample, the baseline predicts the mean home-ownership rate observed in the training data.

The purpose of this model was to establish a simple reference level against which the machine-learning models could be evaluated. A model was considered useful only if it improved predictive performance relative to this baseline.

#### 5.3.2 Linear Regression

Linear Regression was included as a simple and interpretable statistical benchmark. It provides a useful reference for assessing whether the relationship between the engineered predictors and home-ownership rates can be represented adequately through a linear specification.

The model was implemented as a pipeline in which `StandardScaler` was applied before `LinearRegression`. The scaler was fitted only on the corresponding training data during validation, preventing information from the validation observations from entering the preprocessing stage.

#### 5.3.3 Random Forest

Random Forest was evaluated as a nonlinear tree-based alternative capable of representing interactions and nonlinear relationships between the predictors without requiring feature scaling.

The model was configured with 300 trees and a minimum leaf size of two observations:

- `n_estimators = 300`
- `min_samples_leaf = 2`
- `random_state = 42`

A minimum leaf size greater than one was used as a simple form of regularisation, which was considered appropriate given the small dataset.

#### 5.3.4 Gradient Boosting

Gradient Boosting was evaluated as a second nonlinear tree-based approach. The model sequentially combines shallow regression trees, allowing more complex relationships to be represented while controlling individual tree complexity.

The following specification was used:

- `n_estimators = 100`
- `learning_rate = 0.05`
- `max_depth = 2`
- `random_state = 42`

These parameters provide a relatively conservative model specification, using shallow trees and a low learning rate in view of the limited sample size.

No systematic hyperparameter optimisation was performed. This was a deliberate scope decision: the objective of the modelling stage was to compare a small number of representative model families under a consistent validation framework rather than maximise performance through extensive tuning. This also reduces the risk of adapting model-selection decisions too closely to a small dataset.

The comparative performance of the four approaches is presented in Section 6.2.

### 5.4 Validation Strategy and Evaluation Metrics

The structure of the dataset required particular attention when defining the validation strategy. The 156 observations are not independent cross-sectional records, but repeated observations of the same 26 cantons over six years. Exploratory analysis showed that differences between cantons were substantially larger than year-to-year variation within the same canton. Consequently, a conventional random train-test split could place observations from the same canton in both training and validation sets, producing an overly optimistic assessment of the model's ability to generalise geographically.

For this reason, geographic generalisation was evaluated using five-fold `GroupKFold` cross-validation, with the canton identifier (`GEO`) used as the grouping variable. All observations belonging to a given canton were therefore assigned entirely to either the training or validation subset within each fold. This design evaluates a more demanding question: whether relationships learned from a set of Swiss cantons can generalise to cantons that were not represented during model training.

The predictions generated for the held-out cantons in each fold were combined into a single set of out-of-fold predictions covering all 156 observations. Model performance was then calculated from these pooled predictions. This grouped cross-validation constituted the primary model comparison and selection framework.

Three regression metrics were used:

- **Mean Absolute Error (MAE):** measures the average absolute difference between observed and predicted home-ownership rates. Because the target is expressed as a percentage, MAE can be interpreted directly in percentage points and was used as the primary error metric.
- **Root Mean Squared Error (RMSE):** gives greater weight to larger prediction errors and complements MAE by showing whether individual observations produce comparatively large errors.
- **Coefficient of Determination (R²):** measures predictive performance relative to predicting the mean of the target. Values above zero indicate an improvement over this reference, while negative values indicate performance worse than the mean-based reference under the evaluated validation setting.

In addition to geographic cross-validation, a temporal holdout experiment was conducted. Models were trained using observations from 2019 to 2023 and evaluated on 2024. This experiment addresses a different generalisation question: prediction of a new year for cantons that were already represented in the historical training data.

A persistence baseline was also evaluated for the temporal experiment. For each canton, its observed 2023 home-ownership rate was used directly as the prediction for 2024. This provides an important benchmark because the exploratory analysis identified strong year-to-year persistence in canton-level home-ownership rates.

The geographic and temporal evaluations were therefore interpreted separately. `GroupKFold` assesses generalisation to previously unseen cantons, whereas the temporal holdout assesses prediction of a new year for known cantons. The persistence baseline further tests whether a machine-learning model provides additional predictive value beyond simply carrying forward the most recent observation.

This distinction is important when interpreting model performance, since strong results in the temporal holdout do not necessarily imply equally strong generalisation to new geographic units.

# 6. Results

## 6.1 Exploratory Findings

The exploratory analysis revealed substantial geographic variation in home-ownership rates across Swiss cantons. Across the 156 canton-year observations, the mean home-ownership rate was 39.74%, with observed values ranging from 14.0% to 58.0%. This mean represents an unweighted average of canton-year observations and should therefore not be interpreted as the national Swiss home-ownership rate, since cantons differ substantially in population size.

The geographic distribution shown in Figure X illustrates that these differences are not limited to isolated observations, but form a clear regional pattern across Switzerland. Cantons with comparatively high home-ownership rates coexist with cantons where ownership is substantially lower.

[INSERT FIGURE X: home_ownership_map.png]

**Figure X.** Average home-ownership rate across Swiss cantons over the 2019-2024 period. Source: own elaboration based on FSO data and swisstopo administrative boundaries.

Despite these substantial geographic differences, home-ownership rates within individual cantons were relatively stable over the six-year observation period. As shown in Figure X, the trajectories generally remained within relatively narrow ranges, while the differences between cantons persisted over time.

[INSERT FIGURE X: home_ownership_temporal_evolution.png]

**Figure X.** Annual canton-level home-ownership rates between 2019 and 2024. Between-canton and average within-canton standard deviations are reported in percentage points. Source: own elaboration based on FSO data.

This pattern was quantified by comparing variation between and within cantons. The standard deviation of the canton-level averages was 9.64 percentage points, whereas the average within-canton standard deviation was only 0.91 percentage points. Between-canton variation was therefore approximately 10.5 times greater than average variation within individual cantons. This result indicates that the structure of the target variable over the analysed period is predominantly geographic rather than temporal. It also provides empirical support for treating observations from the same canton as dependent when defining the subsequent validation strategy.

Household composition also showed systematic associations with home ownership. Figure X presents the Pearson correlations between the household-size shares and the target variable. The share of two-person households showed the strongest positive correlation (0.36), while the share of three-person households showed the strongest negative correlation (-0.41). The remaining household-size categories exhibited weaker linear associations.

[INSERT FIGURE X: household_homeownership_correlation.png]

**Figure X.** Pearson correlations between household-size shares and canton-level home-ownership rates, 2019-2024. Source: own elaboration based on FSO data.

These correlations are descriptive and should not be interpreted as causal effects. Household-size shares are also compositional variables, meaning that the categories are structurally dependent because their values sum to one. This dependency was considered during feature construction by excluding one household-size category as a reference, as described in Section 5.2.

The demographic exploration showed a similarly structured pattern. Figure X presents the correlation between the population share at each individual age and the home-ownership rate. Rather than showing isolated relationships at specific ages, the results reveal broader patterns across consecutive age ranges. Population shares across much of the younger and middle-adult range were negatively correlated with home ownership, whereas the relationship became predominantly positive at older ages.

[INSERT FIGURE X: age_homeownership_correlation.png]

**Figure X.** Pearson correlation between individual-age population shares and canton-level home-ownership rates, 2019-2024. Source: own elaboration based on FSO data.

As discussed in Section 5.2, these individual-age correlations were used for exploratory analysis rather than for target-driven feature selection. The final demographic representation therefore used broader age groups, defined independently of these correlations and aligned with the demographic grouping approach described in the methodology.

Overall, the exploratory analysis identified three characteristics that directly influenced the subsequent modelling strategy: substantial geographic heterogeneity in home ownership, strong temporal persistence within cantons, and systematic differences in household and demographic composition across cantons.

## 6.2 Model Performance

The four modelling approaches were evaluated under the canton-grouped cross-validation strategy described in Section 5.4. Under this setting, complete cantons were excluded from each training fold, so the reported out-of-fold predictions represent performance on cantons not observed during the corresponding model training.

Table X summarises the performance obtained across the complete set of out-of-fold predictions.

| Model | MAE (pp) | RMSE (pp) | R² |
|---|---:|---:|---:|
| Gradient Boosting | **6.05** | **7.62** | **0.359** |
| Random Forest | 6.56 | 7.86 | 0.317 |
| Mean baseline | 7.51 | 9.74 | -0.049 |
| Linear Regression | 8.71 | 11.56 | -0.479 |

**Table X.** Model performance under 5-fold canton-grouped cross-validation. MAE and RMSE are expressed in percentage points. Source: own elaboration.

Gradient Boosting achieved the best performance across all three evaluation metrics, with an MAE of 6.05 percentage points, an RMSE of 7.62 percentage points, and an R² of 0.359. Compared with the mean baseline, which obtained an MAE of 7.51 percentage points, Gradient Boosting reduced the mean absolute error by approximately 19.4%. This indicates that the demographic and household predictors provide additional predictive information beyond simply predicting the mean home-ownership rate of the training data.

Random Forest produced similar but slightly weaker results, with an MAE of 6.56 percentage points and an R² of 0.317. In contrast, Linear Regression performed worse than the mean baseline, obtaining an MAE of 8.71 percentage points and a negative R² of -0.479. This indicates that the linear model did not capture the relationship between the selected predictors and home ownership effectively under the unseen-canton evaluation setting.

Figure X compares the observed home-ownership rates with the out-of-fold predictions generated by Gradient Boosting. Predictions closer to the diagonal correspond to smaller prediction errors.

[INSERT FIGURE X: gradient_boosting_observed_vs_predicted.png]

**Figure X.** Observed and predicted home-ownership rates for Gradient Boosting using out-of-fold predictions from canton-grouped cross-validation. The dashed diagonal represents perfect agreement between observed and predicted values. Source: own elaboration.

The figure shows that the model captures part of the variation between cantons, but its predictions are more concentrated around intermediate home-ownership rates than the observed values. Larger deviations can be seen for some observations toward the extremes of the target distribution. This is consistent with the moderate R² of 0.359 and indicates that substantial canton-level variation remains unexplained by the selected demographic and household predictors.

Based on this comparison, Gradient Boosting was selected as the final model for the subsequent analyses and the Swiss Data Intelligence MVP. Its performance should nevertheless be interpreted in the context of the relatively small dataset and the demanding unseen-canton validation setting. Geographic and temporal generalisation are examined separately in Section 6.3.

## 6.3 Geographic and Temporal Generalisation

The results presented in Section 6.2 evaluate geographic generalisation: whether the model can estimate home-ownership rates for cantons that were not represented during training. A second experiment was conducted to examine a different question: whether the model can predict a new year for cantons already observed in previous years.

For this temporal evaluation, the Gradient Boosting model was trained using observations from 2019 to 2023 and evaluated exclusively on 2024. This resulted in 130 training observations and 26 test observations, with one 2024 observation for each canton.

Table X compares the main geographic evaluation with the temporal holdout results. A persistence baseline is also included for the temporal experiment. This baseline predicts each canton's 2024 home-ownership rate using its observed value from 2023.

| Evaluation scenario | Model | MAE (pp) | RMSE (pp) | R² |
|---|---|---:|---:|---:|
| Unseen cantons | Gradient Boosting, GroupKFold | 6.05 | 7.62 | 0.359 |
| New year 2024 | Gradient Boosting | 2.29 | 3.16 | 0.885 |
| New year 2024 | 2023 persistence baseline | **1.20** | **1.78** | **0.964** |

**Table X.** Comparison of geographic and temporal generalisation. The evaluation scenarios address different prediction tasks and their metrics should therefore not be interpreted as directly equivalent measures of model performance. Source: own elaboration.

Gradient Boosting performed substantially better in the temporal holdout than in the unseen-canton evaluation. Its MAE decreased from 6.05 to 2.29 percentage points, while R² increased from 0.359 to 0.885. However, this difference should not be interpreted as evidence that the model becomes intrinsically more accurate under temporal validation. The two experiments represent different prediction problems.

In the temporal holdout, the model has already been exposed during training to observations from the same 26 cantons in previous years. As shown in Section 6.1, home-ownership rates exhibit strong temporal persistence within cantons. Predicting 2024 for a canton with observations available from previous years is therefore considerably different from estimating home ownership for a canton that has never been observed during training.

This interpretation is further supported by the persistence baseline. Simply using each canton's observed 2023 home-ownership rate as its prediction for 2024 produced an MAE of 1.20 percentage points and an R² of 0.964, outperforming Gradient Boosting in the temporal holdout.

The persistence result indicates that much of the predictive performance in the temporal experiment can be explained by the stability of canton-level home-ownership rates between consecutive years. Consequently, the high temporal R² of the Gradient Boosting model should not be interpreted in isolation as evidence of strong generalisation to new geographic units.

Taken together, the two experiments reveal an important distinction. The available demographic and household characteristics provide some predictive information for previously unseen cantons, as demonstrated by the results in Section 6.2, but predicting the next observation for an already known canton is a substantially easier task because of the strong temporal persistence of the target.

## 6.4 Model Interpretation and Error Analysis

To better understand the performance of the selected Gradient Boosting model, the out-of-fold prediction errors from the canton-grouped cross-validation were analysed at canton level. Figure X shows the mean absolute error obtained for each canton across its six annual observations.

[INSERT FIGURE X: gradient_boosting_mae_by_canton.png]

**Figure X.** Mean absolute prediction error by canton for Gradient Boosting under canton-grouped cross-validation. Errors are expressed in percentage points. Source: own elaboration.

Prediction accuracy varied substantially across cantons. The largest mean absolute error was observed for Basel-Stadt (17.67 percentage points), followed by Genève (13.52), Neuchâtel (11.68), and Valais (11.26). Other cantons were estimated considerably more accurately.

The distribution of errors does not appear to be explained simply by whether a canton has a particularly high or low home-ownership rate. For example, Zürich has a comparatively low average home-ownership rate but an MAE of only 1.87 percentage points. This suggests that the selected demographic and household characteristics capture the structure of some cantons more effectively than others. Canton-specific factors not represented in the current feature set may therefore contribute to the remaining prediction errors.

The fitted Gradient Boosting model was also examined through its feature importances. Figure X shows the relative impurity-based importance assigned to each predictor in the final model fitted on the complete analytical dataset.

[INSERT FIGURE X: gradient_boosting_feature_importance.png]

**Figure X.** Impurity-based feature importance of the final Gradient Boosting model fitted on the complete 2019-2024 dataset. Source: own elaboration.

The share of the population aged 20-39 was assigned the highest importance (0.624), considerably above all other predictors. Log-transformed total population followed with an importance of 0.080, while the share of four-person households (0.071), population aged 40-64 (0.068), and population aged 65+ (0.054) contributed smaller shares of the model's total feature importance.

These values describe how the fitted Gradient Boosting model used the available predictors and should not be interpreted as causal effects or as the proportion of variation in home ownership explained by each variable. In addition, several demographic and household predictors are related by construction, so importance may be distributed unevenly among correlated features.

Taken together, the error analysis and feature importance results indicate that the model relies strongly on demographic structure, particularly the population share aged 20-39, but that the available predictors do not capture canton-level differences equally well. The comparatively large errors observed for several cantons suggest that relevant explanatory factors remain outside the current feature set. This limitation is considered further in Section 8.2.


# 7. Swiss Data Intelligence MVP

The final stage of the project integrated the prepared public data, analytical results, and selected machine-learning model into a functional minimum viable product (MVP). The objective of the MVP was not to develop a production-ready platform, but to demonstrate how the different components developed throughout the project could be combined into an interactive application for exploring Swiss canton-level data.

## 7.1 System Design and Implementation

Swiss Data Intelligence was implemented as a lightweight Streamlit application built on top of the processed analytical data and the final Gradient Boosting model. The implementation follows the same workflow developed throughout the project, keeping data preparation, exploratory analysis, modelling, and application logic conceptually separated.

The application consumes the processed canton-year modelling dataset generated during the data preparation and feature-engineering stages. The final Gradient Boosting model is stored separately as a serialized model artifact together with the exact feature list required for inference. When the application starts, both the processed dataset and the model artifact are loaded, ensuring that model inference uses the same feature representation defined during model development.

Geographic visualisation is integrated using official canton boundaries from swisstopo. These geometries are harmonised with the FSO geographic identifiers used in the analytical dataset, allowing statistical observations and geographic information to be joined consistently across all 26 cantons.

Figure X summarises the complete workflow implemented in the MVP, from the original public data sources through data preparation, exploratory analysis and modelling, to the final interactive application.

[INSERT FIGURE X: swiss_data_intelligence_mvp_architecture.png]

**Figure X.** Simplified architecture and data flow of the Swiss Data Intelligence MVP, from the original public datasets through data preparation and modelling to the interactive Streamlit application. Source: own elaboration.

Within the application, users select a canton and year from the available 2019-2024 observations. The corresponding demographic and household features are extracted from the processed dataset and passed to the stored Gradient Boosting model using the exact feature set and ordering retained in the model artifact. The resulting model estimate is then presented together with the observed home-ownership rate.

Because the final model used by the application was fitted on the complete 2019-2024 dataset, estimates displayed for historical canton-year observations are in-sample fitted estimates. Their difference from the observed value is therefore reported as a fitted residual and should not be interpreted as an out-of-sample prediction error. The out-of-sample performance of the model is instead represented by the validation results reported in Chapter 6.

The implementation also incorporates several consistency checks. Geographic integration is validated to ensure that all 26 cantons are successfully matched, while the stored model feature list is used directly during inference to avoid inconsistencies between training and application input. Streamlit caching is used for static data, geographic resources, and the model artifact to avoid unnecessary repeated loading during application interaction.

The architecture deliberately remains simple and focused on the objectives of the project. The MVP does not include automated data ingestion, automatic model retraining, external APIs, or production deployment infrastructure. These components were outside the scope of the current work. Instead, the implemented application demonstrates an end-to-end workflow from official Swiss public data to reproducible analysis, machine-learning inference, geographic visualisation, and interactive exploration.

## 7.2 Interactive Application

The interactive application provides a user-oriented interface for exploring the canton-year dataset and the outputs of the machine-learning workflow. Rather than exposing the underlying data-processing and modelling code, the application organises the main analytical components into a single interface in which users can select a canton and year and examine the corresponding information.

The application initially provides an overview of the dataset, including its geographic and temporal coverage. Users can then select one of the 26 Swiss cantons and an available year between 2019 and 2024. This selection is used consistently across the different components of the interface, allowing the demographic, household, home-ownership, geographic, and model information to be explored for the same canton-year observation.

For the selected canton, the application presents a demographic profile based on the age-group shares constructed during feature engineering, together with the distribution of private households by household size. The omitted reference categories used during modelling are reconstructed for visualisation, allowing the interface to display the complete demographic and household compositions rather than only the predictors provided to the model.

Historical context is provided through the evolution of the selected canton's home-ownership rate between 2019 and 2024. The canton is shown together with the unweighted average across the 26 cantons, providing a descriptive reference for interpreting its relative position over the available period. A geographic view complements this temporal perspective by displaying home-ownership rates across Switzerland and highlighting the selected canton.

The application also presents the observed home-ownership rate together with the estimate produced by the final Gradient Boosting model. As explained in Section 7.1, the model used by the application was fitted on the complete 2019-2024 dataset. The difference between the observed and fitted values is therefore labelled as a **fitted residual**, rather than as a prediction error, to distinguish the interactive historical estimate from the out-of-sample evaluation performed during model validation.

Model estimates are accompanied by the main validation results so that they are not presented without information about their predictive performance. The interface distinguishes between generalisation to unseen cantons, prediction of the new year 2024, and the 2023 persistence baseline. This makes the different evaluation scenarios visible alongside the interactive model output and reduces the risk of interpreting the fitted historical estimates as evidence of out-of-sample accuracy.

Figures X(a-c) illustrate the main components of the implemented MVP. Figure X(a) presents the application overview and dataset coverage. Figure X(b) shows the interactive canton exploration, including demographic and household profiles, historical home-ownership evolution, and the model estimate. Figure X(c) presents the model-evaluation results together with the geographic comparison of home-ownership rates across cantons.

[INSERT FIGURE X(a): mvp_interface_01.png]

[INSERT FIGURE X(b): mvp_interface_02.png]

[INSERT FIGURE X(c): mvp_interface_03.png]

**Figure X.** Main components of the Swiss Data Intelligence MVP: (a) application overview and dataset coverage; (b) interactive canton exploration, demographic and household profiles, historical home-ownership evolution, and model estimate; and (c) model evaluation and geographic comparison. Source: own elaboration.

The resulting MVP demonstrates how the complete analytical workflow can be exposed through an interactive interface without requiring users to work directly with the underlying datasets, notebooks, or Python code. It therefore serves both as a demonstration of the technical integration achieved in the project and as a functional foundation for future extensions of Swiss Data Intelligence.

# 8. Discussion and Conclusions

## 8.1 Discussion of Results

This project investigated to what extent demographic characteristics and household structure can explain and predict differences in home-ownership rates across Swiss cantons. The results indicate that these characteristics contain relevant predictive information, but that their explanatory and predictive capacity depends strongly on the type of generalisation being considered.

One of the clearest findings of the exploratory analysis was the strong geographic structure of Swiss home ownership. Differences between cantons were substantially larger than changes within individual cantons over the 2019-2024 period: the between-canton standard deviation was 9.64 percentage points, compared with an average within-canton standard deviation of only 0.91 percentage points. This confirms that, for the period analysed, home ownership is characterised primarily by persistent differences between cantons rather than by large year-to-year changes within them.

This geographic structure is consistent with previous research showing that home ownership in Switzerland is associated with substantial regional differences and cannot be understood exclusively through individual demographic characteristics. Bourassa et al. (2015), for example, identify important spatial variation in Swiss home ownership and discuss the role of economic, demographic, institutional, and housing-market characteristics. Similarly, Bolliger et al. (2025) emphasise the relevance of regional context when analysing housing outcomes in Switzerland. The results of the present project are consistent with this broader view: demographic and household variables capture part of the observed geographic variation, but they do not provide a complete explanation of canton-level differences.

This is particularly visible in the unseen-canton evaluation. Gradient Boosting achieved the best performance among the evaluated models, with an MAE of 6.05 percentage points and an R² of 0.359 under canton-grouped cross-validation. Compared with the mean baseline, the model reduced MAE by approximately 19.4%. The selected predictors therefore contain information that generalises beyond the cantons used for model training. At the same time, an R² of 0.359 indicates that a substantial proportion of the variation between previously unseen cantons remains unexplained.

The comparison between modelling approaches also suggests that the relationship between the selected characteristics and home ownership is not adequately represented by a simple linear specification. Linear Regression performed worse than the mean baseline, whereas both tree-based ensemble models achieved better results. This observation is compatible with findings in the tabular machine-learning literature showing that tree-based methods can remain highly competitive for structured datasets and can capture nonlinear relationships and interactions without requiring an explicit functional specification (Grinsztajn et al., 2022). However, given the small sample size of the present study, the comparison should be interpreted as evidence specific to this dataset rather than as a general conclusion about model families.

The temporal holdout produced a very different result. When Gradient Boosting was trained on 2019-2023 and evaluated on 2024, it achieved an MAE of 2.29 percentage points and an R² of 0.885. Considered alone, these values could suggest very strong predictive performance. However, the persistence baseline, which simply used each canton's 2023 observed rate as its prediction for 2024, performed even better, with an MAE of 1.20 percentage points and an R² of 0.964.

This comparison is important for interpreting the modelling results. The strong temporal performance is largely associated with the stability of home-ownership rates within cantons rather than with the machine-learning model discovering a highly generalisable predictive relationship. In contrast, canton-grouped cross-validation removes this advantage by requiring predictions for geographic units that were completely absent during training. The substantial difference between these two evaluation scenarios demonstrates why the validation strategy must reflect the intended prediction problem when working with structured regional data. This is consistent with the broader methodological literature on dependent and spatially structured observations, which warns that conventional validation strategies can provide overly optimistic estimates when training and validation observations are not sufficiently independent (Roberts et al., 2017; Wang et al., 2023).

The model interpretation and error analysis provide additional evidence that demographic and household characteristics represent only part of the mechanisms associated with home ownership. The population share aged 20-39 received the highest feature importance in the fitted Gradient Boosting model, while population size and several household and age-group variables contributed smaller amounts. These importances describe how the model uses the available predictors and should not be interpreted as causal effects. In particular, the demographic and household variables are related to each other, and the importance assigned by a tree-based model may be distributed unevenly among correlated predictors.

Prediction errors also differed considerably between cantons. Basel-Stadt, Genève, Neuchâtel, and Valais were among the cantons with the largest errors under grouped cross-validation, while other cantons were estimated substantially more accurately. Since these errors were not simply concentrated at the highest or lowest observed home-ownership rates, the pattern suggests that additional canton-specific characteristics are not represented by the current feature set. Potentially relevant dimensions identified in previous housing research include housing prices, income and wealth, taxation, housing supply, urbanisation, and other institutional or regional characteristics (Bourassa et al., 2015; Delbiaggio et al., 2018). These variables were outside the scope of the current MVP but provide plausible directions for extending the analytical dataset.

Overall, the research question can therefore be answered with a qualified conclusion. Demographic characteristics and household structure explain and predict a meaningful part of the differences in home-ownership rates across Swiss cantons, as demonstrated by the improvement over the mean baseline under unseen-canton validation. However, their predictive capacity is moderate when generalising to cantons not represented during training, and substantial geographic variation remains unexplained. The much stronger performance observed when predicting a new year for already known cantons is largely influenced by the temporal persistence of the target. The results therefore support the usefulness of the selected public data for regional analysis while also showing the limits of interpreting predictive performance without considering the geographic and temporal structure of the underlying data.

## 8.2 Limitations and Critical Reflection

The results of this project should be interpreted in the context of several limitations related to the available data, the modelling design, and the scope of the MVP. These limitations do not invalidate the analytical workflow, but they define the boundaries within which the results can be interpreted.

A first limitation is the relatively small size of the analytical dataset. After harmonising the selected FSO datasets, the final dataset contained 156 observations, corresponding to 26 cantons observed annually between 2019 and 2024. Although each observation contains detailed demographic and household information, the effective amount of independent geographic information remains limited because observations from the same canton are related over time. This was one of the main reasons for using canton-grouped cross-validation rather than a conventional random train-test split.

The six-year observation period also limits the temporal dimension of the analysis. Home-ownership rates changed relatively little within individual cantons during 2019-2024, as demonstrated by the substantially lower within-canton variation compared with the variation between cantons. Consequently, the dataset is better suited to studying geographic differences than long-term changes in home ownership. The temporal holdout experiment should therefore be interpreted as prediction of the next observation within a period of strong stability rather than as evidence of long-term forecasting capability.

A further limitation concerns the selection of explanatory variables. The final model uses demographic structure, household composition, and canton population size because these variables could be obtained from compatible official public datasets and harmonised consistently across cantons and years. However, home ownership is influenced by factors that extend beyond these dimensions. Variables related to property prices, household income and wealth, taxation, housing supply, urbanisation, financing conditions, and other regional or institutional characteristics may provide additional explanatory information. Their absence is a plausible reason why substantial variation remains unexplained when the model is evaluated on previously unseen cantons.

This feature selection reflects an important practical trade-off encountered during the project. The original concept of Swiss Data Intelligence was broader than the final analytical scope, and numerous public datasets were considered during data discovery. In practice, differences in temporal coverage, geographic granularity, file structure, and availability limited the number of datasets that could be integrated reliably within the available project time. The final dataset therefore prioritised consistency and reproducibility over the inclusion of a larger number of potentially relevant but less compatible data sources.

The aggregation of the analysis at canton level represents another limitation. Cantons are heterogeneous geographic units, and substantial variation may exist between municipalities or regions within the same canton. Canton-level observations cannot capture these local differences. The relationships identified in this project should consequently be interpreted as associations between aggregated regional characteristics rather than as relationships that necessarily apply to individual households or persons.

The modelling strategy also involved deliberate simplifications. Four modelling approaches were compared, but no systematic hyperparameter optimisation was performed. Given the small dataset and the objective of developing an interpretable and reproducible MVP, extensive tuning was considered unlikely to provide sufficient additional value relative to the risk of adapting the modelling process too closely to the available observations. The reported performance therefore reflects relatively simple model configurations rather than an attempt to maximise predictive accuracy.

The feature-importance analysis has additional interpretative limitations. The reported Gradient Boosting importances are impurity-based measures from the final fitted model. They indicate how the model used the available predictors but do not quantify causal effects or the proportion of the target explained independently by each variable. This distinction is particularly relevant because both demographic and household variables contain structural dependencies. Feature importance was therefore used as a descriptive model interpretation tool rather than as evidence that individual predictors determine home-ownership rates.

The validation experiments themselves also require careful interpretation. Canton-grouped cross-validation provides a more demanding assessment of generalisation to previously unseen cantons than a random observation-level split, but it does not constitute a strict spatial cross-validation design based on geographic distance or spatial blocks. Conversely, the 2024 temporal holdout preserves geographic overlap between training and test data and therefore benefits from the strong persistence of canton-level home-ownership rates. Neither evaluation strategy should be interpreted as universally representative of model performance; instead, they address two different generalisation questions.

The persistence baseline was particularly useful in revealing this distinction. Without this comparison, the R² of 0.885 obtained by Gradient Boosting for the 2024 temporal holdout could easily be interpreted as evidence of strong forecasting performance. The fact that a simple 2023 persistence prediction achieved an even higher R² of 0.964 demonstrated that much of this apparent performance is associated with temporal stability in the target. This result represents an important methodological finding of the project and illustrates the value of selecting baselines that reflect the structure of the prediction problem rather than relying only on generic model comparisons.

Finally, the Swiss Data Intelligence application should be understood as a functional MVP rather than a production system. Data ingestion and model retraining are not automated, and the application operates on the processed 2019-2024 dataset and a previously trained model artifact. The application demonstrates the integration of public data, analytical processing, machine learning, geographic information, and interactive visualisation, but additional engineering would be required for continuous data updates, automated model lifecycle management, deployment, monitoring, and operation as a production service.

These limitations also reflect a deliberate scope decision. Rather than expanding the project with additional technologies or datasets without sufficient time for validation, the final implementation focused on completing and evaluating an end-to-end analytical workflow. This made it possible to examine not only whether a machine-learning model could be trained, but also how its apparent performance changes depending on the validation strategy and how those results should be communicated in an interactive application. In this sense, the limitations identified during the project are also relevant outcomes of the work, as they define both the current capabilities of Swiss Data Intelligence and the areas where future development would provide the greatest value.

## 8.3 Conclusions and Future Work

This project developed Swiss Data Intelligence as an end-to-end machine-learning workflow for exploring home-ownership patterns across Swiss cantons using official public data. Starting from heterogeneous datasets published by the Federal Statistical Office, the project covered data discovery, ingestion, harmonisation, exploratory analysis, feature engineering, model development, validation, interpretation, and the integration of the final analytical workflow into an interactive Streamlit application.

The results provide a qualified answer to the research question. Demographic characteristics and household structure contain useful information for explaining and predicting differences in home-ownership rates across Swiss cantons, but they capture only part of the observed geographic variation. Under canton-grouped cross-validation, Gradient Boosting achieved the best performance of the evaluated models, with an MAE of 6.05 percentage points and an R² of 0.359. Its MAE was approximately 19.4% lower than that of the mean baseline, demonstrating predictive value beyond a simple average while also showing that substantial canton-level variation remains unexplained.

An important outcome of the project was the distinction between geographic and temporal generalisation. Predicting 2024 for cantons already represented in the training data resulted in substantially higher apparent performance than predicting previously unseen cantons. However, the persistence baseline outperformed Gradient Boosting in the temporal experiment, demonstrating that much of this performance can be attributed to the strong year-to-year stability of canton-level home-ownership rates. This finding highlights the importance of selecting validation strategies and baselines that reflect the actual structure of the prediction problem.

Beyond the predictive results, the project demonstrates the feasibility of integrating multiple Swiss public datasets into a reproducible analytical workflow. The resulting MVP connects processed public data, machine-learning outputs, geographic information, and interactive visualisation within a single application. Users can explore demographic and household profiles, historical home-ownership patterns, geographic differences, model estimates, and validation results without interacting directly with the underlying notebooks or Python code.

Future work should initially focus on improving the analytical dataset rather than increasing model complexity. Incorporating additional variables related to property prices, income and wealth, taxation, housing supply, urbanisation, financing conditions, and other regional characteristics could help explain canton-level differences that are not captured by the current demographic and household predictors. Extending the analysis to a longer historical period or to finer geographic units, such as municipalities, could also provide a richer basis for studying temporal and local variation.

Further methodological development could include more explicitly spatial validation strategies, additional model interpretation techniques, and systematic model optimisation once a larger dataset is available. These extensions would be most meaningful after strengthening the underlying data, since the current results suggest that missing explanatory information is a more important limitation than model complexity.

From an engineering perspective, Swiss Data Intelligence could also be extended with automated ingestion of updated public datasets, data-quality validation, model retraining and versioning, and deployment and monitoring components. Such capabilities would transform the current static analytical workflow into a more continuously maintained data product.

A longer-term extension could introduce a natural-language interface for interacting with the available public data. An LLM-based routing or retrieval layer could translate user questions into appropriate analytical operations and make the platform accessible to users without technical knowledge. This functionality was part of the broader Swiss Data Intelligence concept but was deliberately excluded from the current MVP in order to prioritise a complete and validated data and machine-learning workflow.

Overall, the project demonstrates both the potential and the limitations of applying machine learning to structured Swiss public data. The main contribution is not only the final predictive model, but the complete and reproducible process connecting public data acquisition, analytical modelling, critical validation, and an interactive application. Swiss Data Intelligence therefore provides a functional foundation that can be progressively extended as additional data sources, analytical methods, and application capabilities become available.

## References

opendata.swiss. (n.d.). About us. https://opendata.swiss/en/about

Federal Statistical Office. (n.d.). Buildings. https://www.bfs.admin.ch/bfs/en/home/statistics/construction-housing/



## Appendix

## AI / Tools Disclosure