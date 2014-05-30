all:

runserver:
	jekyll serve -w -H 0.0.0.0 -P 8080

scss:
	sass --style compressed --watch css/