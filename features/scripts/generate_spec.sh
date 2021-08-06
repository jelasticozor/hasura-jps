#! /bin/sh

if [ $# -lt 1 ] ; then
  echo "Usage: $0 <version> [<output-dir>]"
  exit 1
fi

VERSION=$1
OUTPUT_DIR=${2:-specification}

generate() {
  app=$1
  output_dir=$2
  version=$3
  mono /pickles/Pickles.exe --feature-directory=. --output-directory=${output_dir} --system-under-test-name=$app --system-under-test-version=$version --language=en --documentation-format=dhtml --exp --et 'in-preparation' --enableComments=false
}

generate "shopozor-api" $OUTPUT_DIR $VERSION