# djangoDBTestRunner
Django custom db test runner class for no db testing or by copying the schema of existing db.

Step to Use:
Put below line to override existing Test runner class.

TEST_RUNNER = 'path_to_file.custom_test_runner.NoDbTestRunner'
