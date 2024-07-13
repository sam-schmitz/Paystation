# very simple Makefile

help:
	echo target: tests clean_src clean_test clean zip

tests:
	python -m unittest

clean_src:
	rm -rf paystation/__pycache__
	find paystation -name '*~' -delete

clean_test:
	rm -rf test/__pycache__
	find paystation -name '*~' -delete

clean: clean_src clean_test
	find . -name paystation.zip -delete 
	rm -rf __pycache__
	find . -name '*~' -delete

zip: clean
	zip -r paystation.zip paystation test Makefile
