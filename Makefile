clean_data/product.csv: raw_data/product.csv clean_dataset.py
	mkdir -p clean_data
	cat $< | python clean_dataset.py $@

clean_data/product_class.csv: raw_data/product_class.csv clean_dataset.py
	cat $< | python clean_dataset.py $@

clean_data/promotion.csv: raw_data/promotion.csv clean_dataset.py
# Clean up media_type values. Replace ', ' with pipes after line 1.
	cat $< | sed -e '2,$ s/, / | /g' | python clean_dataset.py $@

clean_data/transactions.csv: raw_data/transactions.csv clean_dataset.py
# Clean up fact_count values. Strip ');' characters from integers.
	cat $< | sed 's/1);/1/g' | python clean_dataset.py $@

clean_datasets: clean_data/product.csv clean_data/product_class.csv clean_data/promotion.csv clean_data/transactions.csv
