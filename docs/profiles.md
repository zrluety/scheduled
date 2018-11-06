# Profiles

Before you can use a bank with the Schedule D application, a bank profile needs to be created. A profile is a yaml file that consists of the following sections:

* Mapping
* Options

The profile should be named with the bank name. When the Schedule D workbook is opened, all profiles in the profiles directory are loaded as options to choose from.

## Mapping

The mapping section describes which columns in a bank's statement are mapped to the columns in the Schedule D workbook. A mapping is required for each of the following columns in the Schedule D workbook:

* amount
* date
* security name
* shares
* transaction price
* transaction type

## Options

The options section contains inputs to the Schedule D application that refine how the information is extracted from the bank statement and how the extracted data is formatted prior to loading into the Schedule D workbook. The following options are supported:

* columns
* stopwords
* vertical alignment
* horizontal alignment