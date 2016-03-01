clean_data/product.csv: raw_data/product.csv
	mkdir -p clean_data
	python clean_dataset.py $< > $@
