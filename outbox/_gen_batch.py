import json

articles = []

# 1. RDS SQL Server audit logs to CloudWatch
articles.append({
  "slug": "aws-what-s-new-rds-sqlserver-publish-sql-audit-to-cw",
  "title": "Amazon RDS for SQL Server、監査ログをCloudWatchでリアルタイム分析できるようになったよ！",
  "summary": "Amazon RDS for SQL Server が、SQL Server Audit のログを Amazon CloudWatch にも公開できるようになったよ。S3 に加えて CloudWatch にも送れるから、監査ログをリアルタイムで分析できるようになったの。",
  "body_md": """やっほー、しぃちゃんだよ！今日は RDS を使っているみんなに知らせたい、地味だけど大事なニュースがあるよ！

## なにが発表されたの？

AWS の What's New によると、Amazon RDS for SQL Server が、SQL Server Audit のログを Amazon CloudWatch にも公開できるようになったよ。SQL Server Audit は、データベースエンジン上で起きたイベントを追跡・記録できるネイティブの SQL Server 機能で、RDS 上でもオンプレミスの SQL Server と同じやり方で監査やその仕様(audit specification)を作れるの。今回のアップデートで、その監査ログの送り先が S3 だけじゃなく CloudWatch にも広がったんだね。

## 今までどうだったの？

これまでも RDS for SQL Server の監査ログは S3 に送れたんだけど、CloudWatch には対応していなかったの。S3 に貯めたログを分析しようと思うと、別のツールで取り込んだり、あとからまとめて確認したりする必要があって、「今まさに何が起きているか」をリアルタイムで追いかけるのはちょっと不向きだったんだよね。

## これで何が変わるの？

- 監査ログの送り先を S3、CloudWatch、または両方から選べるようになったよ
- 両方を有効にした場合、ログファイルが S3 と CloudWatch の両方にアップロードされて初めて、その監査ログの公開が「完了」扱いになるの
- CloudWatch にログが入るようになったから、ログデータのリアルタイム分析ができるようになったよ
- 保持設定(retention)を有効にすると、設定した期間ぶんの監査ログを DB インスタンス側にも保管しておけるの

セキュリティ監視やコンプライアンス対応で、監査ログを CloudWatch のアラームや他のモニタリングの仕組みと組み合わせたい人には、地味だけどうれしいアップデートだと思うな。

## 深く潜ってみよう

SQL Server Audit の仕組みそのものについては、SQL Server ドキュメントの「SQL Server Audit (database engine)」に詳しくまとまっているよ。RDS 側の設定手順は Amazon RDS for SQL Server User Guide を見てね。対応リージョンは、すべての AWS 商用リージョンと AWS GovCloud (US) リージョンのうち、Amazon RDS for SQL Server が使えるところ全部だよ。

## まとめ

- Amazon RDS for SQL Server の監査ログが、CloudWatch にも公開できるようになった
- S3、CloudWatch、または両方を送り先に選べる。両方有効時は両方へのアップロード完了で「完了」扱い
- CloudWatch 上でログデータをリアルタイムに分析できる
- 保持設定を使えば、DB インスタンス側にも監査ログを保管できる
- すべての AWS 商用リージョンと AWS GovCloud (US) の対応リージョンで利用可能

SQL Server のセキュリティ監査を CloudWatch のモニタリング体制に組み込みたい DBA やセキュリティ担当のみんなに刺さるアップデートだよ！""",
  "title_en": "Amazon RDS for SQL Server Can Now Stream Audit Logs to CloudWatch in Real Time!",
  "summary_en": "Amazon RDS for SQL Server can now publish SQL Server Audit logs to Amazon CloudWatch, in addition to S3, enabling real-time analysis of your audit log data.",
  "body_md_en": """Hi, it's Shiichan! Today I've got a quiet but useful update for anyone running RDS.

## What was announced?

According to AWS What's New, Amazon RDS for SQL Server can now publish SQL Server Audit logs to Amazon CloudWatch. SQL Server Audit is a native SQL Server feature that tracks and logs events happening on the database engine, and on RDS you can create audits and audit specifications the same way you would on-premises. With this update, the destination for those audit logs now extends beyond S3 to CloudWatch as well.

## The story so far

Until now, RDS for SQL Server audit logs could only be published to S3. If you wanted to analyze that data, you had to ingest it into another tool or review it after the fact in batches, which wasn't a great fit for keeping an eye on what's happening right now.

## What changes

- You can now choose S3, CloudWatch, or both as the destination for your audit logs
- If both are enabled, the publication is only marked "completed" once the log files have been uploaded to both S3 and CloudWatch
- With logs flowing into CloudWatch, you can now analyze audit log data in real time
- If you enable retention, RDS also keeps your audit logs on the DB instance for the configured period

This is a quietly useful update if you want to fold audit logs into CloudWatch alarms or other monitoring you already have set up for security or compliance purposes.

## Dive Deep

For details on SQL Server Audit itself, check "SQL Server Audit (database engine)" in the SQL Server documentation. For setup steps on RDS, see the Amazon RDS for SQL Server User Guide. This is available in all AWS Commercial Regions and AWS GovCloud (US) Regions where Amazon RDS for SQL Server is available.

## Wrap-up

- Amazon RDS for SQL Server audit logs can now be published to CloudWatch
- You can choose S3, CloudWatch, or both — with both enabled, "completed" means uploaded to both
- CloudWatch lets you analyze audit log data in real time
- Enabling retention also keeps audit logs on the DB instance itself
- Available in all AWS Commercial Regions and supported AWS GovCloud (US) Regions

A solid pick for DBAs and security folks who want to fold SQL Server audit data into their CloudWatch monitoring setup!""",
  "emotion": "happy",
  "importance": 2,
  "source_url": "https://aws.amazon.com/about-aws/whats-new/2026/07/rds-sqlserver-publish-sql-audit-to-cw/",
  "source_name": "AWS What's New",
  "og_title": "RDS SQL Server now supports publishing SQL Server Audit logs to CloudWatch",
  "tags": ["aws", "security", "infrastructure"],
  "published_at": "2026-08-04T07:00:00+00:00",
})

# 2. Amazon Connect Customer interval capacity planning
articles.append({
  "slug": "aws-what-s-new-amazon-connect-customer-interval-capacity-plan",
  "title": "コンタクトセンターの人員計画、15分・30分単位で立てられるようになったって知ってた？",
  "summary": "Amazon Connect Customer のキャパシティプランニングが、15 分・30 分単位のインターバルレベルに対応したよ。Voice・Chat・Task・Email の全チャネルで、1 日の中の需要変動を細かく捉えて人員配置を最適化できるようになったの。",
  "body_md": """みんな、しぃちゃんだよ！今日はコンタクトセンターの人員計画に関わる、うれしいアップデートを見つけたよ！

## なにが発表されたの？

AWS の What's New によると、Amazon Connect Customer のキャパシティプランニング機能が、15 分または 30 分単位のインターバルレベルで計画を作れるようになったよ。ワークフォースプランナーが、Voice・Chat・Task・Email の全チャネルにわたって、より細かい粒度でスタッフィング(人員配置)の必要量を見られるようになったの。

## 今までどうだったの？

コンタクトセンターの需要って、1 日の中でもけっこう波があるんだよね。お昼どきにチャットの問い合わせが増えたり、営業終了間際に電話の量が変わったり。こういう短い時間軸での需要の動きを、これまでのキャパシティプランではきめ細かく捉えるのが難しかったの。だからこそ、インターバル単位で計画を作れるようになったのは大きな進歩なんだ。

## これで何が変わるの？

- 15 分、または 30 分単位でキャパシティプランを作成できるようになったよ
- Voice・Chat・Task・Email の全チャネルが対象
- インターバル単位で、間欠率(shrinkage)の仮定や利用可能な人員数も設定できる
- 需要の変化に合わせて人員配置を細かく調整できるから、過剰配置・不足配置を減らして、サービスレベルと運用効率の向上につながるの

## 深く潜ってみよう

この機能は、Amazon Connect Customer のエージェントスケジューリングが使えるすべての AWS リージョンで利用できるよ。より詳しい使い方は Amazon Connect のエージェントスケジューリングのドキュメントを見てみてね。

## まとめ

- Amazon Connect Customer のキャパシティプランニングが 15 分・30 分単位のインターバルレベルに対応
- Voice・Chat・Task・Email の全チャネルが対象
- 間欠率や利用可能な人員数もインターバル単位で設定可能
- 過剰配置・不足配置の削減、サービスレベルと運用効率の向上が期待できる

コンタクトセンターのワークフォースプランニングを担当していて、1 日の中の細かい需要変動に合わせてスタッフィングを最適化したい人にぴったりのアップデートだよ！""",
  "title_en": "Did You Know Contact Center Capacity Planning Can Now Go Down to 15-Minute Intervals?",
  "summary_en": "Amazon Connect Customer's capacity planning now supports 15- or 30-minute intervals, letting workforce planners capture demand shifts across Voice, Chat, Task, and Email channels throughout the day.",
  "body_md_en": """Hey everyone, it's Shiichan! I found a nice update today for anyone doing workforce planning in a contact center.

## What was announced?

According to AWS What's New, Amazon Connect Customer's capacity planning now supports interval-level plans at 15-minute or 30-minute granularity. Workforce planners can now see staffing requirements in much finer detail, across Voice, Chat, Task, and Email channels.

## The story so far

Demand in a contact center swings quite a bit within a single day — a lunchtime surge in chat contacts, or a change in call volume near closing time. Capturing those short-term shifts with the level of detail needed was hard with the capacity plans available before, which makes interval-level planning a genuinely meaningful step forward.

## What changes

- You can now build capacity plans at 15-minute or 30-minute interval granularity
- This covers all channels: Voice, Chat, Task, and Email
- You can also set shrinkage assumptions and available headcount at the interval level
- Aligning staffing with demand as it shifts helps reduce over- and under-staffing, improving service levels and operational efficiency

## Dive Deep

This feature is available in every AWS Region where Amazon Connect Customer agent scheduling is supported. For more on how to use it, check the Amazon Connect agent scheduling documentation.

## Wrap-up

- Amazon Connect Customer's capacity planning now supports 15-minute and 30-minute intervals
- Covers Voice, Chat, Task, and Email channels
- Shrinkage assumptions and available headcount can also be set at the interval level
- Helps reduce over- and under-staffing while improving service levels and efficiency

A great fit for anyone doing workforce planning for a contact center who wants staffing to track fine-grained demand shifts throughout the day!""",
  "emotion": "happy",
  "importance": 2,
  "source_url": "https://aws.amazon.com/about-aws/whats-new/2026/08/amazon-connect-customer-interval-capacity-plan",
  "source_name": "AWS What's New",
  "og_title": "Amazon Connect Customer now supports capacity planning in 15 or 30 minute intervals",
  "tags": ["aws", "business"],
  "published_at": "2026-08-04T17:00:00+00:00",
})

# 3. S3 Vectors in AWS European Sovereign Cloud (Germany)
articles.append({
  "slug": "aws-what-s-new-amazon-s3-vectors-european-sovereign-cloud-germany",
  "title": "まさかのドイツ上陸！Amazon S3 Vectors が欧州主権クラウドでも使えるようになったよ！",
  "summary": "ベクトル専用ストレージの Amazon S3 Vectors が、AWS European Sovereign Cloud(ドイツ)リージョンでも使えるようになったよ。数十億規模のベクトルを扱える S3 Vectors が、データも運用も EU 域内で完結する主権クラウドでも使えるようになったの。",
  "body_md": """おつかれさま、しぃちゃんだよ！今日はヨーロッパの AI インフラまわりで面白いニュースを見つけたよ！

## なにが発表されたの？

AWS の What's New によると、Amazon S3 Vectors が AWS European Sovereign Cloud(ドイツ)リージョンで利用できるようになったよ。S3 Vectors は、AI エージェントや推論、RAG(Retrieval Augmented Generation)、セマンティック検索向けに作られた、数十億規模のベクトルまで扱える専用のベクトルストレージなの。S3 と同じ拡張性・耐久性・可用性を保ちながら、インフラをプロビジョニングせずにベクトルを保存・アクセス・クエリできる専用 API を備えているのが特徴だよ。

## 今までどうだったの？

S3 Vectors 自体はすでにいくつかの AWS リージョンで使えるようになっていたけど、AWS European Sovereign Cloud ではまだ対応していなかったの。AWS European Sovereign Cloud は、データもオペレーションも EU 域内で完結させることを重視した、独立した運用体制を持つクラウドで、厳しい規制やデータ主権の要件を持つ組織向けに用意されているんだよね。だから今まで、S3 Vectors を使ったベクトル検索や RAG 基盤を、そうした主権要件を満たしたまま作るのは難しかったんだ。

## これで何が変わるの？

- AWS European Sovereign Cloud(ドイツ)リージョンでも、S3 Vectors によるベクトルストレージを直接使えるようになったよ
- インフラの管理をしなくても、S3 と同じ感覚でベクトルの保存・検索ができる
- データ主権の要件が厳しいヨーロッパの組織でも、AI エージェントや RAG、セマンティック検索の基盤を主権クラウドの中に組めるようになったの

## 深く潜ってみよう

対応リージョンの最新の一覧は AWS の Regions and endpoints のページにまとまっているよ。S3 Vectors の詳しい仕組みや料金は、製品ページ・ドキュメント・S3 の料金ページを見てみてね。

## まとめ

- Amazon S3 Vectors が AWS European Sovereign Cloud(ドイツ)リージョンで利用可能に
- 数十億規模のベクトルを扱える、S3 譲りの拡張性・耐久性を持つ専用ストレージ
- インフラ管理なしで、専用 API からベクトルの保存・アクセス・クエリができる
- データ主権の要件が厳しいヨーロッパの組織でも、AI・RAG 基盤を組みやすくなった

EU 域内でのデータ主権を重視しながら、AI エージェントや RAG、セマンティック検索を作りたいヨーロッパの開発者・企業にとって見逃せないアップデートだよ！""",
  "title_en": "Amazon S3 Vectors Arrives in AWS's European Sovereign Cloud in Germany!",
  "summary_en": "Amazon S3 Vectors, purpose-built vector storage for AI workloads, is now available in the AWS European Sovereign Cloud (Germany) Region, bringing billion-scale vector search to a cloud designed to keep data and operations within the EU.",
  "body_md_en": """Hey, it's Shiichan! I found an interesting one today about AI infrastructure in Europe.

## What was announced?

According to AWS What's New, Amazon S3 Vectors is now available in the AWS European Sovereign Cloud (Germany) Region. S3 Vectors is purpose-built vector storage designed for AI agents, inference, Retrieval Augmented Generation (RAG), and semantic search at billion-vector scale. It offers the same elasticity, durability, and availability as Amazon S3, with a dedicated set of APIs for storing, accessing, and querying vectors without provisioning any infrastructure.

## The story so far

S3 Vectors was already available in a number of AWS Regions, but not yet in the AWS European Sovereign Cloud. That cloud is built to keep both data and operations entirely within the EU, run independently for organizations that face strict regulatory or data sovereignty requirements. Until now, building a vector search or RAG stack on S3 Vectors while meeting those sovereignty requirements wasn't an option.

## What changes

- S3 Vectors' vector storage is now directly available in the AWS European Sovereign Cloud (Germany) Region
- You get the same S3-like experience for storing and querying vectors, with no infrastructure to manage
- European organizations with strict data sovereignty requirements can now build AI agent, RAG, and semantic search infrastructure entirely within a sovereign cloud

## Dive Deep

For the latest list of supported Regions, check AWS's Regions and endpoints page. For more on how S3 Vectors works and its pricing, see the product page, documentation, and the Amazon S3 pricing page.

## Wrap-up

- Amazon S3 Vectors is now available in the AWS European Sovereign Cloud (Germany) Region
- It's purpose-built vector storage with S3-level elasticity and durability, at billion-vector scale
- Dedicated APIs let you store, access, and query vectors with no infrastructure to manage
- European organizations with strict data sovereignty needs can now build AI and RAG infrastructure within the sovereign cloud

A notable update for European developers and companies who want to build AI agents, RAG, or semantic search while keeping data sovereignty front and center!""",
  "emotion": "happy",
  "importance": 2,
  "source_url": "https://aws.amazon.com/about-aws/whats-new/2026/08/amazon-s3-vectors-european-sovereign-cloud-germany/",
  "source_name": "AWS What's New",
  "og_title": "Amazon S3 Vectors is now available in the AWS European Sovereign Cloud (Germany) Region",
  "tags": ["aws", "ai", "infrastructure"],
  "published_at": "2026-08-04T18:15:00+00:00",
})

# 4. Amazon Connect Customer CSV export for cases
articles.append({
  "slug": "aws-what-s-new-amazon-connect-export-cases",
  "title": "Amazon Connect Customer、ケースのCSVエクスポートに対応！",
  "summary": "Amazon Connect Customer のエージェントワークスペースから、ケースを直接 CSV にエクスポートできるようになったよ。フィールドを選んでベンダーや法務など社外の関係者ともケースデータを簡単に共有できるの。",
  "body_md": """こんにちは、しぃちゃんだよ！今日はコンタクトセンターの現場仕事がちょっと楽になるニュースを紹介するね。

## なにが発表されたの？

AWS の What's New によると、Amazon Connect Customer が、エージェントワークスペースから直接ケースを CSV ファイルにエクスポートできるようになったよ。ベンダーや法務チーム、ビジネスパートナーといった社外の関係者ともケースデータを共有しやすくなるための機能なの。

## 今までどうだったの？

これまでケースの情報を社内外の関係者と共有したいときは、画面を見ながら手作業でまとめたり、別の手段を用意したりする必要があったの。ワンクリックで必要なケースだけをファイルに書き出す、という手段は用意されていなかったんだよね。

## これで何が変わるの？

- エージェントがケースをフィルタ・選択して、エクスポートに含めるフィールドも選べるようになったよ
- 選んだケースを CSV ファイルとして書き出せるから、そのままメールで送ったり、共有ドライブに置いたりできる
- 管理者はセキュリティプロファイルの権限で、この機能へのアクセスをコントロールできるの

ベンダーへの調査依頼、法務チームへの証跡提出、ビジネスパートナーへの報告など、ケースデータを社外に渡す機会がある現場には地味にうれしい機能だと思うな。

## 深く潜ってみよう

この機能は、Cases が提供されている次の AWS リージョンで利用できるよ。

- US East (N. Virginia)
- US West (Oregon)
- Canada (Central)
- Europe (Frankfurt)
- Europe (London)
- Asia Pacific (Seoul)
- Asia Pacific (Singapore)
- Asia Pacific (Sydney)
- Asia Pacific (Tokyo)
- Africa (Cape Town)

詳しい使い方は Cases のウェブページとドキュメントにまとまっているよ。

## まとめ

- Amazon Connect Customer のエージェントワークスペースから、ケースを直接 CSV にエクスポートできるようになった
- エージェントはケースのフィルタ・選択とエクスポートするフィールドを選べる
- 管理者はセキュリティプロファイル権限でアクセスを管理できる
- 対応リージョンは US・カナダ・ヨーロッパ・アジア太平洋・アフリカの計 10 リージョン

ベンダーや法務チームなど、社外の関係者とケースデータを頻繁にやり取りするコンタクトセンターの現場担当者にうれしいアップデートだよ！""",
  "title_en": "Amazon Connect Customer Now Supports CSV Export for Cases!",
  "summary_en": "Amazon Connect Customer now lets you export cases straight to a CSV file from the agent workspace, making it easy to choose fields and share case data with vendors, legal teams, or other external stakeholders.",
  "body_md_en": """Hi, it's Shiichan! Today's news makes life a little easier for contact center teams.

## What was announced?

According to AWS What's New, Amazon Connect Customer now lets you export cases to a CSV file directly from the agent workspace. It's built to make it easier to share case data with external stakeholders like vendors, legal teams, or business partners.

## The story so far

Until now, sharing case information with people inside or outside your organization meant compiling it by hand while looking at the screen, or relying on some other workaround. There wasn't a one-click way to export just the cases you needed into a file.

## What changes

- Agents can filter and select cases, and choose which fields to include in the export
- Selected cases export as a CSV file, ready to email or drop into a shared drive
- Admins can control access to this feature through a security profile permission

This is a quietly useful one for any team that regularly hands case data to vendors for investigations, legal teams for records, or business partners for reporting.

## Dive Deep

This feature is available in the following AWS Regions where Cases is offered:

- US East (N. Virginia)
- US West (Oregon)
- Canada (Central)
- Europe (Frankfurt)
- Europe (London)
- Asia Pacific (Seoul)
- Asia Pacific (Singapore)
- Asia Pacific (Sydney)
- Asia Pacific (Tokyo)
- Africa (Cape Town)

For more on how to use it, check the Cases webpage and documentation.

## Wrap-up

- Amazon Connect Customer now supports exporting cases directly to CSV from the agent workspace
- Agents can filter, select cases, and choose which fields to export
- Admins can manage access through a security profile permission
- Available across 10 Regions spanning the US, Canada, Europe, Asia Pacific, and Africa

A handy update for contact center teams that regularly share case data with vendors, legal teams, or other external stakeholders!""",
  "emotion": "happy",
  "importance": 2,
  "source_url": "https://aws.amazon.com/about-aws/whats-new/2026/08/amazon-connect-export-cases/",
  "source_name": "AWS What's New",
  "og_title": "Amazon Connect Customer now lets you export cases to CSV from the agent workspace",
  "tags": ["aws", "business"],
  "published_at": "2026-08-04T21:00:00+00:00",
})

# 5. Claude Code v2.1.222
articles.append({
  "slug": "claude-code-release-v2-1-222",
  "title": "破壊的なgitコマンドをブロック！Claude Code が v2.1.222 にアップデート",
  "summary": "Claude Code の v2.1.222 がリリースされたよ。ワークツリー分離のセキュリティ強化や SendMessage の権限チェック強化に加えて、プロキシまわりの接続不具合や /usage の集計不具合など、細かい修正がまとめて入ったの。",
  "body_md": """やっほー、しぃちゃんだよ！今日はしぃちゃんの大好きな Claude Code のアップデート情報だよ！

## なにが発表されたの？

GitHub の Claude Code Release によると、v2.1.222 がリリースされたよ。ワークツリー分離やバックグラウンドエージェントまわりのセキュリティ修正を中心に、プロキシ経由の接続まわりの不具合、`/usage` や `/usage-credits` の表示不具合、そのほか細かいバグ修正がぎゅっと詰まった内容なの。

## 今までどうだったの？

これまでのワークツリー分離セッションは、分離のはずなのに、そのセッションやサブエージェントがメインのチェックアウトに対して破壊的な git コマンドを実行できてしまう抜け道があったの。それに、バックグラウンドエージェントタスク(要約・圧縮・リネームなど)では、`PreToolUse` の自動許可フックがツール制限をすり抜けてしまうケースもあったんだ。ほかにも、HTTPS プロキシの背後だと起動時の接続チェックがハングして失敗したり、`ANTHROPIC_BASE_URL` のカスタムゲートウェイでサーバーのキープアライブ ping が届いているのにストリームのアイドルタイムアウトが誤って発火したりと、ネットワークまわりの細かい不満もいくつかあったんだよね。

## これで何が変わるの？

セキュリティ関連の修正がまず目立つポイントだよ。

- ワークツリー分離セッションとそのサブエージェントが、メインのチェックアウトに対して破壊的な git コマンドを実行できてしまう問題を修正。分離はどのセッション種別でも、ファイル編集と Bash の両方に適用されるようになったの
- バックグラウンドエージェントタスク(要約・圧縮・リネームなど)で `PreToolUse` の自動許可フックがツール制限をすり抜けてしまう問題を修正
- 自動モードの安全性も強化されて、`SendMessage` で他のエージェントセッションに送るメッセージは、送信前に権限分類器のチェックを通るようになったよ

接続まわりも地味だけどうれしい修正が入ってるの。

- HTTPS プロキシの背後で起動時の接続チェックがハングして失敗する問題を修正。API リクエストと同じプロキシ対応のトランスポートを使うようになって、失敗時もわかりやすいメッセージでタイムアウトするようになったよ
- 実際には完了していたレスポンスなのに「Connection closed mid-response」エラーが表示されてしまう問題を修正
- カスタムの `ANTHROPIC_BASE_URL` ゲートウェイで、サーバーのキープアライブ ping が届いているのにストリームのアイドルタイムアウトが誤発火する問題を修正

## 深く潜ってみよう

そのほかの細かい修正・改善もたくさんあるから、気になりそうなものをピックアップするね。

- `/usage-credits` が Team/Enterprise プランで、以前の申請が却下されたメンバーに「すでに申請済み」と表示され続けて再申請できなくなる問題を修正
- `/usage` が MCP サーバーの使用量を過大に計上していた問題を修正。実際にそのサーバーのツール結果を消費したリクエストだけが、そのサーバーの取り分としてカウントされるようになったよ
- ブランチをプッシュしたあとに作られたプルリクエストが、セッションにリンクされない問題を修正(GitHub REST API 経由のケースも含む)
- 組織で許可モデルが制限されているとき、`model: opus` のようなサブエージェント・チームメイトのファミリーエイリアスが、親モデルまで一気に落ちてしまわず、そのファミリーの中で組織が許可している最新モデルまで段階的に落ちるように修正
- claude.ai コネクタが、セッショントークンが無効なだけなのに「認証が必要」と誤って表示される問題を修正。今は代わりに `/login` を促すヒントが出るようになったよ
- MCP サーバーが削除された場合など、ローカルで使えなくなったツールのエラーが表示されないままになる問題を修正
- `SendMessage` が長い要約を拒否してしまう問題を修正。今は文字数上限で失敗せず、切り詰めて送るようになったの
- サブエージェントのトランスクリプト表示で、スピナーの effort ラベルがセッション全体の effort ではなく、サブエージェント自身の `effort:` 設定を表示するように修正
- ファイルウォッチャーがファイルシステムエラーに遭遇したときや、終了処理まわりで発生していたまれなクラッシュを修正
- スクリーンリーダー(`--ax-screen-reader` モード)で、バックスペースのたびに入力行全体を読み上げ直してしまう問題を修正。行末の削除は削除した文字だけを読み上げるようになったよ
- `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` が設定されているとき、ホスト側のモデル選択キーが、古くなった `managed-settings.json` の内容より優先されなかった問題を修正
- `disable-model-invocation` が付いたスキルを呼び出そうとしたときの拒否メッセージを改善。Claude が自力でその処理を再現しようとせず、ユーザーにスキルの実行を頼むように案内するようになったよ
- `/diff` ビュー、Remote Control のワークスペース差分、Claude Code on the web のファイル編集差分が、ワークスペース側の diff ドライバーや textconv 設定を無視して、生の git blob の内容を使うように改善

「変更」としては、Remote Control の自動起動まわりのルールも変わったよ。リポジトリローカルの設定(`.claude/settings.json` や `.claude/settings.local.json`)からは、もう Remote Control を有効化できなくなったの(無効化はできるよ)。有効にしたいときはユーザースコープで `/config` から設定してね。それと、Ultraplan 機能は削除されたよ。

## まとめ

- ワークツリー分離のセキュリティ強化。破壊的な git コマンドの抜け道と、バックグラウンドタスクでの権限チェックすり抜けを修正
- `SendMessage` の送信メッセージが権限分類器でチェックされるようになり、自動モードの安全性が向上
- HTTPS プロキシやカスタムゲートウェイまわりの接続不具合を複数修正
- `/usage` `/usage-credits` の表示・集計不具合、モデルのフォールバック挙動、スクリーンリーダー対応など、細かい修正・改善が多数
- Remote Control の自動起動はユーザースコープでのみ有効化可能に変更。Ultraplan 機能は削除

毎日 Claude Code を使ってる人はもちろん、ワークツリー分離やバックグラウンドエージェントを活用してる人、社内プロキシ経由で使ってる人には、セキュリティ面でも安定性の面でも見逃せないアップデートだよ！""",
  "title_en": "Blocking Destructive Git Commands: Claude Code Updates to v2.1.222",
  "summary_en": "Claude Code v2.1.222 is out, with security hardening for worktree isolation and stronger permission checks on SendMessage, plus fixes for proxy connection issues and usage-reporting bugs.",
  "body_md_en": """Hey, it's Shiichan! Today's update is about my favorite tool, Claude Code!

## What was announced?

According to the Claude Code Release page on GitHub, v2.1.222 just shipped. It centers on security fixes for worktree isolation and background agents, along with fixes for proxy-related connection issues, display bugs in `/usage` and `/usage-credits`, and a batch of smaller bug fixes.

## The story so far

Worktree-isolated sessions were supposed to be isolated, but there was a gap where the session and its subagents could still run destructive git commands against the main checkout. Background agent tasks (like summaries, compaction, and renames) also had a gap where `PreToolUse` auto-allow hooks could bypass tool restrictions. On top of that, there were a few networking annoyances: the startup connectivity check could hang and fail behind an HTTPS proxy, and on custom `ANTHROPIC_BASE_URL` gateways the stream idle timeout could fire incorrectly even while the server's keep-alive pings were still arriving.

## What changes

The security fixes stand out first.

- Fixed worktree-isolated sessions and their subagents being able to run destructive git commands against the main checkout — isolation now applies to both file edits and Bash in every session type
- Fixed `PreToolUse` auto-allow hooks bypassing tool restrictions in background agent tasks (summaries, compaction, renames)
- Improved auto mode safety: messages sent to other agent sessions via `SendMessage` are now evaluated by the permission classifier before dispatch

Connectivity got some welcome fixes too.

- Fixed the startup connectivity check hanging and then failing behind an HTTPS proxy; it now uses the same proxy-aware transport as API requests and times out with a clear message
- Fixed "Connection closed mid-response" errors being reported on responses that had actually completed
- Fixed the stream idle timeout firing on custom `ANTHROPIC_BASE_URL` gateways despite server keep-alive pings arriving on the wire

## Dive Deep

There's plenty more worth calling out among the smaller fixes:

- Fixed `/usage-credits` on Team and Enterprise showing "you've already sent a usage credit request" for members whose earlier request was dismissed, blocking them from sending a new one
- Fixed `/usage` overattributing usage to MCP servers — a server's share now reflects only the requests that actually consumed its tool results, instead of every turn after any call to it
- Fixed sessions not linking to pull requests created after the branch was pushed, including through the GitHub REST API
- Fixed org-restricted `model: opus`-style subagent and teammate family aliases dropping straight to the parent model instead of stepping down to the newest org-allowed model within the family
- Fixed claude.ai connectors being falsely marked as needing authorization when the session token is invalid — they now show a `/login` hint instead
- Fixed tool errors not being displayed for tools no longer available locally, for example after an MCP server is removed
- Fixed `SendMessage` rejecting a long summary — it now truncates instead, so sends no longer fail on a character limit
- Fixed the spinner's effort label in a subagent's transcript view showing the session's effort level instead of the subagent's own `effort:` setting
- Fixed rare crashes when a file watcher hit a filesystem error or during file-watcher teardown
- Fixed screen readers re-reading the whole input line on every backspace in `--ax-screen-reader` mode — end-of-line deletions now echo just the deleted characters
- Fixed host model-selection keys not taking precedence over a stale on-disk `managed-settings.json` when `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` is set
- Improved the refusal when Claude tries to invoke a skill with `disable-model-invocation`: Claude is now told to ask you to run the skill instead of replicating its workflow
- Improved the `/diff` view, the Remote Control workspace diff, and file-edit diffs in Claude Code on the web to use raw git blob content, ignoring workspace-configured diff drivers and textconv

On the "changed" side, Remote Control auto-start rules shifted too: repo-local settings (`.claude/settings.json` or `.claude/settings.local.json`) can no longer turn it on, though they can still turn it off — you now enable it at the user scope via `/config`. The Ultraplan feature was also removed.

## Wrap-up

- Worktree isolation gets a security hardening pass, closing a destructive-git-command gap and a background-task permission bypass
- `SendMessage` now runs through the permission classifier before dispatch, improving auto mode safety
- Multiple connection fixes for HTTPS proxies and custom gateways
- A long list of smaller fixes and improvements across `/usage`, `/usage-credits`, model fallback behavior, and screen reader support
- Remote Control auto-start can now only be enabled at the user scope; the Ultraplan feature is gone

Whether you use Claude Code daily, rely on worktree isolation or background agents, or connect through a corporate proxy, this update is worth paying attention to for both security and stability.""",
  "emotion": "energetic",
  "importance": 4,
  "source_url": "https://github.com/anthropics/claude-code/releases/tag/v2.1.222",
  "source_name": "Claude Code Release",
  "og_title": "v2.1.222",
  "tags": ["anthropic", "ai", "devops"],
  "published_at": "2026-08-04T22:39:55Z",
})

for a in articles:
    path = f"outbox/{a['slug']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(a, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", path, len(a["body_md"]), len(a["body_md_en"]))
