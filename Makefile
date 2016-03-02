# Make directory for clean dataset, if it doesn't already exist.
clean_data:
	mkdir -p $@

# Clean products, product classes, promotions, and transactions.
clean_data/product.csv: raw_data/product.csv clean_dataset.py clean_data
	cat $< | python clean_dataset.py $@

clean_data/product_class.csv: raw_data/product_class.csv clean_dataset.py clean_data
	cat $< | python clean_dataset.py $@

clean_data/promotion.csv: raw_data/promotion.csv clean_dataset.py clean_data
	# Clean up media_type values. Use sed to replace ', ' with pipes after line 1.
	# Note: make interprets '$' as a variable, '$$' makes sed filter work correctly.
	cat $< | sed -e '2,$$ s/, / | /g' | python clean_dataset.py $@

clean_data/transactions.csv: raw_data/transactions.csv clean_dataset.py clean_data
	# Clean up fact_count values. Used sed to strip ');' characters from integers.
	cat $< | sed 's/1);/1/g' | python clean_dataset.py $@

# Clean all datasets, if they haven't been cleaned already.
.PHONY: clean_datasets
clean_datasets: clean_data/product.csv clean_data/product_class.csv clean_data/promotion.csv clean_data/transactions.csv
