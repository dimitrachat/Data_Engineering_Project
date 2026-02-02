
nulls_per_column = """
    select
          sum(case when Order_ID is null then 1 else 0 end) as Order_ID_nulls,
          sum(case when Product is null then 1 else 0 end) as Product_nulls,
          sum(case when Quantity_Ordered is null then 1 else 0 end) as Quantity_Ordered_nulls,
          sum(case when Price_Each is null then 1 else 0 end) as Price_Each_nulls,
          sum(case when Order_Date is null then 1 else 0 end) as Order_Date_nulls,
          sum(case when Purchase_Address is null then 1 else 0 end) as Purchase_Address_nulls
    from sales_data
"""


total_fully_null_rows = """
    select count(*) AS total_null_rows
    from sales_data
    where Order_ID is null
       and Product is null
       and Quantity_Ordered is null
       and Price_Each is null
       and Order_Date is null
       and Purchase_Address is null
"""

douplicates_count = """
    with cte as (
    select *,
           count(*) as cnt
    from sales_data_enriched
    group by all
    having cnt > 1
    ) 
    select count(*) as duplicates_cnt
    from cte
"""

remove_duplicates = """
    with ranked_sales as (
        select *,
               row_number() over (
                   partition by Order_ID, Product
                   order by Order_Date desc
               ) as rn
        from sales_data_enriched
    )
    select * except(rn)
    from ranked_sales
    where rn = 1
"""