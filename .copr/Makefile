.PHONY : srpm
srpm:
	dnf -y install rpmbuild rpmdevtools
	spectool -g $(spec)
	rpmbuild -bs $(spec)
	# 移动到 $(outdir)
	mv SRPMS/* $(outdir)
srpm-debug:
	# dnf -y install rpmbuild rpmdevtools
	spectool -g $(spec)
	rpmbuild -bs --define 'debug_package %{nil}' $(spec)
	# 移动到 $(outdir)
	mv SRPMS/* $(outdir)