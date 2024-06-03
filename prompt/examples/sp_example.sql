
CREATE PROCEDURE [dbo].[sp_example]
AS
BEGIN
	SET NOCOUNT ON;

	TRUNCATE TABLE  stg.[tblDst1]

	CREATE TABLE #IDs(ID INT PRIMARY KEY);

	WITH validIdems as (SELECT tradingItemId FROM stg.[RussellUS2_IndexTradingItem_tbl] t WHERE t.[status]=0)
	INSERT INTO #IDs(ID) 
		SELECT tradingItemId FROM validIdems

	--Insert the new or update the existing records
	INSERT INTO  stg.[tblDst1]
	-- index value excludes TRs --
	SELECT
		t.tradingItemId,
		p.pricingDate as valueDate
	FROM 
		[dbo].srsTbl1 AS p with (nolock)
		JOIN #IDs AS t with (nolock)
			on p.tradingItemId = t.tradingItemId
		JOIN stg.RussellUS2_IndexToFeedType_vw AS ift with (nolock)
			on t.indexId = ift.indexCompanyId
	UNION
	SELECT
		t.tradingItemId,
		cdi.pricingDate as valueDate
	from 
		srsTbl2 AS p with (nolock)
		JOIN  #IDs AS t with (nolock)
			on p.tradingItemId = t.tradingItemId
		JOIN [$(DataFeedEngineCache)].[dbo].Russell_PriceIndexDataItem_tbl AS cdi with (nolock)
			on t.indexId = ift.indexCompanyId
		WHERE 
			p.endMktValue is not null

		UPDATE  stg.[RussellUS2_IndexTradingItem_tbl]  SET [status]=1 WHERE [status]=0

DELETE FROM  RussellUS2_ConstituentDates_tbl
	WHERE datepart(WEEKDAY, readingDate) IN (1, 7)

	DELETE FROM  RussellUS2_ConstituentDates_tbl
	WHERE readingDate IN (SELECT holidayDate FROM [$(CIQData)].dbo.ExchangeHoliday_tbl with (nolock) WHERE exchangeId = 106)



END
;

