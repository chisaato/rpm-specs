.PHONY : srpm
srpm:
	dnf -y install rpm-build rpmdevtools
	spectool -g $(spec)
	rpmbuild -bs --define "_topdir $(PWD)" --define "_sourcedir $(PWD)" $(spec)
	# 移动到 $(outdir)
	mv SRPMS/* $(outdir)
srpm-debug:
	# dnf -y install rpm-build rpmdevtools
	spectool -g $(spec)
	rpmbuild -bs --define "_topdir $(PWD)" --define "_sourcedir $(PWD)" $(spec)
	# 移动到 $(outdir)
	mv SRPMS/* $(outdir)