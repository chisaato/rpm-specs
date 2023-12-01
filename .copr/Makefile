.PHONY : srpm
srpm:
	dnf -y install rpmbuild rpmdevtools
	spectool -g $(spec)
	rpmbuild -bs --define "_topdir $(PWD)" --define "_sourcedir $(PWD)" $(spec)
	# 移动到 $(outdir)
	mv SRPMS/* $(outdir)
srpm-debug:
	# dnf -y install rpmbuild rpmdevtools
	spectool -g $(spec)
	rpmbuild -bs --define "_topdir $(PWD)" --define "_sourcedir $(PWD)" $(spec)
	# 移动到 $(outdir)
	mv SRPMS/* $(outdir)