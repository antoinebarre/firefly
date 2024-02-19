
from firefly.html.components.tables import Table, TableColumn

# Create a table with 3 columns
table = Table(columns=[
    TableColumn("Name", ["John", "Doe", "Foo"]),
    TableColumn("Age", ["25", "30", "40"]),
    TableColumn("Country", ["USA", "Canada", "France"])
])

print(table.render())