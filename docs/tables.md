# チケット管理リモートサーバ仕様（テーブル）

## １．テーブル一覧

### (1) マスタ系
|No|名称|物理名|説明|
|:-:|:--|:--|:--|
|1|プロジェクト|m_project||
|2|ユーザ|m_user||
|3|言語|m_language||
|4|ロールグループ名|m_rollGroup||
|5|ロール項目名|m_rollItem||

### (2) トランザクション系
|No|名称|物理名|説明|
|:-:|:--|:--|:--|
|1|セッション|t_session||
|2|ロール名|t_roll_name|？？|
|3|ロール許可|t_roll_setting||
|4|チケット|t_ticket||
|5|チケットメモ|t_ticket_memo||
|6|プロジェクト状態|t_proj_stat||
|7|チケット状態|t_ticket_stat||
|8|チケット進捗|t_ticket_progress||
|9|チケット種類|t_ticket_kind||
|10|チケット優先順位|t_ticket_priority||

### (3) 履歴系
|No|名称|物理名|説明|
|:-:|:--|:--|:--|
|1|チケット|h_ticket||
|2|チケットメモ|h_ticket_memo||

## ２．テーブル構造

### (1) マスタ系
#### a. プロジェクト（m_project）
工事中
#### b. ユーザ（m_user）
工事中
#### c. 言語（m_language）
工事中
#### d. ロールグループ名（m_rollGroup）
工事中
#### e. ロール項目名（m_rollItem）
工事中


##### (2) トランザクション系
#### a. セッション（t_session）
工事中
#### b. ロール名（t_roll_name）
工事中
#### c. ロール許可（t_roll_setting）
工事中
#### d. チケット（t_ticket）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|チケットID|id|bigint||1||||
|2|チケットタイトル|title|varchar|256||no|||
|3|説明|description|varchar|1024|||||
|4|ステータスID|status_id|bigint||||||
|5|種類ID|kind_id|bigint||||||
|6|優先順位ID|priority_id|bigint||||||
|7|開始日|start_date|DATE||||||
|8|終了日|finish_date|DATE||||||
|9|チケットの進捗|progress_id|bigint||||||
|10|プロジェクトID|project_id|bigint||||||
|11|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|12|作成者ID|createUserId|int|||no|||
|13|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|14|更新者ID|updateUserId|int|||no|||
|15|バージョンNo|versionNo|int|||no|1||


#### e. チケットメモ（t_ticket_memo）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|メモID|id|bigint||2||||
|2|チケットID|ticket_id|bigint||1||||
|3|説明|memo|varchar|1024||no|||
|4|ルートメモID|root_memo_id|bigint|||no||
|5|親メモID|parent_memo_id|bigint|||no||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

#### f. プロジェクト状態（t_proj_stat）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|bigint||1||||
|2|状態ID|id|bigint||2||||
|3|表示順|disp_seq|int||||||
|4|状態名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

#### g. チケット状態（t_ticket_stat）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|bigint||1||||
|2|状態ID|id|bigint||2||||
|3|表示順|disp_seq|int||||||
|4|状態名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

#### h. チケット進捗（t_ticket_progress）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|bigint||1||||
|2|進捗ID|id|bigint||2||||
|3|表示順|disp_seq|int||||||
|4|進捗名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||


#### l. チケット種類（t_ticket_kind）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|bigint||1||||
|2|種類ID|id|bigint||2||||
|3|表示順|disp_seq|int||||||
|4|種類名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

#### j. チケット優先順位（t_ticket_priority）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|bigint||1||||
|2|優先順位ID|id|bigint||2||||
|3|表示順|disp_seq|int||||||
|4|優先順位名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

##### (3) 履歴系

#### a. チケット履歴（h_ticket）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|チケットID|id|bigint||1||||
|2|チケットタイトル|title|varchar|256||no|||
|3|説明|description|varchar|1024|||||
|4|ステータスID|status_id|bigint||||||
|5|種類ID|kind_id|bigint||||||
|6|優先順位ID|priority_id|bigint||||||
|7|開始日|start_date|DATE||||||
|8|終了日|finish_date|DATE||||||
|9|チケットの進捗|progress_id|bigint||||||
|10|プロジェクトID|project_id|bigint||||||
|11|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|12|作成者ID|createUserId|int|||no|||
|13|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|14|更新者ID|updateUserId|int|||no|||
|15|バージョンNo|versionNo|int||2|no|1||


#### b. チケットメモ履歴（h_ticket_memo）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|メモID|id|bigint||1||||
|2|チケットID|ticket_id|bigint||2||||
|3|説明|memo|varchar|1024||no|||
|4|ルートメモID|root_memo_id|bigint|||no|||
|5|親メモID|parent_memo_id|bigint|||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int||3|no|1||