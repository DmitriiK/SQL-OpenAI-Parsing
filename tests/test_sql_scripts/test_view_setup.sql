-- Use CIQData database to create tables and the view
USE CIQData;
GO

-- Create Table1 in CIQData
CREATE TABLE Table1 (
    ID INT PRIMARY KEY,
    Name NVARCHAR(100),
    Value DECIMAL(18, 2)
);
GO

-- Create Table2 in CIQData
CREATE TABLE Table2 (
    ID INT PRIMARY KEY,
    Table1ID INT FOREIGN KEY REFERENCES Table1(ID),
    Description NVARCHAR(255)
);
GO

-- Create Table3 in CIQData
CREATE TABLE Table3 (
    ID INT PRIMARY KEY,
    Table2ID INT FOREIGN KEY REFERENCES Table2(ID),
    Amount DECIMAL(18, 2)
);
GO

-- Create a view in CIQData that combines relevant tables
CREATE VIEW vSourceData AS
SELECT 
    t1.ID AS Table1ID,
    t1.Name,
    t1.Value,
    t2.ID AS Table2ID,
    t2.Description,
    t3.ID AS Table3ID,
    t3.Amount
FROM 
    Table1 t1
JOIN 
    Table2 t2 ON t1.ID = t2.Table1ID
JOIN 
    Table3 t3 ON t2.ID = t3.Table2ID;
GO

-- Now switch to DataFeedEngineIndex database to create tables and the view
USE DataFeedEngineIndex;
GO

-- Create TableA in DataFeedEngineIndex
CREATE TABLE TableA (
    ID INT PRIMARY KEY,
    ReferenceID INT,
    Data NVARCHAR(100)
);
GO

-- Create TableB in DataFeedEngineIndex
CREATE TABLE TableB (
    ID INT PRIMARY KEY,
    TableAID INT FOREIGN KEY REFERENCES TableA(ID),
    Info NVARCHAR(255)
);
GO

-- Create TableC in DataFeedEngineIndex
CREATE TABLE TableC (
    ID INT PRIMARY KEY,
    TableBID INT FOREIGN KEY REFERENCES TableB(ID),
    Total DECIMAL(18, 2)
);
GO

-- Create a complex view in DataFeedEngineIndex that joins data with CIQData view
CREATE VIEW vComplexView AS
SELECT 
    v.Table1ID,
    v.Name,
    v.Value,
    v.Table2ID,
    v.Description,
    v.Table3ID,
    v.Amount,
    ta.Data AS TableAData,
    tb.Info AS TableBInfo
FROM 
    CIQData.dbo.vSourceData v
JOIN 
    DataFeedEngineIndex.dbo.TableA ta ON ta.ReferenceID = v.Table1ID
JOIN 
	TableB tb ON tb.TableAID = ta.ID;
GO