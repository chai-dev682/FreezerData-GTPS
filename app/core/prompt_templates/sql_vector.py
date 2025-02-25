sql_vector = """
You need to select one proper database, Pinecone VectorDB or MySQL Database to gather information that related to following query.

The query is as follows.
{query}

Here is the original conversation.
{conversation}

Here is SQL Query that is used to create table.
```
CREATE TABLE IF NOT EXISTS retail_leases (
  id INT PRIMARY KEY,
  start_date DATE,
  expiry_date DATE,
  current_rent_pa DECIMAL(10,2), -- Annual rent in thousands
  current_rent_sqm DECIMAL(10,2), -- Rent per square meter
  centre_name VARCHAR(255),
  tenant_category VARCHAR(255),
  tenant_subcategory VARCHAR(255),
  lessor VARCHAR(255),
  lessee VARCHAR(255),
  area DECIMAL(10,2) -- Leased area in square meters
);
```
"""