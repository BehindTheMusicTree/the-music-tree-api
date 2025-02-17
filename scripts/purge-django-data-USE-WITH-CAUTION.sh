#!/bin/bash
# WARNING: This script will purge the Django data. Use with caution.

# Constants
DB_TIMEOUT_SECONDS=5
DB_TIMEOUT_ERROR_MESSAGE="ERROR: Database connection timed out after $DB_TIMEOUT_SECONDS seconds. Please check if the database server is running and accessible."

log_with_script_prefixe () {
    log "[Django data purger] $1"
}

handle_db_timeout() {
	exit_code=$1
	if [ $exit_code -eq 124 ]; then
		log_with_script_prefixe "$DB_TIMEOUT_ERROR_MESSAGE" >&2
		exit 1
	fi
}

check_script_vars_are_set() {
	load_app_env_file_if_exists
	load_project_calculated_paths_env_vars

	REQUIRED_NON_BOOL_VARS=(
		APP_NAME
		LIBRARIES_DIR
		DB_PORT
		DB_BODZIFY_API_DB_NAME
		DB_SUPERUSER_NAME
		DB_SUPERUSER_PASSWORD
		DB_BODZIFY_API_USERNAME
	)
	for VAR in "${REQUIRED_NON_BOOL_VARS[@]}"; do
		check_required_vars_are_set "$VAR"
	done
	check_bool_vars_are_set APP_IS_EXPOSED

	export_value_removing_eventual_surrounding_quotes DB_SUPERUSER_PASSWORD
	export PGPASSWORD=$DB_SUPERUSER_PASSWORD
}

empty_libraries() {
	log_with_script_prefixe "Empty the library directory $LIBRARIES_DIR ..."
	USERS_SUBFOLDERS_COUNT=$(find "$LIBRARIES_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
	TOTAL_TRACK_FILES_COUNT=$(find "$LIBRARIES_DIR" -mindepth 2 -type f | wc -l)
	rm -rf "$LIBRARIES_DIR"*
	if [ $? -ne 0 ]; then
		log_with_script_prefixe "ERROR: Failed to empty the library directory." >&2
		exit 1
	fi
	log_with_script_prefixe "$USERS_SUBFOLDERS_COUNT user subfolders were deleted."
	log_with_script_prefixe "$TOTAL_TRACK_FILES_COUNT track files were deleted."
}

force_close_db_connections_if_exist() {
	log_with_script_prefixe "Force closing connections to database $1 if exists..."

	db_name=$1
	if [ -z "$db_name" ]; then
		log_with_script_prefixe "ERROR: The database name must be provided." >&2
		exit 1
	fi

	log_with_script_prefixe "Check if database is being accessed by other users..."
	output=$(timeout ${DB_TIMEOUT_SECONDS}s psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
	"SELECT COUNT(*) FROM pg_stat_activity WHERE datname='$db_name'" 2>&1)
	exit_code=$?
	handle_db_timeout $exit_code
	if [ $exit_code -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
		log_with_script_prefixe "ERROR: Failed to check if the database is being accessed by other users: $output" >&2
		exit 1
	fi
	if [ "$output" -gt 0 ]; then
		log_with_script_prefixe "Database $db_name is being accessed by other users. Closing connections..."
		output=$(timeout ${DB_TIMEOUT_SECONDS}s psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
			"SELECT pg_terminate_backend(pg_stat_activity.pid) \
			FROM pg_stat_activity \
			WHERE pg_stat_activity.datname = '$db_name' AND pid <> pg_backend_pid();" 2>&1)
		exit_code=$?
		handle_db_timeout $exit_code
		if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
			log_with_script_prefixe "ERROR: Failed to close the connections: $output" >&2
			exit 1
		fi
		log_with_script_prefixe "Connections closed successfully."
	else
		log_with_script_prefixe "Database is not being accessed by other users."
	fi
}

empty_db() {

	databases=("$DB_BODZIFY_API_DB_NAME" "test_$DB_BODZIFY_API_DB_NAME")

	for db_name in "${databases[@]}"; do
		force_close_db_connections_if_exist $db_name

		log_with_script_prefixe "Checking if database $db_name exists..."
		sql="SELECT 1 FROM pg_database WHERE datname='${!db_name}'"
		output=$(timeout ${DB_TIMEOUT_SECONDS}s psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
		"SELECT 1 FROM pg_database WHERE datname='${db_name}'" 2>&1)
		exit_code=$?
		handle_db_timeout $exit_code
		log_with_script_prefixe "${!db_name}"
		log_with_script_prefixe "${db_name}"
		log_with_script_prefixe "$output"
		if [ "$output" = "1" ]; then
			log_with_script_prefixe "Database $db_name exists. Dropping database..."
			output=$(timeout ${DB_TIMEOUT_SECONDS}s psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc "DROP DATABASE ${db_name};" 2>&1)
			exit_code=$?
			handle_db_timeout $exit_code
			if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
				log_with_script_prefixe "ERROR: Failed to drop the database $db_name: $output" >&2
				exit 1
			fi
			log_with_script_prefixe "Database $db_name dropped successfully."
		else
			log_with_script_prefixe "Database $db_name does not exist."
		fi
	done

	log_with_script_prefixe "Dropping user $DB_BODZIFY_API_USERNAME if exists..."
	output=$(timeout ${DB_TIMEOUT_SECONDS}s psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
		"SELECT 1 FROM pg_roles WHERE rolname='${DB_BODZIFY_API_USERNAME}'" 2>&1)
	exit_code=$?
	handle_db_timeout $exit_code
	if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
	log_with_script_prefixe "ERROR: Failed to check if the user exists: $output" >&2
	exit 1
	fi
	if [ "$output" = "1" ]; then
		log_with_script_prefixe "User exists. Dropping user"
		output=$(timeout ${DB_TIMEOUT_SECONDS}s psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc "DROP USER $DB_BODZIFY_API_USERNAME;" 2>&1)
		exit_code=$?
		handle_db_timeout $exit_code
		if [ $? -ne 0 ]; then
		log_with_script_prefixe "ERROR: Failed to drop the user: $output" >&2
		exit 1
		fi
	else 
		log_with_script_prefixe "User $DB_SUPERUSER_NAME does not exist."
	fi
}

remove_migrations() {
	MIGRATIONS_DIR="${PROJECT_DIR}${APP_NAME}/migrations/"
	log_with_script_prefixe "Deleting migrations in directory $MIGRATIONS_DIR ..."
	log_with_script_prefixe "Deleting .py migrations..."
	find "${MIGRATIONS_DIR}" -name "*.py" -not -name "__init__.py" -exec rm -f {} \;
	if [ $? -ne 0 ]; then
		log_with_script_prefixe "ERROR: Failed to delete .py migrations" >&2
		exit 1
	fi
	log_with_script_prefixe ".py migrations deleted successfully."

	log_with_script_prefixe "Deleting .pyc migrations..."
	find "${MIGRATIONS_DIR}" -name "*.pyc" -exec rm -f {} \;
	if [ $? -ne 0 ]; then
		log_with_script_prefixe "ERROR: Failed to delete .pyc migrations" >&2
		exit 1
	fi
	log_with_script_prefixe ".pyc migrations deleted successfully."

	log_with_script_prefixe "Django data purged successfully."
}

main () {
	SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
	PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
	source ${SCRIPTS_DIR}utils.sh

	log_with_script_prefixe "Purging Django data..."

	SKIP_CONFIRMATION=false

	while getopts ":s" opt; do
	case $opt in
		s)
		SKIP_CONFIRMATION=true
		;;
		\?)
		log_with_script_prefixe "ERROR: Invalid option: -$OPTARG" >&2
		exit 1
		;;
	esac
	done

	if [ "$SKIP_CONFIRMATION" != "true" ]; then
		log_with_script_prefixe "WARNING: This script will purge the Django data. Use with caution."
		read -p "Are you sure you want to proceed? (yes/no): " CONFIRMATION

		if [ "$CONFIRMATION" != "yes" ]; then
			log_with_script_prefixe "Operation aborted." >&2
			exit 1
		fi
	fi

	check_script_vars_are_set
	determine_db_host_if_not_set
	empty_libraries
	empty_db
	remove_migrations
}

main "$@"