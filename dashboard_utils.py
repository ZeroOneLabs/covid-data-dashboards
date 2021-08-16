
import dash_html_components as html
import plotly.express as px

def create_bar_graph() -> px.bar:
    pass

def create_html_table(table_data: dict, tableClassname=None, rowClassnames=None) -> html.Table:
    """Returns a list of Dash HTML elements in a list, consisting of HTML table elements.

    Args:
        table_data (dict):
        {
            "data_item_11": {
                "values": [
                    "value 1",
                    "value 2"
                ],
                "classname": "row"
            },
            "data_item_2": {
                "values": [
                    "value 3",
                    "value 4"
                ],
                "classname": "row"
            },
        }

    Returns:
        list: 
        [
            html.Table([
                html.Tr([
                    html.Td("value 1"),
                    html.Td("value 2"),
                ], className="row"),
            ])
        ]

    """

    prev_row_value_count = 0

    for row in table_data:
        if len(table_data[row]['values']) == 0:
            raise Exception("table_dict must have a row item that contains one or more items.")
        else:
            prev_row_value_count = len(table_data[row]['values'])
        # Count over each number of row value totals to make sure that there are no discrepancies.
        # We only hav to do this once, so that's why we're doing it before the break.

        row_value_count = len(table_data[row]['values'])
        for rowcount in table_data:
            if row_value_count != len(table_data[rowcount]['values']):
                raise Exception("There is a table row that has more or less cells than other rows in the table. You can fix this by adding blank data to rows to match the count of row cells. (i.e. See: HTML Table 'colspan' and how tables can't have unmatching cell numbers in each row or column)")
        # Break as we don't need to go through every "row" within the HTML Table Dictionary to perform the same calculations.
        break    

    html_table_tr_list = []
    for row in table_data:

        row_cells = []

        for cell in table_data[row]['values']:
            row_cells.append(html.Td(cell))
        if rowClassnames:
            row_classname = rowClassnames
        elif table_data[row]['classname']:
            row_classname = table_data[row]['classname']
        else:
            row_classname = ""

        html_table_tr_list.append(html.Tr(row_cells, className=row_classname))


    if tableClassname:
        html_table_return = html.Table([ html.Tbody( html_table_tr_list ) ], className=tableClassname)
    else:
        html_table_return = html.Table([ html.Tbody( html_table_tr_list ) ])

    return html_table_return


def main():
    pass

if __name__ == "__main__":
    main()

# table_dict = {
#         "data_item1": {
#             "values": [
#                 "value 1",
#                 "value 23"
#             ],
#             "classname": "row"
#         },
#         "data_item2": {
#             "values": [
#                 "value 1",
#                 "value 22"
#             ],
#             "classname": "row"
#         },
#     }


