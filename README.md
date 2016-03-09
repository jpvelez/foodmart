# Foodmart Data Analysis

To view executive summary of the analysis, [click here]. To view the data quality analysis, [click here](notebooks/data_quality_analysis.html). For in-depth analysis of question one, [click here](notebooks/question_one.html); for question two, [click here](notebooks/question_two.html).

## Installation
To run this analysis, you'll need Make and Python 3.5 installed. To install the necessary python packages, you'll also need [Anaconda](https://docs.continuum.io/anaconda/install).

Once you have Anaconda, type this to make a new virtual environments with all the packages you need:
`conda create --name foodmart_analysis --file requirements.txt`

## Usage
To run the analysis, type
`make all_analyses`

This will clean the analysis data and generate all reports dynamically, savings them as `.html` files within `/notebooks`.
