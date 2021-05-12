MERGE INTO im.product_tgt p
USING ( SELECT DECODE(s.scd_row_type_id,1,-999,m.seq_no) as
        seq_no,
		id,
		name,
		year,
		color,
		pantone_value,
		m.scd_row_type_id
		from (select dp.seq_no,
		             sp.id,
					 sp.name,
					 sp.year,
					 sp.color,
					 sp.pantone_value,
					 CASE
					    WHEN dp.id is NULL
						THEN
						    1
					    WHEN (dp.name!=sp.name or
						      dp.color!=sp.color)
					    THEN
						    2
						ELSE
						    0
					 END
                         AS scd_row_type_id
			   FROM test_product sp
			        LEFT JOIN
					product_tgt dp
					on (sp.id=dp.id and dp.active_flag='Y')
		       )m
       JOIN scd_row_type s
       ON (s.scd_row_type_id <= m.scd_row_type_id)
       )mp
   	ON (p.seq_no=mp.seq_no)
when matched then
  update set p.end_date=sysdate, active_flag='N'
when not matched then
  insert(p.id,p.name,p.year,p.color,p.pantone_value,p.seq_no,p.start_date,p.end_date,p.active_flag)
  values
  (mp.id,mp.name,mp.year,mp.color,mp.pantone_value,SeqDimProd.Nextval,sysdate,to_date('3000-12-31 00:00:00','YYYY-MM-DD HH24:MI:SS'),'Y');
commit;
