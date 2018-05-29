import logging


def generate_table_schema(data, include_columns=None, exclude_columns=None, column_constraints=None):
    example = data[0]
    columns = []

    for k, v in example.items():
        name = k

        if include_columns is not None:
            if name not in include_columns:
                continue
        else:
            if exclude_columns is not None and name in exclude_columns:
                continue

        if isinstance(v, int):
            typename = 'integer'
        elif isinstance(v, bool):
            typename = 'boolean'
        elif isinstance(v, str):
            try:
                float(v)
                typename = 'real'
            except ValueError:
                typename = 'text'
        else:
            raise ValueError(f'value for key "{k}" had unexpected type: "{v}"')

        constraints = ''
        if column_constraints is not None:
            try:
                constraints = column_constraints[name]
            except KeyError:
                pass

        columns.append((name, typename, constraints))

    return columns


def generate_create_table_query(schema, table_name):
    query = f'create table if not exists {table_name} (\n'
    query += ',\n'.join([f'  {" ".join(col)}'.rstrip() for col in schema])
    query += '\n)'

    return query


def create_table(conn, schema, table_name):
    query = generate_create_table_query(schema, table_name)
    logging.info(f'generated schema for table {table_name}:\n' + query)

    c = conn.cursor()
    c.execute(query)


def populate_table(conn, schema, table_name, data, include_columns=None, exclude_columns=None):
    num_columns = len(schema)
    query = f' insert into {table_name} values ({", ".join("?" * num_columns)})'

    c = conn.cursor()
    for row in data:
        if include_columns is not None:
            values = tuple(row[col] for col in row if col in include_columns)
        else:
            if exclude_columns is not None:
                values = tuple(row[col] for col in row if col not in exclude_columns)
            else:
                values = tuple(row.values())

        c.execute(query, values)
