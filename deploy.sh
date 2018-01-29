#!/bin/bash
set -o errexit

stack_name="austinfpvracing-racefinder"
bucket_name="austinfpvracing-deployments"
prefix="$stack_name/$(openssl rand -hex 8)"

set -o xtrace

make

aws cloudformation package \
  --output-template-file=dist/output.yaml \
  --template-file=cloudformation.yaml \
  --s3-bucket="${bucket_name}" \
  --s3-prefix="${prefix}"

aws cloudformation deploy \
  --template-file=dist/output.yaml \
  --stack-name="${stack_name}" \
  --capabilities=CAPABILITY_NAMED_IAM \
  --parameter-overrides MultiGPChapter=Austin-FPV JsonOutputBucket=${stack_name}

rm -rf dist/*

aws cloudformation describe-stacks \
  --stack-name "${stack_name}" \
  --query Stacks[].Outputs \
  --output table
