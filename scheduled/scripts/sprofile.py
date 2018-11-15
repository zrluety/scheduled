import click
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

    # what filet ype does the source data come from?
    file_type = click.prompt(
        "What file type are the statements provided in? [1] CSV, [2] XLS(X), [3] PDF",
        type=int,
    )

    # for PDFs, get the additional required arguments
    if file_type == 3:
        pdf_args = {}

        names = []
        name = True
        while name:
            # For the first prompt give the full explanation
            if len(names) == 0:
                name = click.prompt(
                    "Enter the name of each column in the Transaction Activity Table",
                    type=str
                )

                if name is None:
                    print("Must enter at least one column name\n")
                    continue
                else:
                    names.append(name)
            else:
                name = click.prompt(
                    "Enter the name of the next column, if finished type 'finished'",
                    type=str
                )

                if name.lower() == "finished":
                    break
                else:
                    names.append(name)

        pdf_args["names"] = names
        profile["pdf_args"] = pdf_args

        print(yaml.dump(profile))
