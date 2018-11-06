# Profiles

Before you can use a bank with the Schedule D application, a bank profile needs to be created. A profile is a yaml file that consists of the following sections:

* Name
* Mapping
* Options

## Name

The name property is what the analyst selects in the Populate Schedule D workbook to use a given profile. When the Populate Schedule D workbook is opened, all profiles in the profiles.json file are loaded as options to choose from. To refresh the list of available profiles, run the following in the terminal.

```python
scheduled refresh
```

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
* pandas