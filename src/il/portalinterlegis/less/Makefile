# COMPILACAO DOS ARQUIVOS LESS
#
# Requisitos:
# sudo apt-getitude install libyaml-dev  # (para o watchdog, nao obrigatorio mas preferivel)
# sudo pip install watchdog
# sudo npm install -g recess

BOOTSTRAP_LESS = ./bootstrap/less/bootstrap.less
BOOTSTRAP_CSS = ../static/bootstrap/css/bootstrap.min.css

BOOTSTRAP_RESPONSIVE_LESS = ./bootstrap/less/responsive.less
BOOTSTRAP_RESPONSIVE_CSS = ../static/bootstrap/css/bootstrap-responsive.min.css

build: bootstrap portal

clean:
	rm -r ../static/bootstrap

bootstrap: bootstrap-img bootstrap-css

bootstrap-img: ../static/bootstrap/img/*
../static/bootstrap/img/*: bootstrap/img/*
	mkdir -p ../static/bootstrap/img
	cp bootstrap/img/* ../static/bootstrap/img

bootstrap-css: ../static/bootstrap/css/*.css
../static/bootstrap/css/*.css: bootstrap/less/*.less
	mkdir -p ../static/bootstrap/css
	recess --compress ${BOOTSTRAP_LESS} > ${BOOTSTRAP_CSS}
	recess --compress ${BOOTSTRAP_RESPONSIVE_LESS} > ${BOOTSTRAP_RESPONSIVE_CSS}

portal: ../static/css/style.css
../static/css/style.css: portal/style.less
	recess --compress portal/style.less > ../static/css/style.css

watch:
	echo "Watching PORTAL less files..."; \
	watchmedo shell-command --recursive --command='make portal' portal

watch-all:
	echo "Watching all files (portal + bootstrap)..."; \
	watchmedo shell-command --recursive --command='make' .

.PHONY: build clean bootstrap bootstrap-img bootstrap-css portal watch watch-all