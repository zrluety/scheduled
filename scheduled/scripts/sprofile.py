import inspect

import click
import cutie
import pandas as pd
import yaml


@click.command()
def create_profile():
    profile = {}

    # enter the name of the institution
    profile["name"] = click.prompt("Enter the name of the institution", type=str)

    # create the mapping.
    mapping = {}
    mapping["amount"] = click.prompt(
        "Enter the name of the column that should be assigned to amount", type=str
    )
    mapping["security name"] = click.prompt(
        "Enter the name of the column that should be assigned to security name",
        type=str,
    )
    mapping["shares"] = click.prompt(
        "Enter the name of the column that should be assigned to shares", type=str
    )
    mapping["transaction price"] = click.prompt(
        "Enter the name of the column that should be assigned to transaction price",
        type=str,
    )
    mapping["transaction type"] = click.prompt(
        "Enter the name of the column that should be assigned to transaction type",
        type=str,
    )

    profile["mapping"] = mapping

    # what file type does the source data come from?
    print("How is the statement data provided?")
    file_type_choices = ["CSV", "XLS(X)", "PDF"]
    file_type = file_type_choices[cutie.select(file_type_choices)]

    if file_type == "PDF":
        profile["pdf_args"] = _build_pdf_args()
    elif file_type == "CSV":
        _build_pandas_args()

def _build_pdf_args():
    pdf_args = {}

    # get all field names in the Transaction Activity Table
    names = []
    while True:
        # For the first prompt give the full explanation
        if len(names) == 0:
            name = click.prompt(
                "Enter the name of each column in the Transaction Activity Table",
                type=str,
            )

            names.append(name)
        else:
            name = click.prompt(
                "Enter the name of the next column, if finished type 'finished'",
                type=str,
            )

            if name.lower() == "finished":
                break
            else:
                names.append(name)

    pdf_args["names"] = names

    # get a list of stopwords
    stopwords = []
    print("stop words help the application detect the bottom of table in the PDFs")
    while True:
        stopword = click.prompt(
            "List all stopwords, if finished, type 'finished'", type=str
        )

        if stopword.lower() == "finished":
            break
        else:
            stopwords.append("stopword")

    pdf_args["stopwords"] = stopwords

    # get vertical alignment
    print("How are the rows aligned in the document?")
    alignment_choices = ["TOP", "CENTER"]
    pdf_args["v_align"] = alignment_choices[cutie.select(alignment_choices)]

    return pdf_args


def _build_pandas_args():
    # pandas_args = {}
    print(inspect.getargs(pd.read_csv))
