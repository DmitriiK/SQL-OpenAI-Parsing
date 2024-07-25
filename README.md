# Leveraging of LLMs to analyze SQL code and to build data lineage and Mermaid data flow diagrams
## Objectives:
 - Given a set of files with SQL code, feed them to LLM model in order to build data flow documentation. 
It addresses the pain of necessity of soring out the logic of SQL code in customerms DB, with huge amount of tables and stored procedures, but without any documentation

## Implementation:
- First step. Feed SQL code (stored procedures, functions, views and scripts) to Open AI (or any other LLM). 
For each stored procedure  LLM supposed to build (using Langchain YamlOutputParser) instanses of specific pydantic data classes. Final output is yaml files that look like this:
```yaml
sp_name: MergeData_Russell2_IndexValue_prc
DCSs:
- crud_type: MERGE
  target_table: dbo.Russell2_IndexValue_tbl
  source_tables:
  - dbo.Russell2_Stg_IndexValue_Value112099_tbl
  - dbo.Russell2_Stg_IndexValue_Value112100_tbl
  - dbo.Russell2_Stg_IndexValue_Value112102_tbl
  - dbo.Russell2_Stg_IndexValue_Value112103_tbl
  - dbo.Russell2_Stg_IndexValue_Value112106_tbl
  - dbo.Russell2_Stg_IndexValue_ValueOther_tbl
```
- Second step. Using yaml files from previous step, build the chain of source - target dependenencies and finally - visualize such chain as mermaid data flow diagram, that might look like this
 ```mermaid
flowchart TD
   D1[Indexdata.dbo.IndexConstituent_tbl]
   D2[Indexdata.dbo.IndexToConstituentChain_tbl]
   D[DataFeedOut_Russell2_PortfolioHolding_vw]
   E[Russell2_Stg_PortfolioHolding_tbl]
   F[stg.RussellUS2_Constituent_tbl]
   D1-->|view|D
   D2-->|view|D
   D-->|insert: PullData_Russell2_PortfolioHolding_prc|E
   E-->|insert: PullData_RussellUS2_Constituent_prc|F
   F-->|merge: MergeData_RussellUS2_Constituent_prc| G[RussellUS2_Constituent_tbl]
- 
   
