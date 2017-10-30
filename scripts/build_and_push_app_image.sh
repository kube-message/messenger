#!/usr/bin/env bash
set -e

if [[ $# -lt 1 ]]; then
    echo "Usage: build_and_push_nginx.sh -v IMAGE_VERSION [-p]" >&2
    exit 1
fi

while getopts "v:p" OPTION
do
	case $OPTION in
		v | --version)
			new_tag=app-${OPTARG}
			echo "Using tag: $new_tag"
			docker build -t messenger:"$new_tag" .
			docker tag messenger:"$new_tag" imauld/messenger:"$new_tag"
			echo "Built image: messenger:$new_tag"
			;;
		p | --push)
			echo "Pushing image to DockerHub: messenger:$new_tag"
			docker push imauld/messenger:$new_tag
			;;
	esac
done
