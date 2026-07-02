#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2019-2021 CERN.
# SPDX-FileCopyrightText: 2019-2020 Northwestern University.
# SPDX-FileCopyrightText: 2021-2026 TU Wien.
# SPDX-FileCopyrightText: 2022 Graz University of Technology.
# SPDX-License-Identifier: MIT
#
# Usage:
#   ./run-tests.sh [pytest options and args...]

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Check for arguments
# Note: "-k" would clash with "pytest"
pytest_args=()
for arg in $@; do
	# from the CLI args, filter out some known values and forward the rest to "pytest"
	# note: we don't use "getopts" here b/c of some limitations (e.g. long options),
	#       which means that we can't combine short options (e.g. "./run-tests -Kk pattern")
	case ${arg} in
		*)
			pytest_args+=( ${arg} )
			;;
	esac
done

python -m sphinx.cmd.build -qnN docs docs/_build/html
# Note: expansion of pytest_args looks like below to not cause an unbound
# variable error when 1) "nounset" and 2) the array is empty.
python -m pytest ${pytest_args[@]+"${pytest_args[@]}"}
tests_exit_code=$?
exit "$tests_exit_code"
