# Builds the source RPM. Used by the GitHub Actions repo workflow and `just rpm`.
#   make srpm outdir=<dir>
NAME    := hafnium-dots
TOP     := $(shell git rev-parse --show-toplevel)
GIT     := git -c safe.directory='*' -C "$(TOP)"
VERSION := $(shell sed -n 's/^Version:[[:space:]]*//p' "$(TOP)/$(NAME).spec")
RELEASE := $(shell $(GIT) rev-list --count HEAD).git$(shell $(GIT) rev-parse --short HEAD)
outdir  ?= $(TOP)/out
BUILD   := $(TOP)/.build

srpm:
	command -v rpmbuild >/dev/null || dnf -y install rpm-build
	rm -rf "$(BUILD)" && mkdir -p "$(BUILD)" "$(outdir)"
	$(GIT) archive --format=tar.gz --prefix=$(NAME)-$(VERSION)/ \
		-o "$(BUILD)/$(NAME)-$(VERSION).tar.gz" HEAD
	sed 's/^Release:.*/Release:        $(RELEASE)%{?dist}/' "$(TOP)/$(NAME).spec" > "$(BUILD)/$(NAME).spec"
	rpmbuild -bs "$(BUILD)/$(NAME).spec" \
		--define "_sourcedir $(BUILD)" \
		--define "_srcrpmdir $(outdir)"

.PHONY: srpm
