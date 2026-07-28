MAIN = main
LUA = lualatex
FLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: build clean watch

build:
	$(LUA) $(FLAGS) $(MAIN).tex
	$(LUA) $(FLAGS) $(MAIN).tex

clean:
	rm -f *.aux *.log *.out *.toc *.fls *.fdb_latexmk *.synctex.gz
	rm -f $(MAIN).pdf

watch:
	while true; do \
		inotifywait -e modify **/*.tex; \
		sleep 1; \
		$(LUA) $(FLAGS) $(MAIN).tex 2>&1 | tail -5; \
	done
