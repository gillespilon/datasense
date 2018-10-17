test:
	@pytest -vv

coverage:
	@coverage html

# Hehe
.PHONY: test coverage
