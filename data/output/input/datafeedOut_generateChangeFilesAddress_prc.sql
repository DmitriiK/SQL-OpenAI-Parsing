CREATE procedure [dbo].[datafeedOut_generateChangeFilesAddress_prc]
as 
 
	if exists (select * from DataFeedEngineCache.dbo.sysobjects (nolock) where name = 'dataFeedOut_AddressFile_tbl' and xtype='U')
		drop table DataFeedEngineCache.dbo.dataFeedOut_AddressFile_tbl
 
 
	select 
		(case when dataFeedOut_Address_tbl.addressID is null then 'A' else 'U' end) as changeFlag,
		dataFeedOut_AddressLoad_tbl.addressID,
		dataFeedOut_AddressLoad_tbl.objectID,
		dataFeedOut_AddressLoad_tbl.addressTypeID,
		dataFeedOut_AddressLoad_tbl.streetAddress,
		dataFeedOut_AddressLoad_tbl.streetAddress2,
		dataFeedOut_AddressLoad_tbl.streetAddress3,
		dataFeedOut_AddressLoad_tbl.streetAddress4,
		dataFeedOut_AddressLoad_tbl.city,
		dataFeedOut_AddressLoad_tbl.stateID,
		dataFeedOut_AddressLoad_tbl.countryID,
		dataFeedOut_AddressLoad_tbl.zipCode,
		dataFeedOut_AddressLoad_tbl.primaryFlag,
		dataFeedOut_AddressLoad_tbl.otherPhoneValue,
		dataFeedOut_AddressLoad_tbl.officePhoneValue,
		dataFeedOut_AddressLoad_tbl.officeFaxValue
 
 	into DataFeedEngineCache.dbo.dataFeedOut_AddressFile_tbl 
		from DataFeedEngineCache.dbo.dataFeedOut_AddressLoad_tbl dataFeedOut_AddressLoad_tbl 
			left outer join dataFeedOut_Address_tbl 
				on dataFeedOut_Address_tbl.addressID=dataFeedOut_AddressLoad_tbl.addressID
			where 
				dataFeedOut_Address_tbl.addressID is null
			OR
 			(
				dataFeedOut_AddressLoad_tbl.objectID<> dataFeedOut_Address_tbl.objectID
 			OR 
				dataFeedOut_AddressLoad_tbl.addressTypeID<> dataFeedOut_Address_tbl.addressTypeID
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.streetAddress,'')<> isNull(dataFeedOut_Address_tbl.streetAddress,'')
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.streetAddress2,'')<> isNull(dataFeedOut_Address_tbl.streetAddress2,'')
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.streetAddress3,'')<> isNull(dataFeedOut_Address_tbl.streetAddress3,'')
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.streetAddress4,'')<> isNull(dataFeedOut_Address_tbl.streetAddress4,'')
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.city,'')<> isNull(dataFeedOut_Address_tbl.city,'')
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.stateID,0)<> isNull(dataFeedOut_Address_tbl.stateID,0)
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.countryID,0)<> isNull(dataFeedOut_Address_tbl.countryID,0)
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.zipCode,'')<> isNull(dataFeedOut_Address_tbl.zipCode,'')
 			OR 
				dataFeedOut_AddressLoad_tbl.primaryFlag<> dataFeedOut_Address_tbl.primaryFlag
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.otherPhoneValue,'')<> isNull(dataFeedOut_Address_tbl.otherPhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.officePhoneValue,'')<> isNull(dataFeedOut_Address_tbl.officePhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressLoad_tbl.officeFaxValue,'')<> isNull(dataFeedOut_Address_tbl.officeFaxValue,'')
			)
 
 
	Insert into DataFeedEngineCache.dbo.dataFeedOut_AddressFile_tbl
	select
	(case when dataFeedOut_AddressLoad_tbl.addressID is null then 'D' else 'E' end) as changeFlag,
				dataFeedOut_Address_tbl.addressID,
				dataFeedOut_Address_tbl.objectID,
				dataFeedOut_Address_tbl.addressTypeID,
				dataFeedOut_Address_tbl.streetAddress,
				dataFeedOut_Address_tbl.streetAddress2,
				dataFeedOut_Address_tbl.streetAddress3,
				dataFeedOut_Address_tbl.streetAddress4,
				dataFeedOut_Address_tbl.city,
				dataFeedOut_Address_tbl.stateID,
				dataFeedOut_Address_tbl.countryID,
				dataFeedOut_Address_tbl.zipCode,
				dataFeedOut_Address_tbl.primaryFlag,
				dataFeedOut_Address_tbl.otherPhoneValue,
				dataFeedOut_Address_tbl.officePhoneValue,
				dataFeedOut_Address_tbl.officeFaxValue
		from dataFeedOut_Address_tbl 
			left outer join DataFeedEngineCache.dbo.dataFeedOut_AddressLoad_tbl dataFeedOut_AddressLoad_tbl  
				on dataFeedOut_Address_tbl.addressID=dataFeedOut_AddressLoad_tbl.addressID
		where dataFeedOut_AddressLoad_tbl.addressID is null
 
 	CREATE CLUSTERED INDEX IX_addressId_changeFlag ON DataFeedEngineCache.dbo.dataFeedOut_AddressFile_tbl (addressId, changeFlag) 
 
	if exists (select * from datafeedenginecache.dbo.sysobjects (nolock) where name = 'dataFeedOut_AddressINTLFile_tbl' and xtype='U')
		drop table DataFeedEngineCache.dbo.dataFeedOut_AddressINTLFile_tbl
 
 
	select 
		(case when dataFeedOut_AddressINTL_tbl.addressID is null then 'A' else 'U' end) as changeFlag,
		dataFeedOut_AddressINTLLoad_tbl.addressID,
		dataFeedOut_AddressINTLLoad_tbl.objectID,
		dataFeedOut_AddressINTLLoad_tbl.addressTypeID,
		dataFeedOut_AddressINTLLoad_tbl.streetAddress,
		dataFeedOut_AddressINTLLoad_tbl.streetAddress2,
		dataFeedOut_AddressINTLLoad_tbl.streetAddress3,
		dataFeedOut_AddressINTLLoad_tbl.streetAddress4,
		dataFeedOut_AddressINTLLoad_tbl.city,
		dataFeedOut_AddressINTLLoad_tbl.stateID,
		dataFeedOut_AddressINTLLoad_tbl.countryID,
		dataFeedOut_AddressINTLLoad_tbl.zipCode,
		dataFeedOut_AddressINTLLoad_tbl.primaryFlag,
		dataFeedOut_AddressINTLLoad_tbl.otherPhoneValue,
		dataFeedOut_AddressINTLLoad_tbl.officePhoneValue,
		dataFeedOut_AddressINTLLoad_tbl.officeFaxValue
 
 	into DataFeedEngineCache.dbo.dataFeedOut_AddressINTLFile_tbl 
		from DataFeedEngineCache.dbo.dataFeedOut_AddressINTLLoad_tbl dataFeedOut_AddressINTLLoad_tbl
			left outer join dataFeedOut_AddressINTL_tbl 
				on dataFeedOut_AddressINTL_tbl.addressID = dataFeedOut_AddressINTLLoad_tbl.addressID
			where 
				dataFeedOut_AddressINTL_tbl.addressID is null
			OR
 			(
				dataFeedOut_AddressINTLLoad_tbl.objectID<> dataFeedOut_AddressINTL_tbl.objectID
 			OR 
				dataFeedOut_AddressINTLLoad_tbl.addressTypeID<> dataFeedOut_AddressINTL_tbl.addressTypeID
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.streetAddress,'')<> isNull(dataFeedOut_AddressINTL_tbl.streetAddress,'')
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.streetAddress2,'')<> isNull(dataFeedOut_AddressINTL_tbl.streetAddress2,'')
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.streetAddress3,'')<> isNull(dataFeedOut_AddressINTL_tbl.streetAddress3,'')
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.streetAddress4,'')<> isNull(dataFeedOut_AddressINTL_tbl.streetAddress4,'')
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.city,'')<> isNull(dataFeedOut_AddressINTL_tbl.city,'')
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.stateID,0)<> isNull(dataFeedOut_AddressINTL_tbl.stateID,0)
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.countryID,0)<> isNull(dataFeedOut_AddressINTL_tbl.countryID,0)
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.zipCode,'')<> isNull(dataFeedOut_AddressINTL_tbl.zipCode,'')
 			OR 
				dataFeedOut_AddressINTLLoad_tbl.primaryFlag<> dataFeedOut_AddressINTL_tbl.primaryFlag
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.otherPhoneValue,'')<> isNull(dataFeedOut_AddressINTL_tbl.otherPhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.officePhoneValue,'')<> isNull(dataFeedOut_AddressINTL_tbl.officePhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressINTLLoad_tbl.officeFaxValue,'')<> isNull(dataFeedOut_AddressINTL_tbl.officeFaxValue,'')
			)
 
 
 
	Insert into DataFeedEngineCache.dbo.dataFeedOut_AddressINTLFile_tbl
	select
	(case when dataFeedOut_AddressINTLLoad_tbl.addressID is null then 'D' else 'E' end) as changeFlag,
				dataFeedOut_AddressINTL_tbl.addressID,
				dataFeedOut_AddressINTL_tbl.objectID,
				dataFeedOut_AddressINTL_tbl.addressTypeID,
				dataFeedOut_AddressINTL_tbl.streetAddress,
				dataFeedOut_AddressINTL_tbl.streetAddress2,
				dataFeedOut_AddressINTL_tbl.streetAddress3,
				dataFeedOut_AddressINTL_tbl.streetAddress4,
				dataFeedOut_AddressINTL_tbl.city,
				dataFeedOut_AddressINTL_tbl.stateID,
				dataFeedOut_AddressINTL_tbl.countryID,
				dataFeedOut_AddressINTL_tbl.zipCode,
				dataFeedOut_AddressINTL_tbl.primaryFlag,
				dataFeedOut_AddressINTL_tbl.otherPhoneValue,
				dataFeedOut_AddressINTL_tbl.officePhoneValue,
				dataFeedOut_AddressINTL_tbl.officeFaxValue
			from dataFeedOut_AddressINTL_tbl dataFeedOut_AddressINTL_tbl 		left outer join DataFeedEngineCache.dbo.dataFeedOut_AddressINTLLoad_tbl dataFeedOut_AddressINTLLoad_tbl
				on dataFeedOut_AddressINTL_tbl.addressID = dataFeedOut_AddressINTLLoad_tbl.addressID
	where dataFeedOut_AddressINTLLoad_tbl.addressID is null
 
	CREATE CLUSTERED INDEX IX_addressId_changeFlag ON DataFeedEngineCache.dbo.dataFeedOut_AddressINTLFile_tbl (addressId, changeFlag) 

--INTL PUB

	if exists (select * from datafeedenginecache.dbo.sysobjects (nolock) where name = 'dataFeedOut_AddressINTLPubFile_tbl' and xtype='U')
		drop table DataFeedEngineCache.dbo.dataFeedOut_AddressINTLPubFile_tbl
 
 
	select 
		(case when dataFeedOut_AddressINTLPub_tbl.addressID is null then 'A' else 'U' end) as changeFlag,
		dataFeedOut_AddressINTLPubLoad_tbl.addressID,
		dataFeedOut_AddressINTLPubLoad_tbl.objectID,
		dataFeedOut_AddressINTLPubLoad_tbl.addressTypeID,
		dataFeedOut_AddressINTLPubLoad_tbl.streetAddress,
		dataFeedOut_AddressINTLPubLoad_tbl.streetAddress2,
		dataFeedOut_AddressINTLPubLoad_tbl.streetAddress3,
		dataFeedOut_AddressINTLPubLoad_tbl.streetAddress4,
		dataFeedOut_AddressINTLPubLoad_tbl.city,
		dataFeedOut_AddressINTLPubLoad_tbl.stateID,
		dataFeedOut_AddressINTLPubLoad_tbl.countryID,
		dataFeedOut_AddressINTLPubLoad_tbl.zipCode,
		dataFeedOut_AddressINTLPubLoad_tbl.primaryFlag,
		dataFeedOut_AddressINTLPubLoad_tbl.otherPhoneValue,
		dataFeedOut_AddressINTLPubLoad_tbl.officePhoneValue,
		dataFeedOut_AddressINTLPubLoad_tbl.officeFaxValue
 
 	into DataFeedEngineCache.dbo.dataFeedOut_AddressINTLPubFile_tbl 
		from DataFeedEngineCache.dbo.dataFeedOut_AddressINTLPubLoad_tbl dataFeedOut_AddressINTLPubLoad_tbl 
			left outer join
 				 dataFeedOut_AddressINTLPub_tbl
					on dataFeedOut_AddressINTLPub_tbl.addressID=dataFeedOut_AddressINTLPubLoad_tbl.addressID
			where 
				dataFeedOut_AddressINTLPub_tbl.addressID is null
			OR
 			(
				dataFeedOut_AddressINTLPubLoad_tbl.objectID<> dataFeedOut_AddressINTLPub_tbl.objectID
 			OR 
				dataFeedOut_AddressINTLPubLoad_tbl.addressTypeID<> dataFeedOut_AddressINTLPub_tbl.addressTypeID
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.streetAddress,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.streetAddress,'')
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.streetAddress2,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.streetAddress2,'')
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.streetAddress3,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.streetAddress3,'')
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.streetAddress4,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.streetAddress4,'')
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.city,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.city,'')
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.stateID,0)<> isNull(dataFeedOut_AddressINTLPub_tbl.stateID,0)
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.countryID,0)<> isNull(dataFeedOut_AddressINTLPub_tbl.countryID,0)
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.zipCode,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.zipCode,'')
 			OR 
				dataFeedOut_AddressINTLPubLoad_tbl.primaryFlag<> dataFeedOut_AddressINTLPub_tbl.primaryFlag
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.otherPhoneValue,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.otherPhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.officePhoneValue,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.officePhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressINTLPubLoad_tbl.officeFaxValue,'')<> isNull(dataFeedOut_AddressINTLPub_tbl.officeFaxValue,'')
			)
 
 
 
	Insert into DataFeedEngineCache.dbo.dataFeedOut_AddressINTLPubFile_tbl
	select
	(case when dataFeedOut_AddressINTLPubLoad_tbl.addressID is null then 'D' else 'E' end) as changeFlag,
				dataFeedOut_AddressINTLPub_tbl.addressID,
				dataFeedOut_AddressINTLPub_tbl.objectID,
				dataFeedOut_AddressINTLPub_tbl.addressTypeID,
				dataFeedOut_AddressINTLPub_tbl.streetAddress,
				dataFeedOut_AddressINTLPub_tbl.streetAddress2,
				dataFeedOut_AddressINTLPub_tbl.streetAddress3,
				dataFeedOut_AddressINTLPub_tbl.streetAddress4,
				dataFeedOut_AddressINTLPub_tbl.city,
				dataFeedOut_AddressINTLPub_tbl.stateID,
				dataFeedOut_AddressINTLPub_tbl.countryID,
				dataFeedOut_AddressINTLPub_tbl.zipCode,
				dataFeedOut_AddressINTLPub_tbl.primaryFlag,
				dataFeedOut_AddressINTLPub_tbl.otherPhoneValue,
				dataFeedOut_AddressINTLPub_tbl.officePhoneValue,
				dataFeedOut_AddressINTLPub_tbl.officeFaxValue
		from
		dataFeedOut_AddressINTLPub_tbl left outer join
		DataFeedEngineCache.dbo.dataFeedOut_AddressINTLPubLoad_tbl dataFeedOut_AddressINTLPubLoad_tbl
		on dataFeedOut_AddressINTLPub_tbl.addressID = dataFeedOut_AddressINTLPubLoad_tbl.addressID
		where dataFeedOut_AddressINTLPubLoad_tbl.addressID is null

	CREATE CLUSTERED INDEX IX_addressId_changeFlag ON DataFeedEngineCache.dbo.dataFeedOut_AddressINTLPubFile_tbl (addressId, changeFlag) 
 
--NA 

	if exists (select * from datafeedenginecache.dbo.sysobjects (nolock) where name = 'dataFeedOut_AddressNAFile_tbl' and xtype='U')
		drop table DataFeedEngineCache.dbo.dataFeedOut_AddressNAFile_tbl
 
 
	select 
		(case when dataFeedOut_AddressNA_tbl.addressID is null then 'A' else 'U' end) as changeFlag,
		dataFeedOut_AddressNALoad_tbl.addressID,
		dataFeedOut_AddressNALoad_tbl.objectID,
		dataFeedOut_AddressNALoad_tbl.addressTypeID,
		dataFeedOut_AddressNALoad_tbl.streetAddress,
		dataFeedOut_AddressNALoad_tbl.streetAddress2,
		dataFeedOut_AddressNALoad_tbl.streetAddress3,
		dataFeedOut_AddressNALoad_tbl.streetAddress4,
		dataFeedOut_AddressNALoad_tbl.city,
		dataFeedOut_AddressNALoad_tbl.stateID,
		dataFeedOut_AddressNALoad_tbl.countryID,
		dataFeedOut_AddressNALoad_tbl.zipCode,
		dataFeedOut_AddressNALoad_tbl.primaryFlag,
		dataFeedOut_AddressNALoad_tbl.otherPhoneValue,
		dataFeedOut_AddressNALoad_tbl.officePhoneValue,
		dataFeedOut_AddressNALoad_tbl.officeFaxValue
 
 	into DataFeedEngineCache.dbo.dataFeedOut_AddressNAFile_tbl 
		from DataFeedEngineCache.dbo.dataFeedOut_AddressNALoad_tbl dataFeedOut_AddressNALoad_tbl
			left outer join dataFeedOut_AddressNA_tbl 
				on dataFeedOut_AddressNA_tbl.addressID = dataFeedOut_AddressNALoad_tbl.addressID
			where 
				dataFeedOut_AddressNA_tbl.addressID is null
			OR
 			(
				dataFeedOut_AddressNALoad_tbl.objectID<> dataFeedOut_AddressNA_tbl.objectID
 			OR 
				dataFeedOut_AddressNALoad_tbl.addressTypeID<> dataFeedOut_AddressNA_tbl.addressTypeID
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.streetAddress,'')<> isNull(dataFeedOut_AddressNA_tbl.streetAddress,'')
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.streetAddress2,'')<> isNull(dataFeedOut_AddressNA_tbl.streetAddress2,'')
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.streetAddress3,'')<> isNull(dataFeedOut_AddressNA_tbl.streetAddress3,'')
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.streetAddress4,'')<> isNull(dataFeedOut_AddressNA_tbl.streetAddress4,'')
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.city,'')<> isNull(dataFeedOut_AddressNA_tbl.city,'')
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.stateID,0)<> isNull(dataFeedOut_AddressNA_tbl.stateID,0)
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.countryID,0)<> isNull(dataFeedOut_AddressNA_tbl.countryID,0)
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.zipCode,'')<> isNull(dataFeedOut_AddressNA_tbl.zipCode,'')
 			OR 
				dataFeedOut_AddressNALoad_tbl.primaryFlag<> dataFeedOut_AddressNA_tbl.primaryFlag
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.otherPhoneValue,'')<> isNull(dataFeedOut_AddressNA_tbl.otherPhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.officePhoneValue,'')<> isNull(dataFeedOut_AddressNA_tbl.officePhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressNALoad_tbl.officeFaxValue,'')<> isNull(dataFeedOut_AddressNA_tbl.officeFaxValue,'')
			)
 
 
 
	Insert into DataFeedEngineCache.dbo.dataFeedOut_AddressNAFile_tbl
	select
	(case when dataFeedOut_AddressNALoad_tbl.addressID is null then 'D' else 'E' end) as changeFlag,
				dataFeedOut_AddressNA_tbl.addressID,
				dataFeedOut_AddressNA_tbl.objectID,
				dataFeedOut_AddressNA_tbl.addressTypeID,
				dataFeedOut_AddressNA_tbl.streetAddress,
				dataFeedOut_AddressNA_tbl.streetAddress2,
				dataFeedOut_AddressNA_tbl.streetAddress3,
				dataFeedOut_AddressNA_tbl.streetAddress4,
				dataFeedOut_AddressNA_tbl.city,
				dataFeedOut_AddressNA_tbl.stateID,
				dataFeedOut_AddressNA_tbl.countryID,
				dataFeedOut_AddressNA_tbl.zipCode,
				dataFeedOut_AddressNA_tbl.primaryFlag,
				dataFeedOut_AddressNA_tbl.otherPhoneValue,
				dataFeedOut_AddressNA_tbl.officePhoneValue,
				dataFeedOut_AddressNA_tbl.officeFaxValue
		from
		dataFeedOut_AddressNA_tbl left outer join
		DataFeedEngineCache.dbo.dataFeedOut_AddressNALoad_tbl dataFeedOut_AddressNALoad_tbl
		on dataFeedOut_AddressNA_tbl.addressID=dataFeedOut_AddressNALoad_tbl.addressID
		where dataFeedOut_AddressNALoad_tbl.addressID is null
CREATE CLUSTERED INDEX IX_addressId_changeFlag ON DataFeedEngineCache.dbo.dataFeedOut_AddressNAFile_tbl (addressId, changeFlag) --NAPub  
	if exists (select * from DataFeedEngineCache.dbo.sysobjects (nolock) where name = 'dataFeedOut_AddressNAPubFile_tbl' and xtype='U')
		drop table DataFeedEngineCache.dbo.dataFeedOut_AddressNAPubFile_tbl
 
 
	select 
		(case when dataFeedOut_AddressNAPub_tbl.addressID is null then 'A' else 'U' end) as changeFlag,
		dataFeedOut_AddressNAPubLoad_tbl.addressID,
		dataFeedOut_AddressNAPubLoad_tbl.objectID,
		dataFeedOut_AddressNAPubLoad_tbl.addressTypeID,
		dataFeedOut_AddressNAPubLoad_tbl.streetAddress,
		dataFeedOut_AddressNAPubLoad_tbl.streetAddress2,
		dataFeedOut_AddressNAPubLoad_tbl.streetAddress3,
		dataFeedOut_AddressNAPubLoad_tbl.streetAddress4,
		dataFeedOut_AddressNAPubLoad_tbl.city,
		dataFeedOut_AddressNAPubLoad_tbl.stateID,
		dataFeedOut_AddressNAPubLoad_tbl.countryID,
		dataFeedOut_AddressNAPubLoad_tbl.zipCode,
		dataFeedOut_AddressNAPubLoad_tbl.primaryFlag,
		dataFeedOut_AddressNAPubLoad_tbl.otherPhoneValue,
		dataFeedOut_AddressNAPubLoad_tbl.officePhoneValue,
		dataFeedOut_AddressNAPubLoad_tbl.officeFaxValue
 
 	into DataFeedEngineCache.dbo.dataFeedOut_AddressNAPubFile_tbl 
		from DataFeedEngineCache.dbo.dataFeedOut_AddressNAPubLoad_tbl dataFeedOut_AddressNAPubLoad_tbl
			left outer join dataFeedOut_AddressNAPub_tbl 
				on dataFeedOut_AddressNAPub_tbl.addressID=dataFeedOut_AddressNAPubLoad_tbl.addressID
			where 
				dataFeedOut_AddressNAPub_tbl.addressID is null
			OR
 			(
				dataFeedOut_AddressNAPubLoad_tbl.objectID<> dataFeedOut_AddressNAPub_tbl.objectID
 			OR 
				dataFeedOut_AddressNAPubLoad_tbl.addressTypeID<> dataFeedOut_AddressNAPub_tbl.addressTypeID
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.streetAddress,'')<> isNull(dataFeedOut_AddressNAPub_tbl.streetAddress,'')
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.streetAddress2,'')<> isNull(dataFeedOut_AddressNAPub_tbl.streetAddress2,'')
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.streetAddress3,'')<> isNull(dataFeedOut_AddressNAPub_tbl.streetAddress3,'')
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.streetAddress4,'')<> isNull(dataFeedOut_AddressNAPub_tbl.streetAddress4,'')
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.city,'')<> isNull(dataFeedOut_AddressNAPub_tbl.city,'')
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.stateID,0)<> isNull(dataFeedOut_AddressNAPub_tbl.stateID,0)
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.countryID,0)<> isNull(dataFeedOut_AddressNAPub_tbl.countryID,0)
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.zipCode,'')<> isNull(dataFeedOut_AddressNAPub_tbl.zipCode,'')
 			OR 
				dataFeedOut_AddressNAPubLoad_tbl.primaryFlag<> dataFeedOut_AddressNAPub_tbl.primaryFlag
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.otherPhoneValue,'')<> isNull(dataFeedOut_AddressNAPub_tbl.otherPhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.officePhoneValue,'')<> isNull(dataFeedOut_AddressNAPub_tbl.officePhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressNAPubLoad_tbl.officeFaxValue,'')<> isNull(dataFeedOut_AddressNAPub_tbl.officeFaxValue,'')
			)
 
 
 
	Insert into DataFeedEngineCache.dbo.dataFeedOut_AddressNAPubFile_tbl
	select
	(case when dataFeedOut_AddressNAPubLoad_tbl.addressID is null then 'D' else 'E' end) as changeFlag,
				dataFeedOut_AddressNAPub_tbl.addressID,
				dataFeedOut_AddressNAPub_tbl.objectID,
				dataFeedOut_AddressNAPub_tbl.addressTypeID,
				dataFeedOut_AddressNAPub_tbl.streetAddress,
				dataFeedOut_AddressNAPub_tbl.streetAddress2,
				dataFeedOut_AddressNAPub_tbl.streetAddress3,
				dataFeedOut_AddressNAPub_tbl.streetAddress4,
				dataFeedOut_AddressNAPub_tbl.city,
				dataFeedOut_AddressNAPub_tbl.stateID,
				dataFeedOut_AddressNAPub_tbl.countryID,
				dataFeedOut_AddressNAPub_tbl.zipCode,
				dataFeedOut_AddressNAPub_tbl.primaryFlag,
				dataFeedOut_AddressNAPub_tbl.otherPhoneValue,
				dataFeedOut_AddressNAPub_tbl.officePhoneValue,
				dataFeedOut_AddressNAPub_tbl.officeFaxValue
		from dataFeedOut_AddressNAPub_tbl 
			left outer join DataFeedEngineCache.dbo.dataFeedOut_AddressNAPubLoad_tbl dataFeedOut_AddressNAPubLoad_tbl
				on dataFeedOut_AddressNAPub_tbl.addressID=dataFeedOut_AddressNAPubLoad_tbl.addressID
		where dataFeedOut_AddressNAPubLoad_tbl.addressID is null
 
CREATE CLUSTERED INDEX IX_addressId_changeFlag ON DataFeedEngineCache.dbo.dataFeedOut_AddressNAPubFile_tbl (addressId, changeFlag)  

--USPub

	if exists (select * from datafeedengineCache.dbo.sysobjects (nolock) where name = 'dataFeedOut_AddressUsPubFile_tbl' and xtype='U')
		drop table DataFeedEngineCache.dbo.dataFeedOut_AddressUsPubFile_tbl
 
 
	select 
		(case when dataFeedOut_AddressUsPub_tbl.addressID is null then 'A' else 'U' end) as changeFlag,
		dataFeedOut_AddressUsPubLoad_tbl.addressID,
		dataFeedOut_AddressUsPubLoad_tbl.objectID,
		dataFeedOut_AddressUsPubLoad_tbl.addressTypeID,
		dataFeedOut_AddressUsPubLoad_tbl.streetAddress,
		dataFeedOut_AddressUsPubLoad_tbl.streetAddress2,
		dataFeedOut_AddressUsPubLoad_tbl.streetAddress3,
		dataFeedOut_AddressUsPubLoad_tbl.streetAddress4,
		dataFeedOut_AddressUsPubLoad_tbl.city,
		dataFeedOut_AddressUsPubLoad_tbl.stateID,
		dataFeedOut_AddressUsPubLoad_tbl.countryID,
		dataFeedOut_AddressUsPubLoad_tbl.zipCode,
		dataFeedOut_AddressUsPubLoad_tbl.primaryFlag,
		dataFeedOut_AddressUsPubLoad_tbl.otherPhoneValue,
		dataFeedOut_AddressUsPubLoad_tbl.officePhoneValue,
		dataFeedOut_AddressUsPubLoad_tbl.officeFaxValue
 
 	into DataFeedEngineCache.dbo.dataFeedOut_AddressUsPubFile_tbl 
		from DataFeedEngineCache.dbo.dataFeedOut_AddressUsPubLoad_tbl dataFeedOut_AddressUsPubLoad_tbl 
			left outer join dataFeedOut_AddressUsPub_tbl
				on dataFeedOut_AddressUsPub_tbl.addressID=dataFeedOut_AddressUsPubLoad_tbl.addressID
			where 
				dataFeedOut_AddressUsPub_tbl.addressID is null
			OR
 			(
				dataFeedOut_AddressUsPubLoad_tbl.objectID<> dataFeedOut_AddressUsPub_tbl.objectID
 			OR 
				dataFeedOut_AddressUsPubLoad_tbl.addressTypeID<> dataFeedOut_AddressUsPub_tbl.addressTypeID
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.streetAddress,'')<> isNull(dataFeedOut_AddressUsPub_tbl.streetAddress,'')
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.streetAddress2,'')<> isNull(dataFeedOut_AddressUsPub_tbl.streetAddress2,'')
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.streetAddress3,'')<> isNull(dataFeedOut_AddressUsPub_tbl.streetAddress3,'')
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.streetAddress4,'')<> isNull(dataFeedOut_AddressUsPub_tbl.streetAddress4,'')
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.city,'')<> isNull(dataFeedOut_AddressUsPub_tbl.city,'')
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.stateID,0)<> isNull(dataFeedOut_AddressUsPub_tbl.stateID,0)
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.countryID,0)<> isNull(dataFeedOut_AddressUsPub_tbl.countryID,0)
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.zipCode,'')<> isNull(dataFeedOut_AddressUsPub_tbl.zipCode,'')
 			OR 
				dataFeedOut_AddressUsPubLoad_tbl.primaryFlag<> dataFeedOut_AddressUsPub_tbl.primaryFlag
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.otherPhoneValue,'')<> isNull(dataFeedOut_AddressUsPub_tbl.otherPhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.officePhoneValue,'')<> isNull(dataFeedOut_AddressUsPub_tbl.officePhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressUsPubLoad_tbl.officeFaxValue,'')<> isNull(dataFeedOut_AddressUsPub_tbl.officeFaxValue,'')
			)
 
 
 
	Insert into DataFeedEngineCache.dbo.dataFeedOut_AddressUsPubFile_tbl
	select
	(case when dataFeedOut_AddressUsPubLoad_tbl.addressID is null then 'D' else 'E' end) as changeFlag,
				dataFeedOut_AddressUsPub_tbl.addressID,
				dataFeedOut_AddressUsPub_tbl.objectID,
				dataFeedOut_AddressUsPub_tbl.addressTypeID,
				dataFeedOut_AddressUsPub_tbl.streetAddress,
				dataFeedOut_AddressUsPub_tbl.streetAddress2,
				dataFeedOut_AddressUsPub_tbl.streetAddress3,
				dataFeedOut_AddressUsPub_tbl.streetAddress4,
				dataFeedOut_AddressUsPub_tbl.city,
				dataFeedOut_AddressUsPub_tbl.stateID,
				dataFeedOut_AddressUsPub_tbl.countryID,
				dataFeedOut_AddressUsPub_tbl.zipCode,
				dataFeedOut_AddressUsPub_tbl.primaryFlag,
				dataFeedOut_AddressUsPub_tbl.otherPhoneValue,
				dataFeedOut_AddressUsPub_tbl.officePhoneValue,
				dataFeedOut_AddressUsPub_tbl.officeFaxValue
		from dataFeedOut_AddressUsPub_tbl 
			left outer join DataFeedEngineCache.dbo.dataFeedOut_AddressUsPubLoad_tbl dataFeedOut_AddressUsPubLoad_tbl 
				on dataFeedOut_AddressUsPub_tbl.addressID=dataFeedOut_AddressUsPubLoad_tbl.addressID
		where dataFeedOut_AddressUsPubLoad_tbl.addressID is null
 
CREATE CLUSTERED INDEX IX_addressId_changeFlag ON DataFeedEngineCache.dbo.dataFeedOut_AddressUSPubFile_tbl (addressId, changeFlag)  

--Sample

	if exists (select * from DataFeedEngineCache.dbo.sysobjects (nolock) where name = 'dataFeedOut_AddressSampleFile_tbl' and xtype='U')
		drop table DataFeedEngineCache.dbo.dataFeedOut_AddressSampleFile_tbl
 
 
	select 
		(case when dataFeedOut_AddressSample_tbl.addressID is null then 'A' else 'U' end) as changeFlag,
		dataFeedOut_AddressSampleLoad_tbl.addressID,
		dataFeedOut_AddressSampleLoad_tbl.objectID,
		dataFeedOut_AddressSampleLoad_tbl.addressTypeID,
		dataFeedOut_AddressSampleLoad_tbl.streetAddress,
		dataFeedOut_AddressSampleLoad_tbl.streetAddress2,
		dataFeedOut_AddressSampleLoad_tbl.streetAddress3,
		dataFeedOut_AddressSampleLoad_tbl.streetAddress4,
		dataFeedOut_AddressSampleLoad_tbl.city,
		dataFeedOut_AddressSampleLoad_tbl.stateID,
		dataFeedOut_AddressSampleLoad_tbl.countryID,
		dataFeedOut_AddressSampleLoad_tbl.zipCode,
		dataFeedOut_AddressSampleLoad_tbl.primaryFlag,
		dataFeedOut_AddressSampleLoad_tbl.otherPhoneValue,
		dataFeedOut_AddressSampleLoad_tbl.officePhoneValue,
		dataFeedOut_AddressSampleLoad_tbl.officeFaxValue
 
 	into DataFeedEngineCache.dbo.dataFeedOut_AddressSampleFile_tbl 
		from DataFeedEngineCache.dbo.dataFeedOut_AddressSampleLoad_tbl dataFeedOut_AddressSampleLoad_tbl 
			left outer join dataFeedOut_AddressSample_tbl 
				on dataFeedOut_AddressSample_tbl.addressID = dataFeedOut_AddressSampleLoad_tbl.addressID
			where 
				dataFeedOut_AddressSample_tbl.addressID is null
			OR
 			(
				dataFeedOut_AddressSampleLoad_tbl.objectID<> dataFeedOut_AddressSample_tbl.objectID
 			OR 
				dataFeedOut_AddressSampleLoad_tbl.addressTypeID<> dataFeedOut_AddressSample_tbl.addressTypeID
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.streetAddress,'')<> isNull(dataFeedOut_AddressSample_tbl.streetAddress,'')
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.streetAddress2,'')<> isNull(dataFeedOut_AddressSample_tbl.streetAddress2,'')
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.streetAddress3,'')<> isNull(dataFeedOut_AddressSample_tbl.streetAddress3,'')
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.streetAddress4,'')<> isNull(dataFeedOut_AddressSample_tbl.streetAddress4,'')
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.city,'')<> isNull(dataFeedOut_AddressSample_tbl.city,'')
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.stateID,0)<> isNull(dataFeedOut_AddressSample_tbl.stateID,0)
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.countryID,0)<> isNull(dataFeedOut_AddressSample_tbl.countryID,0)
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.zipCode,'')<> isNull(dataFeedOut_AddressSample_tbl.zipCode,'')
 			OR 
				dataFeedOut_AddressSampleLoad_tbl.primaryFlag<> dataFeedOut_AddressSample_tbl.primaryFlag
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.otherPhoneValue,'')<> isNull(dataFeedOut_AddressSample_tbl.otherPhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.officePhoneValue,'')<> isNull(dataFeedOut_AddressSample_tbl.officePhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressSampleLoad_tbl.officeFaxValue,'')<> isNull(dataFeedOut_AddressSample_tbl.officeFaxValue,'')
			)
 
 
 
	Insert into DataFeedEngineCache.dbo.dataFeedOut_AddressSampleFile_tbl
	select
	(case when dataFeedOut_AddressSampleLoad_tbl.addressID is null then 'D' else 'E' end) as changeFlag,
				dataFeedOut_AddressSample_tbl.addressID,
				dataFeedOut_AddressSample_tbl.objectID,
				dataFeedOut_AddressSample_tbl.addressTypeID,
				dataFeedOut_AddressSample_tbl.streetAddress,
				dataFeedOut_AddressSample_tbl.streetAddress2,
				dataFeedOut_AddressSample_tbl.streetAddress3,
				dataFeedOut_AddressSample_tbl.streetAddress4,
				dataFeedOut_AddressSample_tbl.city,
				dataFeedOut_AddressSample_tbl.stateID,
				dataFeedOut_AddressSample_tbl.countryID,
				dataFeedOut_AddressSample_tbl.zipCode,
				dataFeedOut_AddressSample_tbl.primaryFlag,
				dataFeedOut_AddressSample_tbl.otherPhoneValue,
				dataFeedOut_AddressSample_tbl.officePhoneValue,
				dataFeedOut_AddressSample_tbl.officeFaxValue
		from dataFeedOut_AddressSample_tbl 
			left outer join DataFeedEngineCache.dbo.dataFeedOut_AddressSampleLoad_tbl dataFeedOut_AddressSampleLoad_tbl
				on dataFeedOut_AddressSample_tbl.addressID=dataFeedOut_AddressSampleLoad_tbl.addressID
		where dataFeedOut_AddressSampleLoad_tbl.addressID is null

CREATE CLUSTERED INDEX IX_addressId_changeFlag ON DataFeedEngineCache.dbo.dataFeedOut_AddressSampleFile_tbl (addressId, changeFlag)  

--Global pub

	if exists (select * from datafeedengineCache.dbo.sysobjects (nolock) where name = 'dataFeedOut_AddressGlobalPubFile_tbl' and xtype='U')
		drop table DataFeedEngineCache.dbo.dataFeedOut_AddressGlobalPubFile_tbl
 
 
	select 
		(case when dataFeedOut_AddressGlobalPub_tbl.addressID is null then 'A' else 'U' end) as changeFlag,
		dataFeedOut_AddressGlobalPubLoad_tbl.addressID,
		dataFeedOut_AddressGlobalPubLoad_tbl.objectID,
		dataFeedOut_AddressGlobalPubLoad_tbl.addressTypeID,
		dataFeedOut_AddressGlobalPubLoad_tbl.streetAddress,
		dataFeedOut_AddressGlobalPubLoad_tbl.streetAddress2,
		dataFeedOut_AddressGlobalPubLoad_tbl.streetAddress3,
		dataFeedOut_AddressGlobalPubLoad_tbl.streetAddress4,
		dataFeedOut_AddressGlobalPubLoad_tbl.city,
		dataFeedOut_AddressGlobalPubLoad_tbl.stateID,
		dataFeedOut_AddressGlobalPubLoad_tbl.countryID,
		dataFeedOut_AddressGlobalPubLoad_tbl.zipCode,
		dataFeedOut_AddressGlobalPubLoad_tbl.primaryFlag,
		dataFeedOut_AddressGlobalPubLoad_tbl.otherPhoneValue,
		dataFeedOut_AddressGlobalPubLoad_tbl.officePhoneValue,
		dataFeedOut_AddressGlobalPubLoad_tbl.officeFaxValue
 
 	into DataFeedEngineCache.dbo.dataFeedOut_AddressGlobalPubFile_tbl 
		from DataFeedEngineCache.dbo.dataFeedOut_AddressGlobalPubLoad_tbl dataFeedOut_AddressGlobalPubLoad_tbl 
			left outer join dataFeedOut_AddressGlobalPub_tbl
				on dataFeedOut_AddressGlobalPub_tbl.addressID=dataFeedOut_AddressGlobalPubLoad_tbl.addressID
			where 
				dataFeedOut_AddressGlobalPub_tbl.addressID is null
			OR
 			(
				dataFeedOut_AddressGlobalPubLoad_tbl.objectID<> dataFeedOut_AddressGlobalPub_tbl.objectID
 			OR 
				dataFeedOut_AddressGlobalPubLoad_tbl.addressTypeID<> dataFeedOut_AddressGlobalPub_tbl.addressTypeID
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.streetAddress,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.streetAddress,'')
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.streetAddress2,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.streetAddress2,'')
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.streetAddress3,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.streetAddress3,'')
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.streetAddress4,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.streetAddress4,'')
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.city,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.city,'')
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.stateID,0)<> isNull(dataFeedOut_AddressGlobalPub_tbl.stateID,0)
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.countryID,0)<> isNull(dataFeedOut_AddressGlobalPub_tbl.countryID,0)
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.zipCode,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.zipCode,'')
 			OR 
				dataFeedOut_AddressGlobalPubLoad_tbl.primaryFlag<> dataFeedOut_AddressGlobalPub_tbl.primaryFlag
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.otherPhoneValue,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.otherPhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.officePhoneValue,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.officePhoneValue,'')
 			OR 
				isNull(dataFeedOut_AddressGlobalPubLoad_tbl.officeFaxValue,'')<> isNull(dataFeedOut_AddressGlobalPub_tbl.officeFaxValue,'')
			)
 
 
 
	Insert into DataFeedEngineCache.dbo.dataFeedOut_AddressGlobalPubFile_tbl
	select
	(case when dataFeedOut_AddressGlobalPubLoad_tbl.addressID is null then 'D' else 'E' end) as changeFlag,
				dataFeedOut_AddressGlobalPub_tbl.addressID,
				dataFeedOut_AddressGlobalPub_tbl.objectID,
				dataFeedOut_AddressGlobalPub_tbl.addressTypeID,
				dataFeedOut_AddressGlobalPub_tbl.streetAddress,
				dataFeedOut_AddressGlobalPub_tbl.streetAddress2,
				dataFeedOut_AddressGlobalPub_tbl.streetAddress3,
				dataFeedOut_AddressGlobalPub_tbl.streetAddress4,
				dataFeedOut_AddressGlobalPub_tbl.city,
				dataFeedOut_AddressGlobalPub_tbl.stateID,
				dataFeedOut_AddressGlobalPub_tbl.countryID,
				dataFeedOut_AddressGlobalPub_tbl.zipCode,
				dataFeedOut_AddressGlobalPub_tbl.primaryFlag,
				dataFeedOut_AddressGlobalPub_tbl.otherPhoneValue,
				dataFeedOut_AddressGlobalPub_tbl.officePhoneValue,
				dataFeedOut_AddressGlobalPub_tbl.officeFaxValue
		from dataFeedOut_AddressGlobalPub_tbl 
			left outer join DataFeedEngineCache.dbo.dataFeedOut_AddressGlobalPubLoad_tbl dataFeedOut_AddressGlobalPubLoad_tbl 
				on dataFeedOut_AddressGlobalPub_tbl.addressID=dataFeedOut_AddressGlobalPubLoad_tbl.addressID
		where dataFeedOut_AddressGlobalPubLoad_tbl.addressID is null

	CREATE CLUSTERED INDEX IX_addressId_changeFlag ON DataFeedEngineCache.dbo.dataFeedOut_AddressGlobalPubFile_tbl (addressId, changeFlag)



