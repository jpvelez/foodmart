############
# CLEANING #
############
# Make directory for clean dataset, if it doesn't already exist.
clean_data:
	mkdir -p $@

# Clean products, product classes, promotions, and transactions.
clean_data/product.pkl: raw_data/product.csv clean_dataset.py clean_data
	cat $< | python clean_dataset.py $@

clean_data/product_class.pkl: raw_data/product_class.csv clean_dataset.py clean_data
	cat $< | python clean_dataset.py $@

clean_data/promotion.pkl: raw_data/promotion.csv clean_dataset.py clean_data
	# Clean up media_type values. Use sed to replace ', ' with pipes after line 1.
	# Note: make interprets '$' as a variable, '$$' makes sed filter work correctly.
	cat $< | sed -e '2,$$ s/, / | /g' | python clean_dataset.py $@

clean_data/transactions.pkl: raw_data/transactions.csv clean_dataset.py clean_data
	# Clean up fact_count values. Used sed to strip ');' characters from integers.
	cat $< | sed 's/1);/1/g' | python clean_dataset.py $@

# Clean all datasets, if they haven't been cleaned already.
.PHONY: clean_datasets
clean_datasets: clean_data/product.pkl clean_data/product_class.pkl clean_data/promotion.pkl clean_data/transactions.pkl


############
# ANALYSIS #
############
# Run sanity check analysis, which lives in a jupyter notebook, and save output to HTML.
notebooks/data_quality_analysis.html: clean_data/product.pkl clean_data/product_class.pkl clean_data/promotion.pkl clean_data/transactions.pkl notebooks/data_quality_analysis.ipynb
	# Assign first 4 input files, the dataset filenames, to DATASET var.
	$(eval DATASETS='$(wordlist 1, 4, $^)')
	# Execute notebook cells with datasets as input, and send HTML output to stdout.
  # Dataset filenames are passed to notebook using temp env var `datasets`.
	datasets=$(DATASETS) jupyter nbconvert --execute notebooks/data_quality_analysis.ipynb --to html --stdout > $@

# Run complete analysis notebook for question one, save output to HTML.
notebooks/question_one.html: clean_data/product.pkl clean_data/product_class.pkl clean_data/promotion.pkl clean_data/transactions.pkl notebooks/question_one.ipynb
	$(eval DATASETS='$(wordlist 1, 4, $^)')
	datasets=$(DATASETS) jupyter nbconvert --execute notebooks/question_one.ipynb --to html --stdout > $@

# Run complete analysis notebook for question two, save output to HTML.
notebooks/question_two.html: clean_data/product.pkl clean_data/product_class.pkl clean_data/promotion.pkl clean_data/transactions.pkl notebooks/question_one.ipynb
	$(eval DATASETS='$(wordlist 1, 4, $^)')
	datasets=$(DATASETS) jupyter nbconvert --execute notebooks/question_two.ipynb --to html --stdout > $@

# Run executive summary notebook, save output to HTML.
notebooks/executive_summary.html: notebooks/question_one.html notebooks/question_two.html
	jupyter nbconvert --execute notebooks/executive_summary.ipynb --to html --stdout > $@

.PHONY: all_analyses
all_analyses: notebooks/data_quality_analysis.html notebooks/question_one.html notebooks/question_two.html notebooks/executive_summary.html
