#!/bin/bash
while true
do
isSiteUp=$(curl -k https://${NAMESPACE}.y.balsamhill.com 2>/dev/null | grep "Homepage")
	if test -z "$isSiteUp"
	then
		echo "Waiting for Environment : $NAMESPACE to be up..."
		sleep 300
	else
		envsubst <./Hybris-sampledata/helper_scripts/sftp_upload.py.tmpl> ./Hybris-sampledata/helper_scripts/sftp_upload.py
    	python ./Hybris-sampledata/helper_scripts/sftp_upload.py
		echo "Data Import complete!!!"
		break
	fi
done