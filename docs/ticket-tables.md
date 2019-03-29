# チケット管理リモートサーバ仕様（テーブル）

<a name="table-list"></a>
## １．テーブル一覧

### (1) マスタ系
|No|名称|物理名|説明|
|:-:|:--|:--|:--|
|1|[プロジェクト](#tbl-01-001)|m_project||
|2|[ユーザ](#tbl-01-002)|m_user||
|3|[言語](#tbl-01-003)|m_language||
|4|[ロールグループ名](#tbl-01-004)|m_rollGroup||
|5|[ロール項目名](#tbl-01-005)|m_rollItem||

### (2) トランザクション系
|No|名称|物理名|説明|
|:-:|:--|:--|:--|
|1|[セッション](#tbl-02-001)|t_session||
|2|[ロール名](#tbl-02-002)|t_roll_name||
|3|[ロール許可](#tbl-02-003)|t_roll_setting||
|4|[チケット](#tbl-02-004)|t_ticket||
|5|[チケットメモ](#tbl-02-005)|t_ticket_memo||
|6|[プロジェクト状態](#tbl-02-006)|t_proj_stat||
|7|[チケット状態](#tbl-02-007)|t_ticket_stat||
|8|[チケット進捗](#tbl-02-008)|t_ticket_progress||
|9|[チケット種類](#tbl-02-009)|t_ticket_kind||
|10|[チケット優先順位](#tbl-02-010)|t_ticket_priority||

### (3) 履歴系
|No|名称|物理名|説明|
|:-:|:--|:--|:--|
|1|[チケット](#tbl-03-001)|h_ticket||
|2|[チケットメモ](#tbl-03-002)|h_ticket_memo||

***
## ２．テーブル構造

### (1) マスタ系
<a name="tbl-01-001"></a>
#### a. プロジェクト（m_project）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|ID|id|int||1|||自動付番|
|2|名称|name|varchar|256|||||
|3|説明|description|varchar|1024|||||
|4|管理者ID|manager_id|int|||no|||
|5|進行中|alive|varchar|10||no|'yes'||
|6|第三者に公開|opened|varchar|10||no|'no'||
|7|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|8|作成者ID|createUserId|int|||no|||
|9|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|10|更新者ID|updateUserId|int|||no|||
|11|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-01-002"></a>
#### b. ユーザ（m_user）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|ID|id|int||1||||
|2|ログインID|login_id|varchar|256||||unique|
|3|パスワード|passwd|varchar|256||no||暗号化|
|4|性|name1|varchar|256||no|||
|5|名|name2|varchar|256||no|||
|6|メルアド|email|varchar|256||no|||
|7|言語ID|language_id|int|||no|||
|8|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|作成者ID|createUserId|int|||no|||
|10|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|11|更新者ID|updateUserId|int|||no|||
|12|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-01-003"></a>
#### c. 言語（m_language）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|ID|id|int||1|||自動付番|
|2|言語名|name|varchar|64||no|||
|3|国名|country|varchar|64||no|||
|4|説明|remarks|varchar|64|||||
|5|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|6|作成者ID|createUserId|int|||no|||
|7|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|8|更新者ID|updateUserId|int|||no|||
|9|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-01-004"></a>
#### d. ロールグループ名（m_rollGroup）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|ID|id|int||1||||
|2|グループ名|name|varchar|64||no|||
|3|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|4|作成者ID|createUserId|int|||no|||
|5|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|6|更新者ID|updateUserId|int|||no|||
|7|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-01-005"></a>
#### e. ロール項目名（m_rollItem）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|ID|id|int||1||||
|2|ロール名|name|varchar|64||no|||
|3|ロールグループID|group_id|int|||no|||
|4|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|5|作成者ID|createUserId|int|||no|||
|6|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|更新者ID|updateUserId|int|||no|||
|8|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

***
##### (2) トランザクション系
<a name="tbl-02-001"></a>
#### a. セッション（t_session）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|セッションID|session_id|varchar|64|1||||
|2|ユーザID|user_id|int||||||
|3|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|4|作成者ID|createUserId|int|||no|||
|5|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|6|更新者ID|updateUserId|int|||no|||
|7|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-002"></a>
#### b. ロール名（t_roll_name）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|ID|id|int||1||||
|2|名称|name|varchar|256||no|||
|3|説明|description|varchar|1024|||||
|4|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|5|作成者ID|createUserId|int|||no|||
|6|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|更新者ID|updateUserId|int|||no|||
|8|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-003"></a>
#### c. ロール許可（t_roll_setting）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|名称ID|roll_name_id|int||1||||
|2|項目ID|roll_item_id|int||2||||
|3|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|4|作成者ID|createUserId|int|||no|||
|5|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|6|更新者ID|updateUserId|int|||no|||
|7|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-004"></a>
#### d. チケット（t_ticket）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|チケットID|id|int||1||||
|2|チケットタイトル|title|varchar|256||no|||
|3|説明|description|varchar|1024|||||
|4|ステータスID|status_id|int||||||
|5|種類ID|kind_id|int||||||
|6|優先順位ID|priority_id|int||||||
|7|開始日|start_date|DATE||||||
|8|終了日|finish_date|DATE||||||
|9|チケットの進捗|progress_id|int||||||
|10|プロジェクトID|project_id|int||||||
|11|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|12|作成者ID|createUserId|int|||no|||
|13|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|14|更新者ID|updateUserId|int|||no|||
|15|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-005"></a>
#### e. チケットメモ（t_ticket_memo）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|メモID|id|int||2||||
|2|チケットID|ticket_id|int||1||||
|3|説明|memo|varchar|1024||no|||
|4|ルートメモID|root_memo_id|int|||no||
|5|親メモID|parent_memo_id|int|||no||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-006"></a>
#### f. プロジェクト状態（t_proj_stat）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|int||1||||
|2|状態ID|id|int||2||||
|3|表示順|disp_seq|int||||||
|4|状態名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-007"></a>
#### g. チケット状態（t_ticket_stat）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|int||1||||
|2|状態ID|id|int||2||||
|3|表示順|disp_seq|int||||||
|4|状態名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-008"></a>
#### h. チケット進捗（t_ticket_progress）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|int||1||||
|2|進捗ID|id|int||2||||
|3|表示順|disp_seq|int||||||
|4|進捗名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-009"></a>
#### l. チケット種類（t_ticket_kind）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|int||1||||
|2|種類ID|id|int||2||||
|3|表示順|disp_seq|int||||||
|4|種類名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

<a name="tbl-02-010"></a>
#### j. チケット優先順位（t_ticket_priority）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|プロジェクトID|project_id|int||1||||
|2|優先順位ID|id|int||2||||
|3|表示順|disp_seq|int||||||
|4|優先順位名称|name|varchar|256||no|||
|5|有効フラグ|available|varchar|10||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int|||no|1||

[【一覧へ】](#table-list)

***
##### (3) 履歴系

<a name="tbl-03-001"></a>
#### a. チケット履歴（h_ticket）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|チケットID|id|int||1||||
|2|チケットタイトル|title|varchar|256||no|||
|3|説明|description|varchar|1024|||||
|4|ステータスID|status_id|int||||||
|5|種類ID|kind_id|int||||||
|6|優先順位ID|priority_id|int||||||
|7|開始日|start_date|DATE||||||
|8|終了日|finish_date|DATE||||||
|9|チケットの進捗|progress_id|int||||||
|10|プロジェクトID|project_id|int||||||
|11|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|12|作成者ID|createUserId|int|||no|||
|13|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|14|更新者ID|updateUserId|int|||no|||
|15|バージョンNo|versionNo|int||2|no|1||

[【一覧へ】](#table-list)

<a name="tbl-03-002"></a>
#### b. チケットメモ履歴（h_ticket_memo）

|No|列名称|物理名|型|size|PK|null|default|説明|
|:-:|:--|:--|:-:|--:|:-:|:-:|:--|:--|
|1|メモID|id|int||1||||
|2|チケットID|ticket_id|int||2||||
|3|説明|memo|varchar|1024||no|||
|4|ルートメモID|root_memo_id|int|||no|||
|5|親メモID|parent_memo_id|int|||no|||
|6|作成日時|createDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|7|作成者ID|createUserId|int|||no|||
|8|更新日時|updateDate|TIMESTAMP|||no|CURRENT_TIMESTAMP||
|9|更新者ID|updateUserId|int|||no|||
|10|バージョンNo|versionNo|int||3|no|1||

[【一覧へ】](#table-list)
