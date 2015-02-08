all:

runserver:
	jekyll serve -w -H 0.0.0.0 -P 8080 --force_polling

scss:
	sass --style compressed --poll --watch css/
