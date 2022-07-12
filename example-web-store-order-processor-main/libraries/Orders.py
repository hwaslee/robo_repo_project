from RPA.Excel.Files import Files
from RPA.Tables import Tables


class Orders:
    def get_orders(self, excel):
        files = Files()
        workbook = files.open_workbook(excel)
        rows = workbook.read_worksheet(header=True)
        print('1', rows)
        print('2', type(rows), len(rows))

        tables = Tables()
        print('3', type(tables))
        table = tables.create_table(rows)
        print('4', table)
        tables.filter_empty_rows(table)

        orders = []
        for row in table:
            first_name, last_name = row["Name"].split()
            order = {
                "item": row["Item"],
                "zip": int(row["Zip"]),
                "first_name": first_name,
                "last_name": last_name
            }
            orders.append(order)

        print('5', orders)
        return orders


if __name__ == '__main__':
    orders_obj = Orders()
    orders = orders_obj.get_orders("..\Data.xlsx")